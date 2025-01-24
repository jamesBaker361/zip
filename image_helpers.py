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

def draw_points_on_image(src_image:Image.Image, dot_position_list:list[tuple],radius:int=2)->Image.Image:
    """

    Args:
        src_image (Image.Image): _description_

    Returns:
        Image.Image: _description_
    """
    draw=ImageDraw.Draw(src_image)
    red=(255,0,0)
    for xy in dot_position_list:
        draw.circle(xy,radius,fill=red)

    return src_image

if __name__=="__main__":
    src_image=Image.open("input_1/frame0001.jpg")
    left=[0,408]
    center=[950, 350]
    right=[1919,286]
    final_image=draw_points_on_image(src_image,[left,right,center])
    final_image.save("final.jpg")