from builtins import int
import pyautogui
import time
import cv2
import mss
import numpy as np
from numpy import asarray

from PIL import Image as im 

import os

#Setup PAddle ocr
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')



def textRecognitionOnImage(inputImageInit, forDateAndTime):


    scale_percent = 300 # percent of original size
    if not(forDateAndTime):
        scale_percent = 300
    width = int(inputImageInit.shape[1] * scale_percent / 100)

    height = int(inputImageInit.shape[0] * scale_percent / 100)
  
    dim = (width, height)
    inputImageInit = cv2.resize(inputImageInit, dim, interpolation = cv2.INTER_AREA)
  
    #cv2.imwrite("resImg.png", inputImageInit)
    #inputImageInitP = im.fromarray(cv2.cvtColor(inputImageInit, cv2.COLOR_BGR2RGB))
    #inputImageInitP = inputImageInit.tobytes()# im.fromarray(inputImageInit)

    result = ocr.ocr(inputImageInit,det=True, cls=False)
   
    return result




def isCurrentSymbolDigit(currentSymbol):
    if currentSymbol == '0' or  currentSymbol == '1' or  currentSymbol == '2'  or  currentSymbol == '3' or  currentSymbol == '4' or  currentSymbol == '5' or currentSymbol == '6' or currentSymbol == '7' or  currentSymbol == '8' or currentSymbol == '9':
        return True
    return False 

def isStringContainsDigit(inputString):
    for i in range(len(inputString)):
        if inputString[i] == '0' or  inputString[i] == '1' or  inputString[i] == '2'  or  inputString[i] == '3' or  inputString[i] == '4' or  inputString[i] == '5' or inputString[i] == '6' or inputString[i] == '7' or  inputString[i] == '8' or inputString[i] == '9':
            return True
    return False

def filterDateString(inputString):
    filteredString = ""
    for i in range(len(inputString)):
        if isCurrentSymbolDigit(inputString[i]):
            filteredString = filteredString + inputString[i]        
    
    return  filteredString  

    
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
 
def getDayFromDateAndYear(inputString):
    month, day, year =  getDateAndYearFromData(inputString)
    if len(day) == 2 and day[0] == '0':
        return day[1]
    return day
    
def getMonthFromDateAndYear(inputString):
    month, day, year =  getDateAndYearFromData(inputString)
    if len(month) == 2 and month[0] == '0':
        return month[1]
    return month
 
 
def checkIfStartDateIsValid(inputString, dayFromMouse, monthFromMouse):
    if inputString.count('/') == 1:
        
        startDayData = inputString.split('/')
        day = startDayData[1]
        print("START DAY FINAL")
        print(day)
        print("DAY FROM MOIUSE FINAL")
        print(dayFromMouse)
        if day == dayFromMouse:
            return True
        else:
            return False
    
    inputString.replace(" ", "")
    inputString.replace("'","")
    if inputString == monthFromMouse:
        return True
    return False    
 
def getStartEndDayPosition(inputString, isFirst):
#    print("Start- End Day")
    if isFirst:
        return inputString[0][0][0]
    
    return inputString[0][1][0]
    
    
def findDateYearRegionAndCrop(inputImage):
    isFound = False
    heightImg, widthImg, channelsIm = inputImage.shape
   
    resText = textRecognitionOnImage(inputImage, True)
 
    
    for i in range(len(resText)):
       
        if  str(resText[i][1][0]).count('/') == 2:
            print("Date and time ")
            print(resText[i][1][0])
            xStart = resText[i][0][0][0]
            xEnd = resText[i][0][1][0]
            yStart = resText[i][0][0][1]
            yEnd = resText[i][0][2][1]
            print("While cropping ")
            inputImage1 = inputImage[heightImg - int(1.5*(yEnd - yStart)):heightImg,0:widthImg]
            isFound = True
            return [inputImage1, isFound, xStart, xEnd]
     
    return [inputImage, isFound, -1,-1]
    
