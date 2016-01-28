#!../venv/bin/python

class Offset(object):
    line=0
    start=0
    size=0

    def __init__(self, line=0, start=0, size=0):
        self.line=line
        self.start=start
        self.size=size

class DiffResult(object):

    result = ""
    offsets=list()
    left=""
    right=""

    def __init__(self, result="", decodedleft="", decodedright=""):
        self.result = result
        self.offsets = list()
        self.decodedleft=""
        self.decodedright=""


    def __str__(self):
        #check the result
        if (self.decodedleft == self.decodedright):
            return self.GetEqualResultMsg()

        elif (len(self.decodedleft) != len(self.decodedright)):
            return self.GetDifferentSizeMsg()

        else:
            return self.GetEqualSizeDiffResultMsg()

    def GetEqualResultMsg(self):
        #Set the default message for equal
        json_string='{ "jsondiffer": ' \
                    '{ "sizeleft": ' + len(self.decodedleft).__str__() + \
                    ', "sizeright": ' + len(self.decodedright).__str__() + \
                    ', "result": "left and right are equal" } }'

        return json_string

    def GetDifferentSizeMsg(self):
        #Set the default message for different size
        json_string='{ "jsondiffer": ' \
                    '{ "sizeleft": ' + len(self.decodedleft).__str__() + \
                    ', "sizeright": ' + len(self.decodedright).__str__() + \
                    ', "result": "sizes are different" } }'

        return json_string

    def GetEqualSizeDiffResultMsg(self):
        #Set the default message for equal

        offset = Offset()
        offsets_string = '"offsets": { '


        for offset in self.offsets:
            offsets_string = offsets_string + '"offset": { "line":' + str(offset.line) + ', "start":' + str(offset.start) + ', "size":' + str(offset.size) + ' },'
        print

        json_string='{ "jsondiffer": ' \
                    '{ "sizeleft": ' + len(self.decodedleft).__str__() + \
                    ', "sizeright": ' + len(self.decodedright).__str__() + \
                    ', "result": "Sizes are equal but contents different",' + offsets_string[:-1] + '} } } ' #remove the last ,

        return json_string

