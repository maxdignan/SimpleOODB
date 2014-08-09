#!C:/Python34/python
__author__ = 'Max Dignan'

import pickle
import os
import shutil
import hashlib
import uuid

def connect(address,user,password):
    connection =  ConnectionOO(address,user,password)
    return connection

def add_account_to_database_for_table():
    currUser = input("Enter a current username: ")
    currPass = input("Enter that accounts password: ")
    currDatabase = input("Enter a valid database for this account: ")
    privy = login_db(currUser,currPass, currDatabase)
    if(privy):
        user = input("Please enter your new username: ")
        password = input("Please enter your new password: ")
        database = input("Please enter the database you wish to access: ")
        table = input("Please enter the table you wish to access: ")
        salt = uuid.uuid4().hex
        #password = str.encode(password)
        hash = hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ":" + salt
        #print(type(hash))
        #print(hash)
        address = os.getcwd()
        url = address + "/" + database + "/permissions"
        permissions = pickle.load(open(url,"rb"))
        #print(type(hash))
        #hash.replace("a","ebc")
        #hash.replace("e","fbc")
        permissionForNew = [user,hash,database,table]
        permissions.append(permissionForNew)
        pickle.dump(permissions, open(url, "wb"))
        #return "YOUR MOM!"
    else:
        print("not an account")
        return False

accessGranted = False

def login():
    global accessGranted
    #if accessGranted:
    #    return True
    #else:
    user = input("Please enter your username: ")
    password = input("Please enter your password: ")
    database = input("Please enter the database you wish to access: ")
    table = input("Please enter the table you wish to access: ")
    address = os.getcwd()
    url = address + "/" + database + "/permissions"
    permissions = pickle.load(open(url,"rb"))
    print(permissions)
    numOfPerms = len(permissions)
    pIndex = 0
    allUsers = []
    while pIndex < numOfPerms:
        singlePerm = permissions[pIndex]
        temp = singlePerm[0]
        allUsers.append(temp)
        pIndex += 1
    #print(allUsers)
    try:
        indexOfAcct = allUsers.index(user)
    except:
        indexOfAcct = len(allUsers)
    if indexOfAcct != len(allUsers):
        acct = permissions[indexOfAcct]
        encpassword, salt = acct[1].split(":")
        hash = hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ":" + salt
        if acct[1] == hash:
            #print("password right")
            if acct[3] == table:
                #print("right table")
                accessGranted = True
                return True
            else:
                print("username, password, or table not correct")
                return False
        else:
            print("username, password, or table not correct")
            return False
    else:
        print("username, password, or table not correct")
        return False

def login_db(user, password, dbName):
    global accessGranted
    #if accessGranted:
    #    return True
    #else:
    address = os.getcwd()
    url = address + "/" + dbName + "/permissions"
    permissions = pickle.load(open(url,"rb"))
    #print(permissions)
    numOfPerms = len(permissions)
    pIndex = 0
    allUsers = []
    while pIndex < numOfPerms:
        singlePerm = permissions[pIndex]
        temp = singlePerm[0]
        allUsers.append(temp)
        pIndex += 1
    #print(allUsers)
    try:
        indexOfAcct = allUsers.index(user)
    except:
        indexOfAcct = len(allUsers)
    if indexOfAcct != len(allUsers):
        acct = permissions[indexOfAcct]
        encpassword, salt = acct[1].split(":")
        hash = hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ":" + salt
        if acct[1] == hash:
            #print("password right")
            if acct[2] == dbName:
                #print("correct db")
                #print("right table")
                #accessGranted = True
                return True
            else:
                print("incorrect db")
        else:
            print("username, password, or table not correct")
            return False
    else:
        print("username, password, or table not correct")
        return False

