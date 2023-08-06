class IdSys:
    def __init__(self):
        self.idLength = 4
        self.ids = 0
        self.elements = []
        # self.myId = self.setId(self)
        self.type = "IdSys"

    def setId(self, obj):
        myIdTmp = str(self.ids)
        nbZero = self.idLength - len(myIdTmp)
        myId = ""
        for i in range(nbZero):
            myId += "0"
        myId += myIdTmp
        self.ids += 1
        self.elements.append(obj)
        print(myId)

        return myId

    def getElement(self, myId):
        return self.elements[int(myId)]

    def getElements(self):
        elements = []
        for i in range(len(self.elements)):
            elements.append(self.getElement(i).type)
        return elements


class Element:
    def __init__(self, idSys):
        self.idSys = idSys
        self.myId = self.idSys.setId(self)
        self.type = self.__class__.__name__


class ObjectExemple(Element):
    isObj = True
