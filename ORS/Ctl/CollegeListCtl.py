from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import CollegeForm
from service.models import College
from service.service.CollegeService import CollegeService


class CollegeListCtl(BaseCtl):
    count = 1
    def request_to_form(self, requestForm):
        self.form["collegeName"] = requestForm.get("collegeName",None)
        self.form["collegeAddress"] = requestForm.get("collegeAddress",None)
        self.form["collegeState"] = requestForm.get("collegeState",None)
        self.form["collegeCity"] = requestForm.get("collegeCity",None)
        self.form["collegePhoneNumber"] = requestForm.get("collegePhoneNumber",None)
        self.form["ids"] = requestForm.getlist("ids",None)

    
    
    def display(self, request, params={}):
        CollegeListCtl.count = self.form["pageNo"]
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form["LastId"] = College.objects.last().id
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res
    
    
    
    def next(self,request,params={}):
        CollegeListCtl.count+=1
        self.form["pageNo"] = CollegeListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form["LastId"] = College.objects.last().id
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    
    
    def previous(self,request,params={}):
        CollegeListCtl.count-=1
        self.form["pageNo"] = CollegeListCtl.count
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

    
    
    # Service of college
    def get_template(self):
        return "collegeList.html"

    
    
    def get_service(self):
        return CollegeService()

    
    
    def deleteRecord(self, request, params={}):
        # CollegeListCtl.count = self.form["pageNo"]
        self.form["pageNo"] = CollegeListCtl.count
        
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
                        CollegeListCtl.count =1
                        self.page_list =record["data"]
                        self.form["LastId"] = College.objects.last().id
                        self.form["error"] = False
                        self.form["message"] = "Data successfully deleted"
                        print("-----collegeListCtl self.page_   List-->",self.page_list)
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})

                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
            return res