def login_table(user, password, dbName, tableName):
    global accessGranted
    #if accessGranted:
    #    return True
    #else:
    address = os.getcwd()
    url = address + "/" + dbName + "/permissions"
    permissions = pickle.load(open(url,"rb"))
    #print(permissions)
    numOfPerms = len(permissions)
    pIndex = 0
    allUsers = []
    while pIndex < numOfPerms:
        singlePerm = permissions[pIndex]
        temp = singlePerm[0]
        allUsers.append(temp)
        pIndex += 1
    #print(allUsers)
    try:
        indexOfAcct = allUsers.index(user)
    except:
        indexOfAcct = len(allUsers)
    if indexOfAcct != len(allUsers):
        acct = permissions[indexOfAcct]
        encpassword, salt = acct[1].split(":")
        hash = hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ":" + salt
        if acct[1] == hash:
            #print("password right")
            if acct[2] == dbName:
                #print("correct db")
                if acct[3] == tableName:
                    #print("right table")
                    #accessGranted = True
                    return True
                else:
                    print("username, password, or table not correct")
                    return False
            else:
                print("incorrect db")
                print(acct[2])
                print(dbName)
                return False
        else:
            print("username, password, or table not correct")
            return False
    else:
        print("username, password, or table not correct")
        return False


def temp_add_account(dbName):
    user = "root"
    password = 'root'
    database = dbName
    table = ""
    salt = uuid.uuid4().hex
    hash = hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ":" + salt
    #print(type(hash))
    #print(hash)
    out = ["hi"]
    #print(type(hash))
    #hash.replace("a","ebc")
    #hash.replace("e","fbc")
    permissions = [user, hash, database, table]
    out[0] = permissions
    address = os.getcwd()
    url = address + "/" + database + "/permissions"
    pickle.dump(out, open(url, "wb"))
    return "Default account made user:root password:root database:entered database table:BLANK"

def info():
    print("Welcome to Simple Object-Oriented Database!")
    print("This is an open source project with MIT License hosted on:")
    print("https://github.com/maxdignan/SimpleOODB")
    print("Originally created by: Max Dignan")

class ConnectionOO:
    def __init__(self, address, user, password):
        self.address = address
        self.user = user
        self.password = password
        self.allowed = False
    def allow(self, uniqueForThisdbName):
        privy = login_db(self.user,self.password,uniqueForThisdbName)
        if privy:
            self.allowed = True

    def access_database(self, database):
        if self.allowed:
            db = Database(self.address, self.user, self.password, database)
            return db
        else:
            self.allow(database)
            return self.access_database(database)
    def make_new_db(self, dbName):
        url = self.address + "/" + dbName
        if not os.path.exists(url):
            os.makedirs(url)
            temp_add_account(dbName)
        else: print("already used name, call again")


class Database:
    def __init__(self, address, user, password, database):
        self.address = address
        self.user = user
        self.password = password
        self.database = database
        self.allowed = False
    def allow(self):
        privy = login_db(self.user, self.password, self.database)
        if privy:
            self.allowed = True
    def remove_db(self):
        if self.allowed:
            url = self.address + "/" + self.database
            if os.path.exists(url):shutil.rmtree(url)
            else: print("database doesn't exist, call again")
        else:
            self.allow()
            self.remove_db()
    def access_other_db(self, newDatabase):
        if self.allowed:
            db = Database(self.address, self.user, self.password, newDatabase)
            return db
        else:
            self.allow()
            return self.access_other_db(newDatabase)
    def access_table(self, table):
        if self.allowed:
            tb = Table(self.address, self.user, self.password, self.database, table)
            return tb
        else:
            self.allow()
            return self.access_table(table)
    def make_new_table(self, tableName):
        if self.allowed:
            url = self.address + "/" + self.database + "/" + tableName
            if not os.path.exists(url):os.makedirs(url)
            else: print("already used name, call again")
        else:
            self.allow()
            self.make_new_table(tableName)
    def remove_table(self, tableName):
        if self.allowed:
            url = self.address + "/" + self.database + "/" + tableName
            if os.path.exists(url):shutil.rmtree(url)
            else: print("table doesn't exist, call again")
        else:
            self.allow()
            self.remove_table(tableName)

