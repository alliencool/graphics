from struct import unpack

#
# Specification is taken from:
# http://www.paulbourke.net/dataformats/tga/
#

# Constants for images types

UNMAPPED_RGB = 2
RUN_LENGTH_ENCODED = 10

class TgaException(Exception):
    pass

class TgaModel(object):

    def __init__(self):
        super(TgaModel, self).__init__()
        
        self.image_id_length = 0
        self.image_id = "" 
        
        self.color_map_type = 0
        self.color_map_origin = 0
        self.color_map_length = 0
        self.color_map_entry_size = 0

        self.image_type_code = 0
        self.image_origin_x = 0
        self.image_origin_y = 0
        self.image_width = 0
        self.image_height = 0
        self.image_pixel_size = 0
        self.image_desc_byte = 0
        self.image = []


class TgaParser(object):

    def __init__(self):
        super(TgaParser, self).__init__()

    def _read_color(self, bfd, pixel_size):
        
        if pixel_size == 3:
            buff = bfd.read(pixel_size)
            return tuple(unpack("BBB", buff)[2::-1])
        
        elif pixel_size == 4:
            buff = bfd.read(pixel_size)
            color = unpack("BBBB", buff)
            return tuple(color[2::-1])

        raise TgaException("Don't know how to parse: pixel_size = %s" % (pixel_size))

    def parse(self, file_path):

        tga_model = TgaModel()

        with open(file_path, "rb") as bfd:

            buff = bfd.read(1)
            tga_model.image_id_length, = unpack("B", buff)

            buff = bfd.read(1)
            tga_model.color_map_type, = unpack("B", buff)
            
            buff = bfd.read(1)
            tga_model.image_type_code, = unpack("B", buff)
            
            buff = bfd.read(5)
            tga_model.color_map_origin, tga_model.color_map_length, tga_model.color_map_entry_size, = unpack("HHB", buff)
            
            buff = bfd.read(10)
            tga_model.image_origin_x, tga_model.image_origin_y, tga_model.image_width, tga_model.image_height, tga_model.image_pixel_size, tga_model.image_desc_byte = unpack("HHHHBB", buff)
            
            if tga_model.image_id_length > 0:
                tga_model.image_id = bfd.read(tga_model.image_id_length)

            if tga_model.color_map_type != 0:
                raise TgaException("There should not be color map!") 

            pixel_size = int(tga_model.image_pixel_size / 8)
            image_size = tga_model.image_width * tga_model.image_height

            if tga_model.image_type_code == UNMAPPED_RGB:
                for i in range(tga_model.image_width * tga_model.image_height):
                    tga_model.image.append(self._read_color(bfd, pixel_size))
            
            elif tga_model.image_type_code == RUN_LENGTH_ENCODED:
                curr_image_size = 0 
                while curr_image_size < image_size:
                    buff = bfd.read(1)
                    header, = unpack("B", buff)
                    header_type = header & 128
                    header_count = (header & 127) + 1
                    if header_type == 0:
                        for i in range(header_count):
                            tga_model.image.append(self._read_color(bfd, pixel_size))
                            curr_image_size += 1
                    else:
                        color = self._read_color(bfd, pixel_size) 
                        for i in range(header_count):
                            tga_model.image.append(color)
                            curr_image_size += 1
            else:
                raise TgaException("Unsupported image type")

        return tga_model

def check():
    t_parser = TgaParser()

    t_parser.parse("african_head_diffuse.tga")

