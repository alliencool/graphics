import math

class VectorException(Exception):
    pass

class Vector3D(object):

    def __init__(self, coords=None):
        super(Vector3D, self).__init__()
        if coords == None:
            coords = [0, 0, 0]
        elif len(coords) != 3:
            raise VectorException("Vector3D is only for 3 dimensinal vectors.")
        
        self.coords = coords


    def __add__(self, vector):
        
        if isinstance(vector, int) or isinstance(vector, float):
            return Vector3D([vector + i for i in self.coords])

        if not isinstance(vector, Vector3D):
            raise VectorException("Addition and substraction can be done only with Vector objects or numeric.")

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
            raise VectorException("Vector multiplication can be done only with Vector objects or numer.")

        return Vector3D([self.coords[1] * vector.coords[2] - self.coords[2] * vector.coords[1],
                         self.coords[2] * vector.coords[0] - self.coords[0] * vector.coords[2],
                         self.coords[0] * vector.coords[1] - self.coords[1] * vector.coords[0]])

    def __div__(self, numeric):

        if isinstance(numeric, int) or isinstance(numeric, float):
            if numeric == 0:
                raise VectorException("Division by zero.")
        else:
            raise VectorException("Vector division can be done only with numeric.") 

        return Vector3D([coord / numeric for coord in self.coords])

    def __getitem__(self, index):
        if index < 0 or index > len(self.coords):
            raise VectorException("Index is out of bounds.")

        return self.coords[index]

    def __str__(self):
        return "(" + ", ".join((str(i) for i in self.coords)) + ")"

    def normalize(self):
 
        length = math.sqrt(sum((self.coords[i] * self.coords[i] for i in xrange(len(self.coords)))))
        self.coords = [i / length for i in self.coords]

    @property
    def x(self):
        return self.coords[0]
    
    @x.setter
    def x(self, value):
        self.coords[0] = value
    
    @property
    def y(self):
        return self.coords[1]
    
    @y.setter
    def y(self, value):
        self.coords[1] = value
    
    @property
    def z(self):
        return self.coords[2]
    
    @z.setter
    def z(self, value):
        self.coords[2] = value

def check():
    v1 = Vector3D([1, 2, 3])
    v2 = Vector3D([3, 2, 1])

    print v1 ^ v2

    print Vector3D([1,0,0]) * Vector3D([0,1,0])
    print Vector3D([1,0,0]) + Vector3D([0,1,0])
    print Vector3D([1,0,0]) - Vector3D([0,1,0])

    print v1.x, v1.y, v1.z
    v1.x = 10
    v1.y = 20
    v1.z = 30
    print v1.x, v1.y, v1.z
    print v1
