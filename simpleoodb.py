#!C:/Python34/python
__author__ = 'Max Dignan'

import pickle
import os
import shutil

def connect(address, user, password):
    connection =  ConnectionOO(address, user, password)
    return connection

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
    def access_database(self, database):
        db = Database(self.address, self.user, self.password, database)
        return db
    def make_new_db(self, dbName):
        url = self.address + "/" + dbName
        if not os.path.exists(url):os.makedirs(url)
        else: print("already used name, call again")
    def remove_db(self, dbName):
        url = self.address + "/" + dbName
        if os.path.exists(url):shutil.rmtree(url)
        else: print("database doesn't exist, call again")


class Database:
    def __init__(self, address, user, password, database):
        self.address = address
        self.user = user
        self.password = password
        self.database = database
    def access_other_db(self, newDatabase):
        db = Database(self.address, self.user, self.password, newDatabase)
        return db
    def access_table(self, table):
        tb = Table(self.address, self.user, self.password, self.database, table)
        return tb
    def make_new_table(self, tableName):
        url = self.address + "/" + self.database + "/" + tableName
        if not os.path.exists(url):os.makedirs(url)
        else: print("already used name, call again")
    def remove_table(self, tableName):
        url = self.address + "/" + self.database + "/" + tableName
        if os.path.exists(url):shutil.rmtree(url)
        else: print("table doesn't exist, call again")

class Table:
    def __init__(self, address, user, password, database, table):
        self.address = address
        self.user = user
        self.password = password
        self.database = database
        self.table = table
    def access_group(self, idNum):
        group = Group(self.address, self.user, self.password, self.database, self.table, idNum)
        return group
    ##find number of groups
    def list_groups(self):
        currDir = os.getcwd()
        #print(currDir)
        url = currDir + "/" + self.database + "/" + self.table
        os.chdir(url)
        a = []
        for path,dirs,files in os.walk('.'):
            for fn in files:
                b = [os.path.join(path,fn)]
                a.extend(b)
        os.chdir(currDir)
        try:
            del a[a.index(".\\desktop.ini")]
        except:
            print("you may manually want to remove any non-group-data files from table in file system (don't forget hidden(maybe))... sorry")
        return a
    ##add functionality to add category to each group
    def add_category_to_all_groups(self, categoryName):
        listOfGroups = self.list_groups()
        numberOfGroups = len(listOfGroups) + 1
        for indGroup in range(1,numberOfGroups):
            group = Group(self.address, self.user, self.password, self.database, self.table, str(indGroup))
            group.add_category(categoryName)
    ##add group to table
    def add_group(self):
        nextGroupIDNum = len(self.list_groups()) + 1
        parts = [[],[]]
        url = self.address + "/" + self.database + "/" + self.table + "/" + str(nextGroupIDNum)
        pickle.dump(parts, open(url, "wb"))
    def swap_groups(self,firstIDNum,secondIDNum):
        firstGroup = Group(self.address, self.user, self.password, self.database, self.table, firstIDNum)
        secondGroup = Group(self.address, self.user, self.password, self.database, self.table, secondIDNum)
        temp = firstGroup.access()
        firstGroup.update(secondGroup.access())
        secondGroup.update(temp)
    def list_all_categories(self):
        listOfGroups = self.list_groups()
        numberOfGroups = len(listOfGroups) + 1
        allCats = []
        #make a copy of all cats from all groups to allcats
        for indGroup in range(1,numberOfGroups):
            group = Group(self.address, self.user, self.password, self.database, self.table, str(indGroup))
            groupCats = group.access_categories()
            a = groupCats
            allCats.extend(a)
        index = 0
        while index < len(allCats):
            temp = allCats[index]
            inindex = index + 1
            while inindex < len(allCats):
                if allCats[inindex] == temp:
                    del allCats[inindex]
                else:
                    inindex += 1
            index += 1
        return allCats
    ##remove group
    def remove_group(self, idNum):
        print("Note: Restart all Group instances!")
        currDir = os.getcwd()
        listOfGroups = self.list_groups()
        numberOfGroups = len(listOfGroups)
        idNum = int(idNum) - 1
        index = idNum
        while True:
            if index < numberOfGroups:
                self.swap_groups(str(index),str((index+1)))
                index += 1
            else:
                break
        url = currDir + "/" + self.database + "/" + self.table
        os.chdir(url)
        os.remove(str(numberOfGroups))
        os.chdir(currDir)
    ##list all by category
    def list_values_by_category(self):
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

class Group:
    def __init__(self, address, user, password, database, table, idNum):
        self.address = address
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.idNum = idNum
    def access(self):
        url = self.address + "/" + self.database + "/" + self.table + "/" + self.idNum
        return pickle.load(open(url,"rb"))
    def update(self, obj):
        url = self.address + "/" + self.database + "/" + self.table + "/" + self.idNum
        pickle.dump(obj, open(url, "wb"))
    def access_categories(self):
        group = self.access()
        catas = group[0]
        return catas
    def access_values(self):
        group = self.access()
        values = group[1]
        return values
    def get_value_by_category(self, category):
        cats = self.access_categories()
        try:
            index = cats.index(category)
        except:
            return "none"
        values = self.access_values()
        return values[index]
    def add_category(self, cataName):
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
    def edit_value(self,category,newValue):
        cats = self.access_categories()
        values = self.access_values()
        index = cats.index(category)
        values[index] = newValue
        out = [cats, values]
        self.update(out)
    def delete_category(self, cataName):
        cats = self.access_categories()
        values = self.access_values()
        index = cats.index(cataName)
        del cats[index]
        del values[index]
        out = [cats, values]
        self.update(out)




