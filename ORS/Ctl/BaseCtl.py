from django.http import HttpResponse
from abc import ABC , abstractmethod
from django.shortcuts import render,redirect

'''
Base class is inherited by all other application controller
'''
class BaseCtl(ABC):
    #Contain  preload data
    preload_data = {}

    #Contain list of objects,it will be displayed at page list
    page_list = {}
    
    '''
    intialize controller attributes
    '''
    def __init__(self):
        self.form = {}
        self.form["id"] = 0
        self.form["message"] = ""
        self.form["error"] = False
        self.form["inputError"] = {}
        self.form["pageNo"] = 1
    
    '''
    it loads preload data of page
    '''
    def preload(self , request):
        print("this is baseCtl preload ")

    '''
    Execute method is executed for each http request.
    It turns calls display() or submit() method for http get or post methods
    '''
    def execute(self,request,params={}):
        print("this is baseCtl executed")
        self.preload(request)
        print("<---baseCtl  preload (request)={} and baseCtl execute params= {}----->".format(request,params))
        if "GET" == request.method:
            print("<----------execute of Base Ctl Get Method --------------->")
            return self.display(request,params)
        elif "POST" == request.method:
            print("<----------execute of Base Ctl Post Method --------------->")
            self.request_to_form(request.POST)
            if self.input_validation():
                return self.display(request,params)
            else:
                if (request.POST.get("operation")=="delete"):
                    return self.deleteRecord(request,params)
                elif (request.POST.get("operation")=="next"):
                    return self.next(request,params)
                elif (request.POST.get("operation")=="previous"):
                    return self.previous(request,params)
                else:
                    return self.submit(request,params)
        else:
            message="Request is not supported"
            return HttpResponse(message)

    
    def deleteRecord(self,request,params={}):
        pass
    '''
    delete record of recived id
    '''
    
    # @abstractmethod
    # def next(self,request,params={}):
    #     pass


    # @abstractmethod
    # def previous(self,request,params={}):
    #     pass
    
    '''
     display record of recived id
    '''
    
    @abstractmethod
    def display(self,request,params={}):
        pass
    '''
    submit data
    '''
    
    @abstractmethod
    def submit(self,request,params={}):
        pass
    
    
    '''
    populate values from request POST/GET to controller from object
    '''
    def request_to_form(self,requestForm):
        pass
    
    
    #Populate Form from Model
    def model_to_form(self, obj):
        pass


    '''
    apply input validation
    '''
    def input_validation(self):
        self.form["error"]=False
        self.form["message"]=""
    
    
    '''
    return template of controller
    '''
    @abstractmethod
    def get_template(self):
        pass
    
    
    @abstractmethod
    def get_service(self):
        pass