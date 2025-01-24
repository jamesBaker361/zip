import numpy as np
from image_helpers import draw_points_on_image,draw_line_on_image
from PIL import Image
import sys
import argparse
import os
import json
import time
from evaluation import get_metrics_geometrically

parser=argparse.ArgumentParser()

parser.add_argument("--src_dir",type=str,default="input_1")
parser.add_argument("--output_dir",type=str,default="output")
parser.add_argument("--limit",type=int,default=100000)
parser.add_argument("--rows",type=int,default=1)
parser.add_argument("--step",type=int,default=4)
parser.add_argument("--use_centroids",action="store_true")
parser.add_argument("--kernel_size",type=int,default=3)


def get_image_with_dots(image:Image.Image,rows:int,step:int,use_centroids:bool)->Image.Image:

    dot_position_list=get_class_based_dot_list(image,rows,step,use_centroids)
    dot_position_list=filter_list(image,dot_position_list)
    color_list=[(255,0,0) for _ in dot_position_list]
    final_image=draw_points_on_image(image,dot_position_list,radius=step,color_list=color_list)
    return final_image
    

def get_class_based_dot_list(image:Image.Image,rows:int,step:int,use_centroids:bool):
    image_array=np.array(image)
    sky_rows=np.array([row[0::step] for row in image_array[:rows]])
    
    sky_centroid=np.average(sky_rows,axis=(0,1))
    
    land_rows=np.array([row[0::step] for row in image_array[-rows:]])
    land_centroid=np.average(land_rows,axis=(0,1))
    SKY_CLASS=1
    LAND_CLASS=2
    height,width,_=image_array.shape
    dot_position_list=[]
    class_array=np.zeros((height,width))
    for y in range(1,height-1):
        for x in range(width):
            pixel=image_array[y][x]
            if use_centroids:
                sky_distance=np.linalg.norm(pixel-sky_centroid)
                land_distance=np.linalg.norm(pixel-land_centroid)
            else:
                sky_distance=sys.maxsize
                land_distance=sys.maxsize
                for sky_pixel in sky_rows:
                    sky_distance=min(sky_distance, np.linalg.norm(pixel-sky_pixel))
                for land_pixel in land_rows:
                    land_distance=min(land_distance, np.linalg.norm(pixel-land_pixel))
            if land_distance<sky_distance:
                pixel_class=LAND_CLASS
            else:
                pixel_class=SKY_CLASS
            class_array[y][x]=pixel_class

            if class_array[y][x]==LAND_CLASS and class_array[y-1][x]==SKY_CLASS:
                dot_position_list.append([x,y])
    return dot_position_list

def filter_list(image:Image.Image,dot_position_list:list,kernel_size:int)->list:
    width,height=image.size
    class_array=np.zeros((height,width))
    for [x,y] in dot_position_list:
        class_array[y][x]=1
    final_dot_position_list=[]
    d_spacing=[0]+[k for k in range(1,kernel_size+1)]+[-k for k in range(1,1+kernel_size)]
    for [x,y] in dot_position_list:
        count=0
        for dy in d_spacing:
            for dx in d_spacing:
                
                if class_array[y+dy][x+dx]==1:
                    #print("\t",y+dy,x+dx,class_array[y+dy][x+dx])
                    count+=1
        
        if count>1+2*kernel_size:
            print(y,x,count)
            final_dot_position_list.append([x,y])
    return final_dot_position_list

def get_left_right(image:Image.Image,rows:int,step:int,use_centroids:bool,kernel_size:int):
    width,height=image.size
    dot_position_list=get_class_based_dot_list(image,rows=rows,step=step,use_centroids=use_centroids)
    dot_position_list=filter_list(image,dot_position_list,kernel_size=kernel_size)
    slope, intercept =np.polyfit([dot[0] for dot in dot_position_list], [dot[1] for dot in dot_position_list], 1)
    left=[0,intercept]
    right=[width, intercept+slope*width]
    return left,right

if __name__=="__main__":
    args=parser.parse_args()
    print(args)
    precision_list=[]
    recall_list=[]
    f1_list=[]
    time_list=[]
    with open(os.path.join(args.src_dir, "ground_truth.json"),"r") as file:
        ground_truth=json.load(file)
    for f in os.listdir(args.src_dir):
        if f.endswith(('.jpg', '.png')):
            if args.limit>=0:
                args.limit-=1
                src_image=Image.open(os.path.join(args.src_dir,f))
                start=time.time()
                left,right=get_left_right(src_image,args.rows,args.step,args.use_centroids,args.kernel_size)
                end=time.time()
                true_left=ground_truth[f]["left"]
                true_right=ground_truth[f]["right"]
                [precision,recall, f1]=get_metrics_geometrically(true_left,true_right,left,right)
                precision_list.append(precision)
                recall_list.append(recall)
                f1_list.append(f1_list)
                time_list.append(end-start)
    
    print("precision ",np.average(precision_list))
    print("recall",np.average(recall_list))
    print("f1",np.average(f1_list))
    print("time", np.average(time_list))
