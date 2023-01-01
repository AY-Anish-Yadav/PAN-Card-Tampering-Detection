
# Import packages
import imutils
import cv2
from PIL import Image
import requests
from skimage.metrics import structural_similarity
import glob

# Open Image and Display

O=Image.open(requests.get('https://www.thestatesman.com/wp-content/uploads/2019/07/pan-card.jpg',stream=True).raw)
T=Image.open(requests.get('https://assets1.cleartax-cdn.com/s/img/20170526124335/Pan4.png',stream=True).raw)

# The file format of the source file.
print("Original image format : ",O.format) 
print("Tampered image format : ",T.format)

# Image size, in pixels. The size is given as a 2-tuple (width, height).
print("Original image size : ",O.size) 
print("Tampered image size : ",T.size) 

# Resize Image & Saving
path=r"E:\Projects\Images"
O=O.resize((250,160))
O.save(f"{path}//original.png")
T=T.resize((250,160))
T.save(f"{path}//Tempered.png")

# Read and Look at the images
all_images=sorted(glob.glob(path+"//"+'*.png'))
print(all_images)

for index,image in enumerate(all_images):
    img=cv2.imread(image)
    cv2.imshow("Frame",img)
    cv2.waitKey(0)

# Load the Images
O=cv2.imread(f"{path}//original.png")
T=cv2.imread(f"{path}//Tempered.png")

# Convert to Grayscale
O_G=cv2.cvtColor(O,cv2.COLOR_BGR2GRAY)
T_G=cv2.cvtColor(T,cv2.COLOR_BGR2GRAY)

# Compute the Structural Similarity Index (SSIM) between the two images, ensuring that the difference image is returned
(score, diff) = structural_similarity(O_G, T_G, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))

# Calculating threshold and contours 
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)


for ind, image in enumerate(all_images):
    img1=cv2.imread(f"{path}//original.png")
    img2=cv2.imread(f"{path}//Tempered.png")
    for c in cnts:
        (x,y,w,h)=cv2.boundingRect(c)
        cv2.rectangle(img1,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.imshow("Frame",img1)
        cv2.imshow("Frame",img2)
        cv2.waitKey(0)

# Look at the differance and threshold value.
cv2.imshow("Threshold",thresh)
cv2.imshow("diff",diff) 
cv2.waitKey(0)


    




























