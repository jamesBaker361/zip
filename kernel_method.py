import numpy as np
from image_helpers import draw_points_on_image
from PIL import Image
import sys
def kernel_difference(x:int,y:int,kernel_width:int,kernel_height:int,image_array:np.ndarray)->float:
    """_summary_

    Args:
        u (int): _description_
        v (int): _description_
        kernel_width (int): _description_
        kernel_height (int): _description_
        image_array (np.ndarray): _description_

    Returns:
        float: _description_
    """
    difference=0.0
    for dx in range(kernel_width):
        for dy in range(kernel_height):
            first_point=image_array[y+dy][x+dx]
            second_point=image_array[y-(1+dy)][x+dx]
            difference+=np.linalg.norm(first_point-second_point)
    
    return difference


def get_differences_heatmap(image:Image.Image,kernel_width:int,kernel_height:int,step:int=1)->Image.Image:

    minimum_difference=sys.maxsize
    maximum_difference=0

    image_array=np.array(image)
    
    mod_y=image_array.shape[0]-kernel_height
    mod_x=image_array.shape[1]-kernel_width
    difference_array=np.zeros((mod_y,mod_x))
    for x in range(mod_x):
        for y in range(kernel_height,mod_y):
            difference=kernel_difference(x,y,kernel_width,kernel_height,image_array)
            minimum_difference=min(minimum_difference,difference)
            maximum_difference=max(maximum_difference,difference)
            difference_array[y][x]=difference

    difference_range=maximum_difference-minimum_difference

    dot_position_list=[]
    color_list=[]
    for x in range(0,mod_x,step):
        for y in range(0,mod_y,step):
            scale=float(difference_array[y][x]-minimum_difference)/difference_range
            color=(int(scale*255),0,128)
            dot_position_list.append([x,y])
            color_list.append(color)

    final_image=draw_points_on_image(image,dot_position_list,radius=step,color_list=color_list)
    return final_image
    
if __name__=="__main__":
    
    for x in range(5,30,5):
        src_image=Image.open("input_1/frame0001.jpg")
        final_image=get_differences_heatmap(src_image,x,x,x)
        final_image.save(f"dots_{x}.png")