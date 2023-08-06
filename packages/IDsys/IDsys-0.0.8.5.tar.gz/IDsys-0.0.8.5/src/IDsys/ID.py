class IdSys:
    def __init__(self, idLength=4):
        self.idLength = idLength
        self.ids = 0
        self.definedIds = []
        self.elements = []
        self.type = "IdSys"

    def idExist(self, id):
        if id >= 0 and id <= self.ids:
            return True
        else:
            for definedId in self.definedIds:
                if id == definedId:
                    return True
        return False

    def setId(self, obj, definedID):
        if definedID == None:
            myIdTmp = str(self.ids)
            if not self.idExist(myIdTmp):
                nbZero = self.idLength - len(myIdTmp)
                myId = ""
                for i in range(nbZero):
                    myId += "0"
                myId += myIdTmp
                return
            self.ids += 1
            self.setId(self, obj, definedID)

        else:
            if not self.idExist(definedID):
                self.definedIds.append(definedID)
                if definedID >= 0:
                    myIdTmp = str(definedID)
                    nbZero = self.idLength - len(myIdTmp)
                    myId = ""
                    for i in range(nbZero):
                        myId += "0"
                    myId += myIdTmp
                else:
                    myId = definedID
            else:
                print("This id already exist")

        self.elements.append(obj)

        return myId

    def getElement(self, myId):
        return self.elements[int(myId)]

    def getElements(self):
        elements = []
        for i in range(len(self.elements)):
            elements.append(self.getElement(i).type)
        return elements


class Element:
    def __init__(self, idSys, definedID=None):
        self.idSys = idSys
        self.myId = self.idSys.setId(self, definedID)
        self.type = self.__class__.__name__


class ObjectExemple(Element):
    isObj = True

    def __init__(self, idSys):
        super().__init__(idSys, definedID=None)
        self.nb = None
