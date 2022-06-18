from Area52.settings import EMAIL_HOST_USER,BASE_DIR
from string import Template


class EmailBuilder:
    template_dir = BASE_DIR +"/" + "service/template/"
    @staticmethod
    def sign_up(params):
        msg =""
        msg+="<HTML><BODY>"
        msg+="registration is Successful for ors project"
        msg+="<h1> Hi! Greetings from SunilOs! </h1>"
        msg+="<p> Congratulations for registering on ORS! You can now access your ORS account online - anywhere,anytime and enjoy the flexibility to check the Marksheet Details.</p>"
        msg+="<P>Log in today at <a href='http://ors.sunraystechnologies.com'>http://ors.sunraystechnologies.com</a> with your following credentials:</P>"
        msg+= "<p><b>Login Id : "+params["login"] +"<br>" + " Password: "+params["password"]+"</b></p>"
        msg+= "<p> As a security measure, we recommended that you change your password after you first log in.</p>"
        msg+="<p>For any assistance, please feel free to call us at +91 98273 60504 or 0731-4249244 helpline numbers.</p>"
        msg+="<p>You may also write to us at hrd@sunrays.co.in.</p>"
        msg+="<p>We assure you the best service at all times and look forward to a warm and long-standing association with you.</p>"
        msg+="<P><a href='http://www.sunrays.co.in' >-SUNRAYS Technolgies</a></P>"
        msg+="</BODY></HTML>"
        return msg

    
    @staticmethod
    def change_password(params):
        msg=""
        msg+="<HTML><BODY>"
        msg+= "<h2>"+"Your password has been change successfully !!"+params.firstName+"" +params.lastName+"</h2>"
        msg+="<p><b>"+"To access your account user login id:" +params.login_id+ "<br>" +"Password :"+params.password+"</b><p>"
        msg+="</HTML></BODY>"
        return msg
    
    
    @staticmethod
    def forget_password(params):
        print("000000000009--",params)
        print("------------->",params.firstName)
        msg=""
        msg+="<HTML><BODY>"
        msg+="<H1>"+"YOUR PASSWORD IS RECOVERED "+ params.firstName+" "+ params.lastName + "</H1>"
        msg+="<P><B>"+"To access account user login id: "+params.login_id+"<br>"+" Password: "+params.password
        msg+="</HTML></BODY>"
        return msg
