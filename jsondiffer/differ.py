#!../venv/bin/python

import json
import base64
import difflib

from diffresult import Offset, DiffResult


class Differ(object):
    #
    #left and right are handle args that will be encoded
    left=""
    right=""

    #
    #docodedleft and decodedright are internal args used for validations/processing
    #
    decodedleft=""
    decodedright=""

    #Set the constructor
    def __init__(self, left="", right="", decodedleft="", decodedright=""):
        self.left = left
        self.right = right
        self.decodedleft = decodedleft
        self.decodedright = decodedright

    #function to decode json from base64
    def decode(self):
        self.decodedright=base64.b64decode(self.right)
        self.decodedleft=base64.b64decode(self.left)

    #functions to validate if JSONs are valid
    def isLeftValid(self):
        try:
            #Ensure the json will be decoded first
            self.decode()

            #try to load the json to check whether or not it is valid
            json.loads(self.decodedleft)

            return "true"
        except: # catch *all* exceptions
            return "false"

    def isRightValid(self):
        try:
            #Ensure the json will be decoded first
            self.decode()

            #try to load the json to check whether or not it is valid
            json.loads(self.decodedright)

            return "true"
        except: # catch *all* exceptions
            return "false"

    def getState(self):
        #set the defaults of return
        #this will be used to control the status of the requests in the index screen

        rcleft=""
        rcright=""

        if self.left == "":
            rcleft="2"
        elif self.isLeftValid() == "false":
            rcleft="1"
        else:
            rcleft="0"

        if self.right == "":
            rcright="2"
        elif self.isRightValid() == "false":
            rcright="1"
        else:
            rcright="0"

        # 22 - left empty, right empty
        # 21 - left empty, right invalid
        # 20 - left empty, right valid
        # 12 - left invalid, right empty
        # 11 - left invalid, right invalid
        # 10 - left invalid, right valid
        # 02 - left valid, right empty
        # 01 - left valid, right invalid
        # 00 - left valid, right valid :)

        return rcleft + rcright

    #function to check for differences
    def Diff(self):

        #Validate if the Diff may proceed (Both JSONs must be valid)
        if self.isLeftValid() == "false":
            return "Left is not a valid JSON"
        elif self.isRightValid() == "false":
            return "Right is not a valid JSON"

        diffInstance = difflib.Differ()
        diffList = list(diffInstance.compare(self.decodedleft.splitlines(), self.decodedright.splitlines()))

        bytesread = 0
        count = 1

        #Create a new Diff Result
        #Set decoded values for comparison laters
        diffresult = DiffResult()
        diffresult.decodedleft = self.decodedleft
        diffresult.decodedright = self.decodedright

        #only compare offsets if contents are different and size is the same
        if (self.left != self.right) and (len(self.decodedleft) == len(self.decodedright)):
            #Initiate a new Offset
            offset = Offset()

            #Save the differences in a list of offset
            for line in diffList:

                #if it found a difference
                if line[0] == '?':
                    offset.line= count - (len(diffresult.offsets) +1 )
                    offset.start = bytesread + line.index('^')
                    offset.size = line.count('^')

                    #add the offset in the list
                    diffresult.offsets.append(Offset(offset.line, offset.start, offset.size))

                #sum total of bytes read to calculate the offset position
                bytesread=bytesread+len(line)
                #sum the number of lines read
                count=count+1

            print

        #Unfortunately, all the attempts to serialize the list in JSON have failed..
        #I will try it more in a future version
        #For now, I will proceed with a not elegant way to convert it into JSON

        return diffresult.__str__()

