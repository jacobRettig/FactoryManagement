# -*- coding: utf-8 -*-
# Primary Author: James Shelley
# Database models go here
import uu
from uu import region
from uu import country
from uu import address
from uu import roletable
from uu import generatinformation
from uu import product
from uu import ConfigAttribute
from uu import productattribution
from uu import Warehouse
from uu import Warehousestorage
from uu import categories
from uu import producttocategories
from uu import permission
from uu import Access
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy import CheckConstraint
from sqlalchemy import exc
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///FactoryManagement.db')
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
        row = session.query(LogInformation).get(email)
        return row.password == password
    except exc.SQLAlchemyError as e:
        print("isValidLogin failed with: ", e)

#NOT WORKING
#checks if email exists (returns True/False)
def emailExists(email):
    try:
        return session.query(LogInformation).filter(LogInformation.email.in_(email)) #emails needs to be in list? 
    except exc.SQLAlchemyError as e:
        print("emailExists failed with: ", e)
        



#GETTERS (attempts to get data from specified table and throws meaningful error on failure)

#gets address specific to user
def getAddressID(email):
    pass

#gets role from email
def getRole(email):
    
    #get the role name by joining the LogInformation and Role tables and filtering by email, hopefully won't return more than one row
    try:
        row = session.query(Role).join(LogInformation, Role.roleName==LogInformation.roleName).filter(LogInformation.email == email).one()
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


#returns complete list of accessType
def getAccessTypes():
    pass

#returns description of specified accessType and returns None on NULL description but throws error on failure
def getAccessDescription(accessType):
    pass

#returns access level for specified role and access type
def getAccessLevel(roleName, accessType):
    pass

#gets a list containing all the countries in the DB
def getCountries():
    pass

#if returns list of named tuples belonging to specified user
def getProducts(email):
    pass

#returns list of named tuples belonging to specified user (ignoring default)
def getCategories(email):
    pass

#if email is none just returns default categories but if email is given it also includes non-default
#categories specific to that user
def getCategoriesGlobal(email=None):
    pass

#tries to return warehouse associated with user
def getWarehouse(email):
    pass

#if returns list of named tuples belonging to specified user
def getConfigAttributes(email):
    pass

#if returns list of named tuples belonging to specified user and product
def getProductAttribute(email, productName):
    pass




#CREATION SETTERS (attempts to populate specified table and returns True on success, False on failure)
def createRegion(regionName, regionDescription):
    pass

def createCountry(country, internationalCallPrefix):
    pass

def createRole(roleName, roleDescription):
    pass

def createProduct(productName, price, imageData, quantity, productOwner, description):
    pass

def createConfigAttribute(name, attributeOwner, description, unit):
    pass

def createProductAttribute(name, productName, productOwner, value):
    pass

def createWarehouse(warehouseOwner, description, capacity, addressID):
    pass

def createWarehouseStorage(refillDate, price, productName, productOwner):
    pass

#isDefault will be a bool
def createCategory(categoryName, isDefault, categoryDescription, categoryOwner):
    pass

def createProductCategory(categoryName, productName, productOwner):
    pass

def createPermission(accessType, accessDescription):
    pass

#accessLevel will be one of ('read', 'write', 'both', 'none')
def createAccess(roleName, accessType, accessLevel):
    pass



#MODIFICATION SETTERS (attempts to modify specified table and tuple and returns True on success, False on failure)
#uses primary key as identifier (cannot directly modify)

def modifyRegion(regionName, regionDescription):
    pass

def modifyCountry(country, internationalCallPrefix):
    pass

def modifyRole(roleName, roleDescription):
    pass

def modifyProduct(productName, price, imageData, quantity, productOwner, description):
    pass

def modifyConfigAttribute(name, attributeOwner, description, unit):
    pass

def modifyProductAttribute(name, productName, productOwner, value):
    pass

def modifyWarehouse(warehouseOwner, description, capacity, addressID):
    pass

def modifyWarehouseStorage(refillDate, price, productName, productOwner):
    pass

#isDefault will be a bool
def modifyCategory(categoryName, isDefault, categoryDescription, categoryOwner):
    pass

def modifyProductCategory(categoryName, productName, productOwner):
    pass

def modifyPermission(accessType, accessDescription):
    pass

