from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import RoleForm,UserForm
from service.models import Role,User
from service.service.RoleService import RoleService


class RoleListCtl(BaseCtl):
    count = 1
    def request_to_form(self, requestForm):
        self.form["name"] = requestForm.get("name",None)
        self.form["description"] = requestForm.get("description",None)
        self.form["ids"] = requestForm.getlist("ids",None)

    
    def display(self, request, params={}):
        RoleListCtl.count = self.form["pageNo"]
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form["LastId"] = Role.objects.last().id
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res
    
    
    def next(self,request,params={}):
        RoleListCtl.count+=1
        print("----RoleListCtl next .count------",RoleListCtl.count)
        self.form["pageNo"] = RoleListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form["LastId"] = Role.objects.last().id
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    
    def previous(self,request,params={}):
        RoleListCtl.count-=1
        self.form["pageNo"] = RoleListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    
    def submit(self,request,params={}):
        self.request_to_form(request.POST)
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        if self.page_list == []:
            self.form["msg"] = "No record found"
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    
    # Template of Role
    def get_template(self):
        return "roleList.html"

    # Service of Role
    def get_service(self):
        return RoleService()

    def deleteRecord(self, request, params={}):
        # RoleListCtl.count = self.form["pageNo"]
        self.form["pageNo"] = RoleListCtl.count
        
        print("--------roleListCtl delete self.form[pageno]",RoleListCtl.count)
        if(bool(self.form["ids"])==False):
            record = self.get_service().search(self.form)
            self.page_list = record["data"]
            self.form["error"] = True
            self.form["message"] = "Please select at least one check box"
            return render(request, self.get_template(),{"pageList":self.page_list,"form":self.form})
        else:
            for ids in self.form["ids"]:
                record = self.get_service().search(self.form)
                self.page_list = record["data"]
                
                id =int(ids)
                if(id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form["pageNo"] = 1
                        record = self.get_service().search(self.form)
                        self.page_list =record["data"]
                        RoleListCtl.count =1
                        self.form["LastId"] = Role.objects.last().id
                        self.form["error"] = False
                        self.form["message"] = "Data id successfully deleted"
                        print("pppppppppppp-->",self.page_list)
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})

                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
            return res

