from os.path import join, dirname, abspath
from os import listdir
from datetime import datetime as dt

class LoggingFileV1:
    def __init__(self, filename):
        self.__fileName = filename
        self.__filePath = join(join(dirname(abspath(__file__)), 'log'), filename)
        if filename not in listdir(join(dirname(abspath(__file__)), 'log')):
            self.write('start server !!!', 'start-server')

    def write(self, inputLine, typeData):
        typeData = f'[{typeData.upper()}]'
        formatDate = "[%d-%m-%Y %H:%M:%S:%f]"
        strDateNow = dt.now().strftime(formatDate)
        log = f'{strDateNow}{typeData}: {inputLine}\n'
        with open(self.__filePath, 'a+') as file:
            print(log, end='')
            file.write(log)

Logger = LoggingFileV1(f'{dt.now().strftime("%d_%m_%Y")}_logFile.log')