#accessLevel will be one of ('read', 'write', 'both', 'none')
def modifyAccess(roleName, accessType, accessLevel):
    pass




#DELETERS

def deleteRegion(regionName):
    pass

def deleteCountry(country):
    pass

def deleteRole(roleName):
    pass

def deleteProduct(productName):
    pass

def deleteConfigAttribute(name, attributeOwner):
    pass

def deleteProductAttribute(name, productName, productOwner):
    pass

def deleteWarehouse(warehouseID):
    pass

def deleteWarehouseStorage(warehouseID, productName, productOwner):
    pass

def deleteCategory(categoryName, categoryOwner):
    pass

def deleteProductCategory(categoryName, productName, productOwner):
    pass

def deletePermission(accessType):
    pass

def deleteAccess(roleName):
    pass




#creates a new user if possible and returns True on success, False on failure
#if no second line of address then it will be None
def createUser(role, email, password, firstName, lastName, phoneNumber, birthdate, country, region, addressFirstLine, addressSecondLine):
    
    #create address row
    address = Address(addressLineFirst=addressFirstLine, addressLineSecond=addressSecondLine, country=country, regionName=region)
    session.add(address)

    #create user row, not sure if using address variable will work for address_id
    user = LogInformation(birthdate=birthdate, password=password, phoneNumber=phoneNumber, email=email, firstName=firstName, lastName=lastName, addressID=address)
    session.add(user)

    #try to commit changes to database, if it fails return False - might need to do more with exception
    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createUser failed with: ", e)
        return False




def defaultdata():
    regiontable = region()
    countrytable = country()
    addresstable = address()
    roletable1 = roletable()
    generatinformationtable = generatinformation()
    producttable = product()
    ConfigAttributetable = ConfigAttribute()
    productattributiontable = productattribution()
    Warehousetable = Warehouse()
    WarehouseStoragetable = WarehouseStorage()
    categoriestable = categories()
    producttocategoriestable = producttocategories()
    permissiontable = permission()
    Accesstable = Access()
    for i in range(len(generatinformationtable)):
        createUser(generatinformationtable[i][6], generatinformationtable[i][3], generatinformationtable[i][1],
                   generatinformationtable[i][4], generatinformationtable[i][5]
                   , generatinformationtable[i][2], generatinformationtable[i][0], generatinformationtable[i][3],
                   addresstable[i][4], addresstable[i][1], addresstable[i][2])
    for i in range(len(Accesstable)):
        createAccess(Accesstable[i][0], Accesstable[i][1], Accesstable[i][2])
    for i in range(len(categoriestable)):
        createCategory(categoriestable[i][0], categoriestable[i][1], categoriestable[i][2], categoriestable[i][3])
    for i in range(len(ConfigAttributetable)):
        createConfigAttribute(ConfigAttributetable[i][0], ConfigAttributetable[i][3], ConfigAttributetable[i][1],
                              ConfigAttributetable[i][2])
    for i in range(len(countrytable)):
        createCountry(countrytable[i][0], countrytable[i][1])
    for i in range(len(permissiontable)):
        createPermission(permissiontable[i][0], permissiontable[i][1])
    for i in range(len(roletable1)):
        createRole(roletable1[i][0], roletable1[i][1])
    for i in range(len(productattributiontable)):
        createRegion(productattributiontable[i][0], productattributiontable[i][1], productattributiontable[i][2],
                     productattributiontable[i][3])
    for i in range(len(Warehousetable)):
        createWarehouse(Warehousetable[i][0], Warehousetable[i][1], Warehousetable[i][2], Warehousetable[i][3])
    for i in range(len(WarehouseStoragetable)):
        createWarehouseStorage(WarehouseStoragetable[1][0], WarehouseStoragetable[1][1], WarehouseStoragetable[1][2],
                               WarehouseStoragetable[1][3])
    for i in range(len(producttocategoriestable)):
        createProductCategory(producttocategoriestable[i][0], producttocategoriestable[i][1],
                              producttocategoriestable[i][2])
    for i in range(len(producttable)):
        createProduct(producttable[i][0], producttable[i][1], producttable[i][3], producttable[i][4],
                      producttable[i][5], producttable[i][2])
    for i in range(len(regiontable)):
        createRegion(regiontable[i][0], regiontable[i][1])


# run just the database in command line mode to create content directly
if __name__ == '__main__':
    defaultdata()
