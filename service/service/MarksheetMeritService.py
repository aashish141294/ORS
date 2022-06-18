from service.models import Faculty, Marksheet
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Role business logics.
'''

class MarksheetMeritService(BaseService):

    def search(self,params):
        sql= "select id, rollNumber, name, physics, chemistry, maths, (physics+chemistry+maths) as Total, (physics+chemistry+maths)/3 as Percentage from sos_marksheet where physics>33 and chemistry>33 and maths>33 order by Percentage desc limit 0,10;"
        cursor =connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        print("--------MeritMarksheet result------->",result)
        params["index"] = ((params["pageNo"]-1)*self.pageSize)+1
        columnName =("id","rollNumber","name","physics","chemistry","maths","Total","Percentage")
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





