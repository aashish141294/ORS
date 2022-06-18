from importlib.resources import path
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from service.utility.DataValidator import DataValidator
from ORS.utility.DataValidator import DataValidator
from service.service.UserService import UserService

class LoginCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]

    
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if(DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "Login can not be null"
            self.form["error"] = True
        else:
            if(DataValidator.isemail(self.form["login_id"])):
                inputError["login_id"] = "Login should be xyz@gmail.com format"
                self.form["error"] = True
        if(DataValidator.isNull(self.form["password"])):
            inputError["password"] = "password can not be null"
            self.form["error"] = True
        return self.form["error"]

    
    def display(self, request, params={}):
        print('<---------LoginCtl Display request= {} , params = {} -------->'.format(request,params))
        self.form["out"] = params.get("out")
        res = render(request, self.get_template(),{"form":self.form})
        print("----loginCtl Display---")
        return res

    
    def submit(self,request,params={}):
        PATH = params.get('path')
        print('<---------LoginCtl Submit request= {} , params = {} -------->'.format(request,params))
        user = self.get_service().authenticate(self.form)
        if(user is None):
            self.form["error"] = True
            self.form["message"] = "Invalid Id or Password"
            res = render(request,self.get_template(),{"form":self.form})
        else:
            print("----path loginCtl.py----->",PATH)
            request.session['user'] = user
            print("----------LoginCtl submit user = {}".format(request.session['user']))
            request.session["name"] = user.role_Name
            if PATH is None: #(None,'/ORS/Home','/ORS/Login','/ORS/ForgetPassword','/ORS/Registration','/auth/Logout'):
                res = redirect('/ORS/Welcome')
            else:
                res = redirect(PATH)
        return res  
    
    
    #Template html of Login page
    def get_template(self):
        return "login.html"

    
    #Service of Login
    def get_service(self):
        return UserService()



