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

engine = create_engine('sqlite:///FactoryManagement.db', echo=True)
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

#Classes to create tables, based off the schema

class Region(Base):
    __tablename__ = 'Region'
    regionName = Column('regionName', String(30), primary_key=True)
    regionDescription = Column('regionDescription', String(50))
Base.metadata.create_all(engine)

class Country(Base):
    __tablename__ = 'Country'
    country = Column('country', String(50), primary_key=True)
    internationalCallPrefix = Column('internationalCallPrefix', String(5)) 

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
    imageData = Column('imageData', String(300), nullable=False)
    quantity = Column('quantity', Integer, nullable=False)
    productOwner = Column('productOwner', String(50), ForeignKey("LogInformation.email"), primary_key=True) 
    description = Column('description', String(100))  

class ConfigAttribute(Base):
    __tablename__ = 'ConfigAttribute'
    name = Column('name', String(20), primary_key=True)
    attributeOwner = Column('attributeOwner', String(50), ForeignKey("LogInformation.email"), primary_key=True)
    description = Column('description', String(100))
    unit = Column('unit', String(10))
    

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
def isValidLogin(emailp, passwordp):

    try:
        row = session.query(LogInformation).get(emailp)
        return row.password == passwordp
    except exc.SQLAlchemyError as e:
        print("isValidLogin failed with: ", e)

#checks if email exists (returns True/False)
def emailExists(emailp):
    try:
        row = session.query(LogInformation).filter(LogInformation.email==emailp).one() 
        return True 
    except exc.SQLAlchemyError as e:
        print("emailExists failed with: ", e)
        return False



#GETTERS (attempts to get data from specified table and throws meaningful error on failure)

#gets address specific to user
def getAddressID(emailp):
    try:
        row = session.query(LogInformation).get(emailp)
        return row.addressID
    except exc.SQLAlchemyError as e:
        print("getAddressID failed with: ", e)

#gets role from email
def getRole(emailp):
    
    #get the role name by joining the LogInformation and Role tables and filtering by email, hopefully won't return more than one row
    try:
        row = session.query(Role).join(LogInformation, Role.roleName==LogInformation.roleName).filter(LogInformation.email == emailp).one()
        return row.roleName
    except exc.SQLAlchemyError as e:
        print("getRole failed with: ", e)

#gets a list containing all the regions in the DB
def getRegions():
    
    try:
        rows = session.query(Region).all()
        return rows.regionName 
    except exc.SQLAlchemyError as e:
        print("getRegions failed with: ", e)

#gets a list of products for the specified warehouse owner
def getWarehouseProducts(warehouseManagerp):

    try:
        rows = session.query(WarehouseStorage).join(Warehouse, WarehouseStorage.warehouseID==Warehouse.warehouseID).filter(Warehouse.warehouseOwner == warehouseManagerp).all()
        return rows.productName
    except exc.SQLAlchemyError as e:
        print("getWarehouseProducts failed with", e)


#returns complete list of accessType returns ('read', 'write', 'both', 'none')
def getAccessTypes():
    try:
        rows = session.query(Access).all()
        return rows.accessType
    except exc.SQLAlchemyError as e:
        print("getAccessTypes failed with: ", e)

#returns description of specified accessType and returns None on NULL description but throws error on failure
def getAccessDescription(accessTypep):
    try:
        row = session.query(Access).get(accessTypep)
        return row.accessDescription
    except exc.SQLAlchemyError as e:
        print("getAccessDescription failed with: ", e)


#returns access level for specified role and access type
def getAccessLevel(roleNamep, accessTypep):
    try:
        row = session.query(Access).filter(Access.roleName==roleNamep).filter(Access.accessType==accessTypep).all() 
        return row.accessLevel
    except exc.SQLAlchemyError as e:
        print("getAccessLevel failed with: ", e)

#gets a list containing all the countries in the DB
def getCountries():
    try:
        rows = session.query(Address).all()
        return rows.country
    except exc.SQLAlchemyError as e:
        print("getCountries failed with: ", e)


#returns list of named tuples belonging to specified user
def getProducts(emailp):
    try:
        return session.query(Products).filter(Products.productOwner==emailp).all()
    except exc.SQLAlchemyError as e:
        print("getProducts failed with: ", e)


#returns list of named tuples belonging to specified user (ignoring default)
def getCategories(emailp):
    try:
        return session.query(Category).filter(Category.categoryOwner==emailp).all()
    except exc.SQLAlchemyError as e:
        print("getCategories failed with: ", e)

