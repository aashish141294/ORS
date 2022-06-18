from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ORS.utility.DataValidator import DataValidator
from service.models import Student
from service.forms import StudentForm
from service.service.StudentService import StudentService
from service.service.CollegeService import CollegeService

class StudentCtl(BaseCtl):
    def preload(self, request):
        self.page_list = CollegeService().preload(self.form)
        self.preload_data = self.page_list

    
    # Populate Form from http Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["dob"] = requestForm["dob"]
        self.form["mobileNumber"] = requestForm["mobileNumber"]
        self.form["email"] = requestForm["email"]
        self.form["college_ID"] = requestForm["college_ID"]
        
    
    # Popuate Form from Model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d")
        self.form["mobileNumber"] = obj.mobileNumber
        self.form["email"] = obj.email
        self.form["college_ID"] = obj.college_ID
        self.form["collegeName"] = obj.collegeName
        # self.form["collegeName"] = CollegeService().find_by_unique_key(self.form["college_ID"]).collegeName
        
    
    # Convert Form into Module
    def form_to_model(self, obj):
        c = CollegeService().get(self.form["college_ID"])
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.dob = self.form["dob"]
        obj.mobileNumber = self.form["mobileNumber"]
        obj.email = self.form["email"]
        obj.college_ID = self.form["college_ID"]
        obj.collegeName = c.collegeName
        return obj
        
    
    # Validate Form
    def input_validation(self):
        super().input_validation
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"]= " First Name can not be null"
            self.form["error"] = True
        else:
            if(DataValidator.isaplhacheck(self.form["firstName"])):
                inputError["firstName"] = "First Name should be alphbates only"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"]= " Last Name can not be null"
            self.form["error"] = True
        else:
            if(DataValidator.isaplhacheck(self.form["lastName"])):
                inputError["lastName"] = "Last Name should be alphbates only"
                self.form["error"] = True
        
        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"]= " Date of Birth can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isDate(self.form["dob"])):
                inputError["dob"] = "Date formate should be DD-MM-YYYY "
                self.form["error"] = True

        
        if (DataValidator.isNull(self.form["mobileNumber"])):
            inputError["mobileNumber"]= " Mobile Number can not be null"
            self.form["error"] = True
        else:
            if(DataValidator.ismobilecheck(self.form["mobileNumber"])):
                inputError["mobileNumber"] = "Mobile Number should started from 6,7,8,9"
                self.form["error"] = True
        
        if (DataValidator.isNull(self.form["email"])):
            inputError["email"]= " Email can not be null"
            self.form["error"] = True
        else:
            if(DataValidator.isemail(self.form["email"])):
                inputError["email"] = "Email id should be in @gmail.com"
                self.form["error"] = True
        
        if (DataValidator.isNull(self.form["college_ID"])):
            inputError["college_ID"]= " College name can not be null"
            self.form["error"] = True
        else:
            x = CollegeService().find_by_unique_key(self.form['college_ID'])
            self.form["collegeName"] = x.collegeName
        return self.form["error"]
    
    
    # Display Student page
    def display(self, request, params={}):
        if (params["id"] > 0):
            r= self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(),{"form":self.form,"collegeList":self.preload_data})
        return res

    
    # Submit Student page
    def submit(self,request,params={}):
        if params["id"] >0 :
            pk = params["id"]
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(email = self.form["email"])
            if dup.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Email already exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Student())
                self.get_service().save(r)
                self.form["error"] = False
                self.form["message"] = "DATA is SUCCESSFULLY UPDATED"
                res = render(request,self.get_template(),{"form":self.form,"collegeList":self.preload_data})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(email = self.form["email"])
            if duplicate.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Email already exists"
                res = render(request, self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Student())
                self.get_service().save(r)
                self.form["id"] =r.id
                self.form["error"] = False
                self.form["message"] ="DATA is SUCCESSFULLY SAVED"
                res = render(request,self.get_template(),{"form":self.form,"collegeList":self.preload_data})
            return res

    
    # Template  html of Student page
    def get_template(self):
            return "student.html"
        
    
    # Servive of Student
    def get_service(self):
            return StudentService()