from service.models import Faculty
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Student business logics.
'''

class AddFacultyService(BaseService):
    
    def get_model(self):
        return Faculty
    
    
    def preload(self, params):
        pass

    
    def search(self,params):
        print("Params[pageNO] ={} --->".format(params["pageNo"]))
        pageNo = (params["pageNo"]-1)*self.pageSize
        sql = "select * from sos_faculty where 1=1"
        val = params.get("firstName",None)
        if DataValidator.isNotNUll(val):
            sql+=" and firstName = '"+val+"' "
        sql+=" limit %s,%s"
        cursor = connection.cursor()
        print("--------------val--------->",val)
        cursor.execute(sql,[pageNo,self.pageSize])
        print("----addfacultyList pageno,pagesize------->",sql,pageNo,self.pageSize)
        result = cursor.fetchall()
        params["index"] = ((params["pageNo"]-1)*self.pageSize)+1
        columnName =("id","firstName","lastName","email","password","address","gender","dob","college_ID","collegeName","subject_ID","subjectName","course_ID","courseName")
        res = {
            "data":[]
        }
        # print("------------result-------->",result)
        count = 0   
        for x in result:
            params["MaxId"] = x[0]
            print("-------------addFacultyService params[MaxId] = {}-------".format(params["MaxId"]))
            print({columnName[i] : x[i] for i, _ in enumerate(x)})
            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        # print("-----res---->",res)
        return res