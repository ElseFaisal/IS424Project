from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from .models import certificate,granted # New Added
from django.db import IntegrityError # New Added


class UserLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'usernamefield'}),label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'passwordfield'}),label="")

class UserSignup(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'usernamefield'}),label="")
    fname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'fname'}),label="")
    lname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'lname'}),label="")
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email','class': 'emailfield'}),label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'passwordfield'}),label="")
    
    

class addCerti(forms.Form):
    cname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cetificate Name','class': 'certificateNameField'}),label="")
    ccompany = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Company','class': 'companyfield'}),label="")
    chours = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Cetificate Hours','class': 'hoursfield'}),label="")
    cfield = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Certificate Field','class': 'coursefield'}),label="")
    accredited = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Accredited','class': 'accreditedfield'}),label="")

    
    

class detailsAddCerti(forms.Form):
    cdate = forms.DateField(widget=forms.widgets.DateInput(attrs={'placeholder': 'Cetificate Date','class': 'detailsDateField' , 'type':'date'}),label="")
    cEndDate = forms.DateField(widget=forms.widgets.DateInput(attrs={'placeholder': 'Cetificate Date','class': 'detailsDateField' , 'type':'date'}),label="",required=False)






def signup(request):
    
    try:
        if request.method == "POST":
            formdata = UserSignup(request.POST)
            if formdata.is_valid():
                username = formdata.cleaned_data['username']
                fname = formdata.cleaned_data['fname']
                lname = formdata.cleaned_data['lname']
                email = formdata.cleaned_data['email']
                password = formdata.cleaned_data['password']
                
                myuser = User.objects.create_user(username=username , password=password , email=email)
                myuser.first_name = fname
                myuser.last_name = lname
                
                myuser.save()
                
                messages.success(request,"Your account has been successfully created.")
                return render(request , 'Certificates/login.html',{"form":UserLogin()})

            else:
                messages.error(request,"Make sure you type all fields correctly!") # New Added
     
     # New Added           
    except IntegrityError:
        messages.error(request,"The username already exist, try to login!")
     # New Added
            
    
    return render(request,'Certificates/signup.html',{"form":UserSignup()})


def signin(request):
    
    if request.method == "POST":
        formdata = UserLogin(request.POST)
        if formdata.is_valid():
            userN = formdata.cleaned_data['username']
            passW = formdata.cleaned_data['password']
        
            user = authenticate(request , username = userN , password = passW)
            
            if user:
                login(request,user)
                cert = certificate.objects.exclude(users = request.user)
                render(request,'Certificates/menu.html',{"name":userN.capitalize() , "certi":cert})
                return HttpResponseRedirect(reverse("certificates:menu"))
            else:
                messages.error(request,"Username OR password is incorrect!") # New Added
        
        else:
            return render(request,'Certificates/signup.html')

    
    return render(request,'Certificates/login.html',{"form":UserLogin()})




def menu(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("certificates:login"))
    
    user = request.user
    cert = certificate.objects.exclude(users = user) # New Added
    
    if len(cert) != 0:
        return render(request,'Certificates/menu.html' , {"certi":cert , "name":request.user.first_name.capitalize()})
    else:
        return render(request,'Certificates/menu.html' , {"nocertificates":len(cert) == 0 , "name":request.user.first_name.capitalize()})





def add(request):
    # Added
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("certificates:login"))
    # Added
    
    else:
        if request.method == "POST":
            formdata = addCerti(request.POST)
            if formdata.is_valid():
                cname = formdata.cleaned_data['cname']
                ccompany = formdata.cleaned_data['ccompany']
                chours = formdata.cleaned_data['chours']
                cfield = formdata.cleaned_data['cfield']
                accredited = formdata.cleaned_data['accredited']
                
                c = certificate(cname = cname,ccompany = ccompany , chours = chours , cfield = cfield , accredited = accredited) # New Added
                c.save()
                # user = User.objects.get(id = request.user.id)
                
                # # New Added
                # gdate = formdata.cleaned_data['cdate']
                # g= granted(course = c , user = user , grantedDate = gdate)
                # g.save()
                # # New Added
                
                
                
    return render(request,'Certificates/add.html',{"form":addCerti()})


