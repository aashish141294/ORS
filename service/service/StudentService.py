from service.models import Role, Student
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


'''
It contains Role business logics.
'''

class StudentService(BaseService):
    def search(self,params):
        print("page No -->",params["pageNo"])
        pageNo = (params["pageNo"]-1)*self.pageSize
        sql ="select * from sos_student where 1=1"
        val = params.get("collegename", None)
        if DataValidator.isNotNUll(val):
            sql+=" and collegename = '"+val+"' "
        sql+=" limit %s , %s"
        cursor = connection.cursor()
        print("--------------->",sql,params["pageNo"],self.pageSize)
        cursor.execute(sql, [pageNo,self.pageSize])
        result = cursor.fetchall()
        params["index"] = ((params["pageNo"]-1)*self.pageSize)+1
        columnName =("id","firstName","lastName","dob","mobileNumber","email","college_ID","collegeName")
        res = {
            "data":[]
        }
        count=0
        for x in result:
            params["MaxId"] = x[0]
            print({columnName[i] :x[i] for i, _ in enumerate(x)})
            res["data"].append({columnName[i] : x[i] for i, _ in enumerate(x)})
        return res
    
 
    def get_model(self):
        return Student






