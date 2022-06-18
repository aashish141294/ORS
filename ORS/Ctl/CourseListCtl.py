
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import CourseForm
from service.models import Course
from service.service.CourseService import CourseService


class CourseListCtl(BaseCtl):
    count = 1
    
    def request_to_form(self, requestForm):
        self.form["courseName"] = requestForm.get("courseName",None)
        self.form["courseDescription"] = requestForm.get("courseDescription",None)
        self.form["courseDuration"] = requestForm.get("courseDuration",None)
        self.form["ids"] = requestForm.getlist("ids",None)
        
    
    def display(self, request, params={}):
        CourseListCtl.count = self.form["pageNo"]
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form["LastId"] = Course.objects.last().id
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res
    
    
    def next(self,request,params={}):
        CourseListCtl.count+=1
        self.form["pageNo"] = CourseListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form["LastId"] = Course.objects.last().id
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    
    def previous(self,request,params={}):
        CourseListCtl.count-=1
        self.form["pageNo"] = CourseListCtl.count
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

    
    # Template of course
    def get_template(self):
        return "courseList.html"

    
    # Service of course
    def get_service(self):
        return CourseService()

    
    def deleteRecord(self, request, params={}):
        # CourseListCtl.count = self.form["pageNo"]
        self.form["pageNo"] = CourseListCtl.count
        
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
                        CourseListCtl.count = 1
                        self.form["LastId"] = Course.objects.last().id
                        self.form["error"] = False
                        self.form["message"] = "Data id successfully deleted"
                        print("pppppppppppp-->",self.page_list)
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})

                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
            return res


