#!C:/Python34/python
__author__ = 'Max Dignan'

import pickle


def connect(address, user, password):
    connection =  ConnectionOO(address, user, password)
    return connection

def info():
    print("Welcome to Simple Object-Oriented Database!")
    print("This is an open source project with MIT License hosted on:")
    print("https://github.com/maxdignan/SimpleOODBtest")
    print("Originally created by: Max Dignan")

class ConnectionOO:
    def __init__(self, address, user, password):
        self.address = address
        self.user = user
        self.password = password
    def access_database(self, database):
        db = Database(self.address, self.user, self.password, database)
        return db

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
    ##add functionality to add category to each group
    ##add group to table
    ##add remove group
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
        realUrl = "C:/Pythonfiles/SimpleOODB/MyDBs/testdb/testtab/1"
        if url != realUrl:
            return pickle.load(open(realUrl), "rb")
        return pickle.load(open(url,"rb"))
    def update(self, obj):
        realUrl = "C:/Pythonfiles/SimpleOODB/MyDBs/testdb/testtab/1"
        url = self.address + "/" + self.database + "/" + self.table + "/" + self.idNum
        if url != realUrl:
            pickle.dump(obj, open(realUrl, "wb"))
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
        index = cats.index(category)
        values = self.access_values()
        return values[index]
    def add_catagory(self, cataName):
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




