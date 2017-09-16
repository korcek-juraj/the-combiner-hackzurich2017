import cv2
from matplotlib import pyplot as plt

def feature_image(path):
    #reading the image as gray
    image = cv2.imread(path)[:,:,1]
    
    #These parameters shold be modified
    edged = cv2.Canny(image, 10, 150)
    
    #applying closing function 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    image = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    #Dilate and erode to lose small regions
    image = cv2.dilate(image, None, iterations=10)
    image = cv2.erode(image, None, iterations=10)   
    
    #show image
    plt.imshow(image, "gray")
    plt.show()
    
    return image