#if email is none just returns default categories but if email is given it also includes non-default
#categories specific to that user
def getCategoriesGlobal(emailp=None):
    
    if(emailp==None):
        try:
            return session.query(Category).filter(Category.isDefault=='1').all()
        except exc.SQLAlchemyError as e:
            print("getCategoriesGlobal failed with: ", e)
    else:
        try:
            return session.query(Category).filter(or_(Category.isDefault=='1', Category.categoryOwner==emailp)).all()
        except exc.SQLAlchemyError as e:
            print("getCategoriesGlobal failed with: ", e)

    
#tries to return warehouse associated with user
def getWarehouse(emailp):
    try:
        return session.query(Warehouse).filter(Warehouse.warehouseOwner==emailp).all()
    except exc.SQLAlchemyError as e:
        print("getWarehouse failed with: ", e)

#returns list of named tuples belonging to specified user
def getConfigAttributes(emailp):
    try:
        return session.query(ConfigAttribute).filter(ConfigAttribute.attributeOwner==emailp).all()
    except exc.SQLAlchemyError as e:
        print("getConfigAttributes failed with: ", e)

#returns list of named tuples belonging to specified user and product
def getProductAttribute(emailp, productNamep):
    try:
        return session.query(ProductAttribute).filter(ProductAttribute.productName==productNamep).filter(ProductAttribute.productOwner==emailp).all() 
    except exc.SQLAlchemyError as e:
        print("getProductAttribute failed with: ", e)



#CREATION SETTERS (attempts to populate specified table and returns True on success, False on failure)

#if no second line of address then it will be None
def createUser(role, emailp, passwordp, firstNamep, lastNamep, phoneNumberp, birthdatep, countryp, region, addressFirstLine, addressSecondLine):
    print('role:{}, email:{}, password:{}, firstName:{}, lastName:{}, phoneNumber:{}, birthdate:{}, country:{}, region:{}, addressFirstLine:{}, addressSecondLine:{}'.format(role, emailp, passwordp, firstNamep, lastNamep, phoneNumberp, birthdatep, countryp, region, addressFirstLine, addressSecondLine))
    #create address row
    address = Address(addressLineFirst=addressFirstLine, addressLineSecond=addressSecondLine, country=countryp, regionName=region)
    session.add(address)

    #create user row, not sure if using address variable will work for address_id
    user = LogInformation(birthdate=birthdatep, password=passwordp, phoneNumber=phoneNumberp, email=emailp, firstName=firstNamep, lastName=lastNamep, addressID=address, roleName=role)
    session.add(user)

    #try to commit changes to database, if it fails return False - might need to do more with exception
    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createUser failed with: ", e)
        return False

def createRegion(regionNamep, regionDescriptionp):
    row = Region(regionNamep, regionDescriptionp)
    session.add(row)

    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createRegion failed with: ", e)
        return False

def createCountry(countryp, internationalCallPrefixp):
    row = Country(countryp, internationalCallPrefixp)
    session.add(row)

    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createCountry failed with: ", e)
        return False

def createRole(roleNamep, roleDescriptionp):
    row = Role(roleNamep, roleDescriptionp)
    session.add(row)

    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createRole failed with: ", e)
        return False


def createProduct(productNamep, pricep, imageDatap, quantityp, productOwnerp, descriptionp):
    row = Product(productNamep, pricep, imageDatap, quantityp, productOwnerp, descriptionp)
    session.add(row)

    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createProduct failed with: ", e)
        return False

def createConfigAttribute(namep, attributeOwnerp, descriptionp, unitp):
    row = ConfigAttribute(namep, attributeOwnerp, descriptionp, unitp)
    session.add(row)

    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createConfigAttribute failed with: ", e)
        return False
    
def createProductAttribute(namep, productNamep, productOwnerp, valuep):
    row = ProductAttribute(namep, productNamep, productOwnerp, valuep)
    session.add(row)

    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createProductAttribute failed with: ", e)
        return False

def createWarehouse(warehouseOwnerp, descriptionp, capacityp, addressIDp):
    #not sure if this will auto incr primary key
    row = Warehouse(warehouseOwner=warehouseOwnerp, description=descriptionp, capacity=capacityp, addressID=addressIDp) 
    session.add(row)

    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createWarehouse failed with: ", e)
        return False

def createWarehouseStorage(refillDatep, pricep, productNamep, productOwnerp):
    #not sure if this will auto incr primary key
    row = WarehouseStorage(refillDate=refillDatep, price=pricep, productName=productNamep, productOwner=productOwnerp) 
    session.add(row)

    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createWarehouseStorage failed with: ", e)
        return False

