from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ORS.utility.DataValidator import DataValidator
from service.models import Subject
from service.forms import SubjectForm
from service.service.SubjectService import SubjectService
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService

class SubjectCtl(BaseCtl):

    def preload(self,request):
        self.page_list = CourseService().preload(self.form)
        self.preload_data = self.page_list


    # Populate Form from http Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["subjectName"] = requestForm["subjectName"]
        self.form["subjectDiscription"] = requestForm["subjectDiscription"]
        self.form["course_ID"] = requestForm["course_ID"]

        
    # Popuate Form from Model
    def model_to_form(self, obj):
        if (obj == None):
            return None
        self.form["id"] = obj.id
        self.form["subjectName"] = obj.subjectName
        self.form["subjectDiscription"] = obj.subjectDiscription
        self.form["course_ID"] = obj.course_ID
        # self.form["courseName"] = CourseService().find_by_unique_key(self.form['course_ID']).courseName
        self.form["courseName"] =obj.courseName

    
    # Convert Form into Module
    def form_to_model(self, obj):
        c = CourseService().get(self.form["course_ID"])
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.subjectName = self.form["subjectName"]
        obj.subjectDiscription = self.form["subjectDiscription"]
        obj.course_ID = self.form["course_ID"]
        obj.courseName = c.courseName
        return obj
        
    
    # Validate Form
    def input_validation(self):
        super().input_validation
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["subjectName"])):
            inputError["subjectName"]= " Subject Name can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isaplhacheck(self.form["subjectName"])):
               inputError["subjectName"] = "Subject Name consider only alphabates"
               self.form["error"] = True
               
        if (DataValidator.isNull(self.form["subjectDiscription"])):
            inputError["subjectDiscription"] = "Subject Discription can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "Course Name can not be null"
            self.form["error"] = True
        else:
            x = CourseService().find_by_unique_key(self.form['course_ID'])
            self.form["courseName"] = x.courseName
        return self.form["error"]
        
  
    # Display subject page
    def display(self, request, params={}):
        if (params["id"] > 0):
            r= self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(),{"form":self.form,"collegeList":self.preload_data})
        return res

    
    # Submit Subject page
    def submit(self,request,params={}):
        if params["id"] >0 :
            pk = params["id"]
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(subjectName = self.form["subjectName"])
            if dup.count() > 0: 
                self.form["error"] = True
                self.form["message"] = "Subject Name already exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Subject())
                self.get_service().save(r)
                self.form["error"] = False
                self.form["message"] = "DATA is SUCCESSFULLY UPDATED"
                res = render(request,self.get_template(),{"form":self.form,"collegeList":self.preload_data})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(subjectName = self.form["subjectName"])
            if duplicate.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Subject name already exists"
                res = render(request, self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Subject())
                self.get_service().save(r)
                self.form["id"] =r.id
                self.form["error"] = False
                self.form["message"] ="DATA is SUCCESSFULLY SAVED"
                res = render(request,self.get_template(),{"form":self.form,"collegeList":self.preload_data})
            return res

    
    # Template  html of Subject page
    def get_template(self):
            return "subject.html"
        
    
    # servive of subject
    def get_service(self):
            return SubjectService()