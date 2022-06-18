from.BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from service.utility.DataValidator import DataValidator
from ORS.utility.DataValidator import DataValidator
from service.service.ForgetPasswordService import ForgetPasswordService
from service.service.EmailService import EmailService
from service.service.EmailMessage import EmailMessage
from service.models import User

class ForgetPasswordCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["login_id"] =  requestForm["login_id"]

    
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if(DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "Login can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isemail(self.form["login_id"])):
                inputError["login_id"] = "Login id must be in abc@gmail.com format"
                self.form["error"] = True
        return self.form["error"]

    
    def display(self, request, params={}):
        res = render(request,self.get_template())
        return res

    
    def submit(self, request, params={}):
        if self.input_validation():
            return render(request, self.get_template(),{"form":self.form})
        else:
            q = User.objects.filter(login_id = self.form["login_id"])
            userList = ""
            for userData in q:
                userList = userData
            if userList != "":
                emsg = EmailMessage()
                emsg.to =[userList.login_id]
                emsg.subject = "Forget Password"
                mailResponse = EmailService.send(emsg, "ForgetPassword",userList)
                if mailResponse == 1:
                    self.form["error"] = False
                    self.form["message"] = "PLEASE CHECK YOUR MAIL, YOUR PASSWORD IS SEND SUCCESSFULLY"
                    res = render(request, self.get_template(),{"form":self.form})
                else:
                    self.form["error"] =True
                    self.form["message"] = "Please Check Your Internet Connection"
                    res = render(request,self.get_template(),{"form":self.form})
            else:
                self.form["error"] =True
                self.form["message"] = "login id is not correct"
                res = render(request, self.get_template(), {"form": self.form})
        return res

    
    #Template html of Forget Password page
    def get_template(self):
        return "forgetPassword.html"

    
    # Service of Forget Password Page
    def get_service(self):
        return ForgetPasswordService()

