import random
import time
import tkinter

import obj_handler
import tga_handler
from vector import Vector, Vector3D

BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
WHITE = (255, 255, 255)

class GraphicsException(Exception):
    pass


class MyCanvas:

    C_PATTERN = "#%02x%02x%02x"
    
    def __init__(self, root, window_width, window_height):

        self.width = window_width
        self.height = window_height
        
        self.images = []
        self.images.append(tkinter.PhotoImage(width=self.width, height=self.height))
        self.images.append(tkinter.PhotoImage(width=self.width, height=self.height))
        self.active_image = 0
        
        black_str = self.C_PATTERN % BLACK
        self.image_data = [[black_str for i in range(self.width)] for j in range(self.height)]
        
        self.images[self.active_image].put((self.C_PATTERN % BLACK), (0, 0, self.width, self.height))
        
        self.canvas = tkinter.Canvas(root, width=self.width, height=self.height)
        self.canvas.pack()
        self.image_on_canvas = self.canvas.create_image(0, 0, image=self.images[self.active_image], anchor=tkinter.NW)

    def _data_conv(self):
        return tuple([tuple(row) for row in self.image_data])
    
    def put_to_image(self, x, y, c_tuple):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise GraphicsException("Coordinate does not fit into the canvas sizes.")
        self.image_data[self.height - y - 1][x] = self.C_PATTERN % c_tuple

    def refresh_image(self):
        self.active_image = (self.active_image + 1) % 2
        self.images[self.active_image].put(self._data_conv())
        self.canvas.itemconfig(self.image_on_canvas, image=self.images[self.active_image])

    def line(self, x0, y0, x1, y1, color):
        '''
        Bresenham algorithm for drawing a line
        '''
        if x0 < 0 or x0 >= self.width or y0 < 0 or y0 >= self.height or\
           x1 < 0 or x1 >= self.width or y1 < 0 or y1 >= self.height:
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
        
        for x in range(x0, x1 + 1):
            if steep:
                self.put_to_image(y, x, color)
            else:
                self.put_to_image(x, y, color)
            
            error += factor
            if error > dx:
                y += add
                error -= dx2

    def triangle(self, coord0, coord1, coord2, c_tuple):

        if coord0[1] < coord1[1]:
            coord0, coord1 = coord1, coord0
        if coord0[1] < coord2[1]:
            coord0, coord2 = coord2, coord0
        if coord1[1] < coord2[1]:
            coord1, coord2 = coord2, coord1

        factor10 = factor02 = factor12 = 1

        if coord0[1] != coord2[1]:
            factor02 = 1.0 * (coord2[0] - coord0[0]) / (coord2[1] - coord0[1])
        
        if coord0[1] != coord1[1]:
            factor10 = 1.0 * (coord0[0] - coord1[0]) / (coord0[1] - coord1[1])
        
        if coord1[1] != coord2[1]: 
            factor12 = 1.0 * (coord1[0] - coord2[0]) / (coord1[1] - coord2[1])
        
        step = -1
        if (factor02 * (coord1[1] - coord0[1]) + coord0[0]) > coord1[0]:
            step = 1

        for y in range(coord1[1], coord0[1] + 1):
            x_f = factor10 * (y - coord1[1]) + coord1[0]
            x_s = factor02 * (y - coord0[1]) + coord0[0]
            for x in range(int(x_f), int(x_s) + step, step):
                self.put_to_image(x, y, c_tuple)
        
        for y in range(coord2[1], coord1[1] + 1):
            x_f = factor12 * (y - coord1[1]) + coord1[0]
            x_s = factor02 * (y - coord0[1]) + coord0[0]
            for x in range(int(x_f), int(x_s) + step, step):
                self.put_to_image(x, y, c_tuple)


    def z_triangle(self, coord0, coord1, coord2, tga_model, z_buffer, intensity):
        
        if coord0.y < coord1.y:
            coord0, coord1 = coord1, coord0
        if coord0.y < coord2.y:
            coord0, coord2 = coord2, coord0
        if coord1.y < coord2.y:
            coord1, coord2 = coord2, coord1
        
        total_height = 1.0 * coord0.y - coord2.y
        first_height = 1.0 * coord0.y - coord1.y

        coord21 = coord2
        if total_height > 0:
            coord21 = ((coord2 - coord0) * first_height / total_height  + coord0)
       
        first_base_point = coord1
        second_base_point = coord21

        step_x = 1
        if second_base_point.x < first_base_point.x:
            step_x = -1

        for altitude_point in [coord0, coord2]:
            
            height = 1.0 * altitude_point.y - first_base_point.y
            
            step_y = 1
            
            if height == 0:
                height = 1
            elif height < 0:
                step_y = -1

            A_ = altitude_point - first_base_point
            B_ = altitude_point - second_base_point

            for y in range(first_base_point.y, altitude_point.y + step_y, step_y):
                factor = (y - first_base_point.y) / height
                A = A_ * factor + first_base_point
                B = B_ * factor + second_base_point
                C_ = B - A
                width = (B.x - A.x)
                if width == 0:
                    width = 1

                for x in range(int(A.x), int(B.x) + step_x, step_x):
                    C = C_ * (x - A.x) / width + A
                    if z_buffer[x][y] < C.z:
                        z_buffer[x][y] = C.z
                        self.put_to_image(x, y, 
                                          tuple(int(color * intensity)
                                                for color in tga_model.image[tga_model.image_width * int(C[4]) +
                                                                             int(C[3])]))


