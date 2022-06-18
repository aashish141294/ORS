from sqlite3 import Cursor
from service.models import College
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contain Role business logic.
'''

class CollegeService(BaseService):
    
    def get_model(self):
        return College

    
    def search(self,params):
        pageNo = (params["pageNo"]-1) * self.pageSize
        sql = "Select * from sos_college where 1=1"
        val = params.get("collegeName",None)
        if (DataValidator.isNotNUll(val)):
            sql+= " and collegeName = '" +val + "' "
        sql+= " limit %s,%s"
        cursor = connection.cursor()
        cursor.execute(sql,[pageNo,self.pageSize])
        print("----collegeService--->",sql,pageNo,self.pageSize)
        result = cursor.fetchall()
        params["index"] = ((params["pageNo"]-1)*self.pageSize)+1
        print("----collegeService Result--->",result)
        columnName = ("id","collegeName","collegeAddress","collegeState","collegeCity","collegePhoneNumber")
        res = {
            "data" : []
        }
        count = 0
        for x in result:
            params["MaxId"] = x[0]
            print({columnName[i] : x[i] for i, _ in enumerate(x)})
            res["data"].append({ columnName[i]:x[i] for i, _ in enumerate(x)})
        return res
