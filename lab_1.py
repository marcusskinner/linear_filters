from PIL import Image
import sys
import random
import numpy as np

def add_padding(im, pad_size):
    padded_im = Image.new(im.mode, (im.width + pad_size*2, im.height + pad_size*2))
    padded_im.paste(im, (pad_size, pad_size))
    
    return padded_im

def linear_filter(im, filter_matrix):
    # pad image relative to size of filter. Assumes the filter is square.
    pad_size = (filter_matrix[0].size - 1)//2
    im_filtered = Image.new(im.mode, (im.width, im.height))
    im = add_padding(im, pad_size)
    
    # convert image to numpy array
    im_array = np.asarray(im)
    
    for x in range(pad_size, im.width - pad_size):
        for y in range(pad_size, im.height - pad_size):
            
            new_pixel = (0, 0, 0)
            for i in range(filter_matrix[0].size):
                for j in range(filter_matrix[0].size):
                    new_pixel += filter_matrix[i][j] * im_array[y - pad_size + j][x - pad_size + i]
            
            im_filtered.putpixel((x - pad_size, y - pad_size), tuple(new_pixel.astype(int)))
            
    return im_filtered

# Identity
a = np.array([[0, 0, 0], 
              [0, 1, 0], 
              [0, 0, 0]])

# Box Blur
b = np.array([[1/9, 1/9, 1/9], 
              [1/9, 1/9, 1/9], 
              [1/9, 1/9, 1/9]])

# Horizontal Derivative
c = np.array([[0, 0, 0], 
              [-1, 0, 1], 
              [0, 0 ,0]])

# Approximated Gaussian
d = np.array([[0.003, 0.013, 0.022, 0.013, 0.003], 
              [0.013, 0.059, 0.097, 0.059, 0.013], 
              [0.022, 0.097, 0.0159, 0.097, 0.022], 
              [0.013, 0.059, 0.097, 0.059, 0.013], 
              [0.003, 0.013, 0.022, 0.013, 0.003]])

# Sharpening filter
alpha = 1
a_2 = np.zeros((5,5))
a_2[2][2] = 1
e = ((1 + alpha) * a_2) - d

# Derivative of Gaussian
# found using a modified version of linear_filter with padding the edges as 0s
f = np.array([[ 0.013 ,  0.019 ,  0.    , -0.019 , -0.013 ],
       [ 0.059 ,  0.084 ,  0.    , -0.084 , -0.059 ],
       [ 0.097 , -0.0061,  0.    ,  0.0061, -0.097 ],
       [ 0.059 ,  0.084 ,  0.    , -0.084 , -0.059 ],
       [ 0.013 ,  0.019 ,  0.    , -0.019 , -0.013 ]])

#load image
im = Image.open('lena.png')

filters = [a, b, c, d, e, f]
names = ['a', 'b', 'c', 'd', 'e', 'f']

for i in range(6):
    im = Image.open('lena.png')
    im_new = linear_filter(im, filters[i])
    im_new.save(names[i] + '.png')
    im.close()