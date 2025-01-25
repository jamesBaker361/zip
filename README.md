# Horizon Finding

# Dependencies
This repo was written in python 3.12.8. 
Numpy and PIL are necessary and can be installed with
`pip install numpy pillow`

# Overview
At a high level, we attempt to find the horizon by classifying each pixel as belonging to land or sky,
by assuming that the pixels in the bottom n_rows of the image are all land, and the pixels in the top n_rows are all sky.
Intermediate pixels are then classified based on their similarity to the land/sky pixels
We then find all the transition pixels that are land but border a sky pixel. FOr each x value, where there 
are multiple y values that match, i.e. we have `[x,y_0], [x,y_1]...` we retain only the minimum `y_n`,
 With the remaining pixels x,y locations, we perform linear regression to determine the line of best fit.
 We then create a black and white copy of the original image and draw the line of best fit on it and save it to the output_dir

# How To Use:
The main file `horizon.py` can be run as so:
`python horizon.py --src_dir /path/to/images/ --output_dir /path/to/output  --use_centroids`

It can also be run with some clargs: 

`--src_dir` : path to input image directory

`--output_dir` : directory where generated images will be stored

`--limit` : limit of how many images to process

`--n_rows`: how many rows in the top/bottom to use for sky/land pixels

`--step` : what fraction(1/step) of pixels in the rows to use

And some boolean flags can be added as well

`--use_centroids` : whether we use the average of the pixels in the land/sky classes or the minimum to determine distance- this flag usually is faster and more reliable

`--verbose` : if true, prints out more


# Evaluation
Given that we have the task of finding a line, we essentially only need to find two endpoints
We already know the x value of both endpoints, so we only need to find the absolute value distance between 
the predicted and actual left endpoints y values, and the predicted and actual right endpoints y values
We add those two values, and that is our loss, to be minimized. It is measured in pixels

# Results
Using `n_rows=5`, `step=4` and `--use_verbose=True`, we evaluated both the input1 and input2 directories 
## For input_1:
Visual Results are in `output_1`

 Average absolute value pixel distance:

`left  30.145847652409053`

`right 8.348775074546932`

`total 38.49462272695599`

Average time per image (in seconds)

`time 22.18755831559499`

## For input_2:
Visual Results are in `output_2`

Average absolute value pixel distance:

`left  52.3645577064897`

`right 16.866338280209536`

`total 69.23089598669922`

Average time per image (in seconds)

`time 15.013919939994812`



# Expansions
A few next steps
> Blurring the input images: for a lot of the images in input_2, there are houses and structures that cause the predicted line to diverge far from horizon. Blurring the input image may help this, as there will be fewer below horizon points that would be the same color as the sky.

> Hyperparameter Search: A more methodical, exhaustive search of all the possible values of n_rows and step would be worthwhile

> Geometric Evaluation: given left,right coordinates, we can construct a polygon with points (0,0), (0,image_width),(x_left,y_left), (x_right,y_right), if we have a polygon for both our actual left/right coordinates and predicted, we can find their area of overlap/precision/recall and use that as a metric

> Speedup: this program is pretty slow. SPeeding it up would make it better in real scenarios