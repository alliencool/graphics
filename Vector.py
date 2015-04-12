import math

class VectorException(Exception):
    pass

class Vector3D(object):

    def __init__(self, coords):
        super(Vector3D, self).__init__()
        if len(coords) != 3:
            raise VectorException("Vector3D is only for 3 dimensinal vectors.")
        
        self.coords = coords


    def __add__(self, vector):
        
        if isinstance(vector, int) or isinstance(vector, float):
            return Vector3D([vector + i for i in self.coords])

        if not isinstance(vector, Vector3D):
            raise VectorException("Scalar multiplication can be done only with Vector objects or numer.")

        return Vector3D([self.coords[i] + vector.coords[i] for i in xrange(len(self.coords))])

    def __sub__(self, vector):
        return self.__add__(vector * -1)

    def __xor__(self, vector):

        if not isinstance(vector, Vector3D):
            raise VectorException("Scalar multiplication can be done only with Vector objects.")

        return sum((self.coords[i] * vector.coords[i] for i in xrange(len(self.coords))))

    def __mul__(self, vector):

        if isinstance(vector, int) or isinstance(vector, float):
            return Vector3D([vector * i for i in self.coords])

        if not isinstance(vector, Vector3D):
            raise VectorException("Scalar multiplication can be done only with Vector objects or numer.")

        return Vector3D([self.coords[1] * vector.coords[2] - self.coords[2] * vector.coords[1],
                         self.coords[2] * vector.coords[0] - self.coords[0] * vector.coords[2],
                         self.coords[0] * vector.coords[1] - self.coords[1] * vector.coords[0]])

    def normalize(self):
 
        length = math.sqrt(sum((self.coords[i] * self.coords[i] for i in xrange(len(self.coords)))))
        self.coords = [i / length for i in self.coords]

    def __str__(self):
        return "(" + ", ".join((str(i) for i in self.coords)) + ")"

def check():
    v1 = Vector3D([1, 2, 3])
    v2 = Vector3D([3, 2, 1])

    print v1 ^ v2

    print Vector3D([1,0,0]) * Vector3D([0,1,0])
    print Vector3D([1,0,0]) + Vector3D([0,1,0])
    print Vector3D([1,0,0]) - Vector3D([0,1,0])
