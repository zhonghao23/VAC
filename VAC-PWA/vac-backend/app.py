'''
Programmer Name:    CHIAM ZHONG HAO
Program Name:       app.py
Description:        The entire backend API for VAC
First Written On:   01/01/2021
Edited On:          04/03/2021
'''
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin #REMOVE IN PRODUCTION
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import hashlib
import pyodbc
import config as cfg
import jwt

import pytz
from datetime import date, datetime, timedelta
from functools import wraps
from random import randint
from models import db, SMO, Resident, Visitor, Visit, LicensePlate, EntryExit, Access

#configuration (development)
#DEBUG = True

#instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

#enable CORS
CORS(app, resources={r'/*': {'origins': '*'}}) #REMOVE IN PRODUCTION

#connect to mssqldb
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://@{cfg.dbconfig["host"]}/{cfg.dbconfig["dbname"]}?driver=SQL+Server?trusted_connection=yes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#encryption config
bcrypt = Bcrypt(app)
app.config['BCRYPT_HANDLE_LONG_PASSWORDS'] = True

#JWT secret key config
app.config['SECRET_KEY'] = 'FdjhskASkjsdHWUQO158ASDjNDjkalsdiocpxzcSADJksdjSNADKlwnwe129JSDnaskei8DSA'

#CHECK JWT TOKEN VALIDITY FOR API CALLS *******************************
def token_required(f):
    @wraps(f) #wrapping function/decorator
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token.',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token.',
            'authenticated': False
        }

        if len(auth_headers) != 2: #if the length of the content is not as sent
            return jsonify(invalid_msg)

        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.config['SECRET_KEY']) #decode with defined secret key
            #print(data)
            if (data['resident']): #resident
                user = Resident.query.filter_by(res_id=data['user_id']).first()
            else: #SMO
                user = SMO.query.filter_by(smo_id=data['user_id']).first()
            #print("userid" + str(user))
            if not user:
                raise RuntimeError('User not found')
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg)
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg)
    return _verify

