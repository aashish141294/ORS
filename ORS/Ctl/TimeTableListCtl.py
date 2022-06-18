from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import TimeTableForm
from service.models import TimeTable
from service.service.TimeTableService import TimeTableService


class TimeTableListCtl(BaseCtl):
    count = 1
    def request_to_form(self, requestForm):
        self.form["examTime"] = requestForm.get("examTime",None)
        self.form["examDate"] = requestForm.get("examDate",None)
        self.form["subject_ID"] = requestForm.get("subject_ID",None)
        self.form["subjectName"] = requestForm.get("subjectName",None)
        self.form["course_ID"] = requestForm.get("course_ID",None)
        self.form["courseName"] = requestForm.get("courseName",None)
        self.form["semester"] = requestForm.get("semester",None)
        self.form["ids"] = requestForm.getlist("ids",None)

    
    def display(self, request, params={}):
        TimeTableListCtl.count = self.form["pageNo"]
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form["LastId"] = TimeTable.objects.last().id
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res
    
    
    def next(self,request,params={}):
        TimeTableListCtl.count+=1
        self.form["pageNo"] = TimeTableListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form["LastId"] = TimeTable.objects.last().id
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    
    def previous(self,request,params={}):
        TimeTableListCtl.count-=1
        self.form["pageNo"] = TimeTableListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    
    def submit(self,request,params={}):
        self.request_to_form(request.POST)
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        if self.page_list == []:
            self.form["msg"] = "No record found"
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    
    # Template of Time Table List
    def get_template(self):
        return "TimeTableList.html"

    
    # Service of Time Table List
    def get_service(self):
        return TimeTableService()

    
    def deleteRecord(self, request, params={}):
        # TimeTableListCtl.count = self.form["pageNo"]
        self.form["pageNo"] = TimeTableListCtl.count
        if(bool(self.form["ids"])==False):
            record = self.get_service().search(self.form)
            self.page_list = record["data"]
            self.form["error"] = True
            self.form["message"] = "Please select at least one check box"
            return render(request, self.get_template(),{"pageList":self.page_list,"form":self.form})
        else:
            for ids in self.form["ids"]:
                record = self.get_service().search(self.form)
                self.page_list = record["data"]

                id =int(ids)
                if(id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form["pageNo"] = 1
                        record = self.get_service().search(self.form)
                        self.page_list =record["data"]
                        TimeTableListCtl.count = 1
                        self.form["LastId"] = TimeTable.objects.last().id
                        self.form["error"] = False
                        self.form["message"] = "Data id successfully deleted"
                        print("pppppppppppp-->",self.page_list)
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})

                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
            return res

