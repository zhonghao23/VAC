'''
Programmer Name:    CHIAM ZHONG HAO
Program Name:       models.py
Description:        Database models are set in this file
First Written On:   31/12/2020
Edited On:          15/02/2021
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
db = SQLAlchemy()

class SMO(db.Model):
    __tablename__ = 'SMO_T'
    smo_id = db.Column('SMO_ID', db.Integer, primary_key=True)
    s_name = db.Column('S_Name', db.String, nullable=False)
    s_username = db.Column('S_Username', db.String, nullable=False)
    s_password = db.Column('S_Password', db.String, nullable=False)
    #relationship
    residents = db.relationship('Resident', backref='smo', lazy=True)

    def __init__(self, s_name, s_username, s_password):
        self.s_name = s_name
        self.s_username = s_username
        self.s_password = s_password  

class Resident(db.Model):
    __tablename__ = 'RESIDENT_T'
    res_id = db.Column('Res_ID', db.Integer, primary_key=True)
    r_name = db.Column('R_Name', db.String, nullable=False)
    r_unitno = db.Column('R_UnitNo', db.String, nullable=False)
    r_address = db.Column('R_Address', db.String, nullable=False)
    r_contactno = db.Column('R_ContactNo', db.String, nullable=False)
    r_username = db.Column('R_Username', db.String, nullable=False)
    r_password = db.Column('R_Password', db.String, nullable=False)
    r_secretcode = db.Column('R_SecretCode', db.String, nullable=False)
    smo_id = db.Column(db.Integer, ForeignKey('SMO_T.SMO_ID'), nullable=False)
    #relationship
    license_plates = db.relationship('LicensePlate', backref='resident', lazy=True)    
    visits = db.relationship('Visit', backref='resident', lazy=True)
    accesses = db.relationship('Access', backref='resident', lazy=True)
    
    def __init__(self, r_name, r_unitno, r_address, r_contactno, r_username, r_password, r_secretcode, smo_id):
        self.r_name = r_name
        self.r_unitno = r_unitno
        self.r_address = r_address
        self.r_contactno = r_contactno
        self.r_username = r_username
        self.r_password = r_password
        self.r_secretcode = r_secretcode
        self.smo_id = smo_id

class Visitor(db.Model):
    __tablename__ = 'VISITOR_T'
    visitor_id = db.Column('Visitor_ID', db.Integer, primary_key=True) #, autoincrement=True
    v_contactno = db.Column('V_ContactNo', db.String, nullable=False, unique=True) 
    v_name = db.Column('V_Name', db.String, nullable=False)
    #relationship
    license_plates = db.relationship('LicensePlate', backref='visitor', lazy=True)

    def __init__(self, v_contactno, v_name):
        # self.visitor_id = visitor_id
        self.v_contactno = v_contactno
        self.v_name = v_name

class LicensePlate(db.Model):
    __tablename__ = 'LICENSE_PLATE_T'
    plate_number = db.Column('Plate_Number', db.String, primary_key=True)
    res_id = db.Column(db.Integer, ForeignKey('RESIDENT_T.Res_ID'), nullable=True)
    visitor_id = db.Column(db.Integer, ForeignKey('VISITOR_T.Visitor_ID'), nullable=True)
    #relationship
    visits = db.relationship('Visit', backref='licenseplate', lazy=True)
    accesses = db.relationship('Access', backref='licenseplate', lazy=True)
    entryexits = db.relationship('EntryExit', backref='licenseplate', lazy=True)    

    def __init__(self, plate_number, res_id, visitor_id):
        self.plate_number = plate_number
        self.res_id = res_id
        self.visitor_id = visitor_id

class Visit(db.Model):
    __tablename__ = 'VISIT_T'
    visit_id = db.Column('Visit_ID', db.Integer, primary_key=True)
    res_id = db.Column(db.Integer, ForeignKey('RESIDENT_T.Res_ID'), nullable=False)
    plate_number = db.Column(db.String, ForeignKey('LICENSE_PLATE_T.Plate_Number'), nullable=False)
    visit_on = db.Column('Visit_On', db.Date, nullable=False)
    visit_purpose = db.Column('Visit_Purpose', db.String, nullable=False)
    visit_status = db.Column('Visit_Status', db.String, nullable=False)

    def __init__(self, res_id, plate_number, visit_on, visit_purpose, visit_status):
        self.res_id = res_id
        self.plate_number = plate_number
        self.visit_on = visit_on
        self.visit_purpose = visit_purpose
        self.visit_status = visit_status

class Access(db.Model):
    __tablename__ = 'ACCESS_LIST_T'
    list_id = db.Column('List_ID', db.Integer, primary_key=True)
    res_id = db.Column(db.Integer, ForeignKey('RESIDENT_T.Res_ID'), nullable=False)
    plate_number = db.Column(db.String, ForeignKey('LICENSE_PLATE_T.Plate_Number'), nullable=False)
    lp_status = db.Column('LP_Status', db.String, nullable=False)

    def __init__(self, res_id, plate_number, lp_status):
        self.res_id = res_id
        self.plate_number = plate_number
        self.lp_status = lp_status

class EntryExit(db.Model):
    __tablename__ = 'ENTRYEXIT_T'
    ee_id = db.Column('EE_ID', db.Integer, primary_key=True)
    plate_number = db.Column(db.String, ForeignKey('LICENSE_PLATE_T.Plate_Number'), nullable=False)
    ee_entryon = db.Column('EE_EntryOn', db.DateTime, nullable=False)
    ee_exiton = db.Column('EE_ExitOn', db.DateTime, nullable=True)

    def __init__(self, plate_number, ee_entryon, ee_exiton):
        self.plate_number = plate_number
        self.ee_entryon = ee_entryon
        self.ee_exiton == ee_exiton