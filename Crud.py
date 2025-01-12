"""
subclass JSONEncoder and custom Decoder get in: https://pynative.com/python-serialize-datetime-into-json/
"""

import json, os, datetime, sys
import dateutil.parser
from json import JSONEncoder
from tkinter.filedialog import askdirectory


# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()# subclass JSONEncoder
            
# custom Decoder
def DecodeDateTime(empDict):
   if 'joindate' in empDict:
      empDict["joindate"] = dateutil.parser.parse(empDict["joindate"])
      return empDict


class Crud:

    def __init__ (self):
        self.filesPath = askdirectory(initialdir="C:\\Users\\kauxb\\OneDrive\\Documents\\GitHub\\muon-data-visualiser",
                                      title='Select Folder')
        if self.filesPath == '':
            sys.exit()


    # CRUD BACKUP
    def createBackup(self):
        arquivo = open(self.filesPath + '/backupData.json', "w")
        arquivo.write("{\n}")
        arquivo.close()

    def loadBackup(self):
        with open(self.filesPath + '/backupData.json', 'r') as file:
            backupData = json.loads(file, object_hook=DecodeDateTime) # https://pynative.com/python-serialize-datetime-into-json/
            return backupData

    def saveBackup (self, backupData):

        jsonArray = []
        jsonArray.append(backupData.__dict__) # https://www.youtube.com/watch?v=YfjijpDUwUk

        with open(self.filesPath + '/backupData.json', 'w') as file:
            json.dump(jsonArray, file, ensure_ascii=False, indent=4, cls=DateTimeEncoder) # https://pynative.com/python-serialize-datetime-into-json/


    # CRUD SETTINGS
    def createSettings(self):
        if not os.path.exists(self.filesPath + '/settings.json'):
            arquivo = open(self.filesPath + '/settings.json', "w")
            arquivo.write('{}') # set de configuração padrão
            arquivo.close()

    def loadSettings (self):
        with open(self.filesPath + '/settings.json', 'r') as file:
            settings = json.load(file)
            return settings

    def saveSettings (self, settings):

        jsonArray = [] # https://www.youtube.com/watch?v=YfjijpDUwUk
        jsonArray.append(settings.__dict__)

        with open(self.filesPath + '/settings.json', 'w') as file:
            json.dump(jsonArray, file, ensure_ascii=False, indent=4)
