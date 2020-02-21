import os
from keras.layers import Activation
from keras.models import load_model
from keras.utils import get_custom_objects
import numpy as np
import cv2
from skimage.transform import resize
from PIL import Image
import matplotlib.pyplot as plt
from keras import backend as K
import xlwt

def swish_activation(x):
    return K.sigmoid(x) * x


get_custom_objects().update({'swish_activation': Activation(swish_activation)})


class Solve:
    def __init__(self, path, image='none', folder='none'):
        self.path = path
        self.image = image
        self.predict_dir = folder

    def solve_one(self):
        test = ['NORMAL', 'PENUMONIA']
        model = load_model(self.path)
        pre_x = []

        input_image = cv2.imread(self.image)
        input_image = resize(input_image, (3, 150, 150))

        pre_x.append(input_image)
        pre_x = np.asarray(pre_x)
        pre_y = model.predict(pre_x)
        max_index = np.argmax(pre_y)

        return test[max_index]

    @staticmethod
    def set_style(name, height, bold=False):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        al = xlwt.Alignment()
        al.horz = 0x02
        al.vert = 0x01
        style.alignment = al
        return style

    def solve_excel(self):
        images = []
        label = []
        for fn in os.listdir(self.predict_dir):
            if fn.endswith('jpeg'):
                fd = os.path.join(self.predict_dir, fn)
                images.append(fd)
                self.image = fd
                n = self.solve_one()
                label.append(str(n))
                

        f = xlwt.Workbook()
        sheet1 = f.add_sheet('图片', cell_overwrite_ok=True)
        row0 = ["图片", "标签"]
        colum0 = images

        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i], self.set_style('Times New Roman', 220, True))

        for i in range(0, len(colum0)):
            sheet1.write(i + 1, 0, colum0[i], self.set_style('Times New Roman', 220, True))

        for i in range(0, len(label)):
            sheet1.write(i + 1, 1, label[i], self.set_style('Times New Roman', 220, True))

        first_col = sheet1.col(0)
        first_col.width = 256 * 80
        sec_col = sheet1.col(1)
        sec_col.width = 256 * 30
        f.save('/root/Code/faxianbei/Picture_set.xls')
