from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render


class WelcomeCtl(BaseCtl):

    def display(self, request, params={}):
        user = request.session.get("user",None)
        request.session["name"] =user.role_Name
        if(user is not None):
            self.form["message"] = "Welcome" + user.role_Name
        return render(request,self.get_template(),{"form":self.form})

    
    def submit(self,request,params={}):
        return render(request,self.get_template(),{"form":self.form})


    #Template html of Welcome page
    def get_template(self):
        return 'welcome.html'

    
    #Service of Welcome
    def get_service(self):
        return "RoleService()"