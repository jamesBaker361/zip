import numpy as np
from image_helpers import draw_points_on_image,draw_line_on_image
from PIL import Image
import sys
import argparse
import os
import json
import time

parser=argparse.ArgumentParser()

parser.add_argument("--src_dir",type=str,default="input_1")
parser.add_argument("--output_dir",type=str,default="output")
parser.add_argument("--limit",type=int,default=100000)
parser.add_argument("--n_rows",type=int,default=5)
parser.add_argument("--step",type=int,default=4)
parser.add_argument("--use_centroids",action="store_true")
parser.add_argument("--kernel_size",type=int,default=3)
parser.add_argument("--verbose",action="store_true")


def get_error(true_left:tuple[int], true_right:tuple[int], pred_left:tuple[int], pred_right:tuple[int])->list[float]:
    """
    Calculates the vertical (y-coordinate) error between the true and predicted 
    coordinates of two points: left and right.

    Args:
        true_left (tuple[int, int]): 
            The true coordinates of the left point as a tuple `(u, v)
        true_right (tuple[int, int]): 
            The true coordinates of the right point as a tuple `(u, v)`,
        pred_left (tuple[int, int]): 
            The predicted coordinates of the left point as a tuple `(u, v)`.
        pred_right (tuple[int, int]): 
            The predicted coordinates of the right point as a tuple `(u, v)`.

    Returns:
        list[float]: 
            A list containing two floats:
            - The vertical error for the left point.
            - The vertical error for the right point.
    """
    left_dist=abs(true_left[1]-pred_left[1])
    right_dist=abs(true_right[1]-pred_right[1])
    return [left_dist,right_dist]
    

def get_class_based_pixel_list(image:Image.Image,n_rows:int,step:int,use_centroids:bool):
    """
    Classifies pixels in an image as either "sky" or "land" based on their color 
    similarity to representative rows of pixels. Identifies transition points 
    between "sky" and "land" and returns their positions. 
    The sky_pixels/land_pixels are created by taking (1/step) of all the pixels
    in the first/last n_rows. The centroid for each class is then calculated by averaging
    all of the pixel color values in RGB space in the representative class. For each unclassified pixel,
     If `use_centroids` is `True`, we classify it as belonging to the class whos centroid 
     is a lesser distance from the unclassified pixel. If `use_centroids` is `False`, we find
     the minimum distance between the unclassified pixel values in RGB space and the values in RGB space 
     of each pixel in sky_pixels/land_pixels. Whichever class has the closest minimum distance,
     we assign to the unclassified pixel

    If `use_centroids` is `True`, . If `False`, a more computationally 
    expensive comparison to individual pixels is performed.

    Args:
        image (Image.Image): 
            The input image to process
        n_rows (int): 
            The number of rows from the top and bottom of the image used 
            to define "sky" and "land" classes, respectively.
        step (int): 
            The step size for sampling pixels from the rows to compute 
            centroids or compare individual pixels.
        use_centroids (bool): 
            If `True`, uses the average (centroid) color of the sampled 
            rows to classify pixels. If `False`, compares each pixel 
            to all sampled pixels individually.

    Returns:
        list[list[int]]: 
            A list of `[x, y]` coordinates representing the positions of 
            transition points where "land" pixels are detected directly 
            below "sky" pixels in the image.

    """
    image_array=np.array(image)
    sky_pixels=np.array([row[0::step] for row in image_array[:n_rows]])
    
    sky_centroid=np.average(sky_pixels,axis=(0,1))
    
    land_pixels=np.array([row[0::step] for row in image_array[-n_rows:]])
    land_centroid=np.average(land_pixels,axis=(0,1))
    SKY_CLASS=1
    LAND_CLASS=2
    height,width,_=image_array.shape
    pixel_position_list=[]
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
                for sky_pixel in sky_pixels:
                    sky_distance=min(sky_distance, np.linalg.norm(pixel-sky_pixel))
                for land_pixel in land_pixels:
                    land_distance=min(land_distance, np.linalg.norm(pixel-land_pixel))
            if land_distance<sky_distance:
                pixel_class=LAND_CLASS
            else:
                pixel_class=SKY_CLASS
            class_array[y][x]=pixel_class

            if class_array[y][x]==LAND_CLASS and class_array[y-1][x]==SKY_CLASS:
                pixel_position_list.append([x,y])
    return pixel_position_list

