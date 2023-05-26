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
    
    
    def cnameform(self):
        return self.cname

class detailsAddCerti(forms.Form):
    cdate = forms.DateField(widget=forms.widgets.DateInput(attrs={'placeholder': 'Cetificate Date','class': 'detailsDateField' , 'type':'date'}),label="")






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
                return render(request , 'Food/login.html',{"form":UserLogin()})

            else:
                messages.error(request,"Make sure you type all fields correctly") # New Added
     
     # New Added           
    except IntegrityError:
        messages.error(request,"The username already exist, try to login")
     # New Added
            
    
    return render(request,'Food/signup.html',{"form":UserSignup()})


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
                return render(request,'Food/menu.html',{"name":userN.capitalize() , "certi":cert})
            else:
                messages.error(request,"Username OR password is incorrect!") # New Added
        
        else:
            return render(request,'Food/signup.html')

    
    return render(request,'Food/login.html',{"form":UserLogin()})




def menu(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("food:login"))
    
    user = request.user
    cert = certificate.objects.exclude(users = user) # New Added
    
    return render(request,'Food/menu.html' , {"certi":cert , "name":request.user.first_name.capitalize()})





def add(request):
    # Added
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("food:login"))
    # Added
    
    else:
        if request.method == "POST":
            formdata = addCerti(request.POST)
            if formdata.is_valid():
                cname = formdata.cleaned_data['cname']
                ccompany = formdata.cleaned_data['ccompany']
                c = certificate(cname = cname,ccompany = ccompany) # New Added
                c.save()
                # user = User.objects.get(id = request.user.id)
                
                # # New Added
                # gdate = formdata.cleaned_data['cdate']
                # g= granted(course = c , user = user , grantedDate = gdate)
                # g.save()
                # # New Added
                
                
                
    return render(request,'Food/add.html',{"form":addCerti()})


def view(request):
    # Added
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("food:login"))
    # Added
    
    user = request.user
    grantedCert = granted.objects.filter(user = user) # New Added
     
    return render(request,"Food/view.html",{"certi":grantedCert})
        


# New Added
def details(request,courseid):
    user = request.user
    cert = certificate.objects.filter(users = user) 
    cert = certificate.objects.get(courseid = courseid)
            
    return render(request , 'Food/details.html' , {"certi":cert})
   
   
  
def detailsAdd(request,courseid):
    user = request.user
    cert = certificate.objects.filter(users = user) 
    cert = certificate.objects.get(courseid = courseid)
    
    if request.method == "POST":
        formdata = detailsAddCerti(request.POST)
            
        if formdata.is_valid():
            cdate = formdata.cleaned_data['cdate']
            g= granted(course = cert , user = user , grantedDate = cdate)
            g.save()
            return HttpResponseRedirect(reverse("food:menu"))

    return render(request , 'Food/detailsadd.html' , {"certi":cert , "dateform":detailsAddCerti()})



def deleteMyCertificate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("food:login"))
    else:
        if request.method == "POST":
            courseid = int(request.POST["certificate"])
            course = certificate.objects.get(courseid = courseid)
            granted.objects.get(user = request.user,course = course).delete()
            return HttpResponseRedirect(reverse("food:view"))
    
    user = request.user
    grantedCert = granted.objects.filter(user = user) # New Added
     
    return render(request,"Food/delete.html",{"certi":grantedCert})


def deleteMenuCertificate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("food:login"))
    else:
        if request.method == "POST":
            courseid = int(request.POST["certificate"])
            certificate.objects.get(courseid = courseid).delete()
            return HttpResponseRedirect(reverse("food:menu"))
    
    publicCertificate = certificate.objects.all()# New Added
     
    return render(request,"Food/deleteCertificateMenu.html",{"certi":publicCertificate})
    


def updateMyCertificate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("food:login"))
    
    else:
        if request.method == "POST":
            courseid = int(request.POST["certificate"])
            course = certificate.objects.get(courseid = courseid)
            cc = granted.objects.get(user = request.user,course = course)
            cdate = request.POST['cdate']
            cc.grantedDate = str(cdate)
            cc.save()
            return HttpResponseRedirect(reverse("food:view"))
            
            
                
    
    user = request.user
    grantedCert = granted.objects.filter(user = user) # New Added
     
    return render(request,"Food/updateMyCertificate.html",{"certi":grantedCert})



def updateMenuCertificate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("food:login"))
    
    else:
        if request.method == "POST":
            courseid = int(request.POST["certificate"])
            c = certificate.objects.get(courseid = courseid)
            cname = str(request.POST['cname'])
            ccompany = str(request.POST['ccompany'])
            
            c.cname = cname
            c.ccompany = ccompany
            
            c.save()
            return HttpResponseRedirect(reverse("food:menu"))
            
            
                
    
    cert = certificate.objects.all() # New Added
     
    return render(request,"Food/updateMenuCertificate.html",{"certi":cert})



def logout_view(request):
    # Added
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("food:login"))
    # Added
    
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return render(request , 'Food/login.html',{"form":UserLogin()})