#(VISITOR) REGISTER LICENSE PLATE *******************************
@app.route('/visitor_lp', methods=["POST"])
def visitorLP():
    if request.method == 'POST':
        post_data = request.get_json()
        #CHECK IF PLATE IS BLACKLISTED/WHITELISTED/DELETED
        findAccess = Access.query.filter_by(plate_number=post_data.get('plate_number')).first()
        if (findAccess is not None): #LP FOUND IN ACCESS_LIST_T
            if (findAccess.lp_status == 'BLACKLIST'): #FAIL 
                response_object = '1'
            elif (findAccess.lp_status == 'WHITELIST'): #FAIL
                response_object = '2'
            elif (findAccess.lp_status == 'DELETED'): #PLATE IN LP_T IS NOT NULL FOR SURE
                #CHECK IF THE DELETED PLATE HAS BEEN REUSED BY VISITOR
                findVisit = Visit.query.filter_by(plate_number=post_data.get('plate_number')).first()
                if (findVisit is not None): #LP IS REGISTERED BY VISITOR
                    findVisitor = Visitor.query.filter_by(v_contactno='+601'+post_data.get('v_contactno')).first() #LOOK FOR EXISTING VISITOR RECORD THAT MATCHES WITH CURRENT APPLICATION
                    findLP = LicensePlate.query.filter_by(plate_number=findVisit.plate_number).first() #LP of the Visit
                    if (findVisitor is not None): #FOUND EXISTING VISITOR RECORD MATCH WITH CURRENT APPLICATION
                        if (findVisitor.visitor_id != findLP.visitor_id): #LP IS REGISTERED WITH ANOTHER VISITOR (CONTACT NO)
                            response_object = '3'
                        else: #LP IS REGISTERED BY THE SAME VISITOR
                            findAllVisit = Visit.query.filter( (Visit.plate_number == post_data.get('plate_number')) & (Visit.visit_on == post_data.get('visit_date')) ).all()
                            if (findAllVisit != []): #FOUND RECORDS IN VISIT_T ON THE SAME DATE
                                approved = False
                                pending = False
                                rejected = False
                                for i in range(len(findAllVisit)): #CHECK IF ANY EXISTING VISIT HAS BEEN MADE
                                    if (findAllVisit[i].visit_status == 'APPROVED'):
                                        approved = True
                                    elif (findAllVisit[i].visit_status == 'PENDING'):
                                        pending = True
                                    elif (findAllVisit[i].visit_status == 'REJECTED'):
                                        rejected = True
                                if (approved is True or pending is True): #GOT EXISTING VISIT HAS BEEN MADE ON THE SAME DATE
                                    response_object = '4'
                                elif (rejected is True):
                                    findCode = Resident.query.filter( (Resident.r_secretcode == post_data.get('secret_code')) & (Resident.r_unitno == post_data.get('unit_number')) ).first() #CHECK IF SECRET CODE IS CORRECT
                                    if (findCode is not None): #CORRECT SECRET CODE/UNIT NUMBER
                                        #UPDATE VISITOR_T RECORD
                                        findVisitor.v_name = post_data.get('visitor_name')
                                        #CREATE NEW VISIT
                                        newVisit = Visit(
                                                    res_id=findCode.res_id, 
                                                    plate_number=post_data.get('plate_number'), 
                                                    visit_on=post_data.get('visit_date'), 
                                                    visit_purpose=post_data.get('visit_purpose'),
                                                    visit_status="PENDING")
                                        db.session.add(newVisit)
                                        db.session.commit()
                                        response_object = 'SUCCESS'
                                    else: #WRONG SECRET CODE/UNIT NUMBER
                                        response_object = '5'
                            else: #NO RECORD FOUND IN VISIT_T ON THE SAME DATE
                                findCode = Resident.query.filter( (Resident.r_secretcode == post_data.get('secret_code')) & (Resident.r_unitno == post_data.get('unit_number')) ).first() #CHECK IF SECRET CODE IS CORRECT
                                if (findCode is not None): #CORRECT SECRET CODE/UNIT NUMBER
                                    #UPDATE VISITOR_T RECORD
                                    findVisitor.v_name = post_data.get('visitor_name')
                                    #CREATE NEW VISIT
                                    newVisit = Visit(
                                                res_id=findCode.res_id, 
                                                plate_number=post_data.get('plate_number'), 
                                                visit_on=post_data.get('visit_date'), 
                                                visit_purpose=post_data.get('visit_purpose'),
                                                visit_status="PENDING")
                                    db.session.add(newVisit)
                                    db.session.commit()
                                    response_object = 'SUCCESS'
                                else: #WRONG SECRET CODE/UNIT NUMBER
                                    response_object = '5'
                    else: #NO EXISTING VISITOR RECORD MATCH WITH CURRENT APPLICATION, THE LP IS REGISTERED WITH ANOTHER VISITOR
                        response_object = '3'
                else: #NO RECORD IN VISIT_T
                    findVisitor = Visitor.query.filter_by(v_contactno='+601'+post_data.get('v_contactno')).first() #LOOK FOR EXISTING VISITOR RECORD THAT MATCHES WITH CURRENT APPLICATION
                    if (findVisitor is not None): #FOUND EXISTING VISITOR RECORD WITH CURRENT APPLICATION
                        findCode = Resident.query.filter( (Resident.r_secretcode == post_data.get('secret_code')) & (Resident.r_unitno == post_data.get('unit_number')) ).first() #CHECK IF SECRET CODE IS CORRECT
                        if (findCode is not None): #CORRECT SECRET CODE/UNIT NUMBER
                            #UPDATE LICENSE_PLATE_T RECORD
                            findLP = LicensePlate.query.filter_by(plate_number=post_data.get('plate_number')).first() #FIND THE LP RECORD
                            findLP.res_id = None
                            findLP.visitor_id = findVisitor.visitor_id #REUSE THE EXISTING VISITOR RECORD
                            #UPDATE VISITOR_T RECORD
                            findVisitor.v_name = post_data.get('visitor_name')
                            db.session.commit()
                            #CREATE NEW VISIT
                            newVisit = Visit(
                                        res_id=findCode.res_id, 
                                        plate_number=post_data.get('plate_number'), 
                                        visit_on=post_data.get('visit_date'), 
                                        visit_purpose=post_data.get('visit_purpose'),
                                        visit_status="PENDING")
                            db.session.add(newVisit)
                            db.session.commit()
                            response_object = 'SUCCESS'
                        else: #WRONG SECRET CODE/UNIT NUMBER
                            response_object = '5'
                    else: #NO EXISTING VISITOR RECORD WITH CURRENT APPLICATION
                        findCode = Resident.query.filter( (Resident.r_secretcode == post_data.get('secret_code')) & (Resident.r_unitno == post_data.get('unit_number')) ).first() #CHECK IF SECRET CODE IS CORRECT
                        if (findCode is not None): #CORRECT SECRET CODE/UNIT NUMBER
                            #CREATE NEW VISITOR
                            newVisitor = Visitor(v_contactno="+601"+post_data.get('v_contactno'), v_name=post_data.get('visitor_name'))
                            db.session.add(newVisitor)
                            db.session.commit()
                            #UPDATE LICENSE_PLATE_T RECORD
                            findLP = LicensePlate.query.filter_by(plate_number=post_data.get('plate_number')).first() #FIND THE LP RECORD
                            locateVisitor = Visitor.query.filter_by(v_contactno="+601"+post_data.get('v_contactno')).first()
                            findLP.res_id = None
                            findLP.visitor_id = locateVisitor.visitor_id #ASSIGN THE NEW VISITOR RECORD TO THE LP
                            #CREATE NEW VISIT
                            newVisit = Visit(
                                        res_id=findCode.res_id, 
                                        plate_number=post_data.get('plate_number'), 
                                        visit_on=post_data.get('visit_date'), 
                                        visit_purpose=post_data.get('visit_purpose'),
                                        visit_status="PENDING")
                            db.session.add(newVisit)
                            db.session.commit()
                            response_object = 'SUCCESS'
                        else: #WRONG SECRET CODE/UNIT NUMBER
                            response_object = '5'
        else: #NO LP FOUND IN ACCESS_LIST_T
            findLP = LicensePlate.query.filter_by(plate_number=post_data.get('plate_number')).first() #LP of the Visit
            if (findLP is not None):
                findVisitor = Visitor.query.filter_by(v_contactno='+601'+post_data.get('v_contactno')).first() #LOOK FOR EXISTING VISITOR RECORD THAT MATCHES WITH CURRENT APPLICATIOn
                if (findVisitor is not None): #FOUND EXISTING VISITOR RECORD THAT MATCH WITH CURRENT APPLICATION
                    if (findVisitor.visitor_id != findLP.visitor_id): #LP IS REGISTERED WITH ANOTHER VISITOR
                        response_object = '3'
                    else: #LP IS REGISTERED BY THE SAME VISITOR
                        findAllVisit = Visit.query.filter( (Visit.plate_number == post_data.get('plate_number')) & (Visit.visit_on == post_data.get('visit_date')) ).all()
                        if (findAllVisit != []): #FOUND RECORDS IN VISIT_T ON THE SAME DATE
                            approved = False
                            pending = False
                            rejected = False
                            for i in range(len(findAllVisit)): #CHECK IF ANY EXISTING VISIT HAS BEEN MADE
                                if (findAllVisit[i].visit_status == 'APPROVED'):
                                    approved = True
                                elif (findAllVisit[i].visit_status == 'PENDING'):
                                    pending = True
                                elif (findAllVisit[i].visit_status == 'REJECTED'):
                                    rejected = True
                            if (approved is True or pending is True): #GOT EXISTING VISIT HAS BEEN MADE ON THE SAME DATE
                                response_object = '4'
                            elif (rejected is True):
                                findCode = Resident.query.filter( (Resident.r_secretcode == post_data.get('secret_code')) & (Resident.r_unitno == post_data.get('unit_number')) ).first() #CHECK IF SECRET CODE IS CORRECT
                                if (findCode is not None): #CORRECT SECRET CODE/UNIT NUMBER
                                    #UPDATE VISITOR_T RECORD
                                    findVisitor.v_name = post_data.get('visitor_name')
                                    #CREATE NEW VISIT
                                    newVisit = Visit(
                                                res_id=findCode.res_id, 
                                                plate_number=post_data.get('plate_number'), 
                                                visit_on=post_data.get('visit_date'), 
                                                visit_purpose=post_data.get('visit_purpose'),
                                                visit_status="PENDING")
                                    db.session.add(newVisit)
                                    db.session.commit()
                                    response_object = 'SUCCESS'
                                else: #WRONG SECRET CODE/UNIT NUMBER
                                    response_object = '5'
                        else: #NO RECORD FOUND IN VISIT_T ON THE SAME DATE
                            findCode = Resident.query.filter( (Resident.r_secretcode == post_data.get('secret_code')) & (Resident.r_unitno == post_data.get('unit_number')) ).first() #CHECK IF SECRET CODE IS CORRECT
                            if (findCode is not None): #CORRECT SECRET CODE/UNIT NUMBER
                                #UPDATE VISITOR_T RECORD
                                findVisitor.v_name = post_data.get('visitor_name')
                                #CREATE NEW VISIT
                                newVisit = Visit(
                                            res_id=findCode.res_id, 
                                            plate_number=post_data.get('plate_number'), 
                                            visit_on=post_data.get('visit_date'), 
                                            visit_purpose=post_data.get('visit_purpose'),
                                            visit_status="PENDING")
                                db.session.add(newVisit)
                                db.session.commit()
                                response_object = 'SUCCESS'
                            else: #WRONG SECRET CODE/UNIT NUMBER
                                response_object = '5'
                else: #NO EXISTING VISITOR RECORD THAT MATCH WITH CURRENT APPLICATION, THE LP IS REGISTERED WITH ANOTHER VISITOR
                    response_object = '3'
            else: #NO RECORD IN LP_T
                findVisitor = Visitor.query.filter_by(v_contactno='+601'+post_data.get('v_contactno')).first() #LOOK FOR EXISTING VISITOR RECORD THAT MATCHES WITH CURRENT APPLICATION
                if (findVisitor is not None): #FOUND EXISTING VISITOR RECORD
                    findCode = Resident.query.filter( (Resident.r_secretcode == post_data.get('secret_code')) & (Resident.r_unitno == post_data.get('unit_number')) ).first() #CHECK IF SECRET CODE IS CORRECT
                    if (findCode is not None): #CORRECT SECRET CODE/UNIT NUMBER
                        #UPDATE VISITOR_T RECORD
                        findVisitor.v_name = post_data.get('visitor_name')
                        #CREATE NEW LIENCESE_PLATE_T RECORD
                        newLP = LicensePlate(plate_number=post_data.get('plate_number'), res_id=None, visitor_id=findVisitor.visitor_id)
                        db.session.add(newLP)
                        db.session.commit()
                        #CREATE NEW VISIT
                        newVisit = Visit(
                                    res_id=findCode.res_id, 
                                    plate_number=post_data.get('plate_number'), 
                                    visit_on=post_data.get('visit_date'), 
                                    visit_purpose=post_data.get('visit_purpose'),
                                    visit_status="PENDING")
                        db.session.add(newVisit)
                        db.session.commit()
                        response_object = 'SUCCESS'
                    else: #WRONG SECRET CODE/UNIT NUMBER
                        response_object = '5'
                else: #NO EXISTING VISITOR RECORD
                    findCode = Resident.query.filter( (Resident.r_secretcode == post_data.get('secret_code')) & (Resident.r_unitno == post_data.get('unit_number')) ).first() #CHECK IF SECRET CODE IS CORRECT
                    if (findCode is not None): #CORRECT SECRET CODE/UNIT NUMBER
                        #CREATE NEW VISITOR
                        newVisitor = Visitor(v_contactno="+601"+post_data.get('v_contactno'), v_name=post_data.get('visitor_name'))
                        db.session.add(newVisitor)
                        db.session.commit()
                        locateVisitor = Visitor.query.filter_by(v_contactno="+601"+post_data.get('v_contactno')).first()
                        #CREATE NEW LIENCESE_PLATE_T RECORD
                        newLP = LicensePlate(plate_number=post_data.get('plate_number'), res_id=None, visitor_id=locateVisitor.visitor_id)
                        db.session.add(newLP)
                        db.session.commit()
                        #CREATE NEW VISIT
                        newVisit = Visit(
                                    res_id=findCode.res_id, 
                                    plate_number=post_data.get('plate_number'), 
                                    visit_on=post_data.get('visit_date'), 
                                    visit_purpose=post_data.get('visit_purpose'),
                                    visit_status="PENDING")
                        db.session.add(newVisit)
                        db.session.commit()
                        response_object = 'SUCCESS'
                    else: #WRONG SECRET CODE/UNIT NUMBER
                        response_object = '5'
        return jsonify(response_object)