class Table:
    def __init__(self, address, user, password, database, table):
        self.address = address
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.allowed = False
    def allow(self):
        privy = login_table(self.user, self.password, self.database, self.table)
        if privy:
            self.allowed = True
    def access_group(self, idNum):
        if self.allowed:
            group = Group(self.address, self.user, self.password, self.database, self.table, idNum)
            return group
        else:
            self.allow()
            return self.access_group(idNum)
    ##find number of groups
    def add_value_by_category(self, idNum, category, newValue):
        if self.allowed:
            group = Group(self.address, self.user, self.password, self.database, self.table, idNum)
            group.edit_value(category,newValue)
        else:
            self.allow()
            self.add_value_by_category(idNum, category, newValue)

    def access_value(self, idNum, category):
        if self.allowed:
            maxLength = len(self.list_groups())
            if idNum <= maxLength:
                group = Group(self.address, self.user, self.password, self.database, self.table, idNum)
                return group.get_value_by_category(category)
            else:
                print("index out of range, don't worry nothing was accessed")
        else:
            self.allow()
            return self.access_value(idNum, category)

    def list_groups(self):
        if self.allowed:
            #currDir = os.getcwd()
            #print(currDir)
            trash = 0
            url = self.address + "/" + self.database + "/" + self.table
            os.chdir(url)
            a = []
            for path,dirs,files in os.walk('.'):
                for fn in files:
                    b = [os.path.join(path,fn)]
                    a.extend(b)
            os.chdir(self.address)
            try:
                del a[a.index(".\\desktop.ini")]
            except:
                trash += 1
                #print("you may manually want to remove any non-group-data files from table in file system (don't forget hidden(maybe))... sorry")
            return a
        else:
            self.allow()
            return self.list_groups()
    ##add functionality to add category to each group
    def add_category_to_all_groups(self, categoryName):
        if self.allowed:
            listOfGroups = self.list_groups()
            numberOfGroups = len(listOfGroups) + 1
            for indGroup in range(1,numberOfGroups):
                group = Group(self.address, self.user, self.password, self.database, self.table, str(indGroup))
                group.add_category(categoryName)
        else:
            self.allow()
            self.add_category_to_all_groups(categoryName)
    ##add group to table
    def add_group(self):
        if self.allowed:
            nextGroupIDNum = len(self.list_groups()) + 1
            parts = [[],[]]
            url = self.address + "/" + self.database + "/" + self.table + "/" + str(nextGroupIDNum)
            pickle.dump(parts, open(url, "wb"))
        else:
            self.allow()
            self.add_group()
    def swap_groups(self,firstIDNum,secondIDNum):
        if self.allowed:
            firstGroup = Group(self.address, self.user, self.password, self.database, self.table, firstIDNum)
            secondGroup = Group(self.address, self.user, self.password, self.database, self.table, secondIDNum)
            temp = firstGroup.access()
            firstGroup.update(secondGroup.access())
            secondGroup.update(temp)
        else:
            self.allow()
            self.swap_groups(firstIDNum,secondIDNum)

    def list_all_categories(self):
        if self.allowed:
            listOfGroups = self.list_groups()
            numberOfGroups = len(listOfGroups)
            #print(len(listOfGroups))
            allCats = []
            #make a copy of all cats from all groups to allcats
            x = 1
            while x <= numberOfGroups:
                gr = Group(self.address, self.user, self.password, self.database, self.table, str(x))
                a = gr.access_categories()
                #print(type(a))
                #print(a)
                allCats.extend(a)
                #print(allCats)
                #allCats.append(a)
                x += 1
            #print(allCats)
            index = 0
            while index < len(allCats) - 1:
                temp = allCats[index]
                inindex = index + 1
                while inindex < len(allCats):
                    if allCats[inindex] == temp:
                        del allCats[inindex]
                    else:
                        inindex += 1
                index += 1
            return allCats
        else:
            self.allow()
            return self.list_all_categories()
    ##remove group
    def remove_group(self, idNum):
        if self.allowed:
            print("Note: Restart all Group instances!")
            #currDir = os.getcwd()
            listOfGroups = self.list_groups()
            numberOfGroups = len(listOfGroups)
            idNum = int(idNum)
            #print(idNum)
            index = idNum
            while True:
                if index < numberOfGroups:
                    self.swap_groups(str(index),str((index+1)))
                    index += 1
                else:
                    break
            url = self.address + "/" + self.database + "/" + self.table
            os.chdir(url)
            os.remove(str(numberOfGroups))
            os.chdir(self.address)
        else:
            self.allow()
            self.remove_group(idNum)
    ##list all by category
    def print_values_by_category(self):
        if self.allowed:
            cats = self.list_all_categories()
            index = 0
            groupNum = 0
            listOfGroups = self.list_groups()
            numberOfGroups = len(listOfGroups) + 1
            while index < len(cats):
                catagor = cats[index]
                print(catagor)
                groupNum = 0
                while groupNum < numberOfGroups - 1:
                    groupNum += 1
                    group = Group(self.address, self.user, self.password, self.database, self.table, str(groupNum))
                    print(group.get_value_by_category(catagor))
                index += 1
                print("-------")
        else:
            self.allow()
            self.print_values_by_category()
    def list_values_of_category(self, category):
        if self.allowed:
            out = []
            groupNum = 1
            listOfGroups = self.list_groups()
            numberOfGroups = len(listOfGroups)
            while groupNum <= numberOfGroups:
                group = Group(self.address, self.user, self.password, self.database, self.table, str(groupNum))
                out.append(group.get_value_by_category(category))
                groupNum += 1
            return out
        else:
            self.allow()
            return self.list_values_of_category(category)

