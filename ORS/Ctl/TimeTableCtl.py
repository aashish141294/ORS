from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ORS.utility.DataValidator import DataValidator
from service.models import TimeTable
from service.service.TimeTableService import TimeTableService
from service.service.CollegeService import CollegeService
from service.service.SubjectService import SubjectService
from service.service.CourseService import CourseService

class TimeTableCtl(BaseCtl):

    def preload(self,request):
        self.course_List = CourseService().preload(self.form)
        self.subject_List = SubjectService().preload(self.form)

    
    # Populate Form from http Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["examTime"] = requestForm["examTime"]
        self.form["examDate"] = requestForm["examDate"]
        self.form["subject_ID"] = requestForm["subject_ID"]
        self.form["course_ID"] = requestForm["course_ID"]
        self.form["semester"] = requestForm["semester"]
        
        
    # Popuate Form from Model
    def model_to_form(self, obj):
        if (obj == None):
            return None
        self.form["id"] = obj.id
        self.form["examTime"] = obj.examTime
        self.form["examDate"] = obj.examDate.strftime("%Y-%m-%d")
        self.form["subject_ID"] = obj.subject_ID
        self.form["subjectName"] = obj.subjectName
        self.form["course_ID"] = obj.course_ID
        self.form["courseName"] = obj.courseName
        self.form["semester"] = obj.semester
        
    
    # Convert Form into Module
    def form_to_model(self, obj):
        c = CourseService().get(self.form["course_ID"])
        s = SubjectService().get(self.form["subject_ID"])
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.examTime = self.form["examTime"]
        obj.examDate = self.form["examDate"]
        obj.subject_ID = self.form["subject_ID"]
        obj.course_ID = self.form["course_ID"]
        obj.semester = self.form["semester"]
        obj.courseName = c.courseName
        obj.subjectName = s.subjectName
        return obj
        
    
    # Validate Form
    def input_validation(self):
        super().input_validation
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["examTime"])):
            inputError["examTime"]= " Exam Time can not be null"
            self.form["error"] = True
        
        if (DataValidator.isNull(self.form["examDate"])):
            inputError["examDate"] = "Exam Date can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["subject_ID"])):
            inputError["subject_ID"] = "Subject name can not be null"
            self.form["error"] = True
        else:
            y = SubjectService().find_by_unique_key(self.form['subject_ID'])
            self.form["subjectName"] = y.subjectName

        if (DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"]= " Course name can not be null"
            self.form["error"] = True
        else:
            z = CourseService().find_by_unique_key(self.form['course_ID'])
            self.form["courseName"] = z.courseName
        
        if (DataValidator.isNull(self.form["semester"])):
            inputError["semester"] = "Semester can not be null"
            self.form["error"] = True
        return self.form["error"]
    
    
    # Display TimeTable page
    def display(self, request, params={}):
        if (params["id"] > 0):
            r= self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request,self.get_template(),{"form":self.form,"courseList":self.course_List,"subjectList":self.subject_List})
        return res

    # Submit TimeTable page
    def submit(self,request,params={}):
        if (params["id"] >0):
            q =TimeTable.objects.exclude(id=params["id"]).filter(subject_ID = self.form["subject_ID"],examDate = self.form["examDate"],examTime= self.form["examTime"])
            print("==",q)
            if q.count() >0:
                self.form["error"] = True
                self.form["message"] ="Exam Time, Exam Date, Subject Name already exists"
                res = render(request,self.get_template(),{"form":self.form})
            else:
                r = self.form_to_model(TimeTable())
                self.get_service().save(r)
                self.form["id"] =r.id
                self.form["error"] = False
                self.form["message"] = "DATA IS SUCCESSFULLY UPDATED"
                res = render(request,self.get_template(),{"form":self.form})
        else:
            r = self.form_to_model(TimeTable())
            self.get_service().save(r)
            self.form["id"] =r.id
            self.form["error"] = False
            self.form["message"] = "DATA IS SUCCESSFULLY SAVED"
            res = render(request,self.get_template(),{"form":self.form})
        return res
    
    
    # Template  html of Time Table page
    def get_template(self):
            return "timeTable.html"
        
    
    # Servive of Time Table
    def get_service(self):
            return TimeTableService()