#(VISITOR) CHECK APPROVAL STATUS *******************************
@app.route('/visitor_lp/<plate_number>/<visit_date>', methods=["GET"])
def checkStatus(plate_number, visit_date):
    if request.method == 'GET':
        findLP = LicensePlate.query.filter_by(plate_number=plate_number).first() #look for existing LP in LICENSE_PLATE_T
        if (findLP is None): #NO RECORD IN LICENSE_PLATE_T
            response_object = 'The license plate is not registered yet. Please proceed to License Plate Registration.'
        else: #FOUND RECORD IN LICENSE_PLATE_T
            findAccess = Access.query.filter_by(plate_number=plate_number).first() #look for existing LP in ACCESS_LIST_T
            if (findAccess is not None): #FOUND RECORD IN ACCESS_LIST_T
                if (findAccess.lp_status == 'BLACKLIST'):
                    response_object = "The license plate is blacklisted. Please proceed to the security guard house for registration at the entrance when you arrived the residential area."
                elif (findAccess.lp_status == 'WHITELIST'):
                    response_object = "The license plate has already registered by the resident. You can access the residential area with your registered license plate"
                elif (findAccess.lp_status == 'DELETED'):
                    findAllVisit = Visit.query.filter( (Visit.plate_number == plate_number) & (Visit.visit_on == visit_date) ).all()
                    if (findAllVisit != []): #FOUND RECORDS IN VISIT_T ON THE SAME DATE
                        approved = False
                        pending = False
                        rejected = False
                        for i in range(len(findAllVisit)): #CHECK IF ANY EXISTING VISIT HAS BEEN MADE
                            if (findAllVisit[i].visit_status == 'APPROVED'):
                                approved = True
                            elif (findAllVisit[i].visit_status == 'PENDING'):
                                pending = True
                            elif (findAllVisit[i].visit_status == 'REJECTED'):
                                rejected = True
                        if(approved is True):
                            response_object = "The license plate registration is APPROVED."
                        elif(pending is True):
                            response_object = "The license plate registration is still PENDING."
                        elif(rejected is True and approved is False and pending is False):
                            response_object = "The license plate registration has been REJECTED. Please make another registration."
                    else:
                        response_object = 'The license plate is not registered yet. Please proceed to License Plate Registration.'
            else: #NO RECORD IN ACCESS_LIST_T
                findAllVisit = Visit.query.filter( (Visit.plate_number == plate_number) & (Visit.visit_on == visit_date) ).all()
                if (findAllVisit != []): #FOUND RECORDS IN VISIT_T ON THE SAME DATE
                    approved = False
                    pending = False
                    rejected = False
                    for i in range(len(findAllVisit)): #CHECK IF ANY EXISTING VISIT HAS BEEN MADE
                        if (findAllVisit[i].visit_status == 'APPROVED'):
                            approved = True
                        elif (findAllVisit[i].visit_status == 'PENDING'):
                            pending = True
                        elif (findAllVisit[i].visit_status == 'REJECTED'):
                            rejected = True
                    if(approved is True):
                        response_object = "The license plate registration is APPROVED."
                    elif(pending is True):
                        response_object = "The license plate registration is still PENDING."
                    elif(rejected is True and approved is False and pending is False):
                        response_object = "The license plate registration has been REJECTED. Please make another registration."
                else:
                    response_object = 'The license plate is not registered yet. Please proceed to License Plate Registration.'
        return jsonify(response_object)


        if (findLP is not None and findLP.res_id is None and findLP.visitor_id is not None and findLP.lp_status is None):
            #visits
            findLP2 = Visit.query.filter( (Visit.plate_number == plate_number) & (Visit.visit_on == visit_date) ).first()
            if (findLP2 is not None):
                response_object = "The license plate is " + findLP2.visit_status #APPROVED/REJECTED/PENDING
            else:
                response_object = 'The license plate is not registered' #no record found
        elif (findLP is not None and findLP.res_id is not None and findLP.visitor_id is None and findLP.lp_status is not None):
            #resident
            response_object = 'The license plate is belong to the resident' #resident could access
        elif (findLP is not None and findLP.res_id is not None and findLP.visitor_id is not None and findLP.lp_status is not None):
            #check whitelist/blacklist
            if (findLP.lp_status == 'WHITELIST'): #WHITELIST
                response_object = "The license plate has already registered by the resident. You can access the residential area with your registered license plate"      
            elif (findLP.lp_status == 'BLACKLIST'):
                response_object = "The license plate is blacklisted. Please proceed to the security guard house for registration at the entrance when you arrived the residential area."
        else:
            #did not register
            response_object = 'The license plate is not registered' #no record found       
        return jsonify(response_object)

