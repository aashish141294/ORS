from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Faculty
from service.forms import FacultyForm
from service.service.AddFacultyService import AddFacultyService
from service.service.SubjectService import SubjectService
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService



class AddFacultyCtl(BaseCtl):

    def preload(self, request):
        self.course_list = CourseService().preload(self.form)
        self.college_list = CollegeService().preload(self.form)
        self.subject_list = SubjectService().preload(self.form)


    # Populate Form from http Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["email"] = requestForm["email"]
        self.form["password"] = requestForm["password"]
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["dob"] = requestForm["dob"]
        self.form["college_ID"] = requestForm["college_ID"]
        self.form["subject_ID"] = requestForm["subject_ID"]
        self.form["course_ID"] = requestForm["course_ID"]


    # Popuate Form from Model
    def model_to_form(self, obj):
        if (obj == None):
            return None
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["email"] = obj.email
        self.form["password"] = obj.password
        self.form["address"] = obj.address
        self.form["gender"] = obj.gender
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d")
        self.form["college_ID"] = obj.college_ID
        # self.form["collegeName"] = CollegeService().find_by_unique_key(self.form['college_ID']).collegeName
        self.form["collegeName"] = obj.collegeName
        self.form["subject_ID"] = obj.subject_ID
        # self.form["subjectName"] = SubjectService().find_by_unique_key(self.form['subject_ID']).subjectName
        self.form["subjectName"] = obj.subjectName
        self.form["course_ID"] = obj.course_ID
        # self.form["courseName"] = CourseService().find_by_unique_key(self.form['course_ID']).courseName
        self.form["courseName"] = obj.courseName


    # Convert Form into Module
    def form_to_model(self, obj):
        c =CourseService().get(self.form["course_ID"])
        e =CollegeService().get(self.form["college_ID"])
        s =SubjectService().get(self.form["subject_ID"])
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.email = self.form["email"]
        obj.password = self.form["password"]
        obj.address = self.form["address"]
        obj.gender = self.form["gender"]
        obj.dob = self.form["dob"]
        obj.college_ID = self.form["college_ID"]
        obj.subject_ID = self.form["subject_ID"]
        obj.course_ID = self.form["course_ID"]
        obj.courseName = c.courseName
        obj.collegeName = e.collegeName
        obj.subjectName = s.subjectName
        return obj

    
    # Validate Form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"]= " First Name can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isaplhacheck(self.form["firstName"])):
               inputError["firstName"] = "First Name consider only alphabates"
               self.form["error"] = True

        
        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"]= " Last Name can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isaplhacheck(self.form["lastName"])):
               inputError["lastName"] = "Last Name consider only alphabates"
               self.form["error"] = True

        
        if (DataValidator.isNull(self.form["email"])):
            inputError["email"]= " Email can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isemail(self.form["email"])):
               inputError["email"] = "Email should be in @gmail.com form"
               self.form["error"] = True
               
               
        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True

        
        if (DataValidator.isNull(self.form["address"])):
            inputError["address"] = "Address can not be null"
            self.form["error"] = True

        
        if (DataValidator.isNull(self.form["gender"])):
            inputError["gender"] = "Gender can not be null"
            self.form["error"] = True
            
        
        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "Date of Birth can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isDate(self.form["dob"])):
                inputError["dob"] = "Date formate should be DD-MM-YYYY "
                self.form["error"] = True


        
        if (DataValidator.isNull(self.form["college_ID"])):
            inputError["college_ID"] = "College name can not be null"
            self.form["error"] = True
        else:
            x = CollegeService().find_by_unique_key(self.form['college_ID'])
            self.form["collegeName"] = x.collegeName

        
        if (DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "Course name not be null"
            self.form["error"] = True 
        else:
            y = CourseService().find_by_unique_key(self.form['course_ID']) # we also use get method instead of find_by_unique_key
            self.form["courseName"] = y.courseName
        
        
        if (DataValidator.isNull(self.form["subject_ID"])):
            inputError["subject_ID"] = "Subject name can not be null"
            self.form["error"] = True 
        else:
            z = SubjectService().get(self.form['subject_ID'])
            self.form["subjectName"] = z.subjectName
        return self.form["error"]

    
    
    # Display Faculty page
    def display(self, request, params={}):
        if (params["id"] > 0):
            r= self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(),{"form":self.form,"courseList":self.course_list,"collegeList":self.college_list,"subjectList":self.subject_list})
        return res

    # Submit Faculty page
    def submit(self,request,params={}):
        if params["id"] >0 :
            pk = params["id"]
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(email = self.form["email"])
            if dup.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Email already exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Faculty())
                self.get_service().save(r)
                self.form["error"] = False
                self.form["message"] = "DATA is SUCCESSFULLY UPDATED"
                res = render(request,self.get_template(),{"form":self.form,"courseList":self.course_list,"collegeList":self.college_list,"subjectList":self.subject_list})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(email = self.form["email"])
            if duplicate.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Email already exists"
                res = render(request, self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(Faculty())
                self.get_service().save(r)
                self.form["id"] =r.id
                self.form["error"] = False
                self.form["message"] ="DATA is SUCCESSFULLY SAVED"
                res = render(request,self.get_template(),{"form":self.form,"courseList":self.course_list,"collegeList":self.college_list,"subjectList":self.subject_list})
            return res

    # Template  html of Faculty page
    def get_template(self):
            return "addFaculty.html"
        
    # servive of Faculty
    def get_service(self):
            return AddFacultyService()