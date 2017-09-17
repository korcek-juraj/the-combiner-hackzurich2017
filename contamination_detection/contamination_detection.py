import cv2
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from scipy import ndimage
import numpy as np

def feature_image(path, tresh_min, tresh_max, iterations, k):
    #reading the image as gray
    image = cv2.imread(path, 0)
    image = cv2.equalizeHist(image)
    
    #These parameters shold be modified
    edged = cv2.Canny(image, tresh_min, tresh_max)
    
    #applying closing function 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
    image = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    #Dilate and erode to lose small regions
    image = cv2.dilate(image, None, iterations=iterations)
    image = cv2.erode(image, None, iterations=iterations)   
    
    return image/255

def contamination(path): 
    image = feature_image(path, 138, 217, 6, 7)
    x, y = image.shape
    no_contamination = sum(sum(image))/(x*y)
        
    return 100*(1-no_contamination)

def vector_feature_generation(path): 
    features = []
    
    image = cv2.imread(path)
    #Whatch out the parameters
    img_mask = feature_image(path, 138, 217, 6, 7)
    x, y = img_mask.shape

    #NOT A MUST##################################################################################
    for i in range(x):
        for j in range(y): 
            if img_mask[i,j]!=0:
                image[i,j,:] = [255, 255, 255]
        
    cv2.imwrite("/home/natalija/Documents/HackZurich/contamination_detection/src/contamination_mask.jpg", image)  
    ##############################################################################################
    labeled, nr_objects = ndimage.label(1-img_mask)
    d = {}
    x,y = labeled.shape
    for i in range(1,nr_objects+1): 
        d[i] = np.zeros((x,y,3))

    for i in range(1,x): 
        for j in range(1,y): 
            if labeled[i,j]:
                d[labeled[i,j]][i,j,:] = image[i,j,:]

    for key, value in d.items(): 
        non_empty_columns = np.where(value.max(axis=0)>0)[0]
        non_empty_rows = np.where(value.max(axis=1)>0)[0]
        cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))        
        image_data = value[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]
        #cv2.imwrite("/home/natalija/Documents/HackZurich/contamination_detection/src/image{}.png".format(key), image_data)
        
        vector = np.zeros(84645)
        new = np.concatenate((image_data[:,:,0].ravel(), image_data[:,:,1].ravel(), image_data[:,:,2].ravel()))
        vector[0:len(new)]=new
        features.append(vector)
        
        #reduce dimensionality
    pca = PCA(n_components=100)
    
    while len(features) < 100: 
        features.append(features[0])

        
    features = pca.fit_transform(features)
        
    return features

def predict_grains(path): 
    loaded_model = pickle.load(open("/home/natalija/Documents/HackZurich/server/thecombiners/main_app/static/main_app/img/model.pkl", 'rb'))
    features = vector_feature_generation(path)
    
    maping = {}
    maping[1] = "beans"
    maping[2] = "dried_bean"
    maping[3] = "fines"
    maping[4] = "grains"
    maping[5] = "lentils"
    maping[6] = "pumpkin"
    maping[7] = "stones"
    maping[8] = "straw"
    maping[9] = "quinoa"

    count = {}
    count[1] = 0
    count[2] = 0
    count[3] = 0
    count[4] = 0
    count[5] = 0
    count[6] = 0
    count[7] = 0
    count[8] = 0
    count[9] = 0

    for i in result:
        count[i] +=1
    result = ""
    for i in range(1,10): 
        if count[i] != 0 and i!=4: 
            result+=("{}% of the contaminated grains are {}/n".format(100/count[i], maping[i]))
    return result