def processScreenshotImage(inputImage):
  
  
    heightImg, widthIm, channelsIm = inputImage.shape
    leftRectMax = 0
    rightRectMin = 3.0*widthIm
    firstDate =     False
    lastDate = False
    isDateTime = False
    isFound = False
   
    cropedImageRegion, isFound, dateTimeStart, dateTimeEnd = findDateYearRegionAndCrop(inputImage)
	
    if dateTimeStart == -1 or dateTimeEnd == -1:
        return	
    if isFound == False:
        return
   
    resText = textRecognitionOnImage(cropedImageRegion, False)
    print("After image crop")
    #print("RESULT")
    #for i in range(len(resText)):
    #    print(resText[i])
    #print(resText)
 
    rectStartPos = -1
    rectEndPos = widthIm + 1
    month = '00'
    day = '00'
    year = '00'
    startDayVal = '00'
    
    countOfValidDateAndYear = 0
    countOfValidDate = 0
    for i in range(len(resText)):
        if  str(resText[i][1][0]).count('/') == 2:
            countOfValidDateAndYear = countOfValidDateAndYear + 1
        if  str(resText[i][1][0]).count('/') == 1 or str(resText[i][1][0]).count("'") == 1  or (str(resText[i][1][0]).count(" ") == 1   and  str(resText[i][1][0]).count("/") == 0  and str(resText[i][1][0]).count(":") == 0 )or  (str(resText[i][1][0]).count(" ") == 0   and  str(resText[i][1][0]).count("/") == 0  and str(resText[i][1][0]).count(":") == 0):
            countOfValidDate = countOfValidDate + 1
          
    if countOfValidDate < 2 or countOfValidDateAndYear != 1:
        return
    
    
  #Finding day , month , year from mouse position 
    for i in range(len(resText)):
        if  str(resText[i][1][0]).count('/') == 2:
    
            month, day, year = getDateAndYearFromData(str(resText[i][1][0]))
            month = getMonthFromDateAndYear(str(resText[i][1][0]))
            day = getDayFromDateAndYear(str(resText[i][1][0]))

            
    for i in range(len(resText)):
        

        if  str(resText[i][1][0]).count('/') == 2:
    
            month, day, year = getDateAndYearFromData(str(resText[i][1][0]))
            month = getMonthFromDateAndYear(str(resText[i][1][0]))
            day = getDayFromDateAndYear(str(resText[i][1][0]))
            
            isDateTime = True
     
        if str(resText[i][1][0]).count('/') == 1 or  str(resText[i][1][0]).count("'") == 1 or   (str(resText[i][1][0]).count(" ") == 1 and  str(resText[i][1][0]).count("/") == 0)   or  (str(resText[i][1][0]).count(" ") == 0   and  str(resText[i][1][0]).count("/") == 0  and str(resText[i][1][0]).count(":") == 0 ) :
            if isDateTime:
               
                tmpEndPose = getStartEndDayPosition((resText[i]), False) /1.0
                print("Date and time pos ")
                print(dateTimeEnd)            
                print("End day pos ")
                print(tmpEndPose)				
                print(print(resText[i][1][0]))
                if tmpEndPose < rightRectMin and tmpEndPose >= dateTimeEnd and  str(resText[i][1][0]).count('.') == 0 and  str(resText[i][1][0]).count(':') == 0 and isStringContainsDigit(str(resText[i][1][0])) :
                    print("end !!!!! day")
                    print(print(resText[i][1][0]))
                    ###print("multiple times ")
                    rightRectMin = tmpEndPose
                    rectEndPos = rightRectMin
            else:
                print("start !!!!! day")
                #dayStart = getDayFromStartPosData(resText[i][1][0])				
                print(print(resText[i][1][0]))	
               # print(dayStart)                
                tmpStartPos = getStartEndDayPosition((resText[i]), True)/1.0
                print(tmpStartPos)
                print("Day FROM MOUSE BEFORE FUN CALL")
                print(day)
                if tmpStartPos > leftRectMax and tmpStartPos <= dateTimeStart and  str(resText[i][1][0]).count('.') == 0 and str(resText[i][1][0]).count(':') == 0 and isStringContainsDigit(str(resText[i][1][0])) and checkIfStartDateIsValid(str(resText[i][1][0]), day, month):
                    #######if str(resText[i][1][0]).count('/') == 1  :
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
    filterDateString
    outputImageName = 'results/'  +  filterDateString(str(month)) + "-" + filterDateString(str(day)) + "-" + str('20') +  filterDateString(str(year)) + ".png"
    #outputImageName = 'results/'  +  str(month) + "-" + str(day) + "-" + str('20') +  str(year) + ".png"
    
    resImgCrop = inputImage[0:heightImg,int(rectStartPos/3.0):int(rectEndPos/3.0)]
   # cv2.imshow("RectIMgCrop", resImgCrop)
  #  cv2.waitKey(0)
    heightImgR, widthImR, channelsImR = resImgCrop.shape    
    if heightImgR != 0 and widthImR != 0 and rectStartPos != -1 and rectEndPos != widthIm +1   and rectStartPos  <= dateTimeStart and rectEndPos >= dateTimeEnd :
        cv2.imwrite(outputImageName, resImgCrop)
            




def captureAndProcessScreenshotImages():
   

    with mss.mss() as sct:
            # Capture the entire screen
            monitor = sct.monitors[0]

            # Capture the screen image
            screenshot = sct.shot(output="screenshot.png")
    image = cv2.imread("screenshot.png")
    r = cv2.selectROI("select the area", image)
    cv2.destroyAllWindows() 
    # Crop image
    cropped_image = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
   
    screenshot1 = image.copy()


    while 1:
     
      
        pyautogui.moveTo(350, 200)  #### Initial mouse position 
        pyautogui.click() 
        pyautogui.press(['right'],presses=20)  ### Movement steps
       # time.sleep(30)       #Sleeep time  
        # Initialize the screen capture object
        with mss.mss() as sct:
           
            # Capture the entire screen
            monitor = sct.monitors[0]
            
            # Capture the screen image
            screenshot = sct.shot(output="screenshot.png")
        # Load the captured screenshot using OpenCV
        screen_cv2 = cv2.imread("screenshot.png")
      #  cv2.imshow("CurrScr", screen_cv2)
       # cv2.waitKey(0)
        screen_cv2 = screen_cv2[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]   
        processScreenshotImage(screen_cv2)



if __name__ == "__main__":
         captureAndProcessScreenshotImages()