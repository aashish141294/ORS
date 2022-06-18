from sqlite3 import Cursor
from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains User business logics.
'''
class UserService(BaseService):
   
    def authenticate(self,params):
        userList = self.search2(params)
        print("----USerservice authenticate params = {} ,userList = {} -----".format(params,userList)) 
        if (userList.count() == 1):
            return userList[0]
        else:
            return None

    
    def search2(self,params):
        q = self.get_model().objects.filter()
        print("----userService search2 q ={}----".format(q))

        val = params.get("login_id", None)
        if(DataValidator.isNotNUll(val)):
            q= q.filter(login_id = val)

        val =params.get("password", None)
        if(DataValidator.isNotNUll(val)):
            q =q.filter(password = val)
        return q

    
    def search(self ,params):
        print("----userservice search(self)={} ,params = {}".format(self,params))
        pageNo = (params["pageNo"]-1)*self.pageSize
        print("--params[page]--->",params["pageNo"])
        sql = "Select * from sos_user where 1=1"
        val = params.get("login_id",None)
        # val2 = params.get("firstName",None)
        # print("------------val2",val2 )
        if DataValidator.isNotNUll(val):
            sql+= " and login_id = '"+val+"' "
                
        sql+=" limit %s,%s"
        cursor = connection.cursor()
        cursor.execute(sql,[pageNo,self.pageSize])
        print("----userList pageno,pagesize------->",sql,pageNo,self.pageSize)
        result = cursor.fetchall()
        params["index"] = ((params["pageNo"]-1)*self.pageSize)+1
        # print("-------result of userService---->",result)
        columnName = ("id","firstName","lastName","login_id","password", "confirmpassword","dob","address","gender","mobilenumber","role_Id","role_Name")

        res = {
            "data":[]
        }
        count = 0
        for x in result:
            params["MaxId"] = x[0]
            print("-------------userService params[MaxId] = {}-------".format(params["MaxId"]))
            print("---userServive for loop--->",{columnName[i] : x[i] for i, _ in enumerate(x)})
            res["data"].append({columnName[i] : x[i] for i, _ in enumerate(x)})

        return res
    
    
    def get_login_id(self,login_id):
        self.get_model().objects.all()

    
    def get_model(self):
        return User
