from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import FacultyForm
from service.models import Faculty
from service.service.AddFacultyService import AddFacultyService


class AddFacultyListCtl(BaseCtl):
    count=1
    def request_to_form(self, requestForm):
        self.form["firstName"] = requestForm.get("firstName",None)
        self.form["lastName"] = requestForm.get("lastName",None)
        self.form["email"] = requestForm.get("email",None)
        self.form["password"] = requestForm.get("password",None)
        self.form["address"] = requestForm.get("address",None)
        self.form["gender"] = requestForm.get("gender",None)
        self.form["dob"] = requestForm.get("dob",None)
        self.form["college_ID"] = requestForm.get("college_ID",None)
        self.form["subject_ID"] = requestForm.get("subject_ID",None)
        self.form["subjectName"] = requestForm.get("subjectName",None)
        self.form["course_ID"] = requestForm.get("course_ID",None)
        self.form["courseName"] = requestForm.get("courseName",None)
        self.form["ids"] = requestForm.getlist("ids",None)
        
    
    # Display Faculty Page
    def display(self, request, params={}):
        print("--------------addFacultyList Display params={} request= {} form ={} -----".format(params,request,self.form))
        AddFacultyListCtl.count = self.form["pageNo"]
        print("--addFacultyListCtl Display .count = ",AddFacultyListCtl.count)
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form["LastId"] = Faculty.objects.last().id
        print("-------------addfacultyList self.form[LastId] = {}-------".format(self.form["LastId"]))
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res
    
    
    def next(self,request,params={}):
        AddFacultyListCtl.count+=1
        self.form["pageNo"] = AddFacultyListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form["LastId"] = Faculty.objects.last().id
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    
    def previous(self,request,params={}):
        AddFacultyListCtl.count-=1
        self.form["pageNo"] = AddFacultyListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    
    def submit(self,request,params={}):
        # self.request_to_form(request.POST)
        AddFacultyListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        if self.page_list == []:
            self.form["msg"] = "No record found"
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    # Template html of Faculty page
    def get_template(self):
        return "addFacultyList.html"
    # Service of Faculty
    
    
    def get_service(self):
        return AddFacultyService()

    
    def deleteRecord(self, request, params={}):
        # AddFacultyListCtl.count = self.form["pageNo"]
        self.form["pageNo"] = AddFacultyListCtl.count
        
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
                        AddFacultyListCtl.count = 1
                        self.page_list =record["data"]
                        self.form["LastId"] = Faculty.objects.last().id
                        self.form["error"] = False
                        self.form["message"] = "Data id successfully deleted"
                        print("pppppppppppp-->",self.page_list)
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})

                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
            return res


