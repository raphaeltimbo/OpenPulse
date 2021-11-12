import vtk
import numpy as np 
from time import time
from collections import namedtuple
# from itertools import chain
# from scipy.spatial.transform import Rotation

from abc import ABC, abstractmethod
from pulse.interface.vtkActorBase import vtkActorBase

def loadSymbol(path):
    reader = vtk.vtkOBJReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()

SymbolTransform = namedtuple('SymbolTransform', ['source', 'position', 'rotation', 'scale', 'color'])

class SymbolsActorBase(vtkActorBase):
    def __init__(self, project, deformed=False):
        super().__init__()
        
        self.project = project 
        self.deformed = deformed
        self.scaleFactor = 0.3

        self._connections = self._createConnections()
        self._sequence = self._createSequence()

        self._data = vtk.vtkPolyData()
        self._mapper = vtk.vtkGlyph3DMapper()

    @abstractmethod
    def _createConnections(self):
        return []
    
    @abstractmethod
    def _createSequence(self):
        return []

    def source(self):
        self._createArrays()
        # self._createNodalLinks()
        self._loadSources()

        for data in self._sequence:
            for i, (func, symb) in enumerate(self._connections):
                for transform in func(data):
                    self._createSymbol(i, transform)

        self._populateData()
    
    def map(self):
        self._mapper.SetInputData(self._data)
        self._mapper.SetSourceIndexArray('sources')
        self._mapper.SetOrientationArray('rotations')
        self._mapper.SetScaleArray('scales')
        self._mapper.SetScaleFactor(self.scaleFactor)
        
        self._mapper.SourceIndexingOn()
        self._mapper.SetOrientationModeToRotation()
        self._mapper.SetScaleModeToScaleByVectorComponents()
        self._mapper.Update()
    
    def filter(self):
        pass 
    
    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetOpacity(0.9)
        self._actor.GetProperty().BackfaceCullingOff()
    
    def _createArrays(self):
        self._sources = vtk.vtkIntArray()
        self._positions = vtk.vtkPoints()
        self._rotations = vtk.vtkDoubleArray()
        self._scales = vtk.vtkDoubleArray()
        self._colors = vtk.vtkUnsignedCharArray()

        self._sources.SetName('sources')
        self._rotations.SetName('rotations')
        self._scales.SetName('scales')
        self._rotations.SetNumberOfComponents(3)
        self._scales.SetNumberOfComponents(3)
        self._colors.SetNumberOfComponents(3)

    def _populateData(self):
        self._data.SetPoints(self._positions)
        self._data.GetPointData().AddArray(self._sources)
        self._data.GetPointData().AddArray(self._rotations)
        self._data.GetPointData().AddArray(self._scales)
        self._data.GetPointData().SetScalars(self._colors)

    def _loadSources(self):
        for i, (func, symb) in enumerate(self._connections):
            self._mapper.SetSourceData(i, symb)

    def _createSymbol(self, src, symbol):
        self._sources.InsertNextTuple1(src)
        self._positions.InsertNextPoint(symbol.position)
        self._rotations.InsertNextTuple(symbol.rotation)
        self._scales.InsertNextTuple(symbol.scale)
        self._colors.InsertNextTuple(symbol.color)








