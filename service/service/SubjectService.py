from sqlite3 import Cursor
from service.models import Subject
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Course business logics.
'''

class SubjectService(BaseService):
    def get_model(self):
        return Subject
    
    
    def search(self,params):
        pageNo =(params["pageNo"]-1)*self.pageSize
        sql = "select * from sos_subject where 1=1"
        val = params.get("subjectName",None)
        if DataValidator.isNotNUll(val):
            sql+=" and subjectName =  '"+val+"'  "
        sql+=" limit %s,%s"
        cursor =connection.cursor()
        print("---------->",sql,params["pageNo"],self.pageSize)
        cursor.execute(sql,[pageNo,self.pageSize])
        result = cursor.fetchall()
        params["index"] = ((params["pageNo"]-1)*self.pageSize)+1
        columnName = ("id","subjectName","subjectDiscription","dob","course_ID","courseName")
        res = {
            "data":[]
        }
        count = 0
        for x in result:
            params["MaxId"] = x[0]
            print({columnName[i] : x[i] for i, _ in enumerate(x)})
            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res
