#!/usr/bin/env python3

import os

class Filer():
    """
    DESCRIPTION
    """
    
    def __init__(self, stringToRemove, directory=None, file=None):
        self.__oldFilenames: list = []
        self.__newFilenames: list = []
        self.stringToRemove: str = stringToRemove
        self.directory: str = os.path.abspath(directory)
        self.__getAllFilenames()

    def __getFileFullPath(self, filename):
        return self.directory + os.path.sep + filename

    def __getAllFilenames(self) -> None:
        for item in os.listdir(self.directory):
            if os.path.isfile(self.__getFileFullPath(item)):
                self.__oldFilenames.append(item)

    def __removeStringFromSingleFile(self, string: str, filename: str) -> str:
        return filename.replace(string, '')

    def start(self):
        for filename in self.__oldFilenames:
            self.__newFilenames.append(
                self.__removeStringFromSingleFile(self.stringToRemove, filename))

        for i in range(len(self.__oldFilenames)):
            os.rename(self.directory + os.path.sep +
                      self.__oldFilenames[i], self.directory + os.path.sep + self.__newFilenames[i])