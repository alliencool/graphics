import Tkinter
import obj_handler
import time

BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
WHITE = (255, 255, 255)

class GraphicsException(Exception):
    pass

class MyCanvas(object):

    C_PATTERN = "#%02x%02x%02x"
    
    def __init__(self, root, window_width, window_height):

        self.WIDTH = window_width
        self.HEIGHT = window_height
        
        self.image = Tkinter.PhotoImage(width=self.WIDTH, height=self.HEIGHT)
        
        black_str = self.C_PATTERN % BLACK
        self.image_data = [[black_str for i in xrange(self.WIDTH)] for j in xrange(self.HEIGHT)]

        self.image.put((self.C_PATTERN % BLACK), (0, 0, self.WIDTH, self.HEIGHT))
        
        canvas = Tkinter.Canvas(root, width=self.WIDTH, height=self.HEIGHT)
        canvas.pack()
        canvas.create_image(0, 0, image=self.image, anchor=Tkinter.NW)

    def _data_conv(self):
        return tuple([tuple(row) for row in self.image_data])
    
    def put_to_image(self, x, y, c_tuple):
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            raise GraphicsException("Coordinate does not fit into the canvas sizes.")
        
        self.image_data[self.HEIGHT - y][x] = self.C_PATTERN % c_tuple

    def refresh_image(self):
        self.image.put(self._data_conv())

    def line(self, x0, y0, x1, y1, color):
        '''
        Bresenham algorithm for drawing a line
        '''
        if x0 < 0 or x0 >= self.WIDTH or y0 < 0 or y0 >= self.HEIGHT or\
           x1 < 0 or x1 >= self.WIDTH or y1 < 0 or y1 >= self.HEIGHT:
            raise GraphicsException("Coordinates do not fit into the canvas sizes.")

        steep = False

        if abs(x1 - x0) < abs(y1 - y0):
            x0, x1, y0, y1 = y0, y1, x0, x1
            steep = True

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = y1 - y0
        dx2 = 2 * dx 
        
        add = 1
        if dy < 0:
            add = -1
        
        factor = 2 * abs(dy)
        error = 0
        y = y0
        
        for x in xrange(x0, x1 + 1):
            if steep:
                self.put_to_image(y, x, color)
            else:
                self.put_to_image(x, y, color)
            
            error += factor
            if error > dx:
                y += add
                error -= dx2


def first_lesson(canvas, model, center_x, center_y, shift_x, shift_y):
   
    shift_x = int(shift_x)
    shift_y = int(shift_y)
    
    for face in model.get_faces():
        coords = []
        for i in xrange(3):
            vert = model.get_vertices()[int(face[i][0]) - 1]
   
            x = int((vert[0] + 1) * center_x)
            y = int((vert[1] + 1) * center_y)

            coords.append((x + shift_x, y + shift_y))
        
        for i in xrange(3):
            j = (i + 1) % 3
            canvas.line(coords[i][0], coords[i][1], coords[j][0], coords[j][1], WHITE)


if __name__ == "__main__":
    
    root = Tkinter.Tk()

    size_x = 1024
    size_y = 1024
    center_x = 1.0 * (size_x) / 4
    center_y = 1.0 * (size_y) / 4
    canvas = MyCanvas(root, size_x + 1, size_y + 1)
    
    obj_parser = obj_handler.ObjParser()
    model = obj_parser.parse("african_head.obj.txt")
    first_lesson(canvas, model, center_x, center_y, center_x, center_y)

    #canvas.line(13, 20, 80, 40, WHITE)
    #canvas.line(20, 13, 40, 80, RED)
    #canvas.line(80, 40, 13, 20, GREEN)
    canvas.refresh_image()    
    root.mainloop()
    #root.destroy()