def first_lesson(canvas, model, center_x, center_y, shift_x, shift_y):
   
    shift_x = int(shift_x)
    shift_y = int(shift_y)
    
    for face in model.get_faces():
        coords = []
        for i in range(3):
            vert = model.get_vertices()[int(face[i][0]) - 1]
   
            x = int((vert[0] + 1) * center_x)
            y = int((vert[1] + 1) * center_y)

            coords.append((x + shift_x, y + shift_y))
        
        for i in range(3):
            j = (i + 1) % 3
            canvas.line(coords[i][0], coords[i][1], coords[j][0], coords[j][1], WHITE)

def second_lesson(canvas, model, center_x, center_y, shift_x, shift_y):

    shift_x = int(shift_x)
    shift_y = int(shift_y)

    r_rng = lambda : random.randrange(0, 256)
    
    for face in model.get_faces():
        coords = []
        w_coords = []
        for i in range(3):
            vert = model.get_vertices()[int(face[i][0]) - 1]
   
            x = int((vert[0] + 1) * center_x)
            y = int((vert[1] + 1) * center_y)

            coords.append((x + shift_x, y + shift_y))
            w_coords.append(Vector3D(vert))

        color = WHITE
        norm = (w_coords[2] - w_coords[0]) * (w_coords[1] - w_coords[0])
        norm.normalize()
        intensity = norm ^ Vector3D([0, 0, -1])
        color = tuple(int(intensity * i) for i in color)
        if intensity > 0:
            canvas.triangle(coords[0], coords[1], coords[2], color)


def third_lesson(canvas, obj_model, tga_model, center_x, center_y, shift_x, shift_y):

    shift_x = int(shift_x)
    shift_y = int(shift_y)
    
    z_buffer = [[-1000000.0 for i in range(int(center_x * 3))] for j in range(int(center_y * 3))]
    
    for face in obj_model.get_faces():
        coords = []
        w_coords = []
        for i in range(3):
            vert = obj_model.get_vertices()[int(face[i][0]) - 1]
            texture_vert = obj_model.get_vertex_textures()[int(face[i][1]) - 1]
   
            x = int((vert[0] + 1) * center_x)
            y = int((vert[1] + 1) * center_y)
            z = vert[2]
            coords.append(Vector3D([x + shift_x,
                                    y + shift_y,
                                    z,
                                    texture_vert[0] * tga_model.image_width,
                                    texture_vert[1] * tga_model.image_height]))
            w_coords.append(Vector3D(vert))

        color = WHITE
        norm = (w_coords[2] - w_coords[0]) * (w_coords[1] - w_coords[0])
        norm.normalize()
        intensity = norm ^ Vector3D([0, 0, -1])
        color = tuple(int(intensity * i) for i in color)
        if intensity > 0:
            canvas.z_triangle(coords[0], coords[1], coords[2], tga_model, z_buffer, intensity)

if __name__ == "__main__":
    
    root = tkinter.Tk()

    size_x = 1024
    size_y = 1024
    center_x = (size_x * 0.65) / 2
    center_y = (size_y * 0.65) / 2
    real_center_x = size_x / 2
    real_center_y = size_y / 2
    canvas = MyCanvas(root, size_x + 1, size_y + 1)
    
    obj_parser = obj_handler.ObjParser()
    obj_model = obj_parser.parse("african_head.obj")
    
    tga_parser = tga_handler.TgaParser()
    tga_model = tga_parser.parse("african_head_diffuse.tga")
    
    third_lesson(canvas,
                 obj_model,
                 tga_model,
                 center_x, center_y,
                 int(real_center_x - center_x), int((real_center_y - center_y) * 1.3 )
                )
    canvas.refresh_image()   
    root.mainloop()
