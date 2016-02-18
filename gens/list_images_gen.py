import os
from PIL import Image

__author__ = 'bolotin'
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))



class ListImages:
    def __init__(self, square_size):
        self.square_size = square_size
        self.list_images = []
        self.current_image = 0
        self.count_images = 0
        # border for binarization, will be load forward, default value
        self.border = 100
        self._load_config_()
        self._load_images_()
        if self.count_images == 0:
            # make zero matr
            print("WARNING in module 'list_image_generator.py' zero images was loaded")
            self.list_images.append([ [0 for j in range(self.square_size)] for i in range(self.square_size)])

    def _load_config_(self):
        try:
            f = open(__location__+"\\Images\\config.txt","r")
            self.border = int(f.read())
            f.close()
            if (self.border>255 or self.border<0):
               raise Exception()
        except Exception as e:
             self.border = 100
             print("EXCEPTION in module 'list_image_generator.py' while load config: "+e.__str__())
        # finally:
        #     f.close()
    def _load_images_(self):
        try:
            f = open(__location__+"\\Images\\order.txt","r")
            for line in f:
                #delete /n from end of line
                if (line[len(line)-1] == '\n'):
                    n_line = line[0:len(line)-1]
                else :
                    n_line = line
                if len(n_line)>0:#non empty
                    self._load_image_(n_line)
            f.close()
        except Exception as e:
             print("EXCEPTION in module 'list_image_generator.py' no order file"+e.__str__())
        # finally:
        #     f.close()
    def _load_image_(self, file_name):
        try:
            self.list_images.append([])
            number = self.count_images
            Im = Image.open(__location__+"\\Images\\" + file_name).resize((self.square_size,self.square_size))
            size_x, size_y = Im.size
            # result matr of bytes
            for i in range(size_y):
                 self.list_images[number].append([])
                 for j in range(size_x):
                    color = Im.getpixel((j,i))
                    r,g,b = 0,1,2
                    if (color[r]<self.border and color[g]<self.border and color[b]<self.border):
                        self.list_images[number][i].append(1)
                    else:
                        self.list_images[number][i].append(0)
            self.count_images += 1
        except Exception as e:
            # delete current matr from list
            self.list_images.pop()
            print("EXCEPTION in module 'list_image_generator.py' while load image '{}'".format(file_name)+" "+e.__str__() )
    def move(self):
        self.current_image += 1
        if (self.current_image >= self.count_images):
            self.current_image = 0
    def out(self):
        print(self.current_image)
        for i in self.list_images[self.current_image]:
            print(i)
        print()
    def get_data(self):
        return self.list_images[self.current_image]