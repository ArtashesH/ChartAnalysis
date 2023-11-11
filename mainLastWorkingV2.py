from builtins import int

import cv2
import mss
import numpy as np

from PIL import Image as im 

import os

#Setup PAddle ocr
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')



def textRecognitionOnImage(inputImageInit):


    scale_percent = 250 # percent of original size
    width = int(inputImageInit.shape[1] * scale_percent / 100)
    height = int(inputImageInit.shape[0] * scale_percent / 100)
    dim = (width, height)
    inputImageInit = cv2.resize(inputImageInit, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite("resImg.png", inputImageInit)

    result = ocr.ocr(inputImageInit,det=True, cls=True)
    return result


def getDateAndYearFromData(inputString):
    dateYearData = inputString.split('/')
    #print(dateYearData[2].split(' '))
    month = '00'
    day = '00'
    year = '00'
    if len(dateYearData) == 3:
        month = dateYearData[0][-2:]
        day = dateYearData[1]
        year = dateYearData[2].split(' ')[0][:2]
    return [month, day, year]
 
def getStartEndDayPosition(inputString, isFirst):
#    print("Start- End Day")
    if isFirst:
        return inputString[0][0][0]
    
    return inputString[0][1][0]
    
    
def findDateYearRegionAndCrop(inputImage):
    heightImg, widthImg, channelsIm = inputImage.shape
    resText = textRecognitionOnImage(inputImage)
    for i in range(len(resText)):
        if  str(resText[i][1][0]).count('/') == 2:
           # cv2.imwrite("afterCrop.png", inputImage)
            xStart = resText[i][0][0][0]
            xEnd = resText[i][0][1][0]
            yStart = resText[i][0][0][1]
            yEnd = resText[i][0][2][1]
      #################      print("Gen result")
    #############        print(resText[i])
 ##################           print("Start ebd")
   ################         print(xStart)
  #############          print(xEnd)
   ##############         print(yStart)
 #################           print(yEnd)
            inputImage1 = inputImage[heightImg - int(2.5*(yEnd - yStart)):heightImg,0:widthImg]
            #cv2.imwrite("DateReg.png", inputImage1)
      
            return inputImage1
    return inputImage
    
def processScreenshotImage(inputImage):
   # inputImage = cv2.imread('C:/Users/Kb6m456V/PycharmProjects/pythonProject/8.png')
   
    
   
    heightImg, widthIm, channelsIm = inputImage.shape
    leftRectMax = 0
    rightRectMin = widthIm
    firstDate =     False
    lastDate = False
    isDateTime = False
    cropedImageRegion = findDateYearRegionAndCrop(inputImage)
    
    resText = textRecognitionOnImage(cropedImageRegion)
    print("Result text")
   #### for i in range(len(resText)):
    #####    print(resText[i])
    #print(resText)
    rectStartPos = 0
    rectEndPos = widthIm
    month = '00'
    day = '00'
    year = '00'
    countOfValidDateAndYear = 0
    countOfValidDate = 0
    for i in range(len(resText)):
        if  str(resText[i][1][0]).count('/') == 2:
            countOfValidDateAndYear = countOfValidDateAndYear + 1
        if  str(resText[i][1][0]).count('/') == 1 or str(resText[i][1][0]).count("'") == 1 :
            countOfValidDate = countOfValidDate + 1
    if countOfValidDate < 2 or countOfValidDateAndYear != 1:
        return
                 
    for i in range(len(resText)):
        

        if  str(resText[i][1][0]).count('/') == 2:
    
            month, day, year = getDateAndYearFromData(str(resText[i][1][0]))
            isDateTime = True
     
        if str(resText[i][1][0]).count('/') == 1 or  str(resText[i][1][0]).count("'") == 1:
            if isDateTime:
                tmpEndPose = getStartEndDayPosition((resText[i]), False)/2.5
                if tmpEndPose < rightRectMin:
                    rightRectMin = tmpEndPose
                    rectEndPos = rightRectMin
            else:
                tmpStartPos = getStartEndDayPosition((resText[i]), True)/2.5
                if tmpStartPos > leftRectMax:
                    leftRectMax = tmpStartPos
                    rectStartPos = leftRectMax
                
     

    print("Month ")
    print(month)
    print("day")
    print(day)
    print("year")
    print(year)
    print("star pos")
    print(rectStartPos)
    print("end` pos")
    print(rectEndPos)
    outputImageName = 'results/'  +  str(month) + "-" + str(day) + "-" + str('20') +  str(year) + ".png"
    resImgCrop = inputImage[0:heightImg,int(rectStartPos):int(rectEndPos)]    
    cv2.imwrite(outputImageName, resImgCrop)
            




with mss.mss() as sct:
        # Capture the entire screen
        monitor = sct.monitors[0]

        # Capture the screen image
        screenshot = sct.shot(output="screenshot.png")
image = cv2.imread("screenshot.png")
r = cv2.selectROI("select the area", image)
# Crop image
cropped_image = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]



while 1:
    # Initialize the screen capture object
    with mss.mss() as sct:
        # Capture the entire screen
        monitor = sct.monitors[0]
        #monitor = sct.monitors[self.monitorIndex]
            # Capture the screen image
     
        #screen_cv2 = cv2.imread("screenshot.png")
        #screen_cv2 = screen_cv2[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        #processScreenshotImage(screenshot)
        # Capture the screen image
        screenshot = sct.shot(output="screenshot.png")





    # Load the captured screenshot using OpenCV
    screen_cv2 = cv2.imread("screenshot.png")
    screen_cv2 = screen_cv2[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    #resText = analogDataRecognition(screen_cv2)
    #print("Res text")
    #print(resText[0][2][1][0])
   # print(resText)

    # Display the screenshot using OpenCV (optional)
   # cv2.imshow("Screenshot", screen_cv2)
    
    #cv2.waitKey(10)
    processScreenshotImage(screen_cv2)

