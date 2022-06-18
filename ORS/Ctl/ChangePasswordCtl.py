
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from service.models import User
from service.service.ChangePasswordService import ChangePasswordService
from ORS.utility.DataValidator import DataValidator
from service.service.EmailMessage import EmailMessage
from service.service.EmailService import EmailService
from service.service.UserService import UserService


class ChangePasswordCtl(BaseCtl):

    # Populate Form from http Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["newPassword"] = requestForm["newPassword"]
        self.form["oldPassword"] = requestForm["oldPassword"]
        self.form["confirmPassword"] =requestForm["confirmPassword"]

    
    # Populate Form from Model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["newPassword"] = obj.newPassword
        self.form["oldPassword"] = obj.oldPassword
        self.form["confirmPassword"] = obj.confirmPassword

    
    # Convert form into Module
    def form_to_model(self,obj):
        pk = int(self.form["id"])
        if(pk > 0):
            obj.id =pk
        obj.newPassword = self.form["newPassword"]
        obj.oldPassword = self.form["oldPassword"]
        obj.confirmPassword = self.form["confirmPassword"]
        return obj

    
    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if(DataValidator.isNull(self.form["newPassword"])):
            inputError["newPassword"] = "New Password can not be null"
            self.form["error"] =True

        if(DataValidator.isNull(self.form["oldPassword"])):
            inputError["oldPassword"] = "Old Password can not be null"
            self.form["error"] =True

        if(DataValidator.isNull(self.form["confirmPassword"])):
            inputError["confirmPassword"] = "Confirm Password can not be null"
            self.form["error"] =True
        else:
            if (self.form["newPassword"] != self.form["confirmPassword"]):
                inputError["confirmPassword"] = "oldPassword & newPassword are not match"
                self.form["error"] = True
        return self.form["error"]

    # Display change password page
    def display(self, request, params={}):
        if(params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(),{"form":self.form})
        return res
    
    # Submit of Change Password page
    def submit(self, request, params={}):
        user = request.session.get("user",None)
        print("--------------------->",user)
        q = User.objects.filter(login_id = user.login_id, password = self.form["oldPassword"])
        print("----------- change password submit login_id={} & q= {}".format(user.login_id,q))
        if q.count() > 0:
            if self.form["confirmPassword"] ==self.form["newPassword"]:
                convertUser = self.convert(user,user.id,self.form["newPassword"])
                UserService().save(convertUser)
                print("-----user.login = {} user.paasword = {}".format(user.login_id,user.password))
                emsg = EmailMessage()
                emsg.to = [user.login_id]
                emsg.subject ="Change Password"
                mailResponse = EmailService.send(emsg,"changePassword",user)
                print("------------------>",mailResponse)
                if (mailResponse==1):
                    self.form["error"] = False
                    self.form["message"] = "YOUR PASSWORD IS CHANGED SUCCESSFULLY, PLS CHECK YOUR MAIL"
                    res = render(request,self.get_template(),{"form":self.form})
                
                else:
                    self.form["error"] = True
                    self.form["message"] = "Please check your net connection"
                    res = render(request,self.get_template(),{"form":self.form})
            else:
                self.form["error"] = True
                self.form["message"] = "Confirm Password are not match"
                res = render(request,self.get_template(),{"form":self.form})
        
        else:
                self.form["error"] = True
                self.form["message"] = "old password is wrong"
                res = render(request,self.get_template(),{"form":self.form})
        return res

    
    
    def convert(self,u,uid,upass):
        u.id =uid
        u.password = upass
        return u
    
    
    
    # Template html of Change pasword page
    def get_template(self):
        return "changePassword.html"

    # service of Role
    
    
    
    def get_service(self):
        return ChangePasswordService()
