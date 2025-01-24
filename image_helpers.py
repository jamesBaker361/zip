from PIL import Image,ImageDraw
import numpy as np

def draw_line_on_image(src_image:Image.Image, left:list[int], right:list[int])->Image.Image:
    """
    Given an image and two [u,v] coordinates, returns a black and white version of the image
    with a red line connecting the two coordinates
    Args
        src_image (Image.Image)
        left (list[int]) len==2 u,v coordinate of left point of line, 
        right (list[int]) len==2 u,v coordinate of right point of line, 

    Returns
        final_image (Image.Image)
    """

    final_image=src_image.convert("L").convert("RGB")

    draw=ImageDraw.Draw(final_image)
    red=(255,0,0)
    draw.line(left+right,fill=red,width=3)

    return final_image

def draw_points_on_image(src_image:Image.Image, dot_position_list:list[tuple],radius:int=2,color_list:list=None)->Image.Image:
    """

    Args:
        src_image (Image.Image): _description_

    Returns:
        Image.Image: _description_
    """
    final_image=src_image
    red=(255,0,0)
    draw=ImageDraw.Draw(final_image)
    if color_list is None:
        for xy in dot_position_list:
            draw.circle(xy,radius,fill=red)
    else:
        for c,xy in zip(color_list,dot_position_list):
            #print(c)
            draw.circle(xy,radius,fill=c)

    return final_image

'''def draw_filter_on_image(src_image:Image.Image,dot_position_list:list[tuple],color_list:list)->Image.Image:

    final_image=src_image.convert("RBGA")
    for xy,c in zip(dot_position_list, color_list):
        pixels=final_image.load()
        pixels[*xy]=c

    return final_image'''


def draw_overlap_on_image(true_left:tuple[int], true_right:tuple[int], pred_left:tuple[int], pred_right:tuple[int],img_width:int=1920)-> Image.Image:
    """
    


    Args:
        true_left (tuple[int]): _description_
        true_right (tuple[int]): _description_
        pred_left (tuple[int]): _description_
        pred_right (tuple[int]): _description_
        img_width (int, optional): _description_. Defaults to 1920.

    Returns:
        Image.Image: _description_
    """
    return



if __name__=="__main__":
    src_image=Image.open("input_1/frame0001.jpg")
    left=[0,408]
    center=[950, 350]
    right=[1919,286]
    points=[]
    colors=[]
    for x in range(100):
        for y in range(100):
            points.append([x,y])
            colors.append((255,0,0,128))