def filter_list(image:Image.Image,pixel_position_list:list,kernel_size:int)->list:
    """
    Filters a list of pixel positions by applying a kernel-based density check. 
    The pixels represent predicted transition points between land and sky
    Retains only pixels surrounded by a sufficient amount of pixels within a specified kernel size.
    A pixel is kept if the number of neighboring pixels within the kernel 
    region exceeds `1 + 2 * kernel_size`. If the kernel exceeds the boundaries of the image,
    we assume that there would not be a neighboring pixel in the locations that
    exceed the boundary. 

    Args:
        image (Image.Image): 
            The input image. 
        pixel_position_list (list[list[int]]): 
            A list of `[x, y]` coordinates representing pixel positions 
            on the image.
        kernel_size (int): 
            The size of the kernel used for density filtering. The kernel 
            defines the neighborhood around each pixel for checking the 
            presence of other pixels.

    Returns:
        list[list[int]]: 
            A filtered list of `[x, y]` coordinates

    """
    width,height=image.size
    class_array=np.zeros((height,width))
    for [x,y] in pixel_position_list:
        class_array[y][x]=1
    final_pixel_position_list=[]
    d_spacing=[0]+[k for k in range(1,kernel_size+1)]+[-k for k in range(1,1+kernel_size)]
    for [x,y] in pixel_position_list:
        count=0
        for dy in d_spacing:
            for dx in d_spacing:
                if y+dy>=0 and y+dy<height and x+dx>=0 and x+dx<width: #handle edge case
                    if class_array[y+dy][x+dx]==1:
                        #print("\t",y+dy,x+dx,class_array[y+dy][x+dx])
                        count+=1
        
        if count>1+2*kernel_size:
            #print(y,x,count)
            final_pixel_position_list.append([x,y])
    return final_pixel_position_list

def filter_list_simple(pixel_position_list:list[list[int]])->list[list[int]]:
    """Filters  pixel positions to retain only the minimum y-coordinate 
    for each unique x-coordinate.

    Args:
        pixel_position_list (list[list[int]]): 
            A list of pixel positions, where each position is a list `[x, y]` 

    Returns:
        list[list[int]]: 
            A filtered list of pixel positions, where each entry corresponds 
            to an x-coordinate and the least y-coordinate associated with it
    """
    pixel_dict={}
    for [x,y] in pixel_position_list:
        if x not in pixel_dict:
            pixel_dict[x]=[]
        pixel_dict[x].append(y)
    return [[k,min(v)] for k,v in pixel_dict.items()]

def get_left_right(image:Image.Image,n_rows:int,step:int,use_centroids:bool,kernel_size:int)->tuple[list[float], list[float]]:
    """
    Calculates the left and right endpoints of a line that defines the horizon of an image.

    Args:
        image (Image.Image): 
            The input image.
        n_rows (int): 
            The number of rows from the top and bottom of the image used 
            to define "sky" and "land" classes during pixel detection.
        step (int): 
            The step size for sampling pixels during the classification process.
            We only sample (1/step) of the pixels in the sky_pixels and land_pixels
        use_centroids (bool): 
            If `True`, uses centroid-based classification of "sky" and "land" 
            pixels; if `False`, compares individual pixels. The former is
            faster
        kernel_size (int): 
            The size of the kernel used to filter transition points based 
            on density.

    Returns:
        tuple[list[float], list[float]]: 
            A tuple containing the left and right endpoints of the best-fit line:
            - `left`: `[x, y]` coordinates for the leftmost point (at x = 0).
            - `right`: `[x, y]` coordinates for the rightmost point (at x = image width).
    """
    width,height=image.size
    pixel_position_list=get_class_based_pixel_list(image,n_rows=n_rows,step=step,use_centroids=use_centroids)
    pixel_position_list=filter_list_simple(pixel_position_list)
    #pixel_position_list=filter_list(image,pixel_position_list,kernel_size=kernel_size)
    slope, intercept =np.polyfit([pixel[0] for pixel in pixel_position_list], [pixel[1] for pixel in pixel_position_list], 1)
    left=[0,intercept]
    right=[width, intercept+slope*width]
    return left,right

if __name__=="__main__":
    args=parser.parse_args()
    print(args)
    left_list=[]
    right_list=[]
    total_list=[]
    time_list=[]
    with open(os.path.join(args.src_dir, "ground_truth.json"),"r") as file:
        ground_truth=json.load(file)
    os.makedirs(args.output_dir,exist_ok=True)
    for f in os.listdir(args.src_dir):
        if f.endswith(('.jpg', '.png')):
            if args.limit>=0:
                args.limit-=1
                src_image=Image.open(os.path.join(args.src_dir,f))
                start=time.time()
                left,right=get_left_right(src_image,args.n_rows,args.step,args.use_centroids,args.kernel_size)
                end=time.time()
                elapsed=end-start
                line_image=draw_line_on_image(src_image,left,right)
                line_image.save(os.path.join(args.output_dir,f))
                true_left=ground_truth[f]["left"]
                true_right=ground_truth[f]["right"]
                [left_dist,right_dist]=get_error(true_left,true_right,left,right)
                total=left_dist+right_dist

                if args.verbose:
                    print(f"\t file: {f}")
                    print(f"\t left: {left_dist}")
                    print(f"\t right: {right_dist}")
                    print(f"\t total: {total}")
                    print(f"\t time {elapsed}")
                
                left_list.append(left_dist)
                right_list.append(right_dist)
                total_list.append(total)
                time_list.append(elapsed)
    
    print("left ",np.average(left_list))
    print("right",np.average(right_list))
    print("total",np.average(total_list))
    print("time", np.average(time_list))
