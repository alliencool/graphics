
class ObjParser(object):

    VERTEX_PREFIX = "v "
    FACE_PREFIX = "f "

    def __init__(self):
        super(ObjParser, self).__init__()

    def _parse_vertex(self, line):
        return [float(coord) for coord in line.split(" ")[1:]]
    
    def _parse_face(self, line):
        return [triple.split("/") for triple in line.split(" ")[1:]]

    def parse(self, filename):
        result = ObjModel()
        with open(filename) as fd:
            for line in fd:
                if line.startswith(self.VERTEX_PREFIX):
                    result.add_vertex(self._parse_vertex(line))
                if line.startswith(self.FACE_PREFIX):
                    result.add_face(self._parse_face(line))

        return result


class ObjModel(object):

    def __init__(self):
        super(ObjModel, self).__init__()
        self.vertices = []
        self.faces = []

    def get_vertices(self):
        return self.vertices

    def set_vertices(self, vertices):
        self.vertices = vertices

    def add_vertex(self, vertex):
        self.vertices.append(vertex)
    
    def get_faces(self):
        return self.faces

    def set_faces(self, faces):
        self.faces = faces

    def add_face(self, face):
        self.faces.append(face)
