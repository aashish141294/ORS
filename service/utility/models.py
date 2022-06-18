from email.policy import default
from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def to_json(self):
        data={
            "id": self.id,
            "name": self.name,
            "descriotion": self.description 
        }
        return data
    class Meta:
        db_table = "SOS_ROLE"



class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    login_id = models.EmailField()
    password = models.CharField(max_length=20)
    confirmpassword = models.CharField(max_length=50, default='')
    dob = models.DateField(max_length=20)
    address = models.CharField(max_length=50,default='')
    gender = models.CharField(max_length=50,default='')
    mobilenumber = models.CharField(max_length=50,default='')
    role_Id = models.IntegerField()
    role_Name = models.CharField(max_length=50)

    def to_json(self):
        data = {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "login_id": self.login_id,
            "password": self.password,
            "confirmpassword": self.confirmpassword,
            "dob": self.dob,
            "address": self.address,
            "gender": self.gender,
            "mobilenumber": self.mobilenumber,
            "role_Id": self.role_Id,
            "role_Name": self.role_Name,
        }
        return data
    class Meta:
        db_table = "SOS_USER"



class College(models.Model):
    collegeName = models.CharField(max_length=50)
    collegeAddress = models.CharField(max_length=50)
    collegeState = models.CharField(max_length=50)
    collegeCity = models.CharField(max_length=50)
    collegePhoneNumber = models.CharField(max_length=50)

    def to_json(self):
        data ={
            "id":self.id,
            "collegeName": self.collegeName,
            "collegeAddress": self.collegeAddress,
            "collegeState": self.collegeState,
            "collegeCity": self.collegeCity,
            "collegePhoneNumber": self.collegePhoneNumber
        }
        return data
    class Meta:
        db_table ="SOS_COLLEGE"



class BaseModel(models.Model):
    def to_json(self):
        data = {}
        return data



class Course(models.Model):
    courseName = models.CharField(max_length=50)
    courseDescription = models.CharField(max_length=100)
    courseDuration = models.CharField(max_length=100)

    def to_json(self):
        data = {
            "id": self.id,
            "courseName": self.courseName,
            "coursDescription": self.courseDescription,
            "courseDuration": self.courseDuration,
        
        }
        return data
    class Meta:
        db_table = "SOS_COURSE"



class Faculty(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    adderess = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.DateField(max_length=50)
    college_ID = models.IntegerField()
    collegeName = models.CharField(max_length=50)
    subject_ID = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)

    def to_json(self):
        data = {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "password": self.password,
            "address": self.adderess,
            "gender": self.gender,
            "dob": self.dob,
            "college_ID": self.college_ID,
            "collegeName": self.collegeName,
            "subject_ID": self.subject_ID,
            "subjectName": self.subjectName,
            "course_ID": self.course_ID,
            "courseName": self.courseName,

        }
        return data
    class Meta:
        db_table = "SOS_FACULTY"



class Marksheet(models.Model):
    rollnumber = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    physics = models.IntegerField()
    chemistry = models.IntegerField()
    maths = models.IntegerField()

    def to_json(self):
        data = {
            "rollnumber": self.rollnumber,
            "name": self.name,
            "physics": self.physics,
            "chemistry": self.chemistry,
            "maths": self.maths
        }
        return data

    class Meta:
        db_table = "SOS_MARKSHEET"



class Student(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    mobileNumber = models.CharField(max_length=20)
    email = models.EmailField()
    college_ID = models.IntegerField()
    collegeName = models.CharField(max_length=50)

    def to_json(self):
        data = {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "dob": self.dob,
            "mobileNumber": self.mobileNumber,
            "email": self.email,
            "college_ID": self.college_ID,
            "collegeName": self.collegeName
        }
        return data

    class Meta:
        db_table = "SOS_STUDENT"



class Subject(models.Model):
    subjectName = models.CharField(max_length=50)
    subjectDiscription = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)

    def to_json(self):
        data ={
            "id": self.id,
            "subjectName": self.subjectName,
            "subjectDiscription": self.subjectDiscription,
            "course_ID": self.course_ID,
            # "courseName": self.courseName,
        }
        return data

    class Meta:
        db_table = "SOS_SUBJECT"



class TimeTable(models.Model):
    examTime = models.CharField(max_length=50)
    examDate = models.DateField()
    subject_ID = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)

    def to_json(self):
        data ={
            "id": self.id,
            "examTime": self.examTime,
            "examDate": self.examDate,
            "subject_ID": self.subject_ID,
            "subjectName": self.subjectName,
            "course_ID": self.course_ID,
            "courseName": self.courseName,
            "semester": self.semester,
        }
        return data

    class Meta:
        db_table = "SOS_TIMETABLE"