#(RESIDENT & SMO) SIGN IN *******************************
@app.route('/signin', methods=["POST"])
def signIn():
    if request.method == 'POST':    
        post_data = request.get_json()
        if (post_data.get('resident')): #RESIDENT
            findUser = Resident.query.filter_by(r_username=post_data.get('username')).first()
            if (findUser is not None): #found username
                hash_password = hashlib.sha256(post_data.get('password').encode())
                hd_password = hash_password.hexdigest() #to prevent NULL byte problems
                correct_password = bcrypt.check_password_hash(findUser.r_password, hd_password)
                if (correct_password):
                    #Assigning a JWT Token
                    now = pytz.timezone('Asia/Kuala_Lumpur')
                    token = jwt.encode({'user_id' : findUser.res_id, 'resident' : post_data.get('resident'), 'exp' : datetime.now(now) + timedelta(days=1)}, app.config['SECRET_KEY'], algorithm='HS256')
                    return jsonify({ 'token': token.decode('UTF-8') })
                else:
                    response_object = "Invalid Password"
            else: #username not found
                response_object = "Invalid Username"            
        else: #SMO
            findUser = SMO.query.filter_by(s_username=post_data.get('username')).first()       
            if (findUser is not None): #found username
                hash_password = hashlib.sha256(post_data.get('password').encode())
                hd_password = hash_password.hexdigest() #to prevent NULL byte problems
                correct_password = bcrypt.check_password_hash(findUser.s_password, hd_password)
                if (correct_password):
                    #Assigning a JWT Token
                    now = pytz.timezone('Asia/Kuala_Lumpur')
                    token = jwt.encode({'user_id' : findUser.smo_id, 'resident' : post_data.get('resident'), 'exp' : datetime.now(now) + timedelta(days=1)}, app.config['SECRET_KEY'], algorithm='HS256')
                    return jsonify({ 'token': token.decode('UTF-8') })
                else:
                    response_object = "Invalid Password"
            else: #username not found
                response_object = "Invalid Username"

        return jsonify(response_object)

