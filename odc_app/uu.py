import random
import sys
import csv
import datetime
from fakeUserData import generator as g
from faker import Faker
fake = Faker()
from faker.providers import BaseProvider
from collections import namedtuple
####################################################################
# create new provider class
class product(BaseProvider):
    def product(self):
        a=[]
        str='book pen pencil desktop laptop orange apple'

        x=str.split( )

        return random.choice(x)
    def allproduct(self):
        a = []
        str = 'book pen pencil desktop laptop orange apple'
        x = str.split()
        return x
fake.add_provider(product)
#################################################
class states2(BaseProvider):
    def state1(self):
        a=[]
        str='full outoforder lessaverage aboveaverage good'

        x=str.split( )

        return random.choice(x)

fake.add_provider(states2)
############################################################
def role():
    str = 'admin warehousemanager user '
    x = str.split()
    return x
###########################################
def roledes(a):
    if a=='admin':
        return 'charger all'
    elif a=='warehousemanager':
        return "charge the area"
    elif a=='user':
        return "take care product"
#################################################
def productdescription( a ):
    if a== 'book':
        return "a book"
    elif a== 'pen':
        return "a pen"
    elif a== 'pencil':
        return "a pencil"
    elif a== 'desktop':
        return "a desktop"
    elif a== 'laptop':
        return "a laptop"
    elif a== 'orange':
        return "delicious orange"
    elif a== 'apple':
        return "yummy apple"
###############################################
def productvalue(a):
    if a == 'book':
        return 123
    elif a == 'pen':
        return 5
    elif a == 'pencil':
        return 5
    elif a == 'desktop':
        return 2334
    elif a == 'laptop':
        return 1223
    elif a == 'orange':
        return 5
    elif a == 'apple':
        return 12
#####################################
def imagedata(a):
    if a == 'book':
        return 'book'
    elif a == 'pen':
        return 'pen'
    elif a == 'pencil':
        return 'pencil'
    elif a == 'desktop':
        return 'desktop'
    elif a == 'laptop':
        return 'laptop'
    elif a == 'orange':
        return 'orange'
    elif a == 'apple':
        return 'apple'
#####################################################
def productunit(a):
    if a == 'book':
        return 'per'
    elif a == 'pen':
        return 'per'
    elif a == 'pencil':
        return 'per'
    elif a == 'desktop':
        return 'per'
    elif a == 'laptop':
        return 'per'
    elif a == 'orange':
        return 'lb'
    elif a == 'apple':
        return 'lb'
#############################################
def categories1(a):
    if a == 'book':
        return 'book'
    elif a == 'pen':
        return 'studystuff'
    elif a == 'pencil':
        return 'studystuff'
    elif a == 'desktop':
        return 'electric'
    elif a == 'laptop':
        return 'electric'
    elif a == 'orange':
        return 'fruit'
    elif a == 'apple':
        return 'fruit'
#####################################
def status():

    str='outofstock lowstock full '
    x = str.split()

    return random.choice(x)
##################################
class country(BaseProvider):
    def country(self):
        a=[]
        str='China American Spanish Swaziland Canada Benin Brazil'

        x=str.split( )

        return random.choice(x)
    def allcountries(self):
        a = []
        str = 'China American Spanish Swaziland Canada Benin Brazil'
        x = str.split()
        return x
fake.add_provider(country)
##################################################
def prefix(a):
    if a=='China':
        return '018'
    elif a=='American':
        return '1'
    elif a=='Spanish':
        return '2'
    elif a=='Swaziland':
        return '3'
    elif a== 'Canada':
        return '4'
    elif a== 'Benin':
        return '5'
    elif a=='Brazil':
        return'6'
##################################
def regiondes(a):
    if a=='Canada' or 'America':
        return 'north America'
    elif a=='Brazil':
        return 'south America'
    elif a=="China":
        return 'Asian'
    elif a =='Benin':
        return 'Africa'
    elif a=="Swaziland" or 'Spanish':
        return 'European'
######################################
def regiondes2(a):
    if a == 'NorthAmerica':
        return 'north America'
    elif a == 'SouthAmerica':
        return 'south America'
    elif a == "Asian":
        return 'Asian'
    elif a == 'Africa':
        return 'Africa'
    elif a == 'European':
        return 'European'
#####################################################
def addresscount(a):
    if len(a)>=35:
        c=a[:35]
        return c
    else:
        return a
#################################################3
def other(a):
    if len(a)>=35:
        c=a[35:]
        return c


##############################################################
class region(BaseProvider):
    def region(self):
        str='NorthAmerica SouthAmerica Asian European Africa '
        x=str.split( )

        return random.choice(x)
    def allregion(self):
        a = []
        str = 'NorthAmerica SouthAmerica Asian European Africa'
        x = str.split()
        return x
# then add new provider to faker instance
fake.add_provider(region)
##############################################################
#create region table
def region1():
    a=[]
    MyStruct = namedtuple("MyStruct", " RegionName, RegionDescription ")

    c = fake.allregion()
    for i in range( len(c)):
        MyStruct = (c[i], regiondes2(c[i]) )

    # MyStruct=(c[i][0], productdescription(c[i].productname),random.randint(1,1000),productvalue(c[i].productname),productunit(c[i].productname)),)
        a.append(MyStruct)
    return a
################################################################################
#create country table
def country1():
    a=[]
    MyStruct = namedtuple("MyStruct", " country, internationCallPrefix ")

    c = fake.country()
    for i in range(0, len(c)-1):
        MyStruct = (c[i], prefix(c[i]) )

    # MyStruct=(c[i][0], productdescription(c[i].productname),random.randint(1,1000),productvalue(c[i].productname),productunit(c[i].productname)),)
    a.append(MyStruct)
    return a
