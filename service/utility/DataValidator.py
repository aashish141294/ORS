import re
class DataValidator:
    @classmethod
    def isNotNUll(aashish,val):
        if (val == None or val ==""):
            return False
        else:
            return True
    
    
    @classmethod
    def isNull(aashish, val):
        if (val == None or val ==""):
            return True
        else:
            return False

    
    @classmethod
    def isInt(self, val):
        if(val == 0):
            return False
        else:
            return True

    
    @classmethod
    def ismobilecheck(self ,val):
        if re.match("^[6-9]\d{9}$", val):
            return False
        else:
            return True