class Group:
    def __init__(self, address, user, password, database, table, idNum):
        self.address = address
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.idNum = idNum
        self.allowed = False
    def allow(self):
        privy = login_table(self.user, self.password, self.database, self.table)
        if privy:
            self.allowed = True
    def access(self):
        if self.allowed:
            url = self.address + "/" + self.database + "/" + self.table + "/" + self.idNum
            return pickle.load(open(url,"rb"))
        else:
            self.allow()
            return self.access()
    def update(self, obj):
        if self.allowed:
            url = self.address + "/" + self.database + "/" + self.table + "/" + self.idNum
            pickle.dump(obj, open(url, "wb"))
        else:
            self.allow()
            self.update(obj)
    def access_categories(self):
        if self.allowed:
            group = self.access()
            catas = group[0]
            #print(type(catas))
            #print(catas)
            return catas
        else:
            self.allow()
            return self.access_categories()
    def access_values(self):
        if self.allowed:
            group = self.access()
            values = group[1]
            return values
        else:
            self.allow()
            return self.access_values()
    def get_value_by_category(self, category):
        if self.allowed:
            cats = self.access_categories()
            try:
                index = cats.index(category)
            except:
                return "none"
            values = self.access_values()
            return values[index]
        else:
            self.allow()
            return self.get_value_by_category(category)
    def add_category(self, cataName):
        if self.allowed:
            cats = self.access_categories()
            values = self.access_values()
            try:
                index = cats.index(cataName)
            except:
                index = len(cats)
            if index == len(cats):
                a = [cataName]
                cats.extend(a)
                a = ["000null000"]
                values.extend(a)
                out = [cats, values]
                self.update(out)
        else:
            self.allow()
            self.add_category(cataName)
    def edit_value(self,category,newValue):
        if self.allowed:
            cats = self.access_categories()
            values = self.access_values()
            index = cats.index(category)
            values[index] = newValue
            out = [cats, values]
            self.update(out)
        else:
            self.allow()
            self.edit_value(category,newValue)
    def delete_category(self, cataName):
        if self.allowed:
            cats = self.access_categories()
            values = self.access_values()
            index = cats.index(cataName)
            del cats[index]
            del values[index]
            out = [cats, values]
            self.update(out)
        else:
            self.allow()
            self.delete_category(cataName)




