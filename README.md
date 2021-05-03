# Vehicle Access Control System (VAC)
Vehicle Access Control System for Gated Communities with License Plate Recognition Based on Progressive Web Application

# Motivation
The project is inspired by the exising system implemented in most of the gated communities which is using electronic access card to access the gated communities.

The existing system might be fine for the residents but it might be troublesome and time-consuming for the visitors to access the gated communities. 

The proposed system is powered by the license plate recognition (LPR) technology which can detects and identify the vehicle's license plate to grant access accordingly.

The access lists are managed by the residents which means that the residents are the one who decide if the visitors are allowed to access the gated communities easily through their license plates registered.

The visitors could make a request for access through the web application that requires approval from the residents.

The residents are responsible for either approving their own visitors' request for access or add the visitors to their whitelist to grant access.

The security management office could make use of the web application to monitor the records of visits, records of vehicles' entry and exit and so on.

# Target Users
1. Resident
2. Visitor
3. Security Management Office

# Features
1. Resident
    1. To sign in and logout from the system.
    1. To view their own profile.
    1. To change the account password.
    1. To view their registered license plate number.
    1. To register their own license plate number.
    1. To register the license plate number of their visitors. (Whitelist)
    1. To blacklist a license plate number.
    1. To remove a license plate from the list.
    1. To view the access requests.
    1. To approve or reject the access requests of their visitors.
    1. To access residential areas with their registered license plate.
  
2. Visitor
    1. To fill in their information and license plate number to make a request to the resident for
access to the residential area.
    2. To check the approval status of the request.
    3. To access the residential area with their license plate upon approval by the resident.
    4. To access the residential area with their license plate upon successful registration of their
license plate done by the resident. 

3. Security Management Office
    1. To sign in and logout from the system.
    2. To view their own profile.
    3. To create or reset an account for new residents.
    4. To view the information of residents.
    5. To view the record of visits made by the visitors.
    6. To view the record of vehicles’ entry and exit to the residential area. 

# Tech/Framework used
1. Vue.JS (Frontend)
2. Flask (Backend)
3. OpenCV (License Plate Recognition/Image Processing)
4. TesseractOCR (Optical Character Recognition)
5. RESTful API
6. Flask-SQLAlchemy

## Languages
1. HTML5
2. CSS3
3. Javascript
4. Python
5. Microsoft SQL Server

**built with**
1. VSCode
2. Microsoft SQL Server Management Studio 2018

# Screenshots
## License Plate Recognition (LPR)
### Sample Video
![image](https://user-images.githubusercontent.com/63278063/116912087-52cbaf00-ac7a-11eb-9a81-d7cbaf509eb6.png)

### Extracted License Plate
![image](https://user-images.githubusercontent.com/63278063/116912214-81498a00-ac7a-11eb-8301-66ed8de93ea4.png)

### Result
![image](https://user-images.githubusercontent.com/63278063/116912321-a3430c80-ac7a-11eb-91c5-046ded5a0c34.png)

## Progressive Web Application (PWA)
### Sample UI
![image](https://user-images.githubusercontent.com/63278063/116912535-ed2bf280-ac7a-11eb-8a68-2489c7bdc276.png)

![image](https://user-images.githubusercontent.com/63278063/116912802-485de500-ac7b-11eb-867c-c53f764a6607.png)

![image](https://user-images.githubusercontent.com/63278063/116912867-5b70b500-ac7b-11eb-98de-27432d3b350e.png)

![image](https://user-images.githubusercontent.com/63278063/116912933-73e0cf80-ac7b-11eb-8e4c-d5cf8edb0e3e.png)

![image](https://user-images.githubusercontent.com/63278063/116912989-865b0900-ac7b-11eb-82ee-c68afe2ec549.png)

### Progressive Web App Features
![image](https://user-images.githubusercontent.com/63278063/116913047-95da5200-ac7b-11eb-839a-d7d26ad796cf.png)

![image](https://user-images.githubusercontent.com/63278063/116913115-a8ed2200-ac7b-11eb-9be8-254ee484bbc2.png)

![image](https://user-images.githubusercontent.com/63278063/116913146-b4404d80-ac7b-11eb-8788-cd955b16072a.png)




# Installation


 
