from shapely import geometry


def get_metrics_geometrically(true_left:tuple[int], true_right:tuple[int], pred_left:tuple[int], pred_right:tuple[int],img_width:int=1920)->list[int]:
    """_summary_

    Args:
        true_left (tuple[int]): _description_
        true_right (tuple[int]): _description_
        pred_left (tuple[int]): _description_
        pred_right (tuple[int]): _description_
        img_width (int, optional): _description_. Defaults to 1920.

    Returns:
        list[int]: _description_
    """

    true_quad=geometry.Polygon([(0,0), (0,img_width),true_left,true_right])
    pred_quad=geometry.Polygon([(0,0),(0,img_width),pred_left,pred_right])

    intersection=true_quad.intersection(pred_quad).area
    
    precision=intersection/pred_quad.area
    recall=intersection/true_quad.area

    f1=(2*precision*recall)/(precision+recall)

    return [precision,recall, f1]

def get_metrics_efficiently(true_left:tuple[int], true_right:tuple[int], pred_left:tuple[int], pred_right:tuple[int])->list[float]:
    left_dist=abs(true_left[1]-pred_left[1])
    right_dist=abs(true_right[1]-pred_right[1])
    return [left_dist,right_dist]