def view(request):
    # Added
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("certificates:login"))
    # Added
    
    user = request.user
    grantedCert = granted.objects.filter(user = user) # New Added
     
    if len(grantedCert) != 0:
        return render(request,"Certificates/view.html",{"certi":grantedCert})
    else:
        return render(request,"Certificates/view.html",{"nocertificates":len(grantedCert) == 0})
        
        


# New Added
def details(request,courseid):
    user = request.user
    cert = certificate.objects.filter(users = user) 
    cert = certificate.objects.get(courseid = courseid)
            
    return render(request , 'Certificates/details.html' , {"certi":cert})
   
   
  
def detailsAdd(request,courseid):
    user = request.user
    cert = certificate.objects.filter(users = user) 
    cert = certificate.objects.get(courseid = courseid)
    
    if request.method == "POST":
        formdata = detailsAddCerti(request.POST)
            
        if formdata.is_valid():
            cdate = formdata.cleaned_data['cdate']
            cEndDate = formdata.cleaned_data['cEndDate']
            g= granted(course = cert , user = user , grantedDate = cdate , cEndDate = cEndDate)
            g.save()
            return HttpResponseRedirect(reverse("certificates:menu"))

    return render(request , 'Certificates/detailsadd.html' , {"certi":cert , "dateform":detailsAddCerti()})



def deleteMyCertificate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("certificates:login"))
    else:
        if request.method == "POST":
            courseid = int(request.POST["certificate"])
            course = certificate.objects.get(courseid = courseid)
            granted.objects.get(user = request.user,course = course).delete()
            return HttpResponseRedirect(reverse("certificates:view"))
    
    user = request.user
    grantedCert = granted.objects.filter(user = user) # New Added
     
    return render(request,"Certificates/delete.html",{"certi":grantedCert})


def deleteMenuCertificate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("certificates:login"))
    else:
        if request.method == "POST":
            courseid = int(request.POST["certificate"])
            certificate.objects.get(courseid = courseid).delete()
            return HttpResponseRedirect(reverse("certificates:menu"))
    
    publicCertificate = certificate.objects.all()# New Added
     
    return render(request,"Certificates/deleteCertificateMenu.html",{"certi":publicCertificate})
    


def updateMyCertificate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("certificates:login"))
    
    else:
        if request.method == "POST":
            courseid = int(request.POST["certificate"])
            course = certificate.objects.get(courseid = courseid)
            cc = granted.objects.get(user = request.user,course = course)
            cdate = request.POST['cdate']
            cc.grantedDate = str(cdate)
            cc.save()
            return HttpResponseRedirect(reverse("certificates:view"))
            
            
                
    
    user = request.user
    grantedCert = granted.objects.filter(user = user) # New Added
     
    return render(request,"Certificates/updateMyCertificate.html",{"certi":grantedCert})



def updateMenuCertificate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("certificates:login"))
    
    else:
        try:
            if request.method == "POST":
                courseid = int(request.POST["certificate"])
                c = certificate.objects.get(courseid = courseid)
                cname = str(request.POST['cname'])
                ccompany = str(request.POST['ccompany'])
                chours = str(request.POST['chours'])
                cfield = str(request.POST['cfield'])
                accredited = str(request.POST['accredited'])
                
                c.cname = cname
                c.ccompany = ccompany
                c.chours = chours
                c.cfield = cfield
                c.accredited = accredited
                
                c.save()
                return HttpResponseRedirect(reverse("certificates:menu"))
        except ValueError:
            messages.error(request,"Make sure you type all fields correctly!")
            
            
                
    
    cert = certificate.objects.all() # New Added
     
    return render(request,"Certificates/updateMenuCertificate.html",{"certi":cert})



def logout_view(request):
    # Added
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("certificates:login"))
    # Added
    
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return render(request , 'Certificates/login.html',{"form":UserLogin()})