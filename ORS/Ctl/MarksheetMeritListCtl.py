from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import Marksheet
from service.forms import MarksheetForm
from service.service.MarksheetService import MarksheetService
from service.service.MarksheetMeritService import MarksheetMeritService
from service.service.StudentService import StudentService


class MarksheetMeritListCtl(BaseCtl):
    count = 1
    def request_to_form(self, requestForm):
        self.form["rollNumber"] = requestForm.get("rollNumber",None)
        self.form["name"] = requestForm.get("name",None)
        self.form["physics"] = requestForm.get("physics",None)
        self.form["chemistry"] = requestForm.get("chemistry",None)
        self.form["maths"] = requestForm.get("maths",None)
        self.form["student_ID"] = requestForm.get("student_ID",None)
        self.form["ids"] = requestForm.getlist("ids",None)
        
    # Display Marksheet Merit List page
    def display(self, request, params={}):
        record =self.get_service().search(self.form)
        self.page_list = record["data"]
        res = render(request,self.get_template(),{"form":self.form,"pageList":self.page_list})
        return res
    
    
    # Submit Marksheet Merit List page
    def submit(self, request, params={}):
        res = render(request,self.get_template())
        return res
    
    
    # Template html of Marksheet Merit List page
    def get_template(self):
        return "marksheetMeritList.html"
    
    
    # Service of Marksheet 
    def get_service(self):
        return MarksheetMeritService()




