'''
@author:yvette_suyu
2018.5.8
for data-processing
'''

#encoding=utf-8
from __future__ import print_function
from __future__ import absolute_import

import sys, xml
import numpy as np
import json, cv2, os
import logging
import xml.etree.ElementTree as ET
import PIL.Image

images_path = "/media/hszc/data/syh/tesseract/data"

for x, _, z in os.walk(images_path):
    # print(x)
    for name in z:
        if str(name).endswith(".png"):
            # print(name)
            name_str = name[:-3]
            filename = images_path + '/' + name
            # print(filename)
            new_image = PIL.Image.open(filename)
            pre_savename = '/media/hszc/data/syh/test2'
            new_image.save(os.path.join(pre_savename, os.path.basename(name_str + "font.exp" + ".tif")))


class xmlDataset(object):
    def __init__(self,
                 xml_path="/media/hszc/data/syh/tesseract/data",
                 images_path="/media/hszc/data/syh/tesseract/data",
                 ):
        self.images_path = images_path
        self.index = 0
        self.objs = []

        for x, _, z in os.walk(xml_path):
            for name in z:
                if str(name).endswith(".xml"):
                    oneimg = {}
                    oneimg['boxes'] = []

                    root = ET.parse(os.path.join(x, name)).getroot()
                    img_name = root.findall('filename')[0].text
                    oneimg['img_path'] = os.path.join(images_path, img_name)

                    for size in root.findall('size'):
                        # print ('size is',size)
                        sizeh = int(size.find('h###eight').text)

                        # print('size is',sizeh)

                    for oobj in root.findall('object'):
                        name = oobj.find('name').text
                        if name.startswith("###") or name.startswith("***") or name.startswith("@@@"):
                            continue
                        dis = len(name)

                        strname = str(name)
                        bndbox = oobj.find('polygon')
                        point0 = bndbox.find('point0').text
                        point1 = bndbox.find('point1').text
                        point2 = bndbox.find('point2').text
                        point3 = bndbox.find('point3').text

                        ### 公式 ### ；有现成公式 ###x+y=10
                        ### picture @@@
                        ### 无关区域 ***
                        ###最小外接矩形！

                        point0_list = list(map(lambda x:int(x),point0.strip(',').split(',')))
                        point1_list = list(map(lambda x:int(x),point1.strip(',').split(',')))
                        point2_list = list(map(lambda x:int(x),point2.strip(',').split(',')))
                        point3_list = list(map(lambda x:int(x),point3.strip(',').split(',')))



                        xmin = min(point0_list[0],point1_list[0],point2_list[0],point3_list[0])
                        ymin = min(point0_list[1],point1_list[1],point2_list[1],point3_list[1])
                        xmax = max(point0_list[0],point1_list[0],point2_list[0],point3_list[0])
                        ymax = max(point0_list[1],point1_list[1],point2_list[1],point3_list[1])

                        # delta = ((float(point2_list[0]) - float(point0_list[0])) + 0###.01) / dis * 1.0
                        delta = (xmax-xmin)/dis
                        if abs(delta) < 0.00001:
                            logging.warning("invalid delta ")
                            continue
                        for h in range(dis):
                            xx = str(xmin + h * delta)
                            yy = str(sizeh-ymax)
                            ww = str((h+1)*delta+xmin)
                            # hh = str(ymax-ymin)
                            hh = str(sizeh-ymin)

                            point_str = name[h] + " " + xx + " " + yy + " " + ww + " " + hh + " " + "0"
                            # point_str.append(point_str1)
                            oneimg['boxes'].append(point_str)
                    self.objs.append(oneimg)
        print("length,", len(self.objs))

    def __len__(self):
        return len(self.obj)

    def __getitem__(self, idx):
        return self.objs[idx]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    reload(sys)
    sys.setdefaultencoding('utf-8')


    img_path = "/media/hszc/data/syh/tesseract/data"
    xml_path = img_path
    output_path = "/media/hszc/data/syh/test2"
    xmldataset = xmlDataset(images_path=img_path, xml_path=xml_path)
    for oneimg in xmldataset:
        img_path = oneimg["img_path"]
        box_path = os.path.join(output_path, os.path.basename(img_path) + ".font.exp"+".box")
        logging.info("writting:{}".format(box_path))
        with open(box_path, "wt") as f:
            for polygon in oneimg["boxes"]:
                print(polygon, file=f)
                # print(polygon)
