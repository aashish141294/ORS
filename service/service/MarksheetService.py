from service.models import Faculty, Marksheet
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Role business logics.
'''

class MarksheetService(BaseService):

    def search(self,params):
        print("params[Page No] --->",params["pageNo"])
        pageNo = (params["pageNo"]-1)*self.pageSize
        sql = "Select * from sos_marksheet where 1=1"
        val = params.get("rollNumber",None)
        if DataValidator.isNotNUll(val):
            sql+=" and rollNumber = '"+val+"' "
        sql+=" limit %s,%s"
        cursor = connection.cursor()
        print("------------------------------->",val)
        print("----------------->",sql,pageNo,self.pageSize)
        cursor.execute(sql, [pageNo,self.pageSize])
        result = cursor.fetchall()
        params["index"] = ((params["pageNo"]-1)*self.pageSize)+1
        columnName =("id","rollNumber","name","physics","chemistry","maths")
        res = {
            "data":[]
        }
        count = 0
        for x in result:
            params["MaxId"] = x[0]
            print({columnName[i] : x[i] for i, _ in enumerate(x)})
            res["data"].append({columnName[i] : x[i] for i, _ in enumerate(x)})
        return res

    
    def get_model(self):
        return Marksheet