#(RESIDENT) CHANGE PASSWORD *******************************
@app.route('/resident/change_password', methods=["PUT"])
@token_required
def changePassword():
    if request.method == 'PUT':
        post_data = request.get_json() #user_id, old_password, new_password
        findUser = Resident.query.filter_by(res_id=post_data.get('user_id')).first()
        hash_password1 = hashlib.sha256(post_data.get('old_password').encode())
        hd_password1 = hash_password1.hexdigest() #to prevent NULL byte problems
        correct_password = bcrypt.check_password_hash(findUser.r_password, hd_password1)
        if (correct_password): #correct old password
            #hash new password
            hash_password = hashlib.sha256(post_data.get('new_password').encode())
            hd_password = hash_password.hexdigest()
            new_password = str(bcrypt.generate_password_hash(hd_password))
            new_password2 = new_password[:-1]
            new_password3 = new_password2[2:]
            #update table
            findUser.r_password = new_password3
            db.session.commit()
            response_object = 'SUCCESS'
        else:#wrong old password
            response_object = 'FAIL'

        return jsonify(response_object)

#(RESIDENT) LOAD LICENSE PLATE *******************************
@app.route('/resident/load_lp/<user_id>', methods=["GET"])
@token_required
def loadLicensePlate(user_id):
    if request.method == 'GET':
        response_object = []
        loadLP = Access.query.filter_by(res_id=user_id).all()
        for i in range(len(loadLP)):
            if (loadLP[i].lp_status != 'DELETED'):
                loadIdentity = LicensePlate.query.filter_by(plate_number=loadLP[i].plate_number).first() #CHECK IF PLATE BELONGS TO RES OR VIS
                if (loadIdentity.res_id is not None): #RESIDENT
                    data = {
                        'plate_number': loadLP[i].plate_number,
                        'identity': 'resident',
                        'v_name': '-',
                        'v_contactno': '-',
                        'lp_status': loadLP[i].lp_status
                    }
                    response_object.append(data)
                else: #VISITOR
                    loadVis = Visitor.query.filter_by(visitor_id=loadIdentity.visitor_id).first()
                    data = {
                        'plate_number': loadLP[i].plate_number,
                        'identity': 'visitor',
                        'v_name': loadVis.v_name,
                        'v_contactno': loadVis.v_contactno,
                        'lp_status': loadLP[i].lp_status
                    }
                    response_object.append(data)
        return jsonify(response_object)

#(RESIDENT) LOAD ACCESS REQUEST *******************************
@app.route('/resident/load_access_request/<user_id>', methods=["GET"])
@token_required
def loadAccessRequest(user_id):
    if request.method == 'GET':
        response_object = []
        loadVisit = Visit.query.filter_by(res_id=user_id).order_by(Visit.visit_on.desc()).all()
        now = pytz.timezone('Asia/Kuala_Lumpur')
        today_date_str = datetime.now(now).strftime('%Y-%m-%d')
        x = today_date_str.split("-")
        today_date = date(int(x[0]),int(x[1]),int(x[2]))
        for i in range(len(loadVisit)):
            if (loadVisit[i].visit_status != 'REJECTED' and loadVisit[i].visit_on >= today_date): #ONLY GET VISIT FROM TODAY ONWARDS
                loadLP = LicensePlate.query.filter_by(plate_number=loadVisit[i].plate_number).first()
                loadVisitor = Visitor.query.filter_by(visitor_id=loadLP.visitor_id).first()
                data = {
                    'visit_id': loadVisit[i].visit_id,
                    'plate_number': loadVisit[i].plate_number,
                    'visit_on': str(loadVisit[i].visit_on),
                    'visit_purpose': loadVisit[i].visit_purpose,
                    'visit_status': loadVisit[i].visit_status,
                    'v_name': loadVisitor.v_name,
                    'v_contactno': loadVisitor.v_contactno
                }
                response_object.append(data)
        
        return jsonify(response_object)

#(RESIDENT) REMOVE LICENSE PLATE *******************************
@app.route('/resident/remove_lp', methods=["PUT"])
@token_required
def removeLicensePlate():
    if request.method == 'PUT':
        post_data = request.get_json()
        findLP = Access.query.filter_by(plate_number=post_data.get('plate_number')).first()     
        if (findLP is not None):
            findLP.lp_status = 'DELETED'
            db.session.commit()
            response_object = 'SUCCESS'

        return jsonify(response_object)

#(RESIDENT) APPROVE/REJECT ACCESS REQUEST *******************************
@app.route('/resident/decide_request', methods=["PUT"])
@token_required
def decideRequest():
    if request.method == 'PUT':
        post_data = request.get_json()
        findVisit = Visit.query.filter_by(visit_id=post_data.get('visit_id')).first()
        if (post_data.get('decision') == 'approve'):
            findVisit.visit_status = 'APPROVED'
        else:
            findVisit.visit_status = 'REJECTED'
        db.session.commit()
        response_object = 'SUCCESS'
        return jsonify(response_object)

