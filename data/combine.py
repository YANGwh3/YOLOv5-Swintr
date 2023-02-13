import six
from PIL import Image
import numpy as np
from PIL import Image,ImageFont, ImageDraw
import glob
import os
import random
import itertools
# for i in range(10):
#     print(random.randint(3,10))

classes = ['Ursus thibetanus','lynx rufus','odocoileus hemionus','procyon lotor',
        'tamiasciurus hudsonicus','vulpes vulpes','Elaphodus cephalophus','Macaca mulatta','Prionailurus bengalensis']
all_crop = glob.glob(os.path.join(r"E:\train_data8\animals\data\train_aug","croped","*.jpg"))
import numpy as np


def bbox_iou(box1, box2):
    b1_x1, b1_y1, b1_x2, b1_y2 = box1
    b2_x1, b2_y1, b2_x2, b2_y2 = box2
    #get the corrdinates of the intersection rectangle
    inter_rect_x1 =  max(b1_x1, b2_x1)
    inter_rect_y1 =  max(b1_y1, b2_y1)
    inter_rect_x2 =  min(b1_x2, b2_x2)
    inter_rect_y2 =  min(b1_y2, b2_y2)
    #Intersection area
    inter_width = inter_rect_x2 - inter_rect_x1 + 1
    inter_height = inter_rect_y2 - inter_rect_y1 + 1
    if inter_width > 0 and inter_height > 0:#strong condition
        inter_area = inter_width * inter_height
        #Union Area
        b1_area = (b1_x2 - b1_x1 + 1)*(b1_y2 - b1_y1 + 1)
        b2_area = (b2_x2 - b2_x1 + 1)*(b2_y2 - b2_y1 + 1)
        iou = inter_area / (b1_area + b2_area - inter_area)
    else:
        iou = 0
    return iou
def save_(img,infos,paths):
    draw = ImageDraw.Draw(img)
    for info in infos:
        xmin, ymin, xmax, ymax  = info
        cls_index=0
        int_clas_index = int(cls_index)
        label = classes[int_clas_index]
        for i in range(1):
            draw.rectangle(
                [int(xmin)+i,int(ymin)+i,int(xmax)-i,int(ymax)-i],
                outline =(0,0,255))
        img.save(paths)

for file in glob.glob(os.path.join(r"E:\train_data8\animals\data\train_aug","labels","*.txt")):
    file_img = file.replace(".txt", ".jpg").replace("labels", "images")
    end = ".jpg"
    if not os.path.exists(file_img):
        file_img = file_img.replace(".jpg", ".jpeg")
        end = ".jpeg"
    if not os.path.exists(file_img):
        file_img = file_img.replace(".jpeg", ".png")
        end = ".png"
    if not os.path.exists(file_img):
        print("xxxxxxxxxxx", file_img)
        continue
    file_name = file_img.split(os.sep)[-1].split(".")[0]

    img = Image.open(file_img)
    w,h  = img.width,img.height
    img_copy = img.copy()
    np.random.shuffle(all_crop)
    targt_num = random.randint(1, 3)

    infos = []
    with open(file,"r") as f:
        for line in f.readlines():
            label,xc,yc,ww,hh = line.split(" ")
            label,xmin,ymin,xmax,ymax = int(label.strip()), \
                                        int((float(xc.strip())-float(ww.strip())/2)*w),\
                                        int((float(yc.strip()) - float(hh.strip()) / 2) * h),\
                                        int((float(xc.strip()) + float(ww.strip())/2)*w),\
                                        int((float(yc.strip()) + float(hh.strip())/2)*h)
            infos.append([xmin,ymin,xmax,ymax])
    #save_(img,infos,"./111.jpg")
    #print("-------", len(infos))
    current_index = 0
    tmp = []
    for patch_path in all_crop:
        try:
            img_patch = Image.open(patch_path)
        except:
            continue
        w_patch, h_patch = img_patch.width, img_patch.height
        if w-w_patch <=0 or h-h_patch <= 0:
            continue
        new_bbox_left = random.randint(0, w - w_patch)
        new_bbox_top = random.randint(0, h - h_patch)
        path_box = [new_bbox_left, new_bbox_top, new_bbox_left +w_patch, new_bbox_top + h_patch]

        all_zero = True
        for bbox in infos:
            iou = bbox_iou(path_box, bbox)
            if iou != 0:
                all_zero = False
        if all_zero:
            current_index+=1
            img_copy.paste(img_patch, (path_box[0], path_box[1]))
            tmp.append(path_box)

        if current_index >  targt_num:
            break 
        infos+=tmp

    with open(file, "a+") as f:
        for path_box in tmp:
            xc = str(round((path_box[2]+path_box[0])/(2*w),6))
            yc = str(round((path_box[3] + path_box[1]) / (2 * h), 6))
            www = str(round((path_box[2] - path_box[0]) / w, 6))
            hhh = str(round((path_box[3] - path_box[1]) / h, 6))
            new = " ".join([str(0),xc,yc,www,hhh])
            f.write(new+"\n")
    origin = os.path.join(r"E:\train_data8\animals\data\train_aug","images",file_name+end)
    os.remove(origin)
    img_copy.save(origin)
    #save_(img_copy,infos,origin)
    print("=====",len(infos))

