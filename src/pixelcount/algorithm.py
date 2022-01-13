#!/usr/bin/env python
# coding: utf-8

import cv2
import itertools
import numpy as np
from matplotlib import pyplot as plt
from skimage.segmentation import slic
from skimage.morphology import flood
from skimage import measure

def get_background(SLIC):
    values, counts = np.unique(SLIC, return_counts = True)
    background = SLIC == values[counts.argmax()]
    return background

def pipeline(image, **params):
    # run slic with self tuned defaults
    # these defaults work for me, but I made them easily overwritable
    # just use pipeline(image, compactness = 50) for example
    def slic_defaults(image, **params):
        defaults = {'n_segments' : 3, 
                    'compactness' : 20,
                    'start_label' : 0,
                    'sigma' : 0,
                    'enforce_connectivity' : False}
        # change defaults for values given in params
        for key in params:
            defaults[key] = params[key]
        return slic(image, **defaults)
    
    # run slic with default, but editable, parameters
    SLIC = slic_defaults(image, **params)
    # extract the background
    background = get_background(SLIC.copy())
    
    #foreground = get_foreground(background)
    # label everything that is not background
    labels = measure.label(~background)
    # and get the regions corresponding to these labels
    regions = measure.regionprops(labels)
    # sort by region size
    regions.sort(key = lambda region: region.filled_area, reverse = True)

    return {
        'slic' : SLIC,
        'background' : background,
        'labels' : labels,
        'regions' : regions,
        }