#isDefault will be a bool
def createCategory(categoryNamep, isDefaultp, categoryDescriptionp, categoryOwnerp):
    if(isDefaultp):
        isDefaultp = '1'
    else:
        isDefaultp = '0'
    row = Category(categoryNamep, isDefaultp, categoryDescriptionp, categoryOwnerp) 
    session.add(row)

    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createCategory failed with: ", e)
        return False

def createProductCategory(categoryNamep, productNamep, productOwnerp):
    row = ProductCategory(categoryNamep, productNamep, productOwnerp) 
    session.add(row)

    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createProductCategory failed with: ", e)
        return False

def createPermission(accessTypep, accessDescriptionp):
    row = Permission(accessTypep, accessDescriptionp) 
    session.add(row)

    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createPermission failed with: ", e)
        return False

#accessLevel will be one of ('read', 'write', 'both', 'none')
def createAccess(roleNamep, accessTypep, accessLevelp):
    row = Access(roleNamep, accessTypep, accessLevelp) 
    session.add(row)

    try:
        session.commit()
        return True
    except exc.SQLAlchemyError as e:
        print("createAccess failed with: ", e)
        return False



#MODIFICATION SETTERS (attempts to modify specified table and tuple and returns True on success, False on failure)
#uses primary key as identifier (cannot directly modify)

def modifyRegion(regionNamep, regionDescriptionp):
    try:
        row = session.query(Region).get(regionNamep)
        row.regionDescription = regionDescriptionp
        session.commit() 
    except exc.SQLAlchemyError as e:
        print("modifyRegion failed with: ", e)

def modifyCountry(countryp, internationalCallPrefixp):
    try:
        row = session.query(Country).get(countryp)
        row.internationalCallPrefix = internationalCallPrefixp
        session.commit() 
    except exc.SQLAlchemyError as e:
        print("modifyCountry failed with: ", e)

def modifyRole(roleNamep, roleDescriptionp):
    try:
        row = session.query(Role).get(roleNamep)
        row.rowDescription = roleDescriptionp
        session.commit() 
    except exc.SQLAlchemyError as e:
        print("modifyRole failed with: ", e)


def modifyProduct(productNamep, pricep, imageDatap, quantityp, productOwnerp, descriptionp):
    try:
        row = session.query(Product).filter(productName=productNamep).filter(productOwner=productOwnerp).one()
        row.price = pricep
        row.imageData = imageDatap
        row.quantity = quantityp
        row.description = descriptionp
        session.commit() 
    except exc.SQLAlchemyError as e:
        print("modifyProduct failed with: ", e)

def modifyConfigAttribute(namep, attributeOwnerp, descriptionp, unitp):
    try:
        row = session.query(ConfigAttribute).filter(name=namep).filter(attributeOwner=attributeOwnerp).one()
        row.description = descriptionp
        row.unit = unitp
        session.commit() 
    except exc.SQLAlchemyError as e:
        print("modifyConfigAttribute failed with: ", e)


def modifyProductAttribute(namep, productNamep, productOwnerp, valuep):
    try:
        row = session.query(ProductAttribute).filter(name=namep).filter(productName=productNamep).filter(productOwner=productOwnerp).one()
        row.value = valuep
        session.commit() 
    except exc.SQLAlchemyError as e:
        print("modifyProductAttribute failed with: ", e)

def modifyWarehouse(warehouseIDp, warehouseOwnerp, descriptionp, capacityp, addressIDp):
    try:
        row = session.query(Warehouse).get(warehouseIDp)
        row.warehouseOwner = warehouseOwnerp
        row.description = descriptionp
        row.capacity = capacityp
        addressID = addressIDp
        session.commit() 
    except exc.SQLAlchemyError as e:
        print("modifyWarehouse failed with: ", e)

def modifyWarehouseStorage(warehouseIDp, refillDatep, pricep, productNamep, productOwnerp):
    try:
        row = session.query(WarehouseStorage).filter(warehouseID=warehouseIDp).filter(productName=productNamep).filter(productOwner=productOwnerp).one()
        row.refillDate = refillDatep
        row.price = pricep
        session.commit() 
    except exc.SQLAlchemyError as e:
        print("modifyWarehouseStorage failed with: ", e)

#isDefault will be a bool
def modifyCategory(categoryNamep, isDefaultp, categoryDescriptionp, categoryOwnerp):
    try:
        row = session.query(Category).filter(categoryName=categoryNamep).filter(categoryOwner=categoryOwnerp).one()
        if(isDefaultp):
            row.isDefault = '1'
        else:
            row.isDefault = '0'
        row.categoryDescription = categoryDescriptionp
        session.commit() 
    except exc.SQLAlchemyError as e:
        print("modifyCategory failed with: ", e)

#all primary keys so don't need this function?
#def modifyProductCategory(categoryName, productName, productOwner):
    
def modifyPermission(accessTypep, accessDescriptionp):
    try:
        row = session.query(Permission).get(accessTypep)
        row.accessDescription = accessDescriptionp
        session.commit() 
    except exc.SQLAlchemyError as e:
        print("modifyPermission failed with: ", e)

#accessLevel will be one of ('read', 'write', 'both', 'none')
def modifyAccess(roleNamep, accessTypep, accessLevelp):
    try:
        row = session.query(Access).filter(roleName=roleNamep).filter(accessType=accessTypep).one()
        row.accessLevel = accessLevelp
        session.commit() 
    except exc.SQLAlchemyError as e:
        print("modifyAccess failed with: ", e)




#DELETERS

def deleteRegion(regionNamep):
    try:
        row = session.query(Region).get(regionNamep)
        session.delete(row)
        session.commit()
    except exc.SQLAlchemyError as e:
        print("deleteRegion failed with: ", e)

def deleteCountry(countryp):
    try:
        row = session.query(Country).get(countryp)
        session.delete(row)
        session.commit()
    except exc.SQLAlchemyError as e:
        print("deleteCountry failed with: ", e)

def deleteRole(roleNamep):
    try:
        row = session.query(Role).get(roleNamep)
        session.delete(row)
        session.commit()
    except exc.SQLAlchemyError as e:
        print("deleteRole failed with: ", e)

def deleteProduct(productNamep, emailp):
    try:
        row = session.query(Product).filter(productName=productNamep).filter(productOwner=productOwnerp).one()
        session.delete(row)
        session.commit()
    except exc.SQLAlchemyError as e:
        print("deleteProduct failed with: ", e)

def deleteConfigAttribute(namep, attributeOwnerp):
    try:
        row = session.query(ConfigAttribute).filter(name=namep).filter(attributeOwner=attributeOwnerp).one()
        session.delete(row)
        session.commit()
    except exc.SQLAlchemyError as e:
        print("deleteConfigAttribute failed with: ", e)

def deleteProductAttribute(namep, productNamep, productOwnerp):
    try:
        row = session.query(ProductAttribute).filter(name=namep).filter(productName=productNamep).filter(productOwner=productOwnerp).one()
        session.delete(row)
        session.commit()
    except exc.SQLAlchemyError as e:
        print("deleteProductAttribute failed with: ", e)

def deleteWarehouse(warehouseIDp):
    try:
        row = session.query(Warehouse).get(warehouseIDp)
        session.delete(row)
        session.commit()
    except exc.SQLAlchemyError as e:
        print("deleteWarehouse failed with: ", e)

def deleteWarehouseStorage(warehouseIDp, productNamep, productOwnerp):
    try:
        row = session.query(WarehouseStorage).filter(warehouseID=warehouseIDp).filter(productName=productNamep).filter(productOwner=productOwnerp).one()
        session.delete(row)
        session.commit()
    except exc.SQLAlchemyError as e:
        print("deleteWarehouseStorage failed with: ", e)

def deleteCategory(categoryNamep, categoryOwnerp):
    try:
        row = session.query(Category).filter(categoryName=categoryNamep).filter(categoryOwner=categoryOwnerp).one()
        session.delete(row)
        session.commit()
    except exc.SQLAlchemyError as e:
        print("deleteCategory failed with: ", e)

def deleteProductCategory(categoryNamep, productNamep, productOwnerp):
    try:
        row = session.query(ProductCategory).filter(categoryName=categoryNamep).filter(productName=productNamep).filter(productOwner=productOwnerp).one()
        session.delete(row)
        session.commit()
    except exc.SQLAlchemyError as e:
        print("deleteProductCategory failed with: ", e)


def deletePermission(accessTypep):
    try:
        row = session.query(Permission).get(accessTypep)
        session.delete(row)
        session.commit()
    except exc.SQLAlchemyError as e:
        print("deletePermission failed with: ", e)

def deleteAccess(roleNamep, accessTypep):
    try:
        row = session.query(Access).filter(roleName=roleNamep).filter(accessType=accessTypep).one()
        session.delete(row)
        session.commit()
    except exc.SQLAlchemyError as e:
        print("deleteAccess failed with: ", e)




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
    for i in range(len(regiontable)):
        createRegion(regiontable[i][0], regiontable[i][1])
    for i in range(len(countrytable)):
        createCountry(countrytable[i][0], countrytable[i][1])


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
    
# run just the database in command line mode to create content directly
if __name__ == '__main__':
    defaultdata()
