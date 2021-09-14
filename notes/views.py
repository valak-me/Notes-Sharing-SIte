from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Signup,Notes
from datetime import date
from django.contrib.auth import authenticate,login,logout


def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def userlogin(request):
    error=""
    if request.method=='POST':
        u=request.POST['emailid']
        p=request.POST['pwd']
        print(u,p)
        user=authenticate(username=u,password=p)
        try:
            if user:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    print(error)
    d={'error':error}
    return render(request,'login.html',d)



def login_admin(request):
    error=""
    if request.method=='POST':
        u=request.POST['Username']
        p=request.POST['pwd']
        print(u,p)
        user=authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    print(error)
    d={'error':error}
    return render(request,'login_admin.html',d)



def signup1(request):
    error=""
    if request.method=='POST':
        f=request.POST['first_name']
        l=request.POST['last_name']
        c=request.POST['Contact']
        e=request.POST['emailid']
        p=request.POST['pwd']
        b=request.POST['Branch']
        r=request.POST['role']
        print(c,b,r)
        try:
            users=User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(user=users,contact=c,branch=b,role=r)
            error="no"
        except:
            error="yes"
    
    d={'error':error}
    return render(request,'signup.html',d)



def admin_home(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    p=Notes.objects.filter(status="pending").count()
    ac=Notes.objects.filter(status="Accept").count()
    r=Notes.objects.filter(status="Reject").count()
    a=Notes.objects.all().count()
    d={'pn':p,'an':ac,'rn':r,'alln':a}
    return render(request,'admin_home.html',d)



def Logout(request):
    logout(request)
    return redirect('index')



def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=request.user.id)
    data=Signup.objects.get(user=request.user)
    d={'data':data,'user':user}
    return render(request,'profile.html',d)




def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=='POST':
        o=request.POST['oldpwd']
        n=request.POST['newpwd']
        c=request.POST['confirmpwd']
        if c==n:
            u=User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    d={'error':error}
    return render(request,'change_password.html',d)




def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=request.user.id)
    data=Signup.objects.get(user=request.user)
    error=False
    if request.method=="POST":
        f=request.POST['first_name']
        l=request.POST['last_name']
        c=request.POST['contact']
        b=request.POST['branch']
        user.first_name=f
        user.last_name=l
        data.contact=c
        data.branch=b
        user.save()
        data.save()
        error=True

    d={'data':data,'user':user,'error':error}
    return render(request,'edit_profile.html',d)




def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=='POST':
        b=request.POST['branch']
        s=request.POST['subject']
        n=request.FILES['notesfile']
        f=request.POST['filetype']
        d=request.POST['description']
        u=User.objects.filter(username=request.user.username).first()
        try:
            Notes.objects.create(user=u,uploadingdate=date.today(),branch=b,subject=s,
            notesfile=n,filetype=f,description=d,status='pending')
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'upload_notes.html',d)




def view_mynotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user=User.objects.get(id=request.user.id)
    data=Notes.objects.filter(user=user)
    d={'data':data}
    return render(request,'view_mynotes.html',d)




def delete_mynotes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes=Notes.objects.get(id=pid)
    notes.delete()
    return redirect('view_mynotes')




def view_users(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    users=Signup.objects.all()
    d={'users':users}
    return render(request,'view_users.html',d)




def delete_users(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    users=User.objects.get(id=pid)
    users.delete()
    return redirect('view_users')




def pending_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    data=Notes.objects.filter(status="pending")
    d={'data':data}
    return render(request,'pending_notes.html',d)




def accepted_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    data=Notes.objects.filter(status="Accept")
    d={'data':data}
    return render(request,'accepted_notes.html',d)




def rejected_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    data=Notes.objects.filter(status="Reject")
    d={'data':data}
    return render(request,'rejected_notes.html',d)




def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    data=Notes.objects.all()
    d={'data':data}
    return render(request,'all_notes.html',d)




def assign_status(request,pid):
    if not request.user.is_staff:
        return redirect('login_admin')
    notes=Notes.objects.get(id=pid)
    error=""
    if request.method=='POST':
        s=request.POST['status']
        try:
            notes.status=s
            notes.save()
            error="no"
        except:
            error="yes"
    d={'error':error,'notes':notes}
    return render(request,'assign_status.html',d)




def delete_notes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes=Notes.objects.get(id=pid)
    notes.delete()
    return redirect('all_notes')




def viewallnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data=Notes.objects.filter(status="Accept")
    d={'data':data}
    return render(request,'viewallnotes.html',d)