#(RESIDENT) ADD RESIDENT LICENSE PLATE *******************************
@app.route('/resident/add_res_lp', methods=["POST"])
@token_required
def addResidentLicensePlate():
    if request.method == 'POST':
        post_data = request.get_json()
        findAccess = Access.query.filter_by(plate_number=post_data.get('plate_number')).first()
        if (findAccess is not None): #FOUND IN ACCESS_LIST_T
            if (findAccess.lp_status == 'DELETED'):
                findVisit = Visit.query.filter_by(plate_number=post_data.get('plate_number')).all()
                for i in range(len(findVisit)): #DELETE ALL RELATED VISITS
                    db.session.delete(findVisit[i])
                findLP = LicensePlate.query.filter_by(plate_number=post_data.get('plate_number')).first()
                findAccess.res_id = post_data.get('user_id')
                findAccess.lp_status = 'WHITELIST'
                findLP.res_id = post_data.get('user_id')
                findLP.visitor_id = None
                db.session.commit()
                response_object = 'SUCCESS'
            elif (findAccess.lp_status == 'BLACKLIST'): #FAIL 
                response_object = '1'
            elif (findAccess.lp_status == 'WHITELIST'): #FAIL
                response_object = '2'
        else: #NOT FOUND IN ACCESS_LIST_T
            findVisit = Visit.query.filter_by(plate_number=post_data.get('plate_number')).all()
            for i in range(len(findVisit)): #DELETE ALL RELATED VISITS
                db.session.delete(findVisit[i])
            findLP = LicensePlate.query.filter_by(plate_number=post_data.get('plate_number')).first()
            if (findLP is not None): #FOUND IN LICENSE_PLATE_T
                findLP.res_id = post_data.get('user_id')
                findLP.visitor_id = None
                newAccess = Access(
                            res_id=post_data.get('user_id'), 
                            plate_number=post_data.get('plate_number'),
                            lp_status='WHITELIST')
                db.session.add(newAccess)
                db.session.commit()
                response_object = 'SUCCESS'
            else: #NOT FOUND IN LICENSE_PLATE_T
                newLP = LicensePlate(
                                plate_number=post_data.get('plate_number'),
                                res_id=post_data.get('user_id'),
                                visitor_id=None)
                db.session.add(newLP)
                db.session.commit()
                newAccess = Access(
                                res_id=post_data.get('user_id'), 
                                plate_number=post_data.get('plate_number'),
                                lp_status='WHITELIST')
                db.session.add(newAccess)
                db.session.commit()
                response_object = 'SUCCESS'
        return jsonify(response_object)

#(RESIDENT) ADD VISITOR LICENSE PLATE *******************************
@app.route('/resident/add_vis_lp', methods=["POST"])
@token_required
def addVisitorLicensePlate():
    if request.method == 'POST':
        post_data = request.get_json()
        findAccess = Access.query.filter_by(plate_number=post_data.get('plate_number')).first()
        if (findAccess is not None): #FOUND IN ACCESS_LIST_T
            if (findAccess.lp_status == 'DELETED'):
                findVisit = Visit.query.filter_by(plate_number=post_data.get('plate_number')).all()
                for i in range(len(findVisit)): #DELETE ALL RELATED VISITS
                    db.session.delete(findVisit[i])
                findLP = LicensePlate.query.filter_by(plate_number=post_data.get('plate_number')).first()
                findVisitor = Visitor.query.filter_by(v_contactno='+601'+post_data.get('v_contactno')).first() #CHECK IF GOT EXISTING VISITOR RECORD
                if (findVisitor is not None): #GOT EXISTING VISITOR RECORD
                    findVisitor.v_name = post_data.get('v_name') #UPDATE VISITOR RECORD
                    findAccess.res_id = post_data.get('user_id')
                    if (post_data.get('blacklist') is True):
                        findAccess.lp_status = 'BLACKLIST'
                    else:
                        findAccess.lp_status = 'WHITELIST'
                    findLP.res_id = None
                    findLP.visitor_id = findVisitor.visitor_id
                    db.session.commit()
                    response_object = 'SUCCESS'
                else: #NO EXISTING VISITOR RECORD
                    newVisitor = Visitor(v_contactno="+601"+post_data.get('v_contactno'), v_name=post_data.get('v_name'))
                    db.session.add(newVisitor)
                    db.session.commit()
                    findAccess.res_id = post_data.get('user_id')
                    if (post_data.get('blacklist') is True):
                        findAccess.lp_status = 'BLACKLIST'
                    else:
                        findAccess.lp_status = 'WHITELIST'
                    findLP.res_id = None
                    locateVisitor = Visitor.query.filter_by(v_contactno="+601"+post_data.get('v_contactno')).first()
                    findLP.visitor_id = locateVisitor.visitor_id
                    db.session.commit()
                    response_object = 'SUCCESS'
            elif (findAccess.lp_status == 'BLACKLIST'): #FAIL 
                response_object = '1'
            elif (findAccess.lp_status == 'WHITELIST'): #FAIL
                response_object = '2'
        else: #NOT FOUND IN ACCESS_LIST_T
            findVisit = Visit.query.filter_by(plate_number=post_data.get('plate_number')).all()
            for i in range(len(findVisit)): #DELETE ALL RELATED VISITS
                db.session.delete(findVisit[i])
            findLP = LicensePlate.query.filter_by(plate_number=post_data.get('plate_number')).first()
            if (findLP is not None): #FOUND IN LICENSE_PLATE_T
                findVisitor = Visitor.query.filter_by(v_contactno='+601'+post_data.get('v_contactno')).first() #CHECK IF GOT EXISTING VISITOR RECORD
                if (findVisitor is not None): #GOT EXISTING VISITOR RECORD
                    findVisitor.v_name = post_data.get('v_name') #UPDATE VISITOR RECORD
                    if (post_data.get('blacklist') is True):
                        status = 'BLACKLIST'
                    else:
                        status = 'WHITELIST'
                    findLP.res_id = None
                    findLP.visitor_id = findVisitor.visitor_id
                    newAccess = Access(
                            res_id=post_data.get('user_id'), 
                            plate_number=post_data.get('plate_number'),
                            lp_status=status)
                    db.session.add(newAccess)
                    db.session.commit()
                    response_object = 'SUCCESS'
                else: #NO EXISTING VISITOR RECORD
                    newVisitor = Visitor(v_contactno="+601"+post_data.get('v_contactno'), v_name=post_data.get('v_name'))
                    db.session.add(newVisitor)
                    db.session.commit()
                    findLP.res_id = None
                    locateVisitor = Visitor.query.filter_by(v_contactno="+601"+post_data.get('v_contactno')).first()
                    findLP.visitor_id = locateVisitor.visitor_id
                    if (post_data.get('blacklist') is True):
                        status = 'BLACKLIST'
                    else:
                        status = 'WHITELIST'
                    newAccess = Access(
                            res_id=post_data.get('user_id'), 
                            plate_number=post_data.get('plate_number'),
                            lp_status=status)
                    db.session.add(newAccess)
                    db.session.commit()
                    response_object = 'SUCCESS'
            else: #NOT FOUND IN LICENSE_PLATE_T
                findVisitor = Visitor.query.filter_by(v_contactno='+601'+post_data.get('v_contactno')).first() #CHECK IF GOT EXISTING VISITOR RECORD
                if (findVisitor is not None): #GOT EXISTING VISITOR RECORD
                    findVisitor.v_name = post_data.get('v_name') #UPDATE VISITOR RECORD
                    newLP = LicensePlate(
                                plate_number=post_data.get('plate_number'),
                                res_id=None,
                                visitor_id=findVisitor.visitor_id)
                    db.session.add(newLP)
                    db.session.commit()
                    if (post_data.get('blacklist') is True):
                        status = 'BLACKLIST'
                    else:
                        status = 'WHITELIST'
                    newAccess = Access(
                            res_id=post_data.get('user_id'), 
                            plate_number=post_data.get('plate_number'),
                            lp_status=status)
                    db.session.add(newAccess)
                    db.session.commit()
                    response_object = 'SUCCESS'
                else: #NO EXISTING VISITOR RECORD
                    newVisitor = Visitor(v_contactno="+601"+post_data.get('v_contactno'), v_name=post_data.get('v_name'))
                    db.session.add(newVisitor)
                    db.session.commit()
                    locateVisitor = Visitor.query.filter_by(v_contactno="+601"+post_data.get('v_contactno')).first()
                    newLP = LicensePlate(
                                plate_number=post_data.get('plate_number'),
                                res_id=None,
                                visitor_id=locateVisitor.visitor_id)
                    db.session.add(newLP)
                    db.session.commit()
                    if (post_data.get('blacklist') is True):
                        status = 'BLACKLIST'
                    else:
                        status = 'WHITELIST'
                    newAccess = Access(
                            res_id=post_data.get('user_id'), 
                            plate_number=post_data.get('plate_number'),
                            lp_status=status)
                    db.session.add(newAccess)
                    db.session.commit()
                    response_object = 'SUCCESS'
        return jsonify(response_object)

