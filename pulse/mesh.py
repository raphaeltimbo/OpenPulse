from os.path import isfile
from pulse.utils import split_sequence
from collections import deque
import gmsh 

class Mesh:
    def __init__(self, path=''):
        self.path = path
        self.nodes = []
        self.edges = []

    def reset_variables(self):
        self.nodes = []
        self.edges = []

    def generate(self, min_element_size=0, max_element_size=1e+019):
        if isfile(self.path):
            self.reset_variables()
            self.__initialize_gmsh()
            self.__set_gmsh_options(min_element_size, max_element_size)
            self.__generate_meshes()
            self.__read_nodes()
            self.__read_edges()
            self.__finalize()
        else:
            return FileNotFoundError

    def reorder_index(self):
        neighbors = self.get_neighbors()
        translator = {}
        stack = deque()
        index = 0

        stack.append(self.nodes[0][0])

        while stack:
            top = stack.pop()

            if top not in translator:
                translator[top] = index
                index += 1
            else:
                continue 
            
            for neighbor in neighbors[top]:
                if neighbor not in translator:
                    stack.append(neighbor)

        self.translate_index(translator)

    def translate_index(self, translator):
        translated_nodes = []
        translated_edges = []

        for (index, x, y, z) in self.nodes:
            if index in translator:
                node = (translator[index], x, y, z)
                translated_nodes.append(node)

        for (index, start, end) in self.edges:
            if start and end in translator:
                edge = (index, translator[start], translator[end])
                translated_edges.append(edge)

        self.nodes = translated_nodes
        self.edges = translated_edges

    def get_neighbors(self):
        neighbors = {}

        for _, start, end in self.edges:
            if start not in neighbors:
                neighbors[start] = []

            if end not in neighbors:
                neighbors[end] = []

            neighbors[start].append(end)
            neighbors[end].append(start)

        return neighbors

    def __initialize_gmsh(self):
        gmsh.initialize('', False)
        gmsh.logger.stop()
        gmsh.merge(self.path)

    def __set_gmsh_options(self, min_element_size, max_element_size):
        gmsh.option.setNumber('Mesh.CharacteristicLengthMin', float(min_element_size) * 1000)
        gmsh.option.setNumber('Mesh.CharacteristicLengthMax', float(max_element_size) * 1000)
        gmsh.option.setNumber('Mesh.Optimize', 1)
        gmsh.option.setNumber('Mesh.OptimizeNetgen', 0)
        gmsh.option.setNumber('Mesh.HighOrderOptimize', 0)
        gmsh.option.setNumber('Mesh.ElementOrder', 1)
        gmsh.option.setNumber('Mesh.Algorithm', 2)
        gmsh.option.setNumber('Mesh.Algorithm3D', 1)
        gmsh.option.setNumber('Geometry.Tolerance', 1e-06)

    def __generate_meshes(self):
        gmsh.model.mesh.generate(3)
        gmsh.model.mesh.removeDuplicateNodes()

    def __read_nodes(self):
        index, coordinates, _ = gmsh.model.mesh.getNodes()
        coordinates = split_sequence(coordinates, 3)

        for index, (x, y, z) in zip(index, coordinates):
            node = index, x, y, z
            self.nodes.append(node)

    def __read_edges(self):
        _, index, connectivity = gmsh.model.mesh.getElements() 
        index = index[0]
        connectivity = connectivity[0]
        connectivity = split_sequence(connectivity, 2)

        for index, (start, end) in zip(index, connectivity):
            edges = index, start, end
            self.edges.append(edges)

    def __finalize(self):
        gmsh.finalize()
