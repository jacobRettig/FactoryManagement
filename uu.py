import random
import sys
import csv
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
############################################################
def role():
    str = 'admin warehousemanager user '
    x = str.split()
    return x
###########################################
def roledes(a):
    if a=='admin':
        return 'charger all'
    if a=='warehousemanager':
        return "charge the area"
    if a=='user':
        return "take care product"
#################################################
def productdescription( a ):
    if a== 'book':
        return "a book"
    if a== 'pen':
        return "a pen"
    if a== 'pencil':
        return "a pencil"
    if a== 'desktop':
        return "a desktop"
    if a== 'laptop':
        return "a laptop"
    if a== 'orange':
        return "delicious orange"
    if a== 'apple':
        return "yummy apple"
###############################################
def productvalue(a):
    if a == 'book':
        return 123
    if a == 'pen':
        return 5
    if a == 'pencil':
        return 5
    if a == 'desktop':
        return 2334
    if a == 'laptop':
        return 1223
    if a == 'orange':
        return 5
    if a == 'apple':
        return 12
#####################################
def imagedata(a):
    if a == 'book':
        return 'book'
    if a == 'pen':
        return 'pen'
    if a == 'pencil':
        return 'pencil'
    if a == 'desktop':
        return 'desktop'
    if a == 'laptop':
        return 'laptop'
    if a == 'orange':
        return 'orange'
    if a == 'apple':
        return 'apple'
#####################################################
def productunit(a):
    if a == 'book':
        return 'per'
    if a == 'pen':
        return 'per'
    if a == 'pencil':
        return 'per'
    if a == 'desktop':
        return 'per'
    if a == 'laptop':
        return 'per'
    if a == 'orange':
        return 'lb'
    if a == 'apple':
        return 'lb'
#############################################
def categories(a):
    if a == 'book':
        return 'book'
    if a == 'pen':
        return 'studystuff'
    if a == 'pencil':
        return 'studystuff'
    if a == 'desktop':
        return 'electric'
    if a == 'laptop':
        return 'electric'
    if a == 'orange':
        return 'fruit'
    if a == 'apple':
        return 'fruit'
#####################################
def status():

    str='outofstock lowstock full '
    x = str.split()

    return random.choice(x)
##################################
def regiondes(a):
    if a=='NorthAmerica':
        return 'north America'
    if a=='south America':
        return 'south America'
    if a=="Asian":
        return 'Asian'
    if a =='Africa':
        return 'Africa'
    if a=="European":
        return 'European'
######################################
def access(a):
    if a=='admin':
        return "access all"
    if a=='warehousemanager':
        return "charge the area"
    if a=='user':
        return "take care product and account"
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
#create "loginformation" table
def generatinformation():
    a=[]
    MyStruct = namedtuple("MyStruct", "username, birthdate, password, phonenumber, userRegion, warehouseManageName, productname, email, address")
    for i in range (1,100):
        MyStruct=(g.name(), g.birthday(18),g.createPassword(10),g.usPhoneNumber(),fake.region(),g.name(),fake.product(),g.email(),g.usAddress())
        a.append(MyStruct)

    return a

##############################################################
#create "productattribution" table
def productattribution():
    a=[]


    MyStruct = namedtuple("MyStruct", " username, productname, description, value, quantity,unit ")

    c = generatinformation()
    for i in range(0,99):
        MyStruct=(c[i][0],c[i][6],productdescription(c[i][6]),productvalue(c[i][6]),random.randint(1,1000),productunit(c[i][6]))

   # MyStruct=(c[i][0], productdescription(c[i].productname),random.randint(1,1000),productvalue(c[i].productname),productunit(c[i].productname)),)
    a.append(MyStruct)
    return a