#(RESIDENT & SMO) VIEW OWN PROFILE ****************************
@app.route('/view_own_profile/<user_id>/<resident>', methods=["GET"])
@token_required
def viewOwnProfile(user_id, resident):
    if request.method == 'GET':
        if (resident == 'true'):
            loadProfile = Resident.query.filter_by(res_id=user_id).first()
            #loadLP = LicensePlate.query.filter( (LicensePlate.res_id == loadProfile.res_id) & (LicensePlate.lp_status != None) ).all()
            loadLP = Access.query.filter_by(res_id=loadProfile.res_id).all()
            res_lp = []
            vis_lp = []
            vis_bl_lp = []
            for j in range(len(loadLP)):
                if (loadLP[j].lp_status == 'BLACKLIST'): #IF THE LP IS BLACKLSITED
                    vis_bl_lp.append(loadLP[j].plate_number)
                elif (loadLP[j].lp_status == 'WHITELIST'): #IF THE LP IS WHITELISTED
                    loadIdentity = LicensePlate.query.filter_by(plate_number=loadLP[j].plate_number).first() #CHECK IF PLATE BELONGS TO RES OR VIS
                    if (loadIdentity.res_id is not None): #RESIDENT'S LP
                        res_lp.append(loadLP[j].plate_number)
                    else: #VISITOR'S LP
                        vis_lp.append(loadLP[j].plate_number)
            response_object = {
                'res_id': loadProfile.res_id,
                'r_unitno': loadProfile.r_unitno,
                'r_name': loadProfile.r_name,
                'r_contactno': loadProfile.r_contactno,
                'r_username': loadProfile.r_username,
                'r_secretcode': loadProfile.r_secretcode,
                'r_address': loadProfile.r_address,
                'res_lp': res_lp,
                'vis_lp': vis_lp,
                'vis_bl_lp': vis_bl_lp
            }
        else:
            loadProfile = SMO.query.filter_by(smo_id=user_id).first()
            response_object = {
                's_name': loadProfile.s_name,
                's_username': loadProfile.s_username,
            }
        return jsonify(response_object)

#(SMO) LOAD RESIDENT INFO *******************************
@app.route('/smo/load_resident', methods=["GET"])
@token_required
def loadResident():
    if request.method == 'GET':
        response_object = []

        loadData = Resident.query.order_by(Resident.res_id.asc()).all()
        for i in range(len(loadData)):
            loadLP = Access.query.filter_by(res_id=loadData[i].res_id).all()
            res_lp = []
            vis_lp = []
            vis_bl_lp = []
            for j in range(len(loadLP)):
                if (loadLP[j].lp_status == 'BLACKLIST'): #IF THE LP IS BLACKLSITED
                    vis_bl_lp.append(loadLP[j].plate_number)
                elif (loadLP[j].lp_status == 'WHITELIST'): #IF THE LP IS WHITELISTED
                    loadIdentity = LicensePlate.query.filter_by(plate_number=loadLP[j].plate_number).first() #CHECK IF PLATE BELONGS TO RES OR VIS
                    if (loadIdentity.res_id is not None): #RESIDENT'S LP
                        res_lp.append(loadLP[j].plate_number)
                    else: #VISITOR'S LP
                        vis_lp.append(loadLP[j].plate_number)
            resident = {
                'res_id': loadData[i].res_id,
                'r_unitno': loadData[i].r_unitno,
                'r_name': loadData[i].r_name,
                'r_contactno': loadData[i].r_contactno,
                'r_username': loadData[i].r_username,
                'r_secretcode': loadData[i].r_secretcode,
                'r_address': loadData[i].r_address,
                'res_lp': res_lp,
                'vis_lp': vis_lp,
                'vis_bl_lp': vis_bl_lp
            }
            response_object.append(resident)
        return jsonify(response_object)

