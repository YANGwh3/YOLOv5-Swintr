import six
from PIL import Image
import numpy as np
from PIL import Image,ImageFont, ImageDraw
import glob
import os


classes = ['Ursus thibetanus','lynx rufus','odocoileus hemionus','procyon lotor',
        'tamiasciurus hudsonicus','vulpes vulpes','Elaphodus cephalophus','Macaca mulatta','Prionailurus bengalensis']
all_N_label = {}
k = 0
for file in glob.glob(os.path.join(r"E:\train_data8\animals\data\train_aug","labels","*.txt")):
    file_img = file.replace(".txt",".jpg").replace("labels","images")
    if not os.path.exists(file_img):
        file_img = file_img.replace(".jpg",".jpeg")
    if not os.path.exists(file_img):
        file_img = file_img.replace(".jpeg",".png")
    if not os.path.exists(file_img):
        print("xxxxxxxxxxx",file_img)
        continue
    img = Image.open(file_img)
    w,h  = img.width,img.height

    infos = []
    with open(file,"r") as f: #遍历图片标签
        for line in f.readlines():
            label,xc,yc,ww,hh = line.split(" ")
            label,xmin,ymin,xmax,ymax = int(label.strip()), \
                                        int((float(xc.strip())-float(ww.strip())/2)*w),\
                                        int((float(yc.strip()) - float(hh.strip()) / 2) * h),\
                                        int((float(xc.strip()) + float(ww.strip())/2)*w),\
                                        int((float(yc.strip()) + float(hh.strip())/2)*h)
            infos.append([label,xmin,ymin,xmax,ymax])
            if ymax - ymin <15:
                continue
            if xmin < 0 or ymin <  0 or xmax >  w or ymax >  h:
                print("xxxxx")
                continue
            target = img.crop([xmin, ymin, xmax, ymax])
            try:
                targetp = os.path.join(r"E:\train_data8\animals\data\train_aug","croped")
                if not os.path.exists(targetp):
                    os.mkdir(targetp)
                target.save(os.path.join(targetp,str(k)+".jpg"))
            except:
                print(file_img)
            k+=1

