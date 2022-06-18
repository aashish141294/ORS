from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ORS.utility.DataValidator import DataValidator
from service.models import User
from service.service.UserService import UserService


class UserListCtl(BaseCtl):
    count = 1
    def request_to_form(self, requestForm):
        self.form["firstName"] = requestForm.get("firstName",None)
        self.form["lastName"] = requestForm.get("lastName",None)
        self.form["login_id"] = requestForm.get("login_id",None)
        self.form["ids"] = requestForm.getlist("ids",None)

  
    def display(self, request, params={}):
        print("--------------UserList Display params={} request= {} form ={} -----".format(params,request,self.form))
        UserListCtl.count=self.form["pageNo"]
        print("--userListCtl Display .count = ",UserListCtl.count)
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        self.form["LastId"] = User.objects.last().id
        print("-------------userList self.form[LastId] = {}-------".format(User.objects.last().id))
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res
    
  
    def next(self,request,params={}):
        print("----UserList Next params={} request= {} -----".format(params,request))
        UserListCtl.count+=1
        self.form["pageNo"] = UserListCtl.count
        print("----userListCtl Next .count",UserListCtl.count)
        record = self.get_service().search(self.form)
        self.form["LastId"] = User.objects.last().id
        self.page_list = record["data"]
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

  
    def previous(self,request,params={}):
        print("----UserList previous params={} request= {} -----".format(params,request))
        UserListCtl.count-=1    
        self.form["pageNo"] = UserListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    # it perform on search button
    def submit(self,request,params={}):
        print("----UserList Submit params={} request= {} -----".format(params,request))
        # self.request_to_form(request.POST)
        UserListCtl.count =1
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        if self.page_list == []:
            self.form["msg"] = "No record found"
        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        return res

    
    def deleteRecord(self, request, params={}):
        print("----UserList deleteRecord params={} request= {} -----".format(params,request))
        # UserListCtl.count=self.form["pageNo"]
        self.form["pageNo"] = UserListCtl.count
        print("--userListCtl Delete .count = {} ".format(self.form["pageNo"]))
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
                        UserListCtl.count = 1
                        self.form["LastId"] = User.objects.last().id
                        self.form["error"] = False
                        self.form["message"] = "Data id successfully deleted"
                        # print("user deleteRecord-->",self.page_list)
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})

                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        res = render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
            return res

    
    # Template of user list
    def get_template(self):
        return "userList.html"
    
    
    # Service of user list
    def get_service(self):
        return UserService()
