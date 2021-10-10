import cv2
import numpy as np
import os
import copy

pices = ["pawn", "rook", "bishop", "knight", "queen", "king"]
new_images= []
path = os.path.abspath(os.getcwd())
read_path= path + os.sep + "pices" + os.sep + "set0" 
write_path= path + os.sep + "pices" + os.sep + "temp"

def delete_all_images():
    for new_image in new_images:
        os.remove(write_path + os.sep+ f"{new_image}.png")

def create_pices(size):
    dim= (int(size), int(size))
    for pice in pices:
        original = cv2.imread(read_path+ os.sep + f"{pice}.png")
        img = copy.copy(original)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        #cv2.imshow("Result", img)
        #cv2.waitKey(0)

        #creating white pices
        img[np.where((img==[255,0,0]).all(axis=2))]= [255, 255, 255]
        cv2.imwrite(write_path + os.sep+ f"white_{pice}.png", img)
        new_images.append(f"white_{pice}")
        #cv2.waitKey(0)

        #creating black pices
        img = copy.copy(original)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        img[np.where((img==[255,0,0]).all(axis=2))]= [0, 0, 0]
        #cv2.imshow("Result", img)
        cv2.imwrite(write_path + os.sep+ f"black_{pice}.png", img)
        new_images.append(f"black_{pice}")
        #cv2.waitKey(0)