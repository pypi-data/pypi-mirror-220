import numpy as np
from photutils.datasets import make_noise_image

def poisson_noise(x, mu):
    x = x.astype('float32')
    shape = x.shape
    
    
    gaussiannoise = make_noise_image(shape, distribution='gaussian', mean=0.,
                          stddev=mu)
    poissonnoise = make_noise_image(shape, distribution='poisson', mean=mu)

    x = x + gaussiannoise + poissonnoise

    return x




def image_embedding(image, size):

    
    ndim = len(image.shape)
    if ndim == 2:
        assert len(image.shape) == len(size), f'The provided size {len(size)} should match the image dimensions {len(image.shape)}'
        for i in range(len(size)):
          assert image.shape[i] <= size[i] , f'The image size should be smaller than the volume it is to be embedded in'
          width = []
          for i in range(len(size)):
                width.append(size[i] - image.shape[i])
          width = np.asarray(width)
    
          ResizeImage = np.pad(image, width, 'constant', constant_values = 0)
    if ndim == 3:
        ResizeImage = []
        width = []
        for i in range(len(size)):
                width.append(size[i] - image.shape[i + 1])
        width = np.asarray(width)
        for i in range(image.shape[0]):
             
           ResizeImage.append(np.pad(image[i,:], width, 'constant', constant_values = 0))   
        ResizeImage = np.asarray(ResizeImage)
    return ResizeImage

def image_pixel_duplicator(image, size):

    assert len(image.shape) == len(size), f'The provided size {len(size)} should match the image dimensions {len(image.shape)}'
    
    ndim = len(size)



    if ndim == 3:
                    size_y = size[0]
                    size_x = size[1]
                    size_z = size[2]
                    if size_y <= image.shape[0]:
                        size_y =  image.shape[0]
                    if size_x <= image.shape[1]:
                        size_x =  image.shape[1]
                    if size_z <= image.shape[2]:
                        size_z =  image.shape[2]    

                    size = (size_y, size_x, size_z)
                    ResizeImage = np.zeros(size)
                    j = 0
                    for i in range(0, ResizeImage.shape[1]):
                        
                        if j < image.shape[1]:
                            ResizeImage[:image.shape[0],i,:image.shape[2]] = image[:image.shape[0],j,:image.shape[2]]
                            j = j + 1
                        else:
                            j = 0   
                        
                    j = 0
                    for i in range(0, ResizeImage.shape[2]):
                        
                        if j < image.shape[2]:
                            ResizeImage[:,:,i] = ResizeImage[:,:,j]
                            j = j + 1
                        else:
                            j = 0     

                    j = 0
                    for i in range(0, ResizeImage.shape[0]):
                        
                        if j < image.shape[0]:
                            ResizeImage[i,:,:] = ResizeImage[j,:,:]
                            j = j + 1
                        else:
                            j = 0  

                      

    if ndim == 2:


                    size_y = size[0]
                    size_x = size[1]
                    if size_y <= image.shape[0]:
                        size_y =  image.shape[0]
                    if size_x <= image.shape[1]:
                        size_x =  image.shape[1]
                      

                    size = (size_y, size_x)

                    ResizeImage = np.zeros(size)
                    j = 0
                    for i in range(0, ResizeImage.shape[1]):
                        
                        if j < image.shape[1]:
                            ResizeImage[:image.shape[0],i] = image[:image.shape[0],j]
                            j = j + 1
                        else:
                            j = 0   
                        

                    j = 0
                    for i in range(0, ResizeImage.shape[0]):
                        
                        if j < image.shape[0]:
                            ResizeImage[i,:] = ResizeImage[j,:]
                            j = j + 1
                        else:
                            j = 0  
           

              

    return ResizeImage
