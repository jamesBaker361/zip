from PIL import Image,ImageDraw
import numpy as np

def draw_line_on_image(src_image:Image.Image, left:list[int], right:list[int])->Image.Image:
    """
    Draws a red line connecting two points on an image and converts the image 
    to a black-and-white version with RGB color channels.

    Args:
        src_image (Image.Image): 
            The input image on which the line will be drawn. 
        left (list[int]): 
            A list of two integers [u, v] the starting point of the line.
        right (list[int]): 
            A list of two integers [u, v] the ending point of the line.

    Returns:
        Image.Image: 
            A new image with the red line drawn between the two specified points.
    """

    final_image=src_image.convert("L").convert("RGB")

    draw=ImageDraw.Draw(final_image)
    red=(255,0,0)
    draw.line(left+right,fill=red,width=3)

    return final_image

def draw_points_on_image(src_image:Image.Image, point_position_list:list[tuple[int, int]],radius:int=2,color_list:list[tuple[int, int, int]]=None)->Image.Image:
    """
    Draws points on an image at specified positions, optionally using different colors for each point.

    Args:
        src_image (Image.Image): 
            The input image on which the points will be drawn. 
        point_position_list (list[tuple[int, int]]): 
            A list of tuples, where each tuple contains two integers [u, v] representing 
            the coordinates of each point to be drawn.
        radius (int, optional): 
            The radius of the points. Defaults to 2.
        color_list (list[tuple[int, int, int]], optional): 
            A list of RGB tuples specifying the color of each point. 
            If `None`, all points will be red. Defaults to `None`.

    Returns:
        Image.Image: 
            A new image with points drawn at the specified positions.
    """
    final_image=src_image
    red=(255,0,0)
    draw=ImageDraw.Draw(final_image)
    if color_list is None:
        for xy in point_position_list:
            draw.circle(xy,radius,fill=red)
    else:
        for c,xy in zip(color_list,point_position_list):
            #print(c)
            draw.circle(xy,radius,fill=c)

    return final_image



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