################################################################
#create product table
def product():
    a = []

    MyStruct = namedtuple("MyStruct", "productname, price, description, imagedata, quantity")

    c = fake.allproduct()
    d=productattribution()
    q=w=e=r=t=y=u=0
    for i in range(0,99):
        if d[i][1]=='book':
            q=q+d[i][3]
        if d[i][1]=='pen':
            w=w+d[i][3]
        if d[i][1]=='pencil':
            e=e+d[i][3]
        if d[i][1]=='desktop':
            r=r+d[i][3]
        if d[i][1]=='laptop':
            t=t+d[i][3]
        if d[i][1]=='orange':
            y=y+d[i][3]
        if d[i][1]=='apple':
            u=u+d[i][3]

    for i in range(0, len(c)-1):
        if c[i]=='book':
            MyStruct = ( c[i], productvalue((c[i])), productdescription(c[i]),  imagedata(c[i]),
                        q)
        if c[i]=='pen':
            MyStruct = ( c[i], productvalue((c[i])), productdescription(c[i]),  imagedata(c[i]),
                        w)
        if c[i]=='pencil':
            MyStruct = ( c[i], productvalue((c[i])), productdescription(c[i]),  imagedata(c[i]),
                        e)
        if c[i]=='desktop':
            MyStruct = ( c[i], productvalue((c[i])), productdescription(c[i]),  imagedata(c[i]),
                       r)
        if c[i]=='laptop':
            MyStruct = ( c[i], productvalue((c[i])), productdescription(c[i]),  imagedata(c[i]),
                        t)
        if c[i]=='orange':
            MyStruct = ( c[i], productvalue((c[i])), productdescription(c[i]),  imagedata(c[i]),
                        y)
        if c[i]=='apple':
            MyStruct = ( c[i], productvalue((c[i])), productdescription(c[i]),  imagedata(c[i]),
                        u)

    # MyStruct=(c[i][0], productdescription(c[i].productname),random.randint(1,1000),productvalue(c[i].productname),productunit(c[i].productname)),)
    a.append(MyStruct)
    return a
#####################################################################################
#create region table
def region():
    a=[]
    MyStruct = namedtuple("MyStruct", " RegionName, RegionDescription, WarehouseManagerName ")

    c = fake.allregion()
    for i in range(0, len(c)-1):
        MyStruct = (c[i], regiondes(c[i]),g.name() )

    # MyStruct=(c[i][0], productdescription(c[i].productname),random.randint(1,1000),productvalue(c[i].productname),productunit(c[i].productname)),)
    a.append(MyStruct)
    return a
########################################################################################
def protocat():
    c=fake.allproduct()
    MyStruct = namedtuple("MyStruct","productname, description, categoryname")

    for i in range (0, len(c)-1):
        MyStruct = (c[i], productdescription(c[i]), categories(c[i]))
    a = []
    a.append(MyStruct)
    return a
#########################################################################################
#create Warehouse table
def Warehouse():
    a=[]
    MyStruct = namedtuple("MyStruct", " UserName, ProductName, Description, Categories, Quantity,MaxQuantity, UserRegion ")

    c =generatinformation()
    d=productattribution()

    for i in range(0, len(c)-1):
        for j in range (0,len(d)-1):
            if (d[j][0]==c[i][0]):

                MyStruct = (c[i][0], c[i][6],categories(c[i][6]),d[j][4],random.randint(10000,100000),c[i][4] )

    # MyStruct=(c[i][0], productdescription(c[i].productname),random.randint(1,1000),productvalue(c[i].productname),productunit(c[i].productname)),)
    a.append(MyStruct)
    return a
################################################################################################
def Warehousestorage():
    a=[]
    MyStruct = namedtuple("MyStruct", " ProductName, Warehouse_managername, price, state, refilldate, ProductRegion ")
    e = region()
    c =generatinformation()
    d=productattribution()
    for i in range(0, len(c)-1):
        for j in range (0,len(d)-1):
            if (d[j][0]==c[i][0]):
                for k in range(0,len(e)-1 ):
                    if c[i][4]==e[k][0]:
                        MyStruct = (d[j][1], e[k][2],d[j][3],d[j][4],status(),g.randomDate(),e[k][0] )

    # MyStruct=(c[i][0], productdescription(c[i].productname),random.randint(1,1000),productvalue(c[i].productname),productunit(c[i].productname)),)
    a.append(MyStruct)
    return a
#####################################################################################################
def role():
    c = role()
    MyStruct = namedtuple("MyStruct", "rolename, roledescription, access")

    for i in range(0, len(c) - 1):
        MyStruct = (c[i], roledes(c[i]), access(c[i]))
    a = []
    a.append(MyStruct)
    return a