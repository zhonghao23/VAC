'''
Programmer Name:    CHIAM ZHONG HAO
Program Name:       vac-lpr.py
Description:        The entire process of license plate detection & recognition
                    -updating the entry & exit records to database for SMO 
                    -grant access to vehicles
First Written On:   20/01/2021
Edited On:          04/03/2021
'''
import cv2
import numpy as np
import pytesseract
import os
import re
from collections import Counter
import pyodbc
import pytz
from datetime import date, datetime

conn = pyodbc.connect('Driver={SQL Server};''Server=LAPTOP-H1SOMBBM\SQLEXPRESS;''Database=VAC;''Trusted_Connection=yes;') #connect to mssql
cursor = conn.cursor()

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract' #has to download the tesseract and change the path to the tesseract.exe file
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\zhong\Desktop\Mr_CHIAM_ZHONG_HAO_TP045889_UC3F2007_CS\VAC-LPR\Tesseract-OCR\tesseract'
showStep = False

def cropContours(gray_contours): ### CROP PLATE & SAVE AS IMAGE INTO FOLDER
  ### FIND CONTOUR
  contours, hierarchy = cv2.findContours(gray_contours, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  count = 0

  ### SAVE THE CONTOURS IMAGE INTO FOLDER
  for cnt in contours:
    count += 1
    minX,minY,w,h = cv2.boundingRect(cnt)
    maxX = minX + w
    maxY = minY + h
    cropped_img = gray_contours[int(minY)-5:int(maxY)+5,int(minX)-5:int(maxX)+5]
    img_name = str(count) + '.jpg'
    os.chdir(r'C:\Users\zhong\Desktop\Mr_CHIAM_ZHONG_HAO_TP045889_UC3F2007_CS\VAC-LPR\contours')
    cv2.imwrite(img_name, cropped_img)
  return count

def licensePlateDetection(resize_ori): ### LICENSE PLATE DETECTION
  ### GRAY IMAGE
  gray_img = cv2.cvtColor(resize_ori, cv2.COLOR_BGR2GRAY)

  ### EQUALIZE HISTOGRAM (BRIGHTEN IMAGE)
  eh_img = cv2.equalizeHist(gray_img)

  ### GAUSSIAN BLUR IMAGE (REMOVE NOISE)
  blur_img = cv2.GaussianBlur(eh_img,(9,9), 0)

  ### CANNY EDGE DETECTION
  edge_img = cv2.Canny(blur_img, 40, 70)

  ### DILATION
  kernel = np.ones((3,3),np.uint8)
  dilate_img = cv2.dilate(edge_img, kernel, iterations=1)
  dilate_img_ori = dilate_img.copy()

  ### FIND CONTOUR
  contours, hierarchy = cv2.findContours(dilate_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

  for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    cnt_area = cv2.contourArea(cnt)
    rect_area = w * h
    fullness = cnt_area / rect_area
    height, width = dilate_img.shape
    aspect_ratio = float(w)/h
    if ((x < width * 0.2) or (x > width * 0.8) or (y < height * 0.2) or (y > height * 0.8) or (w < width * 0.03) 
      or (w > width * 0.2) or (h < height * 0.03) or (aspect_ratio < 1.0) or (fullness < 0.5)): # condition to remove noise
      cv2.drawContours(dilate_img, [cnt], 0, (0), -1) # remove noise
  
  ### DILATION (MAKES LICENSE PLATE BIGGER)
  kernel = np.ones((15,15),np.uint8)
  dilate_plate = cv2.dilate(dilate_img, kernel, iterations=1)
  
  ### GRAY PLATE
  gray_contours = cv2.bitwise_and(gray_img, gray_img, mask=dilate_plate)
  
  ### CROP CONTOURS
  count = cropContours(gray_contours)

  ### SHOW PROCESS
  if showStep is True:
    cv2.imshow("gray_img", gray_img)
    cv2.imshow("eh_img", eh_img)
    cv2.imshow("blur_img", blur_img)
    cv2.imshow("edge_img", edge_img)
    cv2.imshow("dilate_img_ori", dilate_img_ori)
    cv2.imshow("dilate_img", dilate_img)
    cv2.imshow("dilate_plate", dilate_plate)
  else:
    cv2.imshow("dilate_plate", dilate_plate)  
  return count

def checkValidPlate(plate_number): ### CHECK THE FORMAT OF THE PLATE DETECTED
  contain_alnum = bool(re.match('^(?=.*[A-Z])(?=.*[0-9])', plate_number))
  count_num = 0
  length = len(plate_number)
  # example: WB7638C
  if contain_alnum == True:
    if plate_number[0].isalpha(): # first letter must be alphabet 'W'
      for i in range(1, length): # 'B7638C'
        if (plate_number[i].isnumeric()): # first encountering number '7'
          count_num += 1
          for j in range(i+1, length): # '638C'
            if plate_number[j].isalpha(): # the following characters after alpha must be alpha 'C'
              if count_num > 4: # more than 4 numbers
                return False
              else:
                if j != length-1: # not last alphabet
                  count_alpha = 1
                  for k in range(j+1, length): # check following characters after the alphabet
                    if plate_number[k].isnumeric(): # numbers again
                      return False
                    count_alpha += 1
                    if count_alpha > 2:
                      return False
                  return True # no numbers after the alphabet
                else: # last alphabet
                  return True
            else:
              count_num += 1
          if count_num > 4: # more than 4 numbers
            return False
          else:
            return True # no alphabet after numbers
    else: # first letter is number
      return False
  else: # not alphanumeric
    return False

def licensePlateRecognition(count): ### LICENSE PLATE RECOGNITION
  ### READ CONTOURS FROM FOLDER
  read_count = 1
  while (read_count <= count): #if there is a contour detected and saved into folder
    img_name = str(read_count) + '.jpg'
    
    ### READ GRAY PLATE
    gray_plate = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)

    ### RESIZE PLATE
    resize_gray_plate = cv2.resize(gray_plate, None, fx=3, fy=3, interpolation = cv2.INTER_CUBIC)

    ### GAUSSIAN BLUR PLATE
    blur_gray_plate = cv2.GaussianBlur(resize_gray_plate, (5,5), 0)

    ### OTSU THRESH TO BINARIZE PLATE
    ret, thresh = cv2.threshold(blur_gray_plate, 0, 255, cv2.THRESH_OTSU)

    ### SHOW IMAGE BEFORE NOISE REMOVAL
    if showStep is True:
      cv2.imshow("thresh before noise removal", thresh)

    ### FIND CONTOURS & REMOVE NOISE
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
      x,y,w,h = cv2.boundingRect(cnt)
      height, width = thresh.shape
      ratio = h / float(w)
      area = h * w
      if ((w < width * 0.05) or (h < height * 0.4) ): # remove noise in plate
        cv2.drawContours(thresh, [cnt], 0, (0), -1)
    
    ### ADJUST SKEW PLATE
    coords = np.column_stack(np.where(thresh)) # get all (x,y) of pixels in thresh
    angle = cv2.minAreaRect(coords)[-1] # get the angle of rotation
    skip = False
    if angle >= 89: # it is nearly perfect
      skip = True
    elif angle < -45:
      angle = -(90 + angle)
    else:
      angle = -angle
    if skip is False: #it can be adjusted for better result
      (h, w) = thresh.shape[:2]
      center = (w // 2, h // 2)
      M = cv2.getRotationMatrix2D(center, angle, 1.0)
      rotated = cv2.warpAffine(thresh, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    else:
      rotated = thresh.copy()

    ### INVERSE PLATE (TESSERACT IS TRAINED BETTER WITH WHITE BACKGROUND & BLACK CHARACTERS)
    ret, thresh2 = cv2.threshold(rotated, 0, 255, cv2.THRESH_BINARY_INV)

    ### PLATE RECOGNITION
    plate_number = ""
    try:
      plate_number = pytesseract.image_to_string(thresh2, lang='eng', config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 7 --oem 3') #psm 7 = single line, psm 8 = single character
    except: 
      plate_number = ""

    cv2.imshow("rotated", rotated)
    cv2.imshow("thresh", thresh)
    cv2.imshow("thresh2", thresh2)

    ### PLATE VALIDATION
    #remove white space & new line
    plate_number = plate_number.replace(" ", "")
    plate_number = plate_number.replace("\n", "")
    plate_number = plate_number.replace("\f", "")

    #check if plate_number is valid plate in malaysia
    valid_plate = checkValidPlate(plate_number)

    ### DELETE IMAGE AFTER VALIDATION
    try: 
      os.remove(img_name)
    except: pass
    read_count += 1

    ### RETURN VALID PLATE
    if valid_plate is True:
      return plate_number
    else:
      return False

def checkLicensePlateStatus(plate_number): ### CHECK THE STATUS OF THE LICENSE PLATE FROM DB
  ### SEARCH LICENSE_PLATE_T
  sql = "SELECT * FROM VAC.dbo.LICENSE_PLATE_T WHERE Plate_Number = '" + plate_number + "'"
  cursor.execute(sql)
  results = cursor.fetchall()
  found_lp = False
  for row in results:
    found_lp = True
  if found_lp is False:
    return False # not found in LICENSE_PLATE_T means have no record in any other table

  ### SEARCH ACCESS_LIST_T (FOUND IN LICENSE_PLATE_T)
  sql = "SELECT * FROM VAC.dbo.ACCESS_LIST_T WHERE Plate_Number = '" + plate_number + "'"
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    if row[3] == 'WHITELIST':
      return True # found in ACCESS_LIST_T 
    elif row[3] == 'BLACKLIST':
      return 'BLACKLIST' # found in ACCESS_LIST_T 
  
  ### SEARCH VISIT_T (FOUND IN LICENSE_PLATE_T BUT NOT ACCESS_LIST_T)
  now = pytz.timezone('Asia/Kuala_Lumpur')
  today_date_str = datetime.now(now).strftime('%Y-%m-%d')
  sql = "SELECT * FROM VAC.dbo.VISIT_T WHERE Plate_Number = '" + plate_number + "' AND Visit_On = '" + today_date_str + "'"
  #sql = "SELECT * FROM VAC.dbo.VISIT_T WHERE Plate_Number = '" + plate_number + "' AND Visit_On = '" + "2021-03-04" + "'"  #***FOR TESTING PURPOSE
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    if row[5] == 'APPROVED':
      return True # license plate is approved
  return False # license plate is rejected/pending

def updateDatabase(final_plate_number): ### UPDATE THE ENTRYEXIT_T
  #CHECK IF THE VEHICLE IS ENTERING OR EXITING
  sql = "SELECT * FROM VAC.dbo.ENTRYEXIT_T WHERE Plate_Number = '" + final_plate_number + "' AND EE_ExitOn IS NULL"
  cursor.execute(sql)
  results = cursor.fetchall()
  exit = False
  for row in results:
    ### EXIT: UPDATE EXISTING RECORD
    exit = True
    now = pytz.timezone('Asia/Kuala_Lumpur')
    today_datetime_str = datetime.now(now).strftime('%Y-%m-%d %H:%M:%S')
    sql = "UPDATE ENTRYEXIT_T SET EE_ExitOn = '" + today_datetime_str + "' WHERE EE_ID = " + str(row[0])
    cursor.execute(sql)
    conn.commit()
    print('EXIT: ACCESS GRANTED')
    accessChecked = True
  if exit is False:
    ### ENTER: CREATE NEW RECORD
    now = pytz.timezone('Asia/Kuala_Lumpur')
    today_datetime_str = datetime.now(now).strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO ENTRYEXIT_T (Plate_Number, EE_EntryOn) VALUES ('%s', '%s')" % (final_plate_number, today_datetime_str)
    cursor.execute(sql)
    conn.commit()
    print('ENTRY: ACCESS GRANTED')
    accessChecked = True

def main():
  ### LOAD VIDEO
  # cap = cv2.VideoCapture(r'C:\Users\zhong\Desktop\Mr_CHIAM_ZHONG_HAO_TP045889_UC3F2007_CS\VAC-LPR\BMS4554_vid.mp4')   ### TEST VIDEO 1
  # cap = cv2.VideoCapture(r'C:\Users\zhong\Desktop\Mr_CHIAM_ZHONG_HAO_TP045889_UC3F2007_CS\VAC-LPR\VFG961_vid.mp4')    ### TEST VIDEO 2
  cap = cv2.VideoCapture(r'C:\Users\zhong\Desktop\Mr_CHIAM_ZHONG_HAO_TP045889_UC3F2007_CS\VAC-LPR\WYA7572_vid.mp4')   ### TEST VIDEO 3

  ### MAIN FUNC 
  frame_count = 0
  plate_numbers = [] # keep track of plate numbers recognized
  accessChecked = False # check if the vehicle has already granted access
  while(cap.isOpened()):
    ret, frame = cap.read()
    frame_count += 1
    if ret == True: # while not end of video
      ### RESIZE FRAME
      resize_ori = cv2.resize(frame, (1024, 768), interpolation = cv2.INTER_AREA)
      cv2.imshow("resize_ori", resize_ori)
      
      ### DETECTION & RECOGNITION ON EVERY 30th FRAMES & ACCESS IS NOT GRANTED YET
      if frame_count % 30 == 0 and accessChecked is False:
        ### LICENSE PLATE DETECTION
        count = licensePlateDetection(resize_ori)

        ### LICENSE PLATE RECOGNITION 
        if (count > 0): # if there is plate detected
          plate_number = licensePlateRecognition(count)
          #print('LICENSE PLATE DETECTED: ', plate_number) #detected license plate on current frame
          
          if plate_number is False: # not license plate
            continue
          else:
            plate_numbers.append(plate_number) # add into plate numbers recognized
            if len(plate_numbers) > 5: # only start to check with database with at least 5 records in plate numbers recognized list
              counter = Counter(plate_numbers) # count occurence of plates in the list
              final_plate_number = counter.most_common(1)[0][0] # takes the plate number with most occurence as the final recognized license plate
              print('FINALIZED PLATE:', final_plate_number)

              ### CHECK IF RECOGNIZED LICENSE PLATE HAS RECORD IN DATABASE
              status = checkLicensePlateStatus(final_plate_number)
              #status = checkLicensePlateStatus('WB7777C')                           #***FOR TESTING PURPOSE
              #final_plate_number = 'WB7777C'                                        #***FOR TESTING PURPOSE
              #status = True                                                         #***FOR TESTING PURPOSE
              if status is True: # found records in database (ACCESS GRANTED)
                updateDatabase(final_plate_number)
                accessChecked = True
                plate_numbers = []
              elif status == 'BLACKLIST': # found record in database (ACCESS DENIED)
                print('ACCESS DENIED. BLACKLISTED')
                accessChecked = True
                plate_numbers = []
              else: # no record found in database
                print('NO RECORD. KEEP CHECKING')
                accessChecked = False
      if cv2.waitKey(1) & 0xFF == ord('q'): #read frames every 1ms and exit with 'q'
        break
    else: # end of video
      break
  print('frame_count:', frame_count)
  cap.release()
  cv2.destroyAllWindows()

if __name__ == "__main__":
  main()