#!C:/Python34/python
__author__ = 'Max Dignan'

import hashlib
import uuid
import os
import pickle

#will allow user to connect with specific data table
#the username and password will be cross checked
#with corresponding table
def connect(table, username, password):
    table = Table(table, username, password)
    if table.load():
        return table
    else:
        print('incorrect information')


#makes new table, will give original permissions to user: root
#password: root
#this can be deleted later on
def make_new_table(tablename):
    salt = uuid.uuid4().hex
    root = 'root'
    hash = hashlib.sha512(salt.encode() + root.encode()).hexdigest() + ":" + salt
    table = Table(tablename, 'root', hash)
    table.commit()
    print(r"Table '" + tablename + "' created with username 'root' and password 'root'")




class Table:
    def __init__(self, tablename, currentUser, currentPassword):
        self.currentUser = currentUser
        self.currentPassword = currentPassword

        self.tableName = tablename
        self.users = [[currentUser, currentPassword]]
        self.data = [[]]
        self.privy = False

    #confirms permissions to specific db
    def load(self):
        address = os.getcwd()
        url = address + "/" + self.tableName
        handle = pickle.load(open(url, "rb"))
        users = handle[0]
        length = len(users)
        index = 0
        while index < length:
            userHandle = users[index]
            if self.currentUser == userHandle[0]:
                hashedPassword, salt = userHandle[1].split(":")
                hash = hashlib.sha512(salt.encode() + self.currentPassword.encode()).hexdigest() + ":" + salt
                if userHandle[1] == hash:
                    self.privy = True
                    self.users = users
                    self.data = handle[1]
                    return True
            index += 1

    #commits adjusted data into file
    def commit(self):
		if self.privy:
			address = os.getcwd()
			url = address + "/" + self.tableName
			obj = [self.users, self.data]
			pickle.dump(obj, open(url, "wb"))
		else
			if self.load():
				self.privy = True
				self.commit()
		
    #adds a new user to table
    def add_user(self, newUser, newPassword):
        if self.privy:
            salt = uuid.uuid4().hex
            hash = hashlib.sha512(salt.encode() + newPassword.encode()).hexdigest() + ":" + salt
            tempObject = [newUser, hash]
            self.users.append(tempObject)
            print(r"username: '"+ newUser + "' and password: '" + newPassword + "' added to table")
            self.commit()
            print('automatically saved to table on disk')
        else:
            if self.load():
                self.privy = True
                self.add_user(newUser, newPassword)

    #deletes a user from having access to database
    def delete_user(self, username):
        if self.privy:
            allUsernames = []
            index = 0
            while index < len(self.users):
                allUsernames.append(self.users[index][0])
                index += 1
            indexToBurn = allUsernames.index(username)
            del self.users[indexToBurn]
            self.commit()
            print('automatically deleted and saved to table on disk')
        else:
            if self.load():
                self.privy = True
                self.delete_user(username)

    #tests whether category exists in a row
    def check_category_present(self, row, categoryName):
        if self.privy:
            keyPairIndex = 0
            while keyPairIndex < len(self.data[row]):
                if categoryName == self.data[row][keyPairIndex][0]:
                    return True
                keyPairIndex += 1
            return False
        else:
            if self.load():
                self.privy = True
                return self.check_category_present(row, categoryName)

    #adds new row to table
    def add_row(self):
        if self.privy:
            tempObject = []
            self.data.append(tempObject)
        else:
            if self.load():
                self.privy = True
                self.add_row()

    #removes row from table
    #do note: subsequent rows will be moved back one space
    def delete_row(self, rowNumber):
        if self.privy:
            try:
                del self.data[rowNumber]
            except:
                print(r"Can't delete row, because row doesn't exist")
        else:
            if self.load():
                self.privy = True
                self.delete_row(rowNumber)

    #edit value to row's category
    def edit_value(self, rowNumber, categoryName, value):
        if self.privy:
            tempind = 0
            index = -1
            while tempind < len(self.data[rowNumber]):
                try:
                    index = self.data[rowNumber][tempind].index(categoryName)
                    break
                except:
                    tempind += 1
            if index != -1:
                self.data[rowNumber][index][1] = value
        else:
            if self.load():
                self.privy = True
                self.edit_value(rowNumber, categoryName, value)

    #remove category and value from specific row
    def delete_category_and_value(self, rowNumber, category):
        if self.privy:
            if self.check_category_present(rowNumber, category):
                keyPairIndex = 0
                while keyPairIndex < len(self.data[rowNumber]):
                    if self.data[rowNumber][keyPairIndex][0] == category:
                        if len(self.data[rowNumber]) == 1:
                            break
                        else:
                            del self.data[rowNumber][keyPairIndex]
                    keyPairIndex += 1
                print(r"last item in row deleted, remember to delete row" + rowNumber)
                del self.data[rowNumber][keyPairIndex]
        else:
            if self.load():
                self.privy = True
                self.delete_category_and_value(rowNumber, category)

    #adds category to all rows
    def add_category_to_all(self, categoryName):
        if self.privy:
            rowIndex = 0
            while rowIndex < len(self.data):
                if not self.check_category_present(rowIndex, categoryName):
                    self.add_category_and_value(rowIndex, categoryName, '000null000')
                rowIndex += 1
        else:
            if self.load():
                self.privy = True
                self.add_category_to_all(categoryName)

    #adds category and value to row in table
    def add_category_and_value(self, rowNumber, category, value):
        if self.privy:
            if rowNumber == len(self.data):
                self.add_row()
            if self.check_category_present(rowNumber, category):
                print('category and value already present')
                return False
            tempObject = [category, value]
            self.data[rowNumber].append(tempObject)
            return True
        else:
            if self.load():
                self.privy = True
                return self.add_category_and_value(rowNumber, category, value)

    #returns value for category and row specified
    def get_rows_value(self, rowNumber, categoryName):
        if self.privy:
            a = 0
            if self.check_category_present(rowNumber, categoryName):
                categoryIndex = 0
                while categoryIndex < len(self.data[rowNumber]):

                    try:
                        index = self.data[rowNumber][categoryIndex].index(categoryName)
                        return self.data[rowNumber][index][1]
                    except:
                        categoryIndex += 1
                return False
            else:
                return False
        else:
            if self.load():
                self.privy = True
                return self.get_rows_value(rowNumber, categoryName)

    #lists all values of each row for a given category name
    #will have 'No Value Set' listed for a row without
    #a value for given category
    def list_values_by_category(self, categoryName):
        if self.privy:
            rowIndex = 0
            theList = []
            while rowIndex < len(self.data):
                if not self.get_rows_value(rowIndex, categoryName):
                    theList.append('No Value Set')
                else:
                    theList.append(self.get_rows_value(rowIndex, categoryName))
                rowIndex += 1
            return theList
        else:
            if self.load():
                self.privy = True
                return self.list_values_by_category(categoryName)
    #lists all categories in table
    def list_all_categories(self):
        if self.privy:
            theList = []
            rowIndex = 0
            while rowIndex < len(self.data):
                categoryIndex = 0
                while categoryIndex < len(self.data[rowIndex]):
                    categoryName = self.data[rowIndex][categoryIndex][0]
                    try:
                        theList.index(categoryName)
                    except:
                        theList.append(categoryName)
                    categoryIndex += 1
                rowIndex += 1
            return theList
        else:
            if self.load():
                self.privy = True
                return self.list_all_categories()