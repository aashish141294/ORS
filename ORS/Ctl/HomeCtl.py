from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render

class HomeCtl(BaseCtl):

    print("--------homeCtl---------")
    def display(self,request,params={}):
        print('---------homeCtl Display request= {} , params = {} -------->'.format(request,params))
        return render(request,self.get_template())

    
    def submit(self,request,params={}):
        pass

    
    #Template html of Home page
    def get_template(self):
        return "Home.html"
        

    #Service of Home
    def get_service(self):
        return "RoleService()"