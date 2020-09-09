from pulse.uix.vtk.vtkRendererBase import vtkRendererBase
from pulse.uix.vtk.vtkInteractorBase import vtkInteractorBase
from pulse.uix.vtk.actor.actorLine import ActorLine
from pulse.uix.vtk.vtkInteractorStyleClicker import vtkInteractorStyleClicker
import vtk

class RendererEntity(vtkRendererBase):
    def __init__(self, project, opv):
        super().__init__(vtkInteractorStyleClicker(self))
        self.project = project
        self.opv = opv
        self.actors = {}
        self.plotRadius = False

    def updateInfoText(self):
        listActorsIDs = self.getListPickedEntities()
        text = ""
        if len(listActorsIDs) == 0:
        
            text = ""
            vertical_position_adjust = None
        
        elif len(listActorsIDs) == 1:

            entity = self.project.get_entity(listActorsIDs[0])
            
            e_type = "undefined"
            material_name = "undefined"
            diam_ext, thickness = "undefined", "undefined"
            offset_y, offset_z = "undefined", "undefined"
            
            if entity.getMaterial() is not None:
                material_name = entity.getMaterial().getName()

            if entity.element_type is not None:
                e_type = entity.element_type.upper()

            if entity.tag in (self.project.lines_multiples_cross_sections or self.project.file.lines_multiples_cross_sections):

                if len(self.project.lines_multiples_cross_sections) != 0:
                    number_cross_sections = self.project.lines_multiples_cross_sections.count(entity.tag)
                    # print(self.project.lines_multiples_cross_sections)

                if len(self.project.file.lines_multiples_cross_sections) != 0:
                    number_cross_sections = self.project.file.lines_multiples_cross_sections.count(entity.tag)
                    # print(self.project.file.lines_multiples_cross_sections)
                if entity.element_type is not None and entity.element_type not in ['beam_1']:
                
                    diam_ext, thickness = "multiples", "multiples"
                    offset_y, offset_z = "multiples", "multiples"
                    insulation_thickness, insulation_density = "multiples", "multiples"

                    text = "Line ID  {} ({} cross-sections)\nMaterial:  {}\nElement type:  {}\nExternal Diameter:  {}\nThickness:  {}\n".format(listActorsIDs[0], number_cross_sections, material_name, e_type, diam_ext, thickness)                
                    text += "Offset y: {}\nOffset z: {}\n".format(offset_y, offset_z)
                    text += "Insulation thickness: {}\nInsulation density: {} ".format(insulation_thickness, insulation_density)
            else:
                if entity.getCrossSection() is not None:
                    if entity.element_type is not None and entity.element_type not in ['beam_1']:

                        diam_ext = entity.getCrossSection().getExternalDiameter()
                        thickness = entity.getCrossSection().getThickness()
                        offset_y = entity.getCrossSection().offset_y
                        offset_z = entity.getCrossSection().offset_z
                        insulation_thickness = entity.crossSection.insulation_thickness
                        insulation_density = entity.crossSection.insulation_density
                        text = "Line ID  {}\nMaterial:  {}\nElement type:  {}\nExternal Diameter:  {} [m]\nThickness:  {} [m]\n".format(listActorsIDs[0], material_name, e_type, diam_ext, thickness)
                        if offset_y != 0 or offset_z != 0:
                            text += "Offset y: {} [m]\nOffset z: {} [m]\n".format(offset_y, offset_z)
                        if insulation_thickness != 0 or insulation_density != 0: 
                            text += "Insulation thickness: {} [m]\nInsulation density: {} [kg/m³]".format(insulation_thickness, int(insulation_density))
            
                    elif entity.element_type is not None and entity.element_type in ['beam_1']:
                        area = entity.getCrossSection().area
                        Iyy = entity.getCrossSection().second_moment_area_y
                        Izz = entity.getCrossSection().second_moment_area_z
                        text = "Line ID  {}\nMaterial:  {}\nElement type:  {}\n".format(listActorsIDs[0], material_name, e_type)
                        text += "Area:  {} [m²]\nIyy:  {} [m^4]\nIzz:  {} [m^4]\n".format(area, Iyy, Izz)

            vertical_position_adjust = (1-0.86)*960
        else:
            text = "{} lines in selection:\n\n".format(len(listActorsIDs))
            i = 0
            correction = 1
            for ids in listActorsIDs:
                if i == 30:
                    text += "..."
                    factor = 1.02
                    break
                elif i == 19: 
                    text += "{}\n".format(ids)
                    factor = 1.02  
                    correction = factor/1.06            
                elif i == 9:
                    text += "{}\n".format(ids)
                    factor = 1.04
                    correction = factor/1.06
                else:
                    text += "{}  ".format(ids)
                    factor = 1.06*correction
                i+=1
            vertical_position_adjust = (1-0.88*factor)*960

        self.createInfoText(text)

    def reset(self):
        for actor in self._renderer.GetActors():
            self._renderer.RemoveActor(actor)
        self.actors = {}
        self._style.clear()

    def plot(self):
        self.reset()
        for entity in self.project.get_entities():
            plot = ActorLine(entity, self.plotRadius)
            plot.build()
            self.actors[plot.getActor()] = entity.get_tag()
            self._renderer.AddActor(plot.getActor())

    def changeColorEntities(self, entity_id, color):
        self._style.clear()
        actors = [key  for (key, value) in self.actors.items() if value in entity_id]
        for actor in actors:
            actor.GetProperty().SetColor(color)
        self.updateInfoText()

    def getListPickedEntities(self):
        return self._style.getListPickedActors()

    def update(self):
        self.opv.update()
        self.opv.updateDialogs()

    def setPlotRadius(self, value):
        self.plotRadius = value

    def getPlotRadius(self):
        return self.plotRadius