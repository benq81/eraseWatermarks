# -*- coding: utf-8 -*-
"""
Spyder Editor

图片水印消除V0.1
By batista
"""
import cv2
import os
import numpy as np


def getCutedImg(origin,printHeight):
    #获取裁切后的图片
    try :
        hight, width, depth = origin.shape[0:3]
        new_array=np.zeros_like(origin)
        new_array[hight-printHeight:hight]=1
        printImg=origin * new_array
    except Exception as e:
        print("%s图片有误......"%origin , e)
        printImg=np.zeros(3)
    return printImg

def editOriginImg(printImg,originImg):
    #修理原图
    try:
        #注意图片颜色排列是[B,G,R]，不是[R,G,B]
        thresh = cv2.inRange(printImg, np.array([60,76,177]), np.array([170,165,250]))
        #构建卷积核
        kernel = np.ones((5,5), np.uint8)
        #膨胀
        hi_mask = cv2.dilate(thresh, kernel, iterations=1)
        newImg = cv2.inpaint(originImg, hi_mask, 5, flags=cv2.INPAINT_TELEA)
    except Exception as e:
        print("%s处理图片时报错"%originImg,e)
        newImg=np.zeros(3)
    return newImg

def saveNewImg(newImg,fileName):
    #保存新图
    try:
        cv2.imwrite(fileName,newImg)
        print("%s 's ok!..............."%fileName)
    except Exception as e:
        print("error......"+e)
#测试时使用，用于显示图片
def showImg(img):
    #显示图片
    hight, width, depth = img.shape[0:3]
    cv2.namedWindow("Image", 0)
    cv2.resizeWindow("Image", int(width / 2), int(hight / 2))
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    #图片源目录.
    filesPath="source_images"
    #新图片保存目录
    newFilesPath="target_images"
    files=os.listdir(filesPath)
    for file in files:
        filePath=os.path.join(filesPath,file)
        origin = cv2.imread(filePath)
        #水印的高度，可以根据具体图片水印的具体高度去处理
        printHeight = 43
        printImg=getCutedImg(origin,printHeight)
        if printImg.size!=0:
            newImg=editOriginImg(printImg,origin)
            if newImg.size!=0:
                newFileName = os.path.join(newFilesPath,file)
                saveNewImg(newImg,newFileName)


if __name__=="__main__":
    main()