class SymbolsActor(vtkActorBase):
    PRESCRIBED_POSITION_SYMBOL = loadSymbol('data/symbols/prescribedPosition.obj')
    PRESCRIBED_ROTATION_SYMBOL = loadSymbol('data/symbols/prescribedRotation.obj')
    NODAL_LOAD_POSITION_SYMBOL = loadSymbol('data/symbols/nodalLoadPosition.obj')
    NODAL_LOAD_ROTATION_SYMBOL = loadSymbol('data/symbols/nodalLoadRotation.obj')
    LUMPED_MASS_SYMBOL = loadSymbol('data/symbols/lumpedMass.obj')
    LUMPED_DAMPER_SYMBOL = loadSymbol('data/symbols/damper.obj')
    LUMPED_SPRING_SYMBOL = loadSymbol('data/symbols/spring.obj')
    VOLUME_VELOCITY_SYMBOL = loadSymbol('data/symbols/volumeVelocity.obj')
    ACOUSTIC_PRESSURE_SYMBOL = loadSymbol('data/symbols/acousticPressure.obj')
    SPECIFIC_IMPEDANCE_SYMBOL = loadSymbol('data/symbols/specificImpedance.obj')
    RADIATION_IMPEDANCE_SYMBOL = loadSymbol('data/symbols/radiationImpedance.obj')
    COMPRESSOR_SYMBOL = loadSymbol('data/symbols/compressor.obj')
    PERFORATED_PLATE_SYMBOL = loadSymbol('data/symbols/perforated_plate.obj')
    VALVE_SYMBOL = loadSymbol('data/symbols/valve_symbol.obj')
    
    def __init__(self, project, deformed=False):
        super().__init__()
        
        self.project = project
        self.nodes = project.get_nodes() 
        self.preprocessor = project.preprocessor
        self.deformed = deformed
        self.scaleFactor = 0.3
        self._show_acoustic_symbols = True
        self._show_structural_symbols = True

        self._data = vtk.vtkPolyData()
        self._mapper = vtk.vtkGlyph3DMapper()
    
    def source(self):
        self.scaleFactor = self.preprocessor.structure_principal_diagonal / 10
        
        self._createArrays()
        self._createNodalLinks()
        self._loadSources()
        self.valves_coord_to_parameters = {}
        
        for node in self.nodes.values():   
            for symbol in self._getAcousticNodeSymbols(node):
                self._createSymbol(symbol)
            for symbol in self._getStructuralNodeSymbols(node):
                self._createSymbol(symbol)

        for element in self.project.get_structural_elements().values():
            for symbol in self._getAcousticElementSymbols(element):
                self._createSymbol(symbol)    
            for symbol in self._getStructuralElementSymbols(element):
                self._createSymbol(symbol)  
        
        self._populateData()

    def map(self):
        self._mapper.SetInputData(self._data)
        self._mapper.SetSourceIndexArray('sources')
        self._mapper.SetOrientationArray('rotations')
        self._mapper.SetScaleArray('scales')
        self._mapper.SetScaleFactor(self.scaleFactor)
        
        self._mapper.SourceIndexingOn()
        self._mapper.SetOrientationModeToRotation()
        self._mapper.SetScaleModeToScaleByVectorComponents()
        self._mapper.Update()

    def filter(self):
        pass
    
    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetOpacity(0.9)
        self._actor.GetProperty().BackfaceCullingOff()

    def _createArrays(self):
        self._sources = vtk.vtkIntArray()
        self._positions = vtk.vtkPoints()
        self._rotations = vtk.vtkDoubleArray()
        self._scales = vtk.vtkDoubleArray()
        self._colors = vtk.vtkUnsignedCharArray()

        self._sources.SetName('sources')
        self._rotations.SetName('rotations')
        self._scales.SetName('scales')
        self._rotations.SetNumberOfComponents(3)
        self._scales.SetNumberOfComponents(3)
        self._colors.SetNumberOfComponents(3)

    def _populateData(self):
        self._data.SetPoints(self._positions)
        self._data.GetPointData().AddArray(self._sources)
        self._data.GetPointData().AddArray(self._rotations)
        self._data.GetPointData().AddArray(self._scales)
        self._data.GetPointData().SetScalars(self._colors)

    def _loadSources(self):
        # HERE YOU SET THE INDEXES OF THE SOURCES
        self._mapper.SetSourceData(1, self.PRESCRIBED_POSITION_SYMBOL)
        self._mapper.SetSourceData(2, self.PRESCRIBED_ROTATION_SYMBOL)
        self._mapper.SetSourceData(3, self.NODAL_LOAD_POSITION_SYMBOL)
        self._mapper.SetSourceData(4, self.NODAL_LOAD_ROTATION_SYMBOL)
        self._mapper.SetSourceData(5, self.LUMPED_MASS_SYMBOL)
        self._mapper.SetSourceData(6, self.LUMPED_SPRING_SYMBOL)
        self._mapper.SetSourceData(7, self.LUMPED_DAMPER_SYMBOL)
        self._mapper.SetSourceData(8, self.VALVE_SYMBOL)
        self._mapper.SetSourceData(9, self.ACOUSTIC_PRESSURE_SYMBOL)
        self._mapper.SetSourceData(10, self.VOLUME_VELOCITY_SYMBOL)
        self._mapper.SetSourceData(11, self.SPECIFIC_IMPEDANCE_SYMBOL)
        self._mapper.SetSourceData(12, self.RADIATION_IMPEDANCE_SYMBOL)
        self._mapper.SetSourceData(13, self.COMPRESSOR_SYMBOL)
        self._mapper.SetSourceData(14, self.PERFORATED_PLATE_SYMBOL)
        
    
    def _createSymbol(self, symbol):
        self._sources.InsertNextTuple1(symbol.source)
        self._positions.InsertNextPoint(symbol.position)
        self._rotations.InsertNextTuple(symbol.rotation)
        self._scales.InsertNextTuple(symbol.scale)
        self._colors.InsertNextTuple(symbol.color)
    
    def _getAcousticNodeSymbols(self, node):
        # HERE YOU CALL THE FUNCTIONS CREATED
        symbols = []
        if self._show_acoustic_symbols:
            symbols.extend(self._getAcousticPressure(node))
            symbols.extend(self._getVolumeVelocity(node))
            symbols.extend(self._getSpecificImpedance(node))
            symbols.extend(self._getRadiationImpedance(node))
            symbols.extend(self._getCompressor(node))
        return symbols

    def _getStructuralNodeSymbols(self, node):
        # HERE YOU CALL THE FUNCTIONS CREATED
        symbols = []
        if self._show_structural_symbols:
            symbols.extend(self._getPrescribedPositionSymbols(node))
            symbols.extend(self._getPrescribedRotationSymbols(node))
            symbols.extend(self._getNodalLoadForce(node))
            symbols.extend(self._getNodalLoadMoment(node))
            symbols.extend(self._getLumpedMass(node))
            symbols.extend(self._getSpring(node))
            symbols.extend(self._getDamper(node))
        return symbols

    def _getAcousticElementSymbols(self, element):
        symbols = []
        if self._show_acoustic_symbols:
            symbols.extend(self._getPerforatedPlate(element))
        return symbols
    
    def _getStructuralElementSymbols(self, element):
        symbols = []
        if self._show_structural_symbols:
            symbols.extend(self._getValve(element))
        return symbols

    def _createNodalLinks(self):
        # temporary structure to plot elastic links 

        linkedNodes = set()
        linkedSymbols = vtk.vtkAppendPolyData()

        # extract from string values that shoud be avaliable
        # create a set without useless repetitions 
        for node in self.nodes.values():
            stif = tuple(node.elastic_nodal_link_stiffness.keys())
            damp = tuple(node.elastic_nodal_link_dampings.keys())
            if stif:
                nodes = sorted(int(i) for i in stif[0].split('-'))
            elif damp:
                nodes = sorted(int(i) for i in damp[0].split('-'))
            else:
                continue 
            linkedNodes.add(tuple(nodes))

        for a, b in linkedNodes:
            # divide the value of the coordinates by the scale factor
            source = vtk.vtkLineSource()
            source.SetPoint1(self.nodes[a].coordinates / self.scaleFactor) 
            source.SetPoint2(self.nodes[b].coordinates / self.scaleFactor)
            source.Update()
            linkedSymbols.AddInputData(source.GetOutput())
        
        s = vtk.vtkSphereSource()
        s.SetRadius(0)

        linkedSymbols.AddInputData(s.GetOutput())
        linkedSymbols.Update()

        self._mapper.SetSourceData(0, linkedSymbols.GetOutput())
        self._sources.InsertNextTuple1(0)
        self._positions.InsertNextPoint(0,0,0)
        self._rotations.InsertNextTuple3(0,0,0)
        self._scales.InsertNextTuple3(1,1,1)
        self._colors.InsertNextTuple3(16,222,129)
    
    def is_value_negative(self, value):
        if isinstance(value, np.ndarray):
            return False
        elif np.real(value)>=0:
            return False
        else:
            return True

    def _getPrescribedPositionSymbols(self, node):
        offset = 0 * self.scaleFactor
        x,y,z = self._getCoords(node)
        src = 1
        scl = (1,1,1)
        col = (0,255,0)

        symbols = []
        mask = [(i is not None) for i in node.getStructuralBondaryCondition()[:3]]
        values = list(node.getStructuralBondaryCondition()[:3])

        if mask[0]:
            pos = (x-offset, y, z)
            rot = (0,0,90)
            if self.is_value_negative(values[0]):
                pos = (x-offset, y, z)
                rot = (0,0,-90)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[1]:
            pos = (x, y-offset, z)
            rot = (180,90,0)
            if self.is_value_negative(values[1]):
                pos = (x, y+offset, z)
                rot = (180,90,180)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (-90,0,0)
            if self.is_value_negative(values[2]):
                pos = (x, y, z+offset)
                rot = (90,0,0)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        
        return symbols

    def _getPrescribedRotationSymbols(self, node):
        offset = 0 * self.scaleFactor
        x,y,z = self._getCoords(node)
        src = 2
        scl = (1,1,1)
        col = (0,200,200)

        symbols = []
        mask = [(i is not None) for i in node.getStructuralBondaryCondition()[3:]]
        values = list(node.getStructuralBondaryCondition()[3:])
        
        if mask[0]:
            pos = (x-offset, y, z)
            rot = (0,0,90)
            if self.is_value_negative(values[0]):
                pos = (x+offset, y, z)
                rot = (0,0,-90)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[1]:
            pos = (x, y-offset, z)
            rot = (180,90,0)
            if self.is_value_negative(values[1]):
                pos = (x, y+offset, z)
                rot = (180,90,180)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (-90,0,0)
            if self.is_value_negative(values[2]):
                pos = (x, y, z+offset)
                rot = (90,0,0)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        
        return symbols

    def _getNodalLoadForce(self, node):
        offset = 0.05 * self.scaleFactor
        x,y,z = self._getCoords(node)
        src = 3
        scl = (1,1,1)
        col = (255,0,0)

        symbols = []
        mask = [(i is not None) for i in node.get_prescribed_loads()[:3]]
        values = list(node.get_prescribed_loads()[:3])
        
        if mask[0]:
            pos = (x-offset, y, z)
            rot = (0,0,90)
            if self.is_value_negative(values[0]):
                pos = (x+offset, y, z)
                rot = (0,0,-90)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[1]:
            pos = (x, y-offset, z)
            rot = (180,90,0)
            if self.is_value_negative(values[1]):
                pos = (x, y+offset, z)
                rot = (180,90,180)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (-90,0,0)
            if self.is_value_negative(values[2]):
                pos = (x, y, z+offset)
                rot = (90,90,0)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        
        return symbols
    
    def _getNodalLoadMoment(self, node):
        offset = 0.05 * self.scaleFactor
        x,y,z = self._getCoords(node)
        src = 4
        scl = (1,1,1)
        col = (0,0,255)

        symbols = []
        values = list(node.get_prescribed_loads()[:3])
        mask = [(i is not None) for i in node.get_prescribed_loads()[3:]]
        
        if mask[0]:
            pos = (x-offset, y, z)
            rot = (0,0,90)
            if self.is_value_negative(values[0]):
                pos = (x+offset, y, z)
                rot = (0,0,-90)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[1]:
            pos = (x, y-offset, z)
            rot = (180,90,0)
            if self.is_value_negative(values[1]):
                pos = (x, y+offset, z)
                rot = (180,90,180)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (-90,0,0)
            if self.is_value_negative(values[2]):
                pos = (x, y, z+offset)
                rot = (90,0,0)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        
        return symbols
    
    def _getLumpedMass(self, node):
        src = 5
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (7,156,231)
        symbols = []

        if any(node.lumped_masses):
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols

    def _getSpring(self, node):
        offset = 0.62 * self.scaleFactor
        x,y,z = self._getCoords(node)
        src = 6
        scl = (1,1,1)
        col = (242,121,0)

        symbols = []
        # mask = node.get_lumped_stiffness()[:3]
        mask = [(i is not None) for i in node.get_lumped_stiffness()[:3]]

        if mask[0]:
            pos = (x-offset, y, z)
            rot = (180,0,90)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[1]:
            pos = (x, y-offset, z)
            rot = (0,0,0)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (90,0,0)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        
        return symbols

    def _getDamper(self, node):
        offset = 0.62 * self.scaleFactor
        x,y,z = self._getCoords(node)
        src = 7
        scl = (1,1,1)
        col = (255,0,100)

        symbols = []
        # mask = node.get_lumped_dampings()[:3]
        mask = [(i is not None) for i in node.get_lumped_dampings()[:3]]

        if mask[0]:
            pos = (x-offset, y, z)
            rot = (180,0,90)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[1]:
            pos = (x, y-offset, z)
            rot = (0,0,0)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        if mask[2]:
            pos = (x, y, z-offset)
            rot = (90,0,0)
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        
        return symbols

    def _getValve(self, element):
        src = 8
        rot = (0,0,0)
        col = (255,100,0)
        col = (0,0,255)
        symbols = []
        
        if element.valve_parameters:
            center_coordinates = element.valve_parameters["valve_center_coordinates"]
            if str(center_coordinates) not in self.valves_coord_to_parameters.keys():
                self.valves_coord_to_parameters[str(center_coordinates)] = element.valve_parameters
                pos = center_coordinates
                rot = element.section_rotation_xyz_undeformed
                rotation = Rotation.from_euler('xyz', rot, degrees=True)
                rot_matrix = rotation.as_matrix()
                vector = [round(value, 5) for value in rot_matrix[:,1]]
                if vector[1] < 0:
                    rot[0] += 180
                factor_x = (element.valve_parameters["valve_length"]/0.247)/self.scaleFactor
                # factor_yz = (element.valve_parameters["valve_section_parameters"]["outer_diameter"]/0.130)/self.scaleFactor
                factor_yz = 1
                scl = (factor_x, factor_yz, factor_yz)
                symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols  
    def _getAcousticPressure(self, node):
        src = 9
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (150,0,210) #violet
        symbols = []

        if node.acoustic_pressure is not None:
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols

    def _getVolumeVelocity(self, node):
        src = 10
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (255,10,10)
        symbols = []

        if (node.volume_velocity is not None) and (node.compressor_excitation_table_names == []):
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols

    def _getSpecificImpedance(self, node):
        src = 11
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (100,255,100)
        symbols = []

        if node.specific_impedance is not None:
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
    
    def _getRadiationImpedance(self, node):
        src = 12
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (224,0,75)
        symbols = []

        if node.radiation_impedance_type in [0,1,2]:
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols    
    
    def _getCompressor(self, node):
        src = 13
        pos = node.coordinates
        rot = (0,0,0)
        scl = (1,1,1)
        col = (255,10,10)
        symbols = []

        if (node.volume_velocity is not None) and (node.compressor_excitation_table_names != []):
            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))
        return symbols
    
    def _getPerforatedPlate(self, element):
        
        src = 14
        pos = element.element_center_coordinates
        rot = element.section_rotation_xyz_undeformed
        col = (255,0,0)
        symbols = []

        if element.perforated_plate:
        
            pos = element.element_center_coordinates
            rot = element.section_rotation_xyz_undeformed
   
            factor_x = (element.perforated_plate.thickness/0.01)/self.scaleFactor
            factor_yz = (element.cross_section.inner_diameter/0.1)/self.scaleFactor
            scl = (factor_x, factor_yz, factor_yz)

            symbols.append(SymbolTransform(source=src, position=pos, rotation=rot, scale=scl, color=col))

        return symbols

    def _getCoords(self, node):
        if self.deformed:
            return node.deformed_coordinates
        else:
            return node.coordinates
