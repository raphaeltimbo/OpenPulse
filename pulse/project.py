from PyQt5.QtWidgets import QProgressBar, QLabel
from pulse.preprocessing.mesh import Mesh
from pulse.processing.solution_structural import SolutionStructural
from pulse.processing.solution_acoustic import SolutionAcoustic
from pulse.preprocessing.entity import Entity
from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.cross_section import CrossSection
from pulse.projectFile import ProjectFile
from pulse.utils import error
import numpy as np
import configparser
from collections import defaultdict
import os

class Project:
    def __init__(self):
        self.mesh = Mesh()
        self.file = ProjectFile()

        self._project_name = ""
        self.project_folder_path = ""

        #Analysis
        self.analysis_ID = None
        self.analysis_type_label = ""
        self.analysis_method_label = ""
        self.global_damping = [0,0,0,0]
        self.modes = 0
        self.frequencies = None
        self.f_min = 0
        self.f_max = 0
        self.f_step = 0
        self.natural_frequencies_structural = []
        self.solution_structural = None
        self.solution_acoustic = None
        self.flag_set_material = False
        self.flag_set_crossSection = False
        self.plot_pressure_field = False
        self.is_file_loaded = False

        self.time_to_checking_entries = None 
        self.time_to_process_cross_sections = None
        self.time_to_solve_model = None
        self.time_to_postprocess = None


    def reset_info(self):
        self.mesh = Mesh()
        self.analysis_ID = None
        self.analysis_type_label = ""
        self.analysis_method_label = ""
        self.global_damping = [0,0,0,0]
        self.modes = 0
        self.frequencies = None
        self.f_min = 0
        self.f_max = 0
        self.f_step = 0
        self.natural_frequencies_structural = []
        self.solution_structural = None
        self.solution_acoustic = None
        self.flag_set_material = False
        self.flag_set_crossSection = False
        self.plot_pressure_field = False
        self.is_file_loaded = False

        self.time_to_process_cross_sections = None
        self.time_to_solve_model = None
        self.time_to_postprocess = None
        self.lines_with_cross_section_by_elements = []
        self.lines_multiples_cross_sections = []

        self.stresses_values_for_color_table = None
        self.min_stress = ""
        self.max_stress = ""
        self.stress_label = ""

    def new_project(self, project_path, project_name, element_size, import_type, material_list_path, fluid_list_path, geometry_path = "", coord_path = "", conn_path = ""):
        self.reset_info()
        self.file.new(project_path, project_name, element_size, import_type, material_list_path, fluid_list_path, geometry_path, coord_path, conn_path)
        self._project_name = project_name

        if self.file.get_import_type() == 0:
            self.mesh.generate(self.file.geometry_path, self.file.element_size)
        elif self.file.get_import_type() == 1:
            self.mesh.load_mesh(self.file.coord_path, self.file.conn_path)

        self.file.create_entity_file(self.get_entities())

    def load_project(self, project_file_path):

        self.reset_info()
        self.file.load(project_file_path)
        self._project_name = self.file._project_name

        if self.file.get_import_type() == 0:
            self.mesh.generate(self.file.geometry_path, self.file.element_size)
        elif self.file.get_import_type() == 1:
            self.mesh.load_mesh(self.file.coord_path, self.file.conn_path)

        self.load_structural_bc_file()
        self.load_acoustic_bc_file()
        self.load_entity_file()

        # if self.file.temp_table_name is None:
        self.load_analysis_file()
        if self.file.temp_table_name is not None:
            self.load_frequencies_from_table()

    def load_project_progress_bar(self, project_file_path, progressBar, textLabel):

        progressBar.setValue(0)
        textLabel.setText("Loading Project File...")
        self.reset_info()
        self.file.load(project_file_path)
        progressBar.setValue(10)
        textLabel.setText("Generating Mesh...")
        self._project_name = self.file._project_name

        if self.file.get_import_type() == 0:
            self.mesh.generate(self.file.geometry_path, self.file.element_size)
        elif self.file.get_import_type() == 1:
            self.mesh.load_mesh(self.file.coord_path, self.file.conn_path)
        progressBar.setValue(30)
        textLabel.setText("Loading Structural B.C File...")

        self.load_structural_bc_file()
        progressBar.setValue(50)
        textLabel.setText("Loading Acoustic B.C File...")
        self.load_acoustic_bc_file()
        progressBar.setValue(70)
        textLabel.setText("Loading Entity File...")
        self.load_entity_file()
        progressBar.setValue(90)

   
        textLabel.setText("Loading Analysis File...")
        self.load_analysis_file()
        if self.file.temp_table_name is not None:
            textLabel.setText("Loading Frequencies from Table...")
            self.load_frequencies_from_table()
        progressBar.setValue(100)
        textLabel.setText("Complete!")
  
    def set_entity(self, tag):
        return Entity(tag)

    def load_entity_file(self):

        dict_materials, dict_cross_sections, dict_element_types, dict_fluids, dict_element_length_correction, dict_capped_end_entity, dict_capped_end_element = self.file.get_dict_of_entities_from_file()
        self.lines_multiples_cross_sections = []

        # Element type to Entities
        for key, el_type in dict_element_types.items():
            if self.file.element_type_is_structural:
                self.load_element_type_by_entity(key, el_type)

        # Length correction to Elements
        for key, value in dict_element_length_correction.items():
            self.load_length_correction_by_elements(value[0], value[1], key)

        # Material to Entities
        for key, mat in dict_materials.items():
            self.load_material_by_entity(key, mat)

        # Fluid to Entities
        for key, fld in dict_fluids.items():
            self.load_fluid_by_entity(key, fld)

        # Cross-section to Entities
        for key, cross in dict_cross_sections.items():
            if "-" in key:
                self.load_cross_section_by_element(cross[1], cross[0])
                self.lines_multiples_cross_sections.append(int(key.split("-")[0]))  
                # self._set_entity_cross_section(key.split("-")[0], cross)
            else:
                self.load_cross_section_by_entity(int(key), cross)

        # capped end
        for key, capped in dict_capped_end_element.items():
            elements = capped[1]
            value = capped[0]
            selection = key
            self.load_capped_end_by_element(elements, value, selection)
        for key, capped in dict_capped_end_entity.items():
            lines = capped[1]
            value = capped[0]
            selection = key
            self.load_capped_end_by_entity( lines, value, selection)

    def load_mapped_cross_section(self):        
        label_etypes = ['pipe_1', 'pipe_2', 'beam_1']
        indexes = [0, 1, 2]
        dict_etype_index = dict(zip(label_etypes,indexes))
        dict_index_etype = dict(zip(indexes,label_etypes))
        # dict_tag_entity = self.mesh.get_dict_of_entities()
        # map_cross_section_to_lines = defaultdict(list)
        map_cross_section_to_elements = defaultdict(list)

        # for line, entity in dict_tag_entity.items():
        for index, element in self.mesh.structural_elements.items():

            ext_diam = element.cross_section.external_diameter
            thickness = element.cross_section.thickness
            offset_y = element.cross_section.offset_y
            offset_z = element.cross_section.offset_z
            insulation_thickness = element.cross_section.insulation_thickness
            insulation_density = element.cross_section.insulation_density

            e_type  = element.element_type

            if e_type is None:
                e_type = 'pipe_1'
                self.acoustic_analysis = True
            
            poisson = element.material.poisson_ratio
            if poisson is None:
                poisson = 0

            #TODO: codify section_parameters of BEAM element
            
            index_etype = dict_etype_index[e_type]
            map_cross_section_to_elements[str([ext_diam, thickness, offset_y, offset_z, poisson, index_etype, insulation_thickness, insulation_density])].append(index)

        for key, elements in map_cross_section_to_elements.items():
            cross_strings = key[1:-1].split(',')
            vals = [float(value) for value in cross_strings]
            el_type = dict_index_etype[vals[5]]
            if el_type in ['pipe_1', 'pipe_2']:
                cross_section = CrossSection(vals[0], vals[1], vals[2], vals[3], poisson_ratio=vals[4], element_type=el_type, insulation_thickness=vals[6], insulation_density=vals[7])
                # list_flatten = [item for sublist in elements for item in sublist]
                self.mesh.set_cross_section_by_element(elements, cross_section, update_cross_section=True)  

    def get_dict_multiple_cross_sections(self):

        if len(self.lines_with_cross_section_by_elements)==0:
            return

        for line in self.lines_with_cross_section_by_elements:
            dict_multiple_cross_sections = defaultdict(list)
            list_elements = self.mesh.line_to_elements[line]
            elements = self.mesh.structural_elements
 
            for _id in list_elements:

                ext_diam = elements[_id].cross_section.external_diameter
                thickness = elements[_id].cross_section.thickness
                offset_y = elements[_id].cross_section.offset_y
                offset_z = elements[_id].cross_section.offset_z
                insultation_thickness = elements[_id].cross_section.insulation_thickness
                insultation_density = elements[_id].cross_section.insulation_density
                
                dict_multiple_cross_sections[str([ext_diam, thickness, offset_y, offset_z, insultation_thickness, insultation_density])].append(_id)
            
            _cross_section = elements[_id].cross_section
            
            if len(dict_multiple_cross_sections) == 1:
                if np.sort(list_elements).tolist() == np.sort(list(dict_multiple_cross_sections.values()))[0].tolist():
                    # print("Line: {}".format(line))
                    self.set_cross_section_by_entity(line, _cross_section)
            else:
                self.file.add_multiple_cross_section_in_file(line, dict_multiple_cross_sections)     

    def load_structural_bc_file(self):
        prescribed_dofs, external_loads, mass, spring, damper = self.file.get_dict_of_structural_bc_from_file()
        
        for key, dofs in prescribed_dofs.items():
            if isinstance(dofs, list):
                try:
                    self.load_prescribed_dofs_bc_by_node(key, dofs)
                except Exception:
                    error("There is some error while loading prescribed dofs data.")

        for key, loads in external_loads.items():
            if isinstance(loads, list):
                try:
                    self.load_structural_loads_by_node(key, loads)
                except Exception:
                    error("There is some error while loading nodal loads data.")

        for key, masses in mass.items():
            if isinstance(masses, list):
                try:
                    self.load_mass_by_node(key, masses)
                except Exception:
                    error("There is some error while loading lumped masses/moments of inertia data.")
                
        for key, stiffness in spring.items():
            if isinstance(stiffness, list):
                try:
                    self.load_spring_by_node(key, stiffness)
                except Exception:
                    error("There is some error while lumped stiffness data.")    

        for key, dampings in damper.items():
            if isinstance(dampings, list):
                try:
                    self.load_damper_by_node(key, dampings)
                except Exception:
                    error("There is some error while lumped damping data.")   

    def load_acoustic_bc_file(self):
        pressure, volume_velocity, specific_impedance, radiation_impedance = self.file.get_dict_of_acoustic_bc_from_file()
        for key, ActPres in pressure.items():
            if ActPres is not None:
                self.load_acoustic_pressure_bc_by_node(key, ActPres)
        for key, VelVol in volume_velocity.items():
            if VelVol is not None:
                self.load_volume_velocity_bc_by_node(key, VelVol)
        for key, SpecImp in specific_impedance.items():
            if SpecImp is not None:
                self.load_specific_impedance_bc_by_node(key, SpecImp)
        for key, RadImp in radiation_impedance.items():
            if RadImp is not None:
                self.load_radiation_impedance_bc_by_node(key, RadImp)

    def load_analysis_file(self):
        self.f_min, self.f_max, self.f_step, self.global_damping = self.file.load_analysis_file()

    def load_frequencies_from_table(self):
        self.f_min, self.f_max, self.f_step = self.file.f_min, self.file.f_max, self.file.f_step
        self.frequencies = self.file.frequencies 

    def set_material(self, material):
        self.mesh.set_material_by_element('all', material)
        self._set_all_entity_material(material)
        for entity in self.mesh.entities:
            self.file.add_material_in_file(entity.get_tag(), material.identifier)

    def set_material_by_entity(self, entity_id, material):
        if self.file.get_import_type() == 0:
            self.mesh.set_material_by_line(entity_id, material)
        elif self.file.get_import_type() == 1:
            self.mesh.set_material_by_element('all', material)

        self._set_entity_material(entity_id, material)
        self.file.add_material_in_file(entity_id, material.identifier)

    def set_cross_section_to_all(self, cross_section):
        self.mesh.set_cross_section_by_element('all', cross_section)
        self._set_all_entity_crossSection(cross_section)
        for entity in self.mesh.entities:
            self.file.add_cross_section_in_file(entity.get_tag(), cross_section)

    def set_cross_section_by_elements(self, elements, cross_section):
        self.mesh.set_cross_section_by_element(elements, cross_section)
        dict_elements_to_line = self.mesh.elements_to_line
        for element in elements:
            line = dict_elements_to_line[element]
            if line not in self.lines_with_cross_section_by_elements:
                self.lines_with_cross_section_by_elements.append(line)

    def set_cross_section_by_entity(self, entity_id, cross_section):
        if self.file.get_import_type() == 0:
            self.mesh.set_cross_section_by_line(entity_id, cross_section)
        elif self.file.get_import_type() == 1:
            self.mesh.set_cross_section_by_element('all', cross_section)

        self._set_entity_cross_section(entity_id, cross_section)
        self.file.add_cross_section_in_file(entity_id, cross_section)

    def set_element_type_to_all(self, element_type):
        self.mesh.set_element_type_by_element('all', element_type)
        self._set_all_entity_element_type(element_type)
        for entity in self.mesh.entities:
            self.file.add_element_type_in_file(entity.get_tag(), element_type)

    def set_element_type_by_entity(self, entity_id, element_type):
        if self.file.get_import_type() == 0:
            self.mesh.set_element_type_by_line(entity_id, element_type)
        elif self.file.get_import_type() == 1:
            self.mesh.set_element_type_by_element('all', element_type)

        self._set_entity_element_type(entity_id, element_type)
        self.file.add_element_type_in_file(entity_id, element_type)

    def set_prescribed_dofs_bc_by_node(self, node_id, values, imported_table, table_name=""):
        self.mesh.set_prescribed_dofs_bc_by_node(node_id, values)
        labels = ["displacements", "rotations"]
        self.file.add_structural_bc_in_file(node_id, values, imported_table, table_name, labels)

    def set_loads_by_node(self, node_id, values, imported_table, table_name=""):
        self.mesh.set_structural_load_bc_by_node(node_id, values)
        labels = ["forces", "moments"]
        self.file.add_structural_bc_in_file(node_id, values, imported_table, table_name, labels)

    def add_lumped_masses_by_node(self, node_id, values, imported_table, table_name=""):
        self.mesh.add_mass_to_node(node_id, values)
        labels = ["masses", "moments of inertia"]
        self.file.add_structural_bc_in_file(node_id, values, imported_table, table_name, labels)

    def add_lumped_stiffness_by_node(self, node_id, values, imported_table, table_name=""):
        self.mesh.add_spring_to_node(node_id, values)
        labels = ["spring stiffness", "torsional spring stiffness"]
        self.file.add_structural_bc_in_file(node_id, values, imported_table, table_name, labels)

    def add_lumped_dampings_by_node(self, node_id, values, imported_table, table_name=""):
        self.mesh.add_damper_to_node(node_id, values)
        labels = ["damping coefficients", "torsional damping coefficients"]
        self.file.add_structural_bc_in_file(node_id, values, imported_table, table_name, labels)

    def load_material_by_entity(self, entity_id, material):
        if self.file.get_import_type() == 0:
            self.mesh.set_material_by_line(entity_id, material)
        elif self.file.get_import_type() == 1:
            self.mesh.set_material_by_element('all', material)

        self._set_entity_material(entity_id, material)

    def load_fluid_by_entity(self, entity_id, fluid):
        if self.file.get_import_type() == 0:
            self.mesh.set_fluid_by_line(entity_id, fluid)
        elif self.file.get_import_type() == 1:
            self.mesh.set_fluid_by_element('all', fluid)

        self._set_entity_fluid(entity_id, fluid)

    def load_cross_section_by_element(self, elements_id, cross_section):
        self.mesh.set_cross_section_by_element(elements_id, cross_section)

    def load_cross_section_by_entity(self, entity_id, cross_section):
        if self.file.get_import_type() == 0:
            self.mesh.set_cross_section_by_line(entity_id, cross_section)
        elif self.file.get_import_type() == 1:
            self.mesh.set_cross_section_by_element('all', cross_section)

        self._set_entity_cross_section(entity_id, cross_section)

    def load_element_type_by_entity(self, entity_id, element_type):
        if self.file.get_import_type() == 0:
            self.mesh.set_element_type_by_line(entity_id, element_type)
        elif self.file.get_import_type() == 1:
            self.mesh.set_element_type_by_element('all', element_type)

        self._set_entity_element_type(entity_id, element_type)

    def load_structural_loads_by_node(self, node_id, values):
        self.mesh.set_structural_load_bc_by_node(node_id, values)

    def load_mass_by_node(self, node_id, mass):
        self.mesh.add_mass_to_node(node_id, mass)

    def load_spring_by_node(self, node_id, stiffness):
        self.mesh.add_spring_to_node(node_id, stiffness)

    def load_damper_by_node(self, node_id, dampings):
        self.mesh.add_damper_to_node(node_id, dampings)
    
    def load_capped_end_by_element(self, elements, value, selection):
        self.mesh.set_capped_end_by_element(elements, value, selection)

    def load_capped_end_by_entity(self, lines, value, selection):
        if self.file.get_import_type() == 0:
            self.mesh.set_capped_end_by_line(lines, value, selection)
        # elif self.file.get_import_type() == 1:
        #     self.mesh.set_capped_end_by_element('all', value)

    def get_nodes_bc(self):
        return self.mesh.nodes_with_prescribed_dofs

    def get_elements(self):
        return self.mesh.structural_elements
    
    def get_element(self, element_id):
        return self.mesh.structural_elements[element_id]

    def set_frequencies(self, frequencies, min_, max_, step_):
        if max_ != 0 and step_ != 0:
            self.f_min, self.f_max, self.f_step = min_, max_, step_
            self.file.add_frequency_in_file(min_, max_, step_)
        self.frequencies = frequencies

    def load_prescribed_dofs_bc_by_node(self, node_id, bc):
        self.mesh.set_prescribed_dofs_bc_by_node(node_id, bc)

    def _set_entity_material(self, entity_id, material):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.material = material
                return

    def _set_all_entity_material(self, material):
        for entity in self.mesh.entities:
            entity.material = material

    def _set_entity_cross_section(self, entity_id, cross):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.crossSection = cross
                return

    def _set_all_entity_crossSection(self, cross):
        for entity in self.mesh.entities:
            entity.crossSection = cross

    def _set_entity_element_type(self, entity_id, element_type):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.element_type = element_type
                return

    def _set_all_entity_element_type(self, element_type):
        for entity in self.mesh.entities:
            entity.element_type = element_type

    def get_nodes_with_prescribed_dofs_bc(self):
        return self.mesh.nodes_with_prescribed_dofs

    def get_structural_elements(self):
        return self.mesh.structural_elements

    def set_fluid_by_entity(self, entity_id, fluid):
        if self.file.get_import_type() == 0:
            self.mesh.set_fluid_by_line(entity_id, fluid)
        elif self.file.get_import_type() == 1:
            self.mesh.set_fluid_by_element('all', fluid)

        self._set_entity_fluid(entity_id, fluid)
        self.file.add_fluid_in_file(entity_id, fluid.identifier)

    def set_fluid(self, fluid):
        self.mesh.set_fluid_by_element('all', fluid)
        self._set_all_entity_fluid(fluid)
        for entity in self.mesh.entities:
            self.file.add_fluid_in_file(entity.get_tag(), fluid.identifier)

    def set_acoustic_pressure_bc_by_node(self, node_id, values, imported_table, table_name=""):
        self.mesh.set_acoustic_pressure_bc_by_node(node_id, values) 
        label = ["acoustic pressure"] 
        self.file.add_acoustic_bc_in_file(node_id, values, imported_table, table_name, label) 
    
    def set_volume_velocity_bc_by_node(self, node_id, values, imported_table, table_name=""):
        self.mesh.set_volume_velocity_bc_by_node(node_id, values) 
        label = ["volume velocity"] 
        self.file.add_acoustic_bc_in_file(node_id, values, imported_table, table_name, label)    
    
    def set_specific_impedance_bc_by_node(self, node_id, values, imported_table, table_name=""):
        self.mesh.set_specific_impedance_bc_by_node(node_id, values) 
        label = ["specific impedance"] 
        self.file.add_acoustic_bc_in_file(node_id, values, imported_table, table_name, label)   

    def set_radiation_impedance_bc_by_node(self, node_id, values, imported_table = None, table_name=""):
        self.mesh.set_radiation_impedance_bc_by_node(node_id, values) 
        label = ["radiation impedance"] 
        self.file.add_acoustic_bc_in_file(node_id, values, imported_table, table_name, label) 
    
    def set_element_length_correction_by_elements(self, elements, value, section):
        # label = ["acoustic element length correction"] 
        self.mesh.set_length_correction_by_element(elements, value, section)
        self.file.add_length_correction_in_file(elements, value, section)

    def set_capped_end_by_elements(self, elements, value, selection):
        self.mesh.set_capped_end_by_element(elements, value, selection)
        self.file.add_capped_end_element_in_file(elements, value, selection)

    def set_capped_end_by_line(self, lines, value, selection):
        if lines == "all":
            self.mesh.set_capped_end_all_lines(value, selection)
            for tag in self.mesh.all_lines:
                self.file.add_capped_end_entity_in_file(tag, value, selection)
        else:
            self.mesh.set_capped_end_by_line(lines, value, selection)
            for tag in lines:
                self.file.add_capped_end_entity_in_file(tag, value, selection)

    def set_capped_end_all_lines(self, lines, value, selection):
        self.mesh.set_capped_end_by_line(lines, value, selection)

    def get_nodes_with_acoustic_pressure_bc(self):
        return self.mesh.nodesAcousticBC

    def get_acoustic_elements(self):
        return self.mesh.acoustic_elements

    def load_acoustic_pressure_bc_by_node(self, node_id, bc):
        self.mesh.set_acoustic_pressure_bc_by_node(node_id, bc)

    def load_volume_velocity_bc_by_node(self, node_id, value):
        self.mesh.set_volume_velocity_bc_by_node(node_id, value)

    def load_specific_impedance_bc_by_node(self, node_id, value):
        self.mesh.set_specific_impedance_bc_by_node(node_id, value)

    def load_radiation_impedance_bc_by_node(self, node_id, value):
        self.mesh.set_radiation_impedance_bc_by_node(node_id, value)

    def load_length_correction_by_elements(self, elements, value, key):
        self.mesh.set_length_correction_by_element(elements, value, key)

    def _set_entity_fluid(self, entity_id, fluid):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.fluid = fluid
                return

    def _set_all_entity_fluid(self, fluid):
        for entity in self.mesh.entities:
            entity.fluid = fluid

    def get_map_nodes(self):
        return self.mesh.map_nodes

    def get_map_elements(self):
        return self.mesh.map_elements

    def get_mesh(self):
        return self.mesh

    def get_nodes_color(self):
        return self.mesh.nodes_color

    def get_nodes(self):
        return self.mesh.nodes

    def get_entities(self):
        return self.mesh.entities

    def get_node(self, node_id):
        return self.mesh.nodes[node_id]

    def get_entity(self, entity_id):
        for entity in self.mesh.entities:
            if entity.get_tag() == entity_id:
                return entity

    def get_element_size(self):
        return self.file.element_size

    def check_entity_material(self):
        for entity in self.get_entities():
            if entity.getMaterial() is None:
                return False
        return True

    def check_entity_crossSection(self):
        for entity in self.get_entities():
            if entity.getCrossSection() is None:
                return False
        return True

    def set_modes(self, modes):
        self.modes = modes

    def get_frequencies(self):
        return self.frequencies

    def get_frequency_setup(self):
        return self.f_min, self.f_max, self.f_step

    def get_modes(self):
        return self.modes

    def get_material_list_path(self):
        return self.file.material_list_path
    
    def get_fluid_list_path(self):
        return self.file._fluid_list_path

    def get_project_name(self):
        return self._project_name

    def set_analysis_type(self, ID, analysis_text, method_text = ""):
        self.analysis_ID = ID
        self.analysis_type_label = analysis_text
        self.analysis_method_label = method_text

    def get_analysis_id(self): 
        return self.analysis_ID

    def get_analysis_type_label(self):
        return self.analysis_type_label

    def get_analysis_method_label(self):
        return self.analysis_method_label

    def set_damping(self, value):
        self.global_damping = value
        self.file.add_damping_in_file(value)

    def get_damping(self):
        return self.global_damping

    def get_structural_solve(self):
        if self.analysis_ID in [5,6]:
            results = SolutionStructural(self.mesh, self.frequencies, acoustic_solution=self.solution_acoustic)
        else:
            results = SolutionStructural(self.mesh, self.frequencies)
        return results

    def set_structural_solution(self, value):
        self.solution_structural = value

    def get_structural_solution(self):
        return self.solution_structural

    def get_acoustic_solve(self):
        return SolutionAcoustic(self.mesh, self.frequencies)

    def set_acoustic_solution(self, value):
        self.solution_acoustic = value
    
    def get_acoustic_solution(self):
        return self.solution_acoustic

    def set_acoustic_natural_frequencies(self, value):
        self.natural_frequencies_acoustic = value
    
    def set_structural_natural_frequencies(self, value):
        self.natural_frequencies_structural  = value

    def get_structural_natural_frequencies(self):
        return self.natural_frequencies_structural

    def get_unit(self, stress=False):
        analysis = self.analysis_ID
        if analysis >=0 and analysis <= 6:
            if (analysis in [3,5,6] and self.plot_pressure_field) or stress:
                return "Pa"
            elif analysis in [5,6] and not self.plot_pressure_field:
                return "m"            
            elif analysis in [0,1]:
                return "m"
            else:
                return "-"  

    def set_stresses_values_for_color_table(self, values):
        self.stresses_values_for_color_table = values
    
    def set_min_max_type_stresses(self, min_stress, max_stress, stress_label):
        self.min_stress = min_stress
        self.max_stress = max_stress
        self.stress_label = stress_label