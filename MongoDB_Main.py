from databaseconfig import Databaseconfig
import databaseconfig as dbc
import json
class Document:

    def __init__(self):
        connection = Databaseconfig()
        connection.connect()
        self.db = dbc.client ["Arima"]

    def DB_Write(self, data, col):
        parameter = data
        collection = self.db[col]
        collection.insert_one(parameter)


    def DB_Read(self,col):
        collection = self.db[col]
        v = collection.find()
        list = []
        for i in v:
            value = i
            list.append(value)
        print(list)
        return list

    def Read_Document(self, col, DeviceID):
        collection = self.db[col]
        myquery = { 'DeviceID': DeviceID }
        x = collection.find_one(myquery)
        # print(updatedCount, "documents updated.")
        return x
    
    def Write_Document(self, col, DeviceID, data):
        collection = self.db[col]
        myquery = { 'DeviceID': DeviceID }
        x = collection.replace_one(myquery, data)
        updatedCount = x.matched_count
        # print(updatedCount, "documents updated.")
        return updatedCount

