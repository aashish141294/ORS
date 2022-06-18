from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Marksheet
from service.forms import MarksheetForm
from service.service.MarksheetService import MarksheetService



class MarksheetCtl(BaseCtl):

    # Populate Form from http Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["rollNumber"] = requestForm["rollNumber"]
        self.form["name"] = requestForm["name"]
        self.form["physics"] = requestForm["physics"]
        self.form["chemistry"] = requestForm["chemistry"]
        self.form["maths"] = requestForm["maths"]
        
    
    # Popuate Form from Model
    def model_to_form(self, obj):
        if (obj == None):
            return None
        self.form["id"] = obj.id
        self.form["rollNumber"] = obj.rollNumber
        self.form["name"] = obj.name
        self.form["physics"] = obj.physics
        self.form["chemistry"] = obj.chemistry
        self.form["maths"] = obj.maths
        
    
    # Convert Form into Module
    def form_to_model(self, obj):
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.rollNumber = self.form["rollNumber"]
        obj.name = self.form["name"]
        obj.physics = self.form["physics"]
        obj.chemistry = self.form["chemistry"]
        obj.maths = self.form["maths"]
        return obj

    
    # Validate Form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["rollNumber"])):
            inputError["rollNumber"]= " Roll Number can not be null"
        else:
            if (DataValidator.ischeckroll(self.form["rollNumber"])):
               inputError["rollNumber"] = "RollNumber should be capital & alphanumeric"
               self.form["error"] = True

        if (DataValidator.isNull(self.form["name"])):
            inputError["name"]= " Name can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isaplhacheck(self.form["name"])):
               inputError["name"] = "Name consider only alphabates"
               self.form["error"] = True

        if (DataValidator.isNull(self.form["physics"])):
            inputError["physics"]= " Physics can not be null"
            self.form["error"] = True
            if (DataValidator.ischeck(self.form["physics"])):
               inputError["physics"] = "Please enter number below 100"
               self.form["error"] = True

        if (DataValidator.isNull(self.form["chemistry"])):
            inputError["chemistry"]= " Chemistry can not be null"
            self.form["error"] = True
            if (DataValidator.ischeck(self.form["chemistry"])):
               inputError["chemistry"] = "Please enter number below 100"
               self.form["error"] = True

        if (DataValidator.isNull(self.form["maths"])):
            inputError["maths"]= " Maths can not be null"
            self.form["error"] = True
            if (DataValidator.ischeck(self.form["maths"])):
               inputError["maths"] = "Please enter number below 100"
               self.form["error"] = True
        return self.form["error"]

    # Display Marksheet page
    def display(self, request, params={}):
        if (params["id"] > 0):
            r= self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(),{"form":self.form,})
        return res

    # Submit Marksheet page
    def submit(self,request,params={}):
        if params["id"] >0 :
            pk = params["id"]
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(rollNumber = self.form["rollNumber"])
            if dup.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Rollnumber already exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Marksheet())
                self.get_service().save(r)
                self.form["error"] = False
                self.form["message"] = "DATA is SUCCESSFULLY UPDATED"
                res = render(request,self.get_template(),{"form":self.form})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(rollNumber = self.form["rollNumber"])
            if duplicate.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Rollnumber already exists"
                res = render(request, self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Marksheet())
                self.get_service().save(r)
                self.form["id"] =r.id
                self.form["error"] = False
                self.form["message"] ="DATA is SUCCESSFULLY SAVED"
                res = render(request,self.get_template(),{"form":self.form})
            return res

    
    # Template  html of Marksheet page
    def get_template(self):
        return "marksheet.html"
        
    
    # servive of Marksheet
    def get_service(self):
        return MarksheetService()