###############################################################################
#create address table
def address1():
    a=[]
    MyStruct = namedtuple("MyStruct", " addressID, addresslinefirst,addresslinesecond,country, region ")


    for i in range(100):
        country1=fake.country()
        MyStruct = (i, addresscount(g.street()),other(g.street()),country1,regiondes(country1) )

    # MyStruct=(c[i][0], productdescription(c[i].productname),random.randint(1,1000),productvalue(c[i].productname),productunit(c[i].productname)),)
        a.append(MyStruct)
    return a
##############################################################################3
def roletable1():
    c = role()
    a = []
    MyStruct = namedtuple("MyStruct", "rolename, roledescription")

    for i in range(0, len(c) - 1):
        MyStruct = (c[i], roledes(c[i]))

        a.append(MyStruct)
    return a
#################################################################################
#create "loginformation" table
def generatinformation1():
    a=[]
    MyStruct = namedtuple("MyStruct", "birthdate, password, phonenumber, email,firstname, lastname,addressID, rolename")
    k=address1()
    c=role()


    for i in range (3):

        MyStruct=( datetime.datetime.utcnow(),g.createPassword(10),g.usPhoneNumber(),g.email(g.firstName(),g.lastName()),g.firstName(),g.lastName(),k[i],'admin')
        a.append(MyStruct)
    for i in range(3,8):
        MyStruct = (
            datetime.datetime.utcnow(), g.createPassword(10), g.usPhoneNumber(), g.email(g.firstName(),g.lastName()), g.firstName(), g.lastName(), k[i], 'warehousemanager')
        a.append(MyStruct)
    for i in range(8,100):
        MyStruct = (
            datetime.datetime.utcnow(), g.createPassword(10), g.usPhoneNumber(), g.email(g.firstName(),g.lastName()), g.firstName(), g.lastName(), k[i],
            'User')
        a.append(MyStruct)
   # k=0
    #

    return a
#############################################################
#create product table
def product1():
    a = []

    MyStruct = namedtuple("MyStruct", "productname, price, description, imagedata, quantity,productowner")
    b=generatinformation1()

    for i in range(8,100):
        c=fake.product()
        MyStruct = (c, productvalue(c), productdescription(c), imagedata(c), random.randint(1,1000),b[i][3])
        a.append(MyStruct)
    return a

##############################################################
#create table ConfigAttribute
def ConfigAttribute1():
    a = []

    MyStruct = namedtuple("MyStruct", "name description, unit, attributerowner")
    b=product1()

    for i in range(len(b)):

        MyStruct = (categories1(b[i][0]),productdescription(b[i][0]),productunit(b[i][0]),b[i][5])
        a.append(MyStruct)
    return a
##############################################################
#create "productattribution" table
def productattribution1():
    a=[]


    MyStruct = namedtuple("MyStruct", " attributionname, productname,productowner, value ")

    k=product1()
    for i in range(len(k)):
        MyStruct=(categories1(k[i][0]),k[i][0],k[i][5],productvalue(k[i][0]))
        a.append(MyStruct)
    return a
################################################################

#create Warehouse table
def Warehouse1():
    a=[]
    MyStruct = namedtuple("MyStruct", " UserName, description, capacity,addressID ")

    c =generatinformation1()
    d=productattribution1()
    k=fake.allregion()
    for i in range(len(k)):
        MyStruct = (c[i+3][3],k[i],random.randint(10000,100000),random.randint(0,99) )
        a.append(MyStruct)
    return a
################################################################################################
def Warehousestorage1():
    a=[]
    MyStruct = namedtuple("MyStruct", "  refilldate, price, ProductName,productowner ")
    k=product1()

    for i in range(len(k)):

        MyStruct = (g.randomDate(),productvalue(k[i][0]),k[i][0],k[i][5] )
        a.append(MyStruct)
    return a
#####################################################################################################
#create table categories
def categories2():
    a=[]
    MyStruct = namedtuple("MyStruct", " categoryname, isdefault, categoryDescription, categoryowner ")
    q=generatinformation1()
    f=product1()
    s='t f'
    k=s.split()
    for i in range(8,100):
        for j in range(len(f)):
            if q[i][3]==f[j][5]:
                MyStruct = (categories1(f[j][0]),random.choice(k),categories1(f[j][0]),q[i][3] )
                a.append(MyStruct)
    return a
##########################################################################################################
#table producttocategories
def producttocategories1():
    a=[]
    MyStruct = namedtuple("MyStruct", " categoryname, productname,productowner ")
    c=product1()
    for i in range(len(c)):

        MyStruct = (categories1(c[i][0]),c[i][0],c[i][5])
        a.append(MyStruct)
    return a
#############################################################################################################
#table permission
def permission1():
    a=[]
    MyStruct = namedtuple("MyStruct", " accessType, accessdescription ")
    k=role()
    for i in range(len(k)):

        MyStruct = (k[i],roledes(k[i]))
        a.append(MyStruct)
    return a
#################################################################################################################
#table Access
def Access1():
    a=[]
    MyStruct = namedtuple("MyStruct", " rolename, accesstype,accesslevel ")
    k=role()
    for i in range(len(k)):
        if k[i]=='admin':
            MyStruct = (k[i],'all','b')
            a.append(MyStruct)
        elif k[i]=='warehousemanager':
            MyStruct = (k[i], 'selfregion', 'r')
            a.append(MyStruct)
        elif k[i]=='user':
            MyStruct = (k[i], 'uploadproduct', 'n')
            a.append(MyStruct)
    return a
################################################################################################################
