import skimage as ski
import matplotlib.pyplot as plt
import numpy as np
import requests
from io import BytesIO

class Image:

    def __init__(self, image=None, url=None) -> None:
        self.CH_CONSTANT = 1.78
        if image and url:
            raise ValueError("Provide image or link to the Image")
        elif image:
            self.obj = ski.io.imread(image)
        else:
            response = requests.get(url)
            image_data = response.content
            self.obj = ski.io.imread(BytesIO(image_data))
        self.image = self.obj
        self.bwimg = ski.color.rgb2gray(self.obj[:,:,:3])
        self.w, self.h = self.obj.shape[1], self.obj.shape[0]
        
    def show(self, bw=False):
        plt.axis('off')
        if not bw:
            plt.imshow(self.image)
        else:
            plt.imshow(self.bwimg, cmap='gray')
        plt.show()

    def set_dim(self, width:int=None, height:int=None):
        if width != None and height == None:
            w, h = width, int((self.h/self.w * width)/self.CH_CONSTANT)
        elif width == None and height != None:
            w, h = int((self.w/self.h * height) * self.CH_CONSTANT), height
        else:
            w, h = width, height
        self.image = ski.transform.resize(self.obj, (h, w), anti_aliasing=True)
        self.bwimg = ski.color.rgb2gray(self.image[:,:,:3])
    
    def normalize(self):
        self.bwimg = np.subtract(self.bwimg, np.min(self.bwimg))
        self.bwimg = np.divide(self.bwimg, np.max(self.bwimg))