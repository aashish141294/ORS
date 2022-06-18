from django.shortcuts import render
from django.http import HttpResponse
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from .Ctl.RegistrationCtl import RegistrationCtl
from .Ctl.HomeCtl import HomeCtl
from .Ctl.LoginCtl import LoginCtl
from .Ctl.StudentCtl import StudentCtl
from .Ctl.StudentList import StudentListCtl
from .Ctl.MarksheetCtl import MarksheetCtl
from .Ctl.MarksheetMeritListCtl import MarksheetMeritListCtl
from .Ctl.SubjectCtl import SubjectCtl
from .Ctl.SubjectListCtl import SubjectListCtl
from .Ctl.TimeTableCtl import TimeTableCtl
from .Ctl.TimeTableListCtl import TimeTableListCtl
from .Ctl.UserCtl import UserCtl
from .Ctl.UserListCtl import UserListCtl
from .Ctl.CollegeCtl import CollegeCtl
from .Ctl.CollegeListCtl import CollegeListCtl
from .Ctl.MarksheetCtl import MarksheetCtl
from .Ctl.MarksheetList import MarksheetListCtl
from .Ctl.MarksheetMeritListCtl import MarksheetMeritListCtl
from .Ctl.ForgetPasswordCtl import ForgetPasswordCtl
from .Ctl.ChangePasswordCtl import ChangePasswordCtl
from .Ctl.LogoutCtl import LogoutCtl
from .Ctl.MyProfileCtl import MyProfileCtl
from .Ctl.WelcomeCtl import WelcomeCtl
from .Ctl.RoleCtl import RoleCtl
from .Ctl.RoleListCtl import RoleListCtl
from .Ctl.AddFacultyCtl import AddFacultyCtl
from .Ctl.AddFacultyList import AddFacultyListCtl
from .Ctl.CourseCtl import CourseCtl
from .Ctl.CourseListCtl import CourseListCtl
from .Ctl.RegistrationCtl import RegistrationCtl


# Create your views here.
@csrf_exempt
def action(request, page, action=""):
    ctlName = page +"Ctl()"
    ctlObj =eval(ctlName)
    return ctlObj.execute(request, {"id": 0})


'''
Calls respective controller with id
'''    

@csrf_exempt
def actionId(request,page="",opration="",id=0):
    path = request.META.get("PATH_INFO")
    print("-------PATH action id----->",path)
    print("-------actionId={} request ={},,,page={},,,opration={},,,id={}----".format(actionId,request,page,opration,id))
    if request.session.get('user') is not None and page !=  "":
        request.session['msg'] = None
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        print('-------------ActionId if block Page+Ctl----------------')
        res = ctlObj.execute(request, {"id": id})
    elif page == "Registration":
        ctlName = "Registration" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request,{"id": id})
    elif page == "Home":
        ctlName = "Home" + "Ctl()"
        ctlObj = eval("HomeCtl()")
        print("---------Home Ctl of views-------------")
        res = ctlObj.execute(request,{"id": id})
    elif page =="ForgetPassword":
        ctlName = "ForgetPassword" +"Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request,{"id":id})
    elif page == "Login":
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = None
        print("----session msg--->",request.session.get('msg'))
        res = ctlObj.execute(request,{"id":id,})
    else:
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] ="Your Session has been Expired, Please Login again"
        print('actionId else block loginCtl')
        res = ctlObj.execute(request,{"id":id,"path":path})
    return res
    

@csrf_exempt
def auth(request, page="",operation="",id=0):
    if page == "Logout":
        Session.objects.all().delete()
        request.session['user'] = None
        out = "LOGOUT SUCCESSFULLY"
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request,{"id":id,"operation": operation,"out":out})

    elif page == "ForgetPassword":
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request,{"id":id,"operation":operation})

    # else:
    #     ctlName = "Login" + "Ctl()"
    #     ctlObj = eval(ctlName)
    #     res = ctlObj.execute(request,{"id":id,"operation":operation})
    return res



def index(request):
    return render(request,'project.html')

# to remove favicon.ico error
def remove(self):
    print("--------------->fevicon error remove")
    return HttpResponse("favicon error removed") 
    