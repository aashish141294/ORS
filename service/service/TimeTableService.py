
from service.models import TimeTable
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Student business logics.
'''

class TimeTableService(BaseService):
    def preload(self, rid):
        pass
   
   
    def search(self,params):
        print("pageNo -->",params["pageNo"])
        pageNo =(params["pageNo"]-1)*self.pageSize
        sql = "Select * from sos_timetable where 1=1"
        val = params.get("semester",None)
        if DataValidator.isNotNUll(val):
            sql+= " and semester=  '"+val+"'  "
        sql+=" limit %s,%s"
        cursor =connection.cursor()
        print("-->",sql,params["pageNo"],self.pageSize)
        cursor.execute(sql,[pageNo,self.pageSize])
        result = cursor.fetchall()
        params["index"] = ((params["pageNo"]-1)*self.pageSize)+1
        columnName = ("id","examTime","examDate","subject_ID","subjectName","course_ID","courseName","semester")
        res = {
            "data":[]
        }
        count = 0
        for x in result:
            print("--------------->",x)
            params["MaxId"] = x[0]
            print({columnName[i] : x[i] for i, _ in enumerate(x)})
            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res
    

    def get_model(self):
        return TimeTable
