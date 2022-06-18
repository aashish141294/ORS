from django.shortcuts import render, redirect
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.utility.DataValidator import DataValidator
from ORS.utility.DataValidator import DataValidator
from service.models import User
from service.service.UserService import UserService
from service.service.RoleService import RoleService
from service.service.EmailService import EmailService
from service.service.EmailMessage import EmailMessage


class RegistrationCtl(BaseCtl):
    def preload(self,request):
        self.page_list = RoleService().search(self.form)
        self.preloadData = self.page_list

    
    #Populate From Http Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]
        self.form["confirmpassword"] = requestForm["confirmpassword"]
        self.form["dob"] = requestForm["dob"]
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["mobilenumber"] = requestForm["mobilenumber"]
        self.form["role_Id"] = 2
        self.form["role_Name"] = "Student"
        print("----Reg. request_to_form----")
    
    
    #populate Form from Model
    def model_to_form(self,obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["login_id"] = obj.login_id
        self.form["password"] = obj.password
        self.form["confirmpassword"] = obj.confirmpassword
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d")
        self.form["address"] = obj.address
        self.form["gender"] = obj.gender
        self.form["mobilenumber"] = obj.mobilenumber
        self.form["role_Id"] = 2
        self.form["role_Name"] = "Student"
        print("----Reg. model_to_form----")


    #Convert Form into Module
    def form_to_model(self,obj):
        pk =int(self.form["id"])
        if pk > 0:
            obj.id =pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.login_id = self.form["login_id"]
        obj.password = self.form["password"]
        obj.confirmpassword = self.form["confirmpassword"]
        obj.dob = self.form["dob"]
        obj.address = self.form["address"]
        obj.gender = self.form["gender"]
        obj.mobilenumber = self.form["mobilenumber"]
        obj.role_Id = self.form["role_Id"]
        obj.role_Name = self.form["role_Name"]
        print("----Reg. form_to_model----")
        return obj
        

    
    #Validate Form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["firstName"]):
            inputError["firstName"] = "Name can not be null"
            self.form["error"] = True
        
        if DataValidator.isNull(self.form["lastName"]):
            inputError["lastName"] = "lastName can not be null"
            self.form["error"] = True
        
        if DataValidator.isNull(self.form["login_id"]):
            inputError["login_id"] = "login_id can not be null"
            self.form["error"] = True
        else:
            if(DataValidator.isemail(self.form["login_id"])):
                inputError["login_id"] = "Login should be in xyz@gmail.com format"
                self.form["error"] = True
        
        if DataValidator.isNull(self.form["password"]):
            inputError["password"] = "password can not be null"
            self.form["error"] = True
        
        if DataValidator.isNull(self.form["confirmpassword"]):
            inputError["confirmpassword"] = "confirmpassword can not be null"
            self.form["error"] = True
        
        if DataValidator.isNotNull(self.form["confirmpassword"]):
            if self.form["password"] != self.form["confirmpassword"]:
                inputError["confirmpassword"] = " password & confirmpassword are not same"
                self.form["error"] = True
        
        if DataValidator.isNull(self.form["address"]):
            inputError["address"] = "address can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "Date of Birth can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isDate(self.form["dob"])):
                inputError["dob"] = "Date formate should be DD-MM-YYYY "
                self.form["error"] = True
        
        if (DataValidator.isNull(self.form["gender"])):
            inputError["gender"] = "Gender can not be null"
            self.form["error"] = True
        
        if DataValidator.isNull(self.form["mobilenumber"]):
            inputError["mobilenumber"] = "mobilenumber can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.ismobilecheck(self.form["mobilenumber"])):
                inputError["mobilenumber"] = "Type a digit"
                self.form["error"] = True
        
        if DataValidator.isNull(self.form["role_Id"]):
            inputError["role_Id"] = "Role name can not be null"
            self.form["error"] = True
        else:
            w = RoleService().find_by_unique_key(self.form['role_Id'])
            self.form["role_Name"] = w.name
        return self.form["error"]

    
    #Display Registration page
    def display(self,request,params={}):
        print('<---------RegistrationCtl Display request= {} , params = {} -------->'.format(request,params))
        # this if block use when call edit
        if params["id"] > 0:
            r =self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form, "roleList": self.preloadData})
        return res


    #Submit Registration page
    def submit(self,request,params={}):
        print('<---------Reg.Ctl Submit request= {} , params = {} -------->'.format(request,params))
        q = User.objects.filter()
        q = q.filter(login_id = self.form["login_id"])
        if q.count() > 0:
            self.form["error"] = True
            self.form["message"] = "Already exists"
            res = render(request, self.get_template(),{"form": self.form})
        else:
            user = request.session.get("user", None)
            emsg = EmailMessage()
            emsg.to = [self.form["login_id"]]
            e ={}
            e["login"] = self.form["login_id"]
            e["password"] = self.form["password"]
            emsg.subject = "ORS Registration Successful"
            mailResponse = EmailService.send(emsg, "signup", e)
            if mailResponse == 1:
                r = self.form_to_model(User())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "YOU HAVE REGISTERED SUCCESSFULLY"
                res = render(request, self.get_template(), {"form": self.form})
            else:
                self.form["error"] = True
                self.form["message"] = "Please Check Your Internet Connection"
                res =render(request,self.get_template(),{"form": self.form})
        return res

    
    #Template of Registration
    def get_template(self):
        return "Registration.html"

    
    #Service of Registration
    def get_service(self):
        return UserService()

