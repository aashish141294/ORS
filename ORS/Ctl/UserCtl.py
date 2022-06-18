from this import d
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ORS.utility.DataValidator import DataValidator
from service.models import User
from service.service.UserService import UserService
from service.service.RoleService import RoleService

class UserCtl(BaseCtl):

    def preload(self,request):
        print("----userCtl preload---")
        self.page_list = RoleService().preload(self.form)
        self.preload_data = self.page_list

    
    # Populate Form from http Request
    def request_to_form(self, requestForm):
        print("----userCtl request_to_form---")
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
        self.form["role_Id"] = requestForm["role_Id"]

        
    # Popuate Form from Model
    # GET-display method call function
    def model_to_form(self, obj):
        print("----userCtl model_to_form---")
        if (obj == None):
            return None
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
        self.form["role_Id"] = obj.role_Id
        self.form["role_Name"] = obj.role_Name
        
    
    # Convert Form into Module
    def form_to_model(self, obj):
        c = RoleService().get(self.form["role_Id"])
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
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
        obj.role_Name = c.name
        return obj
        
    
    # Validate Form
    def input_validation(self):
        print("----userCtl input validation---")
        super().input_validation
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"]= " First Name can not be null"
            self.form["error"] = True
        
        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "Login id can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isemail(self.form["login_id"])):
                inputError["login_id"] = "Login id must be in abc@gmail.com format"
                self.form["error"] = True
        
        if (DataValidator.isNull(self.form["password"])):
            inputError["password"]= " Password can not be null"
            self.form["error"] = True
        
        if (DataValidator.isNull(self.form["confirmpassword"])):
            inputError["confirmpassword"] = "Confirm Password can not be null"
            self.form["error"] = True
        
        if (DataValidator.isNotNull(self.form["confirmpassword"])):
            if self.form["password"] != self.form["confirmpassword"]:
                inputError["confirmpassword"] = "Confirm Password can not be null"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "Date of Birth can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isDate(self.form["dob"])):
                inputError["dob"] = "Date formate should be DD-MM-YYYY "
                self.form["error"] = True

        if (DataValidator.isNull(self.form["address"])):
            inputError["address"] = "Address can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["mobilenumber"])):
            inputError["mobilenumber"] = "Mobile Number can not be null"
            self.form["error"] = True
        if (DataValidator.isNotNull(self.form["mobilenumber"])):
            if (DataValidator.ismobilecheck(self.form["mobilenumber"])):
                inputError["mobilenumber"] = "Mobile Number should be Ten Digits $ start with 6,7,8,9"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["gender"])):
            inputError["gender"] = "Gender can not be null"
            self.form["error"] = True
            
        if (DataValidator.isNull(self.form["role_Id"])):
            inputError["role_Id"] = "Role Name can not be null"
            self.form["error"] = True
        else:
            w = RoleService().find_by_unique_key(self.form["role_Id"])
            self.form["role_Name"] = w.name
        return self.form["error"]
    
    
    # Display User page
    def display(self, request, params={}):
        print("----UserCtl Display params={} request= {} -----".format(params,request))
        # it perform on edit 
        if (params["id"] > 0):
            r= self.get_service().get(params["id"])
            self.model_to_form(r)
            print("---------r = {} &&&& model_to_form = {} &&&& form ={}------------->".format(r,self.model_to_form(r),self.form))
        res = render(request,self.get_template(),{"form":self.form,"roleList":self.preload_data})
        return res

    
    # Submit User page
    def submit(self, request, params={}):
        print("----UserCtl Submit params={} request= {} -----".format(params,request))
        if params["id"]>0:
            pk = params["id"]
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(login_id=self.form["login_id"])
            if dup.count() > 0:
                self.form["error"]= True
                self.form["message"] ="Login id already exist"
                res = render(request, self.get_template(), {"form": self.form})
                
            else:
                r = self.form_to_model(User())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "DATA IS SUCCESSFULLY UPDATED"
                res = render(request, self.get_template(), {"form": self.form,"roleList":self.preload_data})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(login_id=self.form["login_id"])
            if duplicate.count() > 0:
                self.form["error"] =True
                self.form["message"]= "Login id already exists"
                res= render(request,self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(User())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "DATA IS SUCCESSFULLY SAVED"
                res = render(request, self.get_template(), {"form": self.form,"roleList":self.preload_data})
                print("--- userCtl form_to_model--->",r)
            return res

    
    # Template  html of user page
    def get_template(self):
            return "user.html"
        
    # Servive of User
    def get_service(self):
            return UserService()