import Tkinter
import obj_handler

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

        x = 0
        y = 0
        while True:
            self.put_to_image(x, y, BLACK)
            x += 1
            if x == self.WIDTH:
                x = 0
                y += 1
            if y == self.HEIGHT:
                break


        canvas = Tkinter.Canvas(root, width=self.WIDTH, height=self.HEIGHT)
        canvas.pack()
        canvas.create_image(0, 0, image=self.image, anchor=Tkinter.NW)

    def put_to_image(self, x, y, c_tuple):
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            raise GraphicsException("Coordinate does not fit into the canvas sizes.")
       
        self.image.put(self.C_PATTERN % c_tuple, (x, self.HEIGHT - y))

    def simple_line(self, x0, y0, x1, y1, color):
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
                self.put_to_image(int(y), int(x), color)
            else:
                self.put_to_image(int(x), int(y), color)
            
            error += factor
            if error > dx:
                y += add
                error -= dx2

if __name__ == "__main__":
    
    root = Tkinter.Tk()
    
    obj_parser = obj_handler.ObjParser()
    model = obj_parser.parse("african_head.obj.txt")

    size_x = 1024
    size_y = 1024
    center_x = 1.0 * (size_x) / 2
    center_y = 1.0 * (size_y) / 2
    canvas = MyCanvas(root, size_x + 1, size_y + 1)
    
    for face in model.get_faces():
        for i in xrange(3):
            vert0 = model.get_vertices()[int(face[i][0]) - 1]
            vert1 = model.get_vertices()[int(face[(i + 1) % 3][0]) - 1]
   
            x0 = int((vert0[0] + 1) * center_x)
            y0 = int((vert0[1] + 1) * center_y)
    
            x1 = int((vert1[0] + 1) * center_x)
            y1 = int((vert1[1] + 1) * center_y)
            
            canvas.simple_line(x0, y0, x1, y1, WHITE)

    #canvas.simple_line(13, 20, 80, 40, WHITE)
    #canvas.simple_line(20, 13, 40, 80, RED)
    #canvas.simple_line(80, 40, 13, 20, GREEN)
    
    root.mainloop()
    #root.destroy()

