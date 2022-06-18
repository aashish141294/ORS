from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Course, College
from service.forms import CollegeForm
from service.service.CourseService import CourseService

class CourseCtl(BaseCtl):
    # Populate Form from http Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["courseName"] = requestForm["courseName"]
        self.form["courseDescription"] = requestForm["courseDescription"]
        self.form["courseDuration"] = requestForm["courseDuration"]

    
    def next(self,request,params={}):
        pass
        
    
    # Popuate Form into Model
    def model_to_form(self, obj):
        if (obj == None):
            return None
        self.form["id"] = obj.id
        self.form["courseName"] = obj.courseName
        self.form["courseDescription"] = obj.courseDescription
        self.form["courseDuration"] = obj.courseDuration
        
    
    # Convert Form into Module
    def form_to_model(self, obj):
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.courseName = self.form["courseName"]
        obj.courseDescription = self.form["courseDescription"]
        obj.courseDuration = self.form["courseDuration"]
        return obj
        
    # Validate Form
    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["courseName"])):
            inputError["courseName"]= " Course Name can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isaplhacheck(self.form["courseName"])):
               inputError["courseName"] = "Course Name consider only alphabates"
               self.form["error"] = True
        
        if (DataValidator.isNull(self.form["courseDescription"])):
            inputError["courseDescription"] = "Course Description can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["courseDuration"])):
            inputError["courseDuration"] = "Course Duration can not be null"
            self.form["error"] = True
        return self.form["error"]
        
        
        
    # Display college page
    def display(self, request, params={}):
        if (params["id"] > 0):
            r= self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(),{"form":self.form})
        return res

    
    # Submit course page
    def submit(self,request,params={}):
        if params["id"] >0 :
            pk = params["id"]
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(courseName = self.form["courseName"])
            if dup.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Course Name already exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Course())
                self.get_service().save(r)
                self.form["error"] = False
                self.form["message"] = "DATA is SUCCESSFULLY UPDATED"
                res = render(request,self.get_template(),{"form":self.form})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(courseName = self.form["courseName"])
            if duplicate.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Course Name already exists"
                res = render(request, self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Course())
                self.get_service().save(r)
                self.form["id"] =r.id
                self.form["error"] = False
                self.form["message"] ="DATA is SUCCESSFULLY SAVED"
                res = render(request,self.get_template(),{"form":self.form})
            return res

    
    
    # Template  html of course page
    def get_template(self):
            return "course.html"
        
    
    
    # Servive of course
    def get_service(self):
            return CourseService()