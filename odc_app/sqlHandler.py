# -*- coding: utf-8 -*-
# Primary Author: James Shelley
# Database models go here

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy import CheckConstraint
from sqlalchemy import exc
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:////absolute/path/to/foo.db')
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

#Classes to create tables, based off the schema

class Region(Base):
	__tablename__ = 'Region'
	regionName = Column('regionName', String(30), primary_key=True)
	regionDescription = Column('regionDescription', String(50))

class Country(Base):
	__tablename__ = 'Country'
	country = Column('country', String(50), primary_key=True)
	internationalCallPrefix = Column('internationalCallPrefix', String(5)) #NOT NULL CHECK (internationalCallPrefix NOT LIKE “%[^0-9]%”),

class Address(Base):
	__tablename__ = 'Address'
	addressID = Column('addressID', Integer, primary_key=True) #autoincr automatic? 
	addressLineFirst = Column('addressLineFirst', String(50), nullable=False)
	addressLineSecond = Column('adressLineSecond', String(50))
	country = Column('country', String(50), ForeignKey("Country.country"), nullable=False)
	regionName = Column('regionName', String(30), ForeignKey("Region.regionName"), nullable=False)

class Role(Base):
	__tablename__ = 'Role'
	roleName = Column('roleName', String(20), primary_key=True)
	roleDescription = Column('roleDescription', String(300))

class LogInformation(Base):
	__tablename__ = 'LogInformation'
	birthdate = Column('birthdate', Date, nullable=False)
	password = Column('password', String(16), nullable=False)
	phoneNumber = Column('phoneNumber', String(10), nullable=False) 
	email = Column('email', String(50), primary_key=True)
	firstName = Column('firstName', String(75), nullable=False)
	lastName = Column('lastName', String(75), nullable=False) 
	addressID = Column('addressID', Integer, ForeignKey("Address.addressID"), nullable=False)
	roleName = Column('roleName', String(20), ForeignKey("Role.roleName"), nullable=False)	

class Product(Base):
	__tablename__ = 'Products'
	productName = Column('productName', String(30), primary_key=True)
	price = Column('price', Numeric, nullable=False)
	description = Column('description', String(100))
	imageData = Column('imageData', String(300), nullable=False)
	quantity = Column('quantity', Integer, nullable=False)
	productOwner = Column('productOwner', String(50), ForeignKey("LogInformation.email"), primary_key=True)	

class ConfigAttribute(Base):
	__tablename__ = 'ConfigAttribute'
	name = Column('name', String(20), primary_key=True)
	description = Column('description', String(100))
	unit = Column('unit', String(10))
	attributeOwner = Column('attributeOwner', String(50), ForeignKey("LogInformation.email"), primary_key=True)

class ProductAttribute(Base):
	__tablename__ = 'ProductAttribute'
	name = Column('name', String(20), ForeignKey("ConfigAttribute.name"), primary_key=True)
	productName = Column('productName', String(30), ForeignKey("Product.productName"), primary_key=True)
	productOwner = Column('productOwner', String(50), ForeignKey("Product.productOwner"), primary_key=True)
	value = Column('value', Numeric, nullable=False)

class Warehouse(Base):
	__tablename__ = 'Warehouse'
	warehouseID = Column('warehouseID', Integer, primary_key=True)
	warehouseOwner = Column('warehouseOwner', String(50), ForeignKey("LogInformation.email"), nullable=False)
	description = Column('description', String(100))
	capacity = Column('capacity', Integer)
	addressID = Column('addressID', Integer, ForeignKey("Address.addressID"), nullable=False)

class WarehouseStorage(Base):
	__tablename__ = 'WarehouseStorage'
	warehouseID = Column('warehouseID', Integer, ForeignKey("Warehouse.warehouseID"), primary_key=True)
	refillDate = Column('refillDate', Date)
	#state = Column('state', String(30))
	price = Column('price', Numeric(20), nullable=False)
	productName = Column('productName', String(30), ForeignKey("Product.productName"), primary_key=True)
	productOwner = Column('productOwner', String(50), ForeignKey("Product.productOwner"), primary_key=True)

class Category(Base):
	__tablename__ = 'Category'
	categoryName = Column('categoryName', String(30), primary_key=True)
	isDefault = Column('isDefault', String(1), nullable=False)
	categoryDescription = Column('categoryDescription', String(100))
	categoryOwner = Column('categoryOwner', String(30), ForeignKey("LogInformation.email"), primary_key=True)

class ProductCategory(Base):
	__tablename__ = 'ProductCategory'
	categoryName = Column('categoryName', String(30), ForeignKey("Category.categoryName"), primary_key=True)
	productName = Column('productName', String(30), ForeignKey("Product.productName"), primary_key=True)
	productOwner = Column('productOwner', String(50), ForeignKey("Product.productOwner"), primary_key=True)

class Permission(Base):
	__tablename__ = 'Permission'
	accessType = Column('accessType', String(20), primary_key=True)
	accessDescription = Column('accessDescription', String(150))

class Access(Base):
	__tablename__ = 'Access'
	roleName = Column('roleName', String(20), ForeignKey("Role.roleName"), primary_key=True)
	accessType = Column('accessType', String(20), ForeignKey("Permission.accessType"), primary_key=True)
	accessLevel = Column('accessLevel', String(1))


#checks if email/password combination is valid (returns True/False)
def isValidLogin(email, password):

	try:
		row = session.query(LogInformation).get(self.email)
		return row.password == self.password
	except exc.SQLAlchemyError as e:
		print("isValidLogin failed with: ", e)


#checks if email exists (returns True/False)
def emailExists(email):
	try:
		return session.query(LogInformation).filter(LogInformation.email.in_(self.email)) #emails needs to be in list?
	except exc.SQLAlchemyError as e:
		print("emailExists failed with: ", e)
		
#creates a new user if possible and returns True on success, False on failure
#if no second line of address then it will be None
def createUser(role, email, password, firstName, lastName, phoneNumber, birthdate, country, region, addressFirstLine, addressSecondLine):
	
	#create address row
	address = Address(addressLineFirst=addressFirstLine, addressLineSecond=addressSecondLine, country=self.country, regionName=region)
	session.add(address)

	#create user row, not sure if using address variable will work for address_id
	user = LogInformation(birthdate=self.birthdate, password=self.password, phoneNumber=self.phoneNumber, email=self.email, firstName=self.firstName, lastName=self.lastName, addressID=address)
	session.add(user)

	#try to commit changes to database, if it fails return False - might need to do more with exception
	try:
		session.commit()
		return True
	except exc.SQLAlchemyError as e:
		print("createUser failed with: ", e)
		return False

#gets role from email
def getRole(email):
	
	#get the role name by joining the LogInformation and Role tables and filtering by email, hopefully won't return more than one row
	try:
		row = session.query(Role).join(LogInformation, Role.roleName==LogInformation.roleName).filter(LogInformation.email == self.email).one()
		return row.roleName
	except exc.SQLAlchemyError as e:
		print("getRole failed with: ", e)

#gets a list containing all the regions in the DB
def getRegions():
	
	try:
		rows = session.query(Region).all()
		return rows.regionName #will this return a list?
	except exc.SQLAlchemyError as e:
		print("getRegions failed with: ", e)

#gets a list of products for the specified warehouse owner
def getWarehouseProducts(warehouseManager):

	try:
		rows = session.query(WarehouseStorage).join(Warehouse, WarehouseStorage.warehouseID==Warehouse.warehouseID).filter(Warehouse.warehouseOwner == warehouseManager).all()
		return rows.productName
	except exc.SQLAlchemyError as e:
		print("getWarehouseProducts failed with", e)