#(SMO) LOAD VISIT RECORD *******************************
@app.route('/smo/load_visit', methods=["GET"])
@token_required
def loadVisit():
    if request.method == 'GET':
        response_object = []
        loadData = Visit.query.order_by(Visit.visit_on.desc()).all()
        for i in range(len(loadData)):
            loadRes = Resident.query.filter_by(res_id=loadData[i].res_id).first()
            loadLP = LicensePlate.query.filter_by(plate_number=loadData[i].plate_number).first()
            loadVis = Visitor.query.filter_by(visitor_id=loadLP.visitor_id).first()
            visit = {
                'visit_id': loadData[i].visit_id,
                'plate_number': loadData[i].plate_number,
                'visit_on': str(loadData[i].visit_on),
                'r_name': loadRes.r_name,
                'r_unitno': loadRes.r_unitno,
                'v_name': loadVis.v_name,
                'v_contactno': loadVis.v_contactno,
                'visit_purpose': loadData[i].visit_purpose,
                'visit_status': loadData[i].visit_status
            }
            response_object.append(visit)
        return jsonify(response_object)

#(SMO) LOAD ENTRY EXIT RECORD *******************************
@app.route('/smo/load_ee', methods=["GET"])
@token_required
def loadEE():
    if request.method == 'GET':
        response_object =[]
        loadData = EntryExit.query.order_by(EntryExit.ee_entryon.desc()).all()
        for i in range(len(loadData)):
            loadLP = LicensePlate.query.filter_by(plate_number=loadData[i].plate_number).first()
            if (loadLP.visitor_id is not None):
                loadVis = Visitor.query.filter_by(visitor_id=loadLP.visitor_id).first()
                ee = {
                    'ee_id': loadData[i].ee_id,
                    'plate_number': loadData[i].plate_number,
                    'ee_entryon': str(loadData[i].ee_entryon),
                    'ee_exiton': str(loadData[i].ee_exiton),
                    'name': loadVis.v_name,
                    'contactno': loadVis.v_contactno,
                }
                response_object.append(ee)
            elif (loadLP.res_id is not None):
                loadRes = Resident.query.filter_by(res_id=loadLP.res_id).first()
                ee = {
                    'ee_id': loadData[i].ee_id,
                    'plate_number': loadData[i].plate_number,
                    'ee_entryon': str(loadData[i].ee_entryon),
                    'ee_exiton': str(loadData[i].ee_exiton),
                    'name': loadRes.r_name,
                    'contactno': loadRes.r_contactno,
                }
                response_object.append(ee)
        return jsonify(response_object)

#(SMO) CREATE ACC FOR RESIDENT *******************************
@app.route('/smo/createacc', methods=["POST"])
@token_required
def createAcc():
    if request.method == 'POST':
        post_data = request.get_json()
        findUser = Resident.query.filter_by(r_unitno=post_data.get('unit_number')).first()
        if (findUser is None): #does not find dupicate unit number
            new_username = post_data.get('r_name')[:2].lower() + post_data.get('unit_number') + post_data.get('contact_number')[-4:]
            unique_code = False
            while(unique_code is not True):
                new_secretcode = str(randint(100000, 999999))
                findCode = Resident.query.filter_by(r_secretcode=new_secretcode).first()
                if (findCode is None):
                    unique_code = True
                    break
            hash_password = hashlib.sha256("Temppw123!".encode())
            hd_password = hash_password.hexdigest() #to prevent NULL byte problems
            new_password = str(bcrypt.generate_password_hash(hd_password))
            new_password2 = new_password[:-1]
            new_password3 = new_password2[2:]
            newResident = Resident(r_name=post_data.get('r_name'), 
                                    r_unitno=post_data.get('unit_number'), 
                                    r_address=post_data.get('r_address'),
                                    r_contactno="+601" + post_data.get('contact_number'),
                                    r_username=new_username,
                                    r_password=new_password3,
                                    r_secretcode=new_secretcode,
                                    smo_id=post_data.get('user_id'))
            db.session.add(newResident)
            db.session.commit()
            response_object = "Success"
        else: #got existing unit number (update)
            new_username = post_data.get('r_name')[:2].lower() + post_data.get('unit_number') + post_data.get('contact_number')[-4:]
            unique_code = False
            while(unique_code is not True):
                new_secretcode = str(randint(100000, 999999))
                findCode = Resident.query.filter_by(r_secretcode=new_secretcode).first()
                if (findCode is None):
                    unique_code = True
                    break
            hash_password = hashlib.sha256("Temppw123!".encode())
            hd_password = hash_password.hexdigest() #to prevent NULL byte problems
            new_password = str(bcrypt.generate_password_hash(hd_password))
            new_password2 = new_password[:-1]
            new_password3 = new_password2[2:]
            findUser.r_name = post_data.get('r_name')
            findUser.r_address = post_data.get('r_address')
            findUser.r_contactno = "+601" + post_data.get('contact_number')
            findUser.r_username = new_username
            findUser.r_password = new_password3
            findUser.r_secretcode = new_secretcode
            findUser.smo_id = post_data.get('user_id')
            db.session.commit()
            ### UPDATE ACCESS_LIST_T
            findList = Access.query.filter_by(res_id=findUser.res_id).all()
            for i in range(len(findList)):
                findList[i].lp_status = 'DELETED'
            db.session.commit()
            ### UPDATE VISIT_T
            findVisit = Visit.query.filter_by(res_id=findUser.res_id).all()
            for i in range(len(findVisit)): #DELETE ALL RELATED VISITS
                db.session.delete(findVisit[i])
            db.session.commit()
            response_object = "Updated Record"
        return jsonify(response_object)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) 