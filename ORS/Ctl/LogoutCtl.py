from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from service.utility.DataValidator import DataValidator
from service.service.UserService import UserService

class LogoutCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]

    
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if(DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "Login can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True
        return self.form["error"]


    
    def display(self, request, params={}):
        request.session["user"] = None
        self.form["message"] = "Logout Successful"
        res = render(request, self.get_template(),{"form":self.form})
        return res

    
    def submit(self,request,params={}):
        pass
    
    
    #Template html of Logout page
    def get_template(self):
        return "login.html"

    
    #Service of Logout
    def get_service(self):
        return UserService








