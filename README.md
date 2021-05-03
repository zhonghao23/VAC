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



 
