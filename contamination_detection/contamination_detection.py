import cv2
from matplotlib import pyplot as plt

def feature_image(path):
    #reading the image as gray
    image = cv2.imread(path, 0)
    
    #These parameters shold be modified
    edged = cv2.Canny(image, 30, 230)
    
    #applying closing function 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    image = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    #Dilate and erode to lose small regions
    image = cv2.dilate(image, None, iterations=10)
    image = cv2.erode(image, None, iterations=10)   
    
    return image/255

def contamination(path): 
    image = feature_image(path)
    print(image)
    x, y = image.shape
    no_contamination = sum(sum(image))/(x*y)
        
    return 100*(1-no_contamination)