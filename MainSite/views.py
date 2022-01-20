import os
import xlwt
import datetime
import hashlib
import xlrd
from django.utils import timezone

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render,redirect
from django.contrib import messages
from datetime import datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, Template,RequestContext
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from .swimming import getBookableSlots,getDate,getSlotDisplay,random_alphaNumeric_string

from .fantasyLeague import getPlayerCode,getEncodedPlayerList,isListUnique,stringToList


from .models import yearBookComments, yearBookPeople, People, Event, Gallery, Announcement, LiveMatch, Comment, Pride, JuniorExe,FantasyLeagueMatch, FantasyLeaguePlayer, FantasyLeagueSubmission , FantasyLeaguePoints , DailyFantasyLeaguePoints , swimmingUser, swimmingUserConfirmation, swimmingForm, swimmingRelative, Hof,coachFeedback, ReimbursementForms
from .feedbackValidEmails import feedbackValidEmails
from .yearbookValidEmails import yearbookValidEmails

# Create your views here.

"""DECLARE LINK TO STATIC DISPLAY IMAGES HERE"""
STATIC_DIR = 'static'
SHOWCASE_DIR = 'showcase'
""" END"""

Batsman = 'Batsman'
Bowler = 'Bowler'
AllRounder = 'AllRounder'

Secretary = 'Secretary'
Executive = 'Executive'
Faculty = 'Faculty'
Captain = 'Captain'
ViceCaptain = 'Vice-Captain'
JuniorExecutive = 'Junior Executive'
GeneralSecretary = 'General Secretary'
DeputyGeneralSecretary = 'Deputy General Secretary'
MAX_RECENT_MATCHES = 5

SLOT_STRENGTH = 100
#change in swimming.py ALSO!!!!!!!!!

ADMIN_PASSWORD = "swadmin123"
MAX_WEEK_SLOTS = 3
MAX_MONTH_SLOTS = 12

FANTASY_LEAGUE_LEADERBOARD_LIMIT = 20
  
slots = ["AM67","AM78","AM89","PM56","PM67","PM78"]


def index(request):
    announcements = Announcement.objects.all()
    live_matches = []
    upcoming_matches = []
    for match in LiveMatch.objects.all():
        if match.start_time > datetime.now() - match.duration:
            live_matches.append(match)
        elif match.start_time > datetime.now():
            upcoming_matches.append(match)
    context = {'announcements': announcements, 'live_matches': live_matches, 'upcoming_matches': upcoming_matches}
    return render(request, 'MainSite/index.html', context)


def people(request):
    faculty_list = People.objects.filter(type=Faculty)
    secretaries = People.objects.filter(type=Secretary)
    executives = People.objects.filter(type=Executive)
    junior_executives = People.objects.filter(type=JuniorExecutive)
    general_secretary = People.objects.filter(type=GeneralSecretary)
    deputy_general_secretary = People.objects.filter(type=DeputyGeneralSecretary)
    team_members = People.objects.filter(type=Captain).union(
        People.objects.filter(type=ViceCaptain)).order_by('team')
    context = {'faculty_list': faculty_list, 'secretaries': secretaries, 'executives': executives,
               'team_members': team_members, 'junior_executives': junior_executives,
               'general_secretary' : general_secretary,'deputy_general_secretary' : deputy_general_secretary}
    return render(request, 'MainSite/people.html', context)

def hof(request):
    InterIITBestPlayer = Hof.objects.filter(type ='Inter IIT Best Player')
    context = {'InterIITBestPlayer': InterIITBestPlayer}
    return render(request, 'MainSite/hof.html', context)
    
def magazine(request):
    return render(request, 'MainSite/magazine.html')

def pride(request):
    pride_list = Pride.objects.all()
    context = {'pride_list': pride_list}
    return render(request, 'MainSite/pride.html', context)

def register(request):
    pride_list = Pride.objects.all()
    context = {'pride_list': pride_list}
    return render(request, 'MainSite/pride.html', context)


def timeline(request):
    date = datetime.today()
    day_events = Event.objects.filter(date=date)
    past_events = Event.objects.filter(date__lt=date).order_by("-date")[0:5]
    upcoming_events = Event.objects.filter(date__gt=date).order_by("date")[0:5]
    context = {'day_events': day_events, 'past_events': past_events, 'upcoming_events': upcoming_events}
    return render(request, 'MainSite/timeline.html', context)


def gallery(request):
    all_event_images = []
    showcase_images = []
    for root, dirs, files in os.walk(os.path.join(STATIC_DIR, SHOWCASE_DIR)):
        for filename in files:
            showcase_images.append(filename)
    showcase = {
        "base_dir": SHOWCASE_DIR,
        "images": showcase_images
    }
    for item in Gallery.objects.all():
        images = []
        for root, dirs, files in os.walk(os.path.join(STATIC_DIR, item.path_to_images)):
            for filename in files:
                images.append(filename)
        event = {
            "event_name": item.event.name,
            "base_dir": item.path_to_images,
            "images": images
        }
        all_event_images.append(event)
    return render(request, 'MainSite/gallery.html', {'all_event_images': all_event_images, 'showcase': showcase,
                                                     "static_dir": STATIC_DIR})


def live(request):
    live_matches = []
    temp = []
    upcoming_matches = []
    for match in LiveMatch.objects.all():
        if match.start_time > datetime.now() - match.duration:
            live_matches.append(match)
        elif match.start_time > datetime.now():
            upcoming_matches.append(match)
        else:
            temp.append()
    comments = {}
    for match in live_matches:
        comments[match.header] = match.comment_set.all()
    recent_matches = []
    for match in temp:
        if match.start_time > datetime.now() - timedelta(days=7):
            recent_matches.append(match)
    context = {'upcoming_matches': upcoming_matches, 'live_matches': live_matches, 'recent_matches': recent_matches, 'comments': comments}
    return render(request, 'MainSite/live.html', context)


def freshers(request):
    return render(request, 'MainSite/freshers.html')


def orientation(request):
    return render(request, 'MainSite/orientation.html')


def interhostel(request):
    return render(request, 'MainSite/interhostel.html')
    
def interiit(request):
    return render(request, 'MainSite/interiit.html')

def weekenders(request):
    return render(request, 'MainSite/weekenders.html')


def sportech(request):
    return render(request, 'MainSite/sportech.html')


def leagues(request):
    return render(request, 'MainSite/leagues.html')


def summer(request):
    return render(request, 'MainSite/summer.html')


def bsanight(request):
    return render(request, 'MainSite/bsanight.html')


def aquatics(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='Aquatics').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='Aquatics'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/aquatics.html', context)


def athletics(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='Athletics').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='Athletics'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/athletics.html', context)


def badminton(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='Badminton').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='Badminton'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/badminton.html', context)


def basketball(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='Basketball').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='Basketball'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/basketball.html', context)


def cricket(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='Cricket').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='Cricket'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/cricket.html', context)


def football(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='Football').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='Football'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/football.html', context)


def hockey(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='Hockey').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='Hockey'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/hockey.html', context)


def ISC(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='ISC').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='ISC'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/ISC.html',context)


def lawntennis(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='Lawn Tennis').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='Lawn Tennis'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/lawntennis.html', context)


def squash(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='Squash').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='Squash'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/squash.html', context)


def tabletennis(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='Table Tennis').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='Table Tennis'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/tabletennis.html', context)


def volleyball(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='Volleyball').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='Volleyball'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/volleyball.html', context)


def weightlifting(request):
    team_members = People.objects.filter(type=Captain).filter(team__startswith='Weight-lifting').union(
        People.objects.filter(type=ViceCaptain).filter(team__startswith='Weight-lifting'))
    context = {'team_members': team_members}
    return render(request, 'MainSite/sports/weightlifting.html',context)

def contactUs(request):
    if(request.method == "GET"):
        return render(request, 'MainSite/contactUs.html')
    else:
        concern = request.POST.get('concern')
        contact = request.POST.get('contact')
        msg = "QUERY : \n"+concern+"\nCONTACT DETAILS : \n"+contact
        send_mail("BSA Contact Us Query",msg,settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER],fail_silently=True)
        messages.error(request, 'You query has been received.')
        return render(request, 'MainSite/contactUs.html')



###################################################################################

@csrf_exempt
def yearbookLogin(request):
    if(request.method == "GET"):
        return render(request,'MainSite/yearBookLogin.html')
    else:
        username = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username = username,password = password)
        if(user is not None ):
            auth.login(request,user)
            return redirect(('mainsite:yearbook'))    
        else :
            messages.error(request, 'Invalid Credentials')
            return render(request, 'MainSite/yearBookLogin.html')

@csrf_exempt
def yearbookRegister(request):
    if(request.method == "GET"):
        return render(request,'MainSite/yearBookRegister.html')
    elif(request.POST.get('step')=='1'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        userName = request.POST['email']
        lastName = request.POST['entno']
        password1 = request.POST['password']
        password2 = request.POST['confPassword']

        if(email.endswith('@iitd.ac.in') == False):
            messages.error(request, 'Please enter the institute email ending with "@iitd.ac.in')
            return render(request, 'MainSite/yearBookRegister.html')
        elif (lastName.upper() not in yearbookValidEmails):
            messages.error(request, 'You are not allowed to register')
            return render(request, 'MainSite/yearBookRegister.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'MainSite/yearBookRegister.html')
        elif(password1 != password2):
            messages.error(request, 'Passwords dont match')
            return render(request, 'MainSite/yearBookRegister.html')
        elif(len(password1) < 6):
            messages.error(request, 'Password too short')
            return render(request, 'MainSite/yearBookRegister.html')
        else:
            code = random_alphaNumeric_string(0,4)
            msg = "Your verification code for is " + code
            send_mail("IITD YearBook Verification Code",msg,settings.EMAIL_HOST_USER,[email])
            swc = swimmingUserConfirmation(email=email,code = code)
            swc.save()
            return render(request, 'MainSite/yearbook_verify_email.html',{'email' : email, 'first_name' :first_name,'last_name' :last_name,'userName' : userName,'lastName':lastName,'password':password1,})
    else:
        name = request.POST['first_name'] + " " + request.POST['last_name'] 
        email = request.POST['email']
        userName = request.POST['userName']
        lastName = request.POST['lastName']
        password = request.POST['password']
        code = request.POST['verificationCode']

        if(swimmingUserConfirmation.objects.filter(email = email).filter(code = code).exists()==False):
            messages.error(request, 'The verification code entered was incorrect')
            swimmingUserConfirmation.objects.filter(email = email).delete()
            return render(request, 'MainSite/yearBookRegister.html')
        else:
            user = User.objects.create_user(username = userName,password = password, email = email,first_name = name,last_name = lastName)
            user.save()
            msg = "Your registration is successfull. Please remember your password for future use.\nPassword : " + password
            send_mail("IITD YearBook Verification Code",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
            messages.error(request, 'Registration Successful, please check your email for confirmation')
            return redirect('mainsite:yearbookLogin')

def deleteComm(request):
    yearBookComments.objects.filter(commentedBy = 'Shyama Yadav').delete()
    return redirect('mainsite:yearbookLogin')


def yearbookResetPswd(request):
    if(request.method == "GET"):
        return render(request,'MainSite/yearBookResetPswd.html')
    elif(request.POST.get('step')=='1'):
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confPassword']

        if(email.endswith('@iitd.ac.in') == False):
            messages.error(request, 'Please enter the institute email ending with "@iitd.ac.in')
            return render(request, 'MainSite/yearBookResetPswd.html')
        elif (User.objects.filter(email=email).exists()==False):
            messages.error(request, 'Email not registered')
            return render(request, 'MainSite/yearBookResetPswd.html')
        elif(password1 != password2):
            messages.error(request, 'Passwords dont match')
            return render(request, 'MainSite/yearBookResetPswd.html')
        elif(len(password1) < 6):
            messages.error(request, 'Password too short')
            return render(request, 'MainSite/yearBookResetPswd.html')
        else:
            person = User.objects.filter(email = email)[0]
    
            first_name = person.first_name
            last_name = person.last_name
            code = random_alphaNumeric_string(0,4)
            msg = "Your verification code for is " + code
            send_mail("IITD YearBook Verification Code",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
            swc = swimmingUserConfirmation(email=email,code = code)
            swc.save()
            return render(request, 'MainSite/yearbook_verify_email1.html',{'email' : email, 'first_name' :first_name,'last_name' :last_name,'password':password1})
    else:
        name = request.POST['first_name'] 
        email = request.POST['email']
        userName = request.POST['email']
        lastName = request.POST['last_name']
        password = request.POST['password']
        code = request.POST['verificationCode']

        if(swimmingUserConfirmation.objects.filter(email = email).filter(code = code).exists()==False):
            messages.error(request, 'The verification code entered was incorrect')
            swimmingUserConfirmation.objects.filter(email = email).delete()
            return render(request, 'MainSite/yearBookResetPswd.html')
        else:
            User.objects.filter(email = email).delete()
            user = User.objects.create_user(username = userName,password = password, email = email,first_name = name,last_name = lastName)
            
            user.save()
            msg = "Your password reset is successfull. Please remember your password for future use.\nPassword : " + password
            send_mail("IITD YearBook Verification",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
            messages.error(request, 'Registration Successful, please check your email for confirmation')
            return redirect('mainsite:yearbookLogin')


@login_required(login_url = "/home/yearbookLogin/")
@csrf_exempt
def yearbook(request):
    people_list = yearBookPeople.objects.all()
    
    if(request.method == "POST"):
        if(request.POST['step'] == '1'):
            for student in yearBookPeople.objects.all():
                if student.entryno == request.POST['entryno'].upper():
                    comments = yearBookComments.objects.filter(uid = student.entryno)
                    context = {"people" : student, 'people_list' : people_list, 'comments': comments}
                    return render(request, 'MainSite/yearBoo.html', context)    
            messages.error(request, "INVALID ENTRY NO")
            context = {'people_list' : people_list}
            return render(request, 'MainSite/yearBoo.html', context)
        elif(request.POST['step'] == '2'):
            cmt = yearBookComments(uid = request.POST['id'], comment = request.POST['comment'], commentedBy = request.POST['by'])
            if (yearBookComments.objects.filter(uid = request.POST['id']).filter(commentedBy = request.POST['by']).filter(comment = request.POST['comment']).exists() == False):
                cmt.save()
            for student in yearBookPeople.objects.all():
                if student.entryno == request.POST['id']:
                    #messages.error(request, "VALID ENTRY NO")
                    comments = yearBookComments.objects.filter(uid = student.entryno)
                    context = {"people" : student, 'people_list' : people_list, 'comments': comments}
                    return render(request, 'MainSite/yearBoo.html', context)
            context = {'people_list' : people_list}
            return render(request, 'MainSite/yearBoo.html', context)
    else:
        context = {'people_list' : people_list}
        return render(request, 'MainSite/yearBoo.html', context)


def createYearbookPeople(filename):
    loc = (filename) 
  
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0)
    for i in range(1,sheet.nrows):
        yearBookPeople.objects.update_or_create(
        uid = sheet.cell_value(i, 4),
        name = sheet.cell_value(i, 1),
        
        sports = sheet.cell_value(i, 2),
        contact = sheet.cell_value(i, 3),
        entryno = sheet.cell_value(i, 4),
        image_link = "/static/yearBookImages/"+ sheet.cell_value(i, 4) + ".jpg",
        email = sheet.cell_value(i, 6),
        q1 = sheet.cell_value(0, 7),
        q2 = sheet.cell_value(0, 8), 
        q3 = sheet.cell_value(0, 9),
        q4 = sheet.cell_value(0, 10),
        a1 = sheet.cell_value(i, 7),
        a2 = sheet.cell_value(i, 8), 
        a3 = sheet.cell_value(i, 9), 
        a4 = sheet.cell_value(i, 10),
        )

@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def updateYearbook(request):
    #FantasyLeaguePoints.objects.all().delete()
    createYearbookPeople("YearBookPeople.xlsx")
    return redirect('mainsite:yearbookLogin')


###################################################################################


@csrf_exempt
def coachFeedbackForm(request):
    if(request.method == "GET"):
        return render(request,'MainSite/Feedback/coachFeedbackForm.html')
    elif(request.POST.get('step')=='1'):
        name = request.POST['firstName'] + " " + request.POST['lastName']
        email = request.POST['email']
        sports = request.POST['sports']
        feedback = request.POST['feedback']

        if email not in feedbackValidEmails:
            messages.error(request, 'Your email is not registered for submitting feedbacks')
            return render(request, 'MainSite/Feedback/coachFeedbackForm.html')
        else:
            fdbk = coachFeedback(name = name,email = email,sports = sports,feedback=feedback)
            fdbk.save()
            code = random_alphaNumeric_string(0,4)
            msg = "Your verification code is " + code
            send_mail("Feedback Verification Code",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
            swc = swimmingUserConfirmation(email=email,code = code)
            swc.save()
            return render(request, 'MainSite/Feedback/verify_email.html',{'email':email})
    else:
        email = request.POST['email']
        code = request.POST['verificationCode']
        
        if(swimmingUserConfirmation.objects.filter(email = email).filter(code = code).exists()==False):
            messages.error(request, 'The verification code entered was incorrect')
            swimmingUserConfirmation.objects.filter(email = email).delete()
            coachFeedback.objects.filter(email = email).delete()
            return render(request, 'MainSite/Feedback/coachFeedbackForm.html')
        else:
            messages.error(request, 'Your feedback has been submitted successfully.')
            return render(request, 'MainSite/Feedback/coachFeedbackForm.html')

@csrf_exempt
def feedbackAdminLogin(request):
    if(request.method == "GET"):
        return render(request,'MainSite/Feedback/feedbackAdminLogin.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username,password = password)
        if(user is not None ):
            auth.login(request,user)
            return redirect(('mainsite:feedbackAdminHome'))    
        else :
            messages.error(request, 'Invalid Credentials')
            return render(request, 'MainSite/Feedback/feedbackAdminLogin.html')

@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)
def feedbackAdminHome(request):
    if(request.method == "POST" and ReimbursementForms.objects.filter(uid = request.POST.get('uid')).filter(status = request.POST.get('step')).exists() == False):
        obj = ReimbursementForms.objects.get(uid = request.POST.get('uid'))
        obj.status = request.POST.get('step')
        obj.save()
        msg = ""
        if(request.POST.get('step') == '2'):
            msg = "Your reimbursement form with submission code " + request.POST.get('uid')+ " has been approved. We will notify you when the payment is completed."
        else:
            msg += "Payment for your reimbursement form with submission code " + request.POST.get('uid')+ " has been completed."
        
        send_mail("BSA Reimbursement Form",msg,settings.EMAIL_HOST_USER,[request.POST.get('email')],fail_silently=True)
    data = {}
    data['forms'] = ReimbursementForms.objects.filter()
    print(data)
    return render(request,'MainSite/Feedback/feedbackAdminHome.html',data)

@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def getFeedbacks(request):
    filename = "CoachesFeedback.xls"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    wb = xlwt.Workbook(encoding='utf-8')
    SPORTS = ['Athletics','Aquatics','Badminton','Basketball','Cricket','Football','Hockey','ISC','Lawn-Tennis','Squash','Table-Tennis','Volleyball','Weight-lifting']
    
    for sp in SPORTS : 
        ws = wb.add_sheet(sp)
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Name', 'Email', 'Feedback']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = coachFeedback.objects.filter(sports = sp).all().values_list('name', 'email','feedback')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

def generateUid():
    code = str(random_alphaNumeric_string(0,4))
    while(ReimbursementForms.objects.filter(uid = code).exists()):
        code = str(random_alphaNumeric_string(0,4))
    return code

@csrf_exempt
def reimbursementForm(request):
    if(request.method == "GET"):
        return render(request,'MainSite/ReimbursementForms/reimbursementForm.html')
    elif(request.POST.get('step')=='1'):
        email = request.POST['email']
        if email not in feedbackValidEmails:
            messages.error(request, 'Your email is not registered for submitting the form')
            return render(request, 'MainSite/ReimbursementForms/reimbursementForm.html')
        else:
            code = random_alphaNumeric_string(0,4)
            msg = "Your verification code is " + code
            send_mail("Verification Code",msg,settings.EMAIL_HOST_USER,[email],fail_silently=False)
            swc = swimmingUserConfirmation(email=email,code = code)
            swc.save()
            return render(request, 'MainSite/ReimbursementForms/verify_email.html',{'email':email})
    else:
        email = request.POST['email']
        code = request.POST['verificationCode']
        form = request.FILES['form']
        name = request.POST['firstName'] + " " + request.POST['lastName']
        
        if(swimmingUserConfirmation.objects.filter(email = email).filter(code = code).exists()==False):
            messages.error(request, 'The verification code entered was incorrect')
            swimmingUserConfirmation.objects.filter(email = email).delete()
            return render(request, 'MainSite/ReimbursementForms/reimbursementForm.html')
        else:
            uid = generateUid()
            rbf = ReimbursementForms(name = name,email = email,uid = uid,image=form,status=1)
            rbf.save()
            messages.error(request, 'Your form has been submitted successfully (submission code = '+ uid +' ). You will be notified with its progress. Please note the submission code')
            return render(request, 'MainSite/ReimbursementForms/reimbursementForm.html')

#---------------------------------------Fanatasy League------------------------

def getPlayerNameFromCode(code,playersList):
    for p in playersList:
        if(getPlayerCode(p.name)==code):
            return p.name

@login_required(login_url = "/home/fantasyLeagueLogin/")
@csrf_exempt
def fantasyLeagueHome(request):
    if(request.method == "GET"):
        currTime = timezone.now()
        fantasyLeagueMatches = FantasyLeagueMatch.objects.all()
        validMatches = []
        for m in fantasyLeagueMatches:
            if(m.activationTime < currTime and m.deactivationTime > currTime):
                validMatches.append(m)
        userPoints = 0
        userRank = getFantasyLeagueRank(request.user.username)
        if(FantasyLeaguePoints.objects.filter(email = request.user.username).exists()):
            l = FantasyLeaguePoints.objects.all().filter(email = request.user.username)
            userPoints = l[0].points
        
        leaderboard = list(FantasyLeaguePoints.objects.all().order_by('-points'))
        if(len(leaderboard) > FANTASY_LEAGUE_LEADERBOARD_LIMIT):
            leaderboard = leaderboard[0:FANTASY_LEAGUE_LEADERBOARD_LIMIT]

        rank = []
        currRank = 1
        for l in leaderboard:
            rank.append(currRank)
            currRank += 1

        dailyLeaderboard = list(DailyFantasyLeaguePoints.objects.all().order_by('-points'))
        if(len(dailyLeaderboard) > FANTASY_LEAGUE_LEADERBOARD_LIMIT):
            dailyLeaderboard = dailyLeaderboard[0:FANTASY_LEAGUE_LEADERBOARD_LIMIT]

        dailyRank = []
        currRank = 1
        for l in dailyLeaderboard:
            dailyRank.append(currRank)
            currRank += 1


        context = {'matches': validMatches,'userPoints' : userPoints,'userRank':userRank,'leaderboard':zip(rank,leaderboard),'dailyLeaderboard':zip(dailyRank,dailyLeaderboard)}
        return render(request,'MainSite/FantasyLeague/fantasyLeagueHome.html',context)
    elif(request.POST.get('step')=='1'):
        matchCode = request.POST['matchCode']
        return redirect('mainsite:fantasyLeagueMakeTeam',matchCode)
    else:
        matchCode = request.POST['matchCode']
        return redirect('mainsite:fantansyLeagueSubmissions',matchCode)
        
@login_required(login_url = "/home/fantasyLeagueLogin/")
@csrf_exempt
def fantasyLeagueMakeTeam(request,matchCode):
    if(request.method == "GET"):
        match = FantasyLeagueMatch.objects.all().get(matchCode = matchCode)
        team1 = match.team1
        team2 = match.team2

        players = FantasyLeaguePlayer.objects.filter(matchCode=matchCode)
        encodedPlayers = getEncodedPlayerList(players)

        batsmen = FantasyLeaguePlayer.objects.filter(matchCode=matchCode).filter(playerType = Batsman)
        encodedBatsmen = getEncodedPlayerList(batsmen)

        bowlers = FantasyLeaguePlayer.objects.filter(matchCode=matchCode).filter(playerType = Bowler)
        encodedBowlers = getEncodedPlayerList(bowlers)

        allRounders = FantasyLeaguePlayer.objects.filter(matchCode=matchCode).filter(playerType = AllRounder)
        encodedAllRounders = getEncodedPlayerList(allRounders)

        allRounders = FantasyLeaguePlayer.objects.filter(matchCode=matchCode).filter(playerType = AllRounder)
        context = {'players': list(zip(players,encodedPlayers)),'matchCode':matchCode,'team1':team1,'team2':team2,'batsmen':list(zip(batsmen,encodedBatsmen)),'bowlers':list(zip(bowlers,encodedBowlers)),'allRounders':list(zip(allRounders,encodedAllRounders))}
        return render(request,'MainSite/FantasyLeague/fantasyLeagueMakeTeamForm.html',context)
    else:
        matchCode = request.POST.get('matchCode')
        match = FantasyLeagueMatch.objects.all().get(matchCode = matchCode)
        team1 = match.team1
        team2 = match.team2
        playersList = FantasyLeaguePlayer.objects.filter(matchCode=matchCode)

        captain = getPlayerNameFromCode(request.POST.get('captain'),playersList)
        vice_captain = getPlayerNameFromCode(request.POST.get('vice_captain'),playersList)
        leadingScorer = getPlayerNameFromCode(request.POST.get('leadingScorer'),playersList)
        leadingWicketTaker = getPlayerNameFromCode(request.POST.get('leadingWicketTaker'),playersList)
        winner = team1
        if(request.POST.get('winner') == "2"):
            winner = team2
        
        batsmenList = []
        batsmenList.append(getPlayerNameFromCode(request.POST.get('batsman1'),playersList))
        batsmenList.append(getPlayerNameFromCode(request.POST.get('batsman2'),playersList))
        batsmenList.append(getPlayerNameFromCode(request.POST.get('batsman3'),playersList))
        batsmenList.append(getPlayerNameFromCode(request.POST.get('batsman4'),playersList))
        bowlersList = []
        bowlersList.append(getPlayerNameFromCode(request.POST.get('bowler1'),playersList))
        bowlersList.append(getPlayerNameFromCode(request.POST.get('bowler2'),playersList))
        bowlersList.append(getPlayerNameFromCode(request.POST.get('bowler3'),playersList))
        bowlersList.append(getPlayerNameFromCode(request.POST.get('bowler4'),playersList))
        allRounderList = []
        allRounderList.append(getPlayerNameFromCode(request.POST.get('allRounder1'),playersList))
        allRounderList.append(getPlayerNameFromCode(request.POST.get('allRounder2'),playersList))
        allRounderList.append(getPlayerNameFromCode(request.POST.get('allRounder3'),playersList))

        combinedList = batsmenList+bowlersList+allRounderList

        username = request.user.username
        currTime = timezone.now()

        if(request.user.is_superuser):
            messages.error(request, 'You cannot submit a team thorugh a superuser account')
            return redirect('mainsite:fantasyLeagueMakeTeam',matchCode)
        elif(match.activationTime > currTime or match.deactivationTime < currTime):
            messages.error(request, 'Submissions for this match are not open')
            return redirect('mainsite:fantasyLeagueMakeTeam',matchCode)
        elif(FantasyLeagueSubmission.objects.filter(matchCode = matchCode).filter(email = username).exists()):
            messages.error(request, 'You have already submitted a team for this match')
            return redirect('mainsite:fantasyLeagueMakeTeam',matchCode)
        elif(isListUnique(batsmenList) == False):
            messages.error(request, 'Please select 4 different batsmen')
            return redirect('mainsite:fantasyLeagueMakeTeam',matchCode)
        elif(isListUnique(bowlersList) == False):
            messages.error(request, 'Please select 4 different bowlers')
            return redirect('mainsite:fantasyLeagueMakeTeam',matchCode)
        elif(isListUnique(allRounderList) == False):
            messages.error(request, 'Please select 3 different all-rounders')
            return redirect('mainsite:fantasyLeagueMakeTeam',matchCode)
        elif(captain not in combinedList):
            messages.error(request, 'Captain must be in the team')
            return redirect('mainsite:fantasyLeagueMakeTeam',matchCode)
        elif(vice_captain not in combinedList):
            messages.error(request, 'Vice-Captain must be in the team')
            return redirect('mainsite:fantasyLeagueMakeTeam',matchCode)
        elif(captain == vice_captain):
            messages.error(request, 'Captain and Vice-captain must be different')
            return redirect('mainsite:fantasyLeagueMakeTeam',matchCode)
        else:
            # print(matchCode)
            # print(winner)
            # print(leadingScorer)
            # print(leadingWicketTaker)
            # print(combinedList)
            # print(captain)
            # print(vice_captain)
            combinedList.append(captain)
            combinedList.append(vice_captain)
            combinedList.append(winner)
            combinedList.append(leadingScorer)
            combinedList.append(leadingWicketTaker)
            user = request.user
            fls = FantasyLeagueSubmission(matchCode = matchCode,name = user.first_name,entryno = user.last_name,email=user.username,submittedString = stringToList(combinedList))
            fls.save()
            return render(request, 'MainSite/FantasyLeague/fantasyLeagueFormSubmissionMessage.html')
        # batsman1 = 
        # batsman2 = request.POST.get('batsman2')
        # batsman3 = request.POST.get('batsman3')
        # batsman4 = request.POST.get('batsman4')
        # bowler1 = request.POST.get('bowler1')
        # bowler2 = request.POST.get('bowler2')
        # bowler3 = request.POST.get('bowler3')
        # bowler4 = request.POST.get('bowler4')
        # allRounder1 = request.POST.get('allRounder1')
        # allRounder2 = request.POST.get('allRounder2')
        # allRounder3 = request.POST.get('allRounder3')
        
        


@csrf_exempt
def fantasyLeagueRegister(request):
    if(request.method == "GET"):
        return render(request,'MainSite/FantasyLeague/fantasyLeagueRegister.html')
    elif(request.POST.get('step')=='1'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        userName = request.POST['email']
        lastName = request.POST['entno']
        password1 = request.POST['password']
        password2 = request.POST['confPassword']

        if(email.endswith('@iitd.ac.in') == False):
            messages.error(request, 'Please enter the institute email ending with "@iitd.ac.in')
            return render(request, 'MainSite/FantasyLeague/fantasyLeagueRegister.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'MainSite/FantasyLeague/fantasyLeagueRegister.html')
        elif(password1 != password2):
            messages.error(request, 'Passwords dont match')
            return render(request, 'MainSite/FantasyLeague/fantasyLeagueRegister.html')
        elif(len(password1) < 6):
            messages.error(request, 'Password too short')
            return render(request, 'MainSite/FantasyLeague/fantasyLeagueRegister.html')
        else:
            code = random_alphaNumeric_string(0,4)
            msg = "Your verification code for is " + code
            send_mail("IITD Fantasy League Verification Code",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
            swc = swimmingUserConfirmation(email=email,code = code)
            swc.save()
            return render(request, 'MainSite/FantasyLeague/verify_email.html',{'email' : email, 'first_name' :first_name,'last_name' :last_name,'userName' : userName,'lastName':lastName,'password':password1,})
    else:
        name = request.POST['first_name'] + " " + request.POST['last_name'] 
        email = request.POST['email']
        userName = request.POST['userName']
        lastName = request.POST['lastName']
        password = request.POST['password']
        code = request.POST['verificationCode']

        if(swimmingUserConfirmation.objects.filter(email = email).filter(code = code).exists()==False):
            messages.error(request, 'The verification code entered was incorrect')
            swimmingUserConfirmation.objects.filter(email = email).delete()
            return render(request, 'MainSite/FantasyLeague/fantasyLeagueRegister.html')
        else:
            user = User.objects.create_user(username = userName,password = password, email = email,first_name = name,last_name = lastName)
            user.save()
            msg = "Your registration is successfull. Please remember your password for future use.\nPassword : " + password
            send_mail("IITD Fantasy League Verification Code",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
            messages.error(request, 'Registration Successful, please check your email for confirmation')
            return redirect('mainsite:fantasyLeagueLogin')

@csrf_exempt
def fantasyLeagueLogin(request):
    if(request.method == "GET"):
        return render(request,'MainSite/FantasyLeague/fantasyLeagueLogin.html')
    else:
        # pass
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        print(password)
        user = auth.authenticate(username = email,password = password)
        print(user)
        if(user is not None):
            auth.login(request,user)
            return redirect(('mainsite:fantasyLeagueHome'))    
        else :
            messages.error(request, 'Invalid Credentials')
            return render(request, 'MainSite/FantasyLeague/fantasyLeagueLogin.html')

@csrf_exempt
def fantasyLeagueLogout(request):
    auth.logout(request)
    messages.error(request, 'Logout Successfull')
    return redirect('mainsite:fantasyLeagueLogin')  


@csrf_exempt
def fantansyLeagueSubmissions(request,matchCode):
    if(FantasyLeagueMatch.objects.filter(matchCode = matchCode).exists() == False):
        return HttpResponse("Match doesnt exist")

    match = FantasyLeagueMatch.objects.all().get(matchCode = matchCode)
    filename = "MatchCode:" + matchCode + " " + match.team1 + " VS " + match.team2 + ".xls"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Submissions')
    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Entry No', 'Email', 'Submission','MatchCode']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = FantasyLeagueSubmission.objects.filter(matchCode = matchCode).all().values_list('name', 'entryno', 'email', 'submittedString','matchCode')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
# control 1 for weekly and 2 for daily
def updatePoints(filename,control):
    loc = (filename) 
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0)

    if(control == 1):
        for i in range(1,sheet.nrows):
            FantasyLeaguePoints.objects.update_or_create(
            name=sheet.cell_value(i, 0),
            entryno=sheet.cell_value(i, 1),
            email=sheet.cell_value(i, 2),
            defaults={
                "points" : int(sheet.cell_value(i, 3),),
                })
    else:
        for i in range(1,sheet.nrows):
            DailyFantasyLeaguePoints.objects.update_or_create(
            name=sheet.cell_value(i, 0),
            entryno=sheet.cell_value(i, 1),
            email=sheet.cell_value(i, 2),
            defaults={
                "points" : int(sheet.cell_value(i, 3),),
                })


@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def fantansyLeagueUpdatePoints(request):
    FantasyLeaguePoints.objects.all().delete()
    updatePoints("IITDFantasyLeague.xlsx",1)
    return redirect('mainsite:fantasyLeagueHome')

@user_passes_test(lambda u: u.is_superuser)
@csrf_exempt
def fantansyLeagueUpdateDailyPoints(request):
    DailyFantasyLeaguePoints.objects.all().delete()
    updatePoints("IITDFantasyLeagueDaily.xls",2)
    return redirect('mainsite:fantasyLeagueHome')

def getFantasyLeagueRank(email):
    allPlayers = FantasyLeaguePoints.objects.all().order_by('-points')
    for i in range(len(allPlayers)): 
        if(allPlayers[i].email == email):
            return str(i+1) 
    return "Submit a team to get ranked"

#--------------------------Swimming Portal-------------------------

# def get_slots_left(request):
#     slots = ["slotTTS_67AM","slotTTS_78AM","slotTTS_89AM","slotTTS_56PM","slotTTS_67PM","slotTTS_78PM","slotWFS_67AM","slotWFS_78AM","slotWFS_89AM","slotWFS_56PM","slotWFS_67PM","slotWFS_78PM"]
#     slots_info = {}
#     for s in slots:
#         slots_info[s] = SLOT_STRENGTH - swimmingUser.objects.filter(slot=s).count()
#         if(slots_info[s]<=0):
#             slots_info[s] = "Selected slot is full, try another slot"
#         else :
#             slots_info[s] = str(slots_info[s]) + " place(s) left in this slot"
#     return slots_info

# def form_submission(request):
#     if(request.method == "GET"):
#         return render(request, 'MainSite/Swimming Portal/swimming_form_submission.html')
#     elif(request.POST.get('step')=='1'):
#         email = request.POST['email']
        
#         if(email.endswith('@iitd.ac.in') == False):
#             messages.error(request, 'Please enter the institute email ending with "@iitd.ac.in"')
#             return render(request, 'MainSite/Swimming Portal/swimming_form_submission.html')
        
#         # #if user has already uploaded and is approved
#         # if(swimmingForm.objects.filter(email = email).filter(approvedStatus = True).() == False()):
#         #     messages.error(request, 'You have already uploaded a form which has been approved') return HttpResponse("Lol")
#         #     return render(request, 'MainSite/Swimming Portal/swimming_form_submission.html')
    
        
#         code = random_alphaNumeric_string(0,4)
#         msg = "Your verification code for submitting the Swimming Form is " + code
#         send_mail("IITD Swimming Registration Verification Code",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
#         swc = swimmingUserConfirmation(email=email,code = code)
#         swc.save()
#         return render(request, 'MainSite/Swimming Portal/verify_email2.html',{'email' : email,})  
#     else:
#         email = request.POST['email']
#         swimmingform = request.FILES['swimmingform']
#         name = request.POST['name']
#         usertype = request.POST['userType']
#         code = request.POST['verificationCode']
#         relativeCode = "0000"
        
#         if(usertype=='nonstudentrelativetype'):
#             relativeCode = request.POST['relativeCode']
#             #if the relative Code is approved or not
#             if(swimmingRelative.objects.filter(email=email).exists() == False
#                 or swimmingRelative.objects.filter(email=email).filter(relativeCode = relativeCode).exists() == False
#                 or swimmingRelative.objects.filter(email=email).filter(relativeCode = relativeCode).filter(approvedStatus = True).exists() == False):
#                 messages.error(request, 'The relative code entered was incorrect')
#                 swimmingUserConfirmation.objects.filter(email = email).delete()
#                 return render(request, 'MainSite/Swimming Portal/swimming_form_submission.html')

#         if(swimmingForm.objects.filter(email = email).filter(approvedStatus = True).filter(relativeCode=relativeCode).exists()):
#             messages.error(request, 'You have already uploaded a form which has been approved')
#             return render(request, 'MainSite/Swimming Portal/swimming_form_submission.html')



#         if(swimmingUserConfirmation.objects.filter(email = email).filter(code = code).exists()==False):
#             messages.error(request, 'The verification code entered was incorrect')
#             swimmingUserConfirmation.objects.filter(email = email).delete()
#             return render(request, 'MainSite/Swimming Portal/swimming_form_submission.html')
#         else:
            
#             resubmission = False
#             if(swimmingForm.objects.filter(email = email).filter(relativeCode=relativeCode).exists()):
#                 swimmingForm.objects.filter(email = email).filter(relativeCode=relativeCode).delete()
#                 resubmission = True
#             usr = swimmingForm(email = email,image=swimmingform,name=name,date = datetime.today(),approvedStatus=False,disapprovedStatus=False,usertype=usertype,relativeCode=relativeCode)
#             usr.save()
#             swimmingUserConfirmation.objects.filter(email = email).delete()
#             return render(request, 'MainSite/Swimming Portal/form_submission_message.html',{'resubmission':resubmission})

# def relative_submission(request):
#     if(request.method == "GET"):
#         return render(request, 'MainSite/Swimming Portal/swimming_relative_submission.html')
#     elif(request.POST.get('step')=='1'):
#         email = request.POST['email']
        
#         if(email.endswith('@iitd.ac.in') == False):
#             messages.error(request, 'Please enter the institute email ending with "@iitd.ac.in"')
#             return render(request, 'MainSite/Swimming Portal/swimming_form_submission.html')
        
#         #if user has already uploaded and is approved
#         # if(swimmingForm.objects.filter(email = email).filter(approvedStatus = True).exists()):
#         #     messages.error(request, 'You have already uploaded a form which has been approved')
#         #     return render(request, 'MainSite/Swimming Portal/swimming_form_submission.html')
    
        
#         code = random_alphaNumeric_string(0,4)
#         msg = "Your verification code for submitting the Swimming Form is " + code
#         send_mail("IITD Swimming Registration Verification Code",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
#         swc = swimmingUserConfirmation(email=email,code = code)
#         swc.save()
#         return render(request, 'MainSite/Swimming Portal/verify_email3.html',{'email' : email,})  
#     else:
#         email = request.POST['email']
#         proof = request.FILES['swimmingRelative']
#         code = request.POST['verificationCode']
#         relation = request.POST['relation']
#         relativeName = request.POST['relativeName']
#         relativeCode = random_alphaNumeric_string(0,4)
#         while(swimmingRelative.objects.filter(email = email).filter(relativeCode=relativeCode).exists() or relativeCode == "0000"):
#             print(relativeCode)
#             relativeCode = random_alphaNumeric_string(0,4)

#         if(swimmingRelative.objects.filter(email = email).filter(relativeName__iexact=relativeName).filter(approvedStatus=True).exists()):
#             messages.error(request, 'The relative with the following name has already been registered successfully')
#             return render(request, 'MainSite/Swimming Portal/swimming_form_submission.html')

#         if(swimmingUserConfirmation.objects.filter(email = email).filter(code = code).exists()==False):
#             messages.error(request, 'The verification code entered was incorrect')
#             swimmingUserConfirmation.objects.filter(email = email).delete()
#             return render(request, 'MainSite/Swimming Portal/swimming_relative_submission.html')
#         else:
            
#             resubmission = False
#             if(swimmingRelative.objects.filter(email = email).filter(relativeName__iexact=relativeName).exists()):
#                 swimmingRelative.objects.filter(email = email).filter(relativeName__iexact=relativeName).delete()
#                 resubmission = True
#             usr = swimmingRelative(email = email,relation = relation,relativeName=relativeName,image=proof,date = datetime.today(),approvedStatus=False,disapprovedStatus=False,relativeCode = relativeCode)
#             usr.save()
#             swimmingUserConfirmation.objects.filter(email = email).delete()
#             return render(request, 'MainSite/Swimming Portal/relative_submission_message.html',{'resubmission':resubmission})


# @csrf_exempt
# def register(request):

#     if(request.method == "GET"):
#         data = getBookableSlots(datetime.now(),datetime.today())
#         return render(request, 'MainSite/Swimming Portal/form.html',data)

#     elif(request.POST['step']=='1'):
#         name = request.POST['name']
#         email = request.POST['email']
#         phno = request.POST['phno']
#         usrtype = request.POST['userType']
#         gender = request.POST['gender']
#         # swimmingform = request.FILES['swimmingform']
#         # user_pic = request.FILES['user_pic']
#         entno = "NON-STUDENT"
#         hostel = "NON-STUDENT"

#         relativeCode = "0000"
#         if(usrtype == 'nonstudentrelativetype'):
#             relativeCode = request.POST['relativeCode']
#             if(relativeCode == ''):
#                 messages.error(request, 'Please enter the Relative Code')
#                 return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))
        
#         slot=request.POST['maleSlot']

#         date = getDate(slot[0:10])
#         weekno = date.isocalendar()[1]
#         monthno = int(slot[3:5])   

#         if(email.endswith('@iitd.ac.in') == False):
#             messages.error(request, 'Please enter the institute email ending with "@iitd.ac.in"')
#             return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))

#         #verifying if form is present
#         if(swimmingForm.objects.filter(email = email).exists()==False):
#             messages.error(request, 'You have not uploaded the swimming form. Please upload it before booking slots.')
#             return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))

#         if(swimmingForm.objects.filter(email = email).filter(relativeCode=relativeCode).exists()==False):
#             messages.error(request, 'You have not uploaded the swimming form or the relative code is incorrect')
#             return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))

#         #verifying if form is disapproved
#         if(swimmingForm.objects.filter(email = email).filter(relativeCode=relativeCode).filter(disapprovedStatus = True).exists()):
#             messages.error(request, 'Your swimming form has been disapproved. Please reupload a correct one.')
#             return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))
        
#         #verifying if form is approved or not
#         if(swimmingForm.objects.filter(email = email).filter(relativeCode=relativeCode).filter(approvedStatus = False).exists()):
#             messages.error(request, 'Your swimming form has not been approved yet.')
#             return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))


#         if(usrtype == 'studenttype'):   #Getting hostel and entry no only for students
#             entno = request.POST['entno']
#             hostel = request.POST['hostel']
#             if(entno == ''):
#                 messages.error(request, 'Please enter the Entry Number')
#                 return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))

#             if(hostel == ''):
#                 messages.error(request, 'Please enter the Hostel')
#                 return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))
                
        
#         if(swimmingUser.objects.filter(email = email).filter(relativeCode=relativeCode).filter(date = date).exists()):  #If email has already for the day
#                 print(relativeCode)
#                 messages.error(request, 'You have already registered for a slot in the chosen date')
#                 return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))
            
#         if(swimmingUser.objects.filter(email = email).filter(relativeCode=relativeCode).filter(weekno = weekno).count() >= MAX_WEEK_SLOTS):  #If email has 3 registrations for the week
#                 messages.error(request, 'You have reached the weekly limit of '+str(MAX_WEEK_SLOTS)+' slots')
#                 return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))

#         if(swimmingUser.objects.filter(email = email).filter(relativeCode=relativeCode).filter(monthno = monthno).count() >= MAX_MONTH_SLOTS):  #If email has 12 registrations for the month
#                 messages.error(request, 'You have reached the monthly limit of '+str(MAX_MONTH_SLOTS)+' slots')
#                 return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))
                
#         # else: 
#         #     if(swimmingUser.objects.filter(email = email).filter(date = date).exists()):  #If email has already for the day
#         #         messages.error(request, 'The user with the e-mail has already registered for a slot in the chosen date')
#         #         return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))
            
#         #     if(swimmingUser.objects.filter(email = email).filter(weekno = weekno).count() >= MAX_WEEK_SLOTS):  #If email has 3 registrations for the week
#         #         messages.error(request, 'The user with the e-mail has reached the weekly limit of 3 slots')
#         #         return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))

#         #     if(swimmingUser.objects.filter(email = email).filter(monthno = monthno).count() >= MAX_MONTH_SLOTS):  #If email has 12 registrations for the month
#         #         messages.error(request, 'The user with the e-mail has reached the monthly limit of 12 slots')
#         #         return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))      

#         #if chosen slot has been filled
#         if(swimmingUser.objects.filter(date=date).filter(slot=slot[10:14]).count()>=SLOT_STRENGTH):
#             messages.error(request, 'The chosen slot is full')
#             return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))

#         else:   #The registration is valid !
#             code = random_alphaNumeric_string(0,4)
#             msg = "Your verification code is " + code
#             send_mail("IITD Swimming Registration Verification Code",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
#             swc = swimmingUserConfirmation(email=email,code = code)
#             swc.save()
#             return render(request, 'MainSite/Swimming Portal/verify_email.html',{'name':name,'entryno' : entno,'mobileno' : phno,'email' : email,'hostel':hostel,'gender' : gender,'slot' : slot,'relativeCode':relativeCode})
#     else:
#         name = request.POST['name']
#         email = request.POST['email']
#         phno = request.POST['phno']
#         gender = request.POST['gender']
#         user_pic = request.FILES['user_pic']
#         entno = request.POST['entno']
#         hostel = request.POST['hostel']
#         slot=request.POST['maleSlot']
#         relativeCode = request.POST['relativeCode']

#         date = getDate(slot[0:10])
#         weekno = date.isocalendar()[1]
#         monthno = int(slot[3:5]) 

#         code = request.POST['verificationCode']
        
        
#         if(swimmingUserConfirmation.objects.filter(email = email).filter(code = code).exists()==False):
#             messages.error(request, 'The verification code entered was incorrect')
#             swimmingUserConfirmation.objects.filter(email = email).delete()
#             return render(request, 'MainSite/Swimming Portal/form.html',getBookableSlots(datetime.now(),datetime.today()))
#         else:
#             usr = swimmingUser(name=name,entryno = entno,mobileno = phno,email = email,hostel=hostel,gender = gender,slot = slot[10:14],user_pic=user_pic,weekno = weekno,monthno = monthno,date = date,relativeCode=relativeCode)
#             usr.save()
#             swimmingUserConfirmation.objects.filter(email = email).delete()
#             return render(request, 'MainSite/Swimming Portal/display.html',{'name':name,'email':email,'phno':phno,'entno':entno,'hostel':hostel,'gender':gender,'slot':getSlotDisplay(slot),'user_pic':user_pic})

# def swimming_admin_logout(request):
#     auth.logout(request)
#     return redirect('mainsite:swimming_admin_login')

# def swimming_admin_login(request):
#     if(request.method == "GET"):
#         return render(request,'MainSite/Swimming Portal/swimming_admin_login.html')
#     elif(request.POST['step']=='1'):
#         psw = request.POST['psw']
#         usr = request.POST['usr']

#         user = auth.authenticate(username = usr,password = psw)

#         if user is not None : 
#             auth.login(request,user)
#             return redirect('mainsite:swimming_admin_responses')
#             # return render(request,'MainSite/Swimming Portal/swimming_admin_login.html')
#         else:
#             messages.info(request,'invalid credentials')
#             return render(request,'MainSite/Swimming Portal/swimming_admin_login.html')

# @login_required(login_url = "/home/swimming_admin_login")
# def swimming_admin_responses(request):
#     if(request.method == "GET"):
#         data={}
#         td = datetime.today()
#         for s in slots:
#             data[s] = swimmingUser.objects.filter(date = td).filter(slot=s).values()
#             data['today'] = td.strftime("%d/%m/%Y")
#             data['today2'] = td.strftime("%Y-%m-%d")
#             data['unverifiedCount'] = swimmingForm.objects.filter(approvedStatus = False).filter(disapprovedStatus = False).count()
#             data['unverifiedCountRelatives'] = swimmingRelative.objects.filter(approvedStatus = False).filter(disapprovedStatus = False).count()
#         return render(request,'MainSite/Swimming Portal/slot_details.html',data)
#     else:
#         requestType = request.POST['requestType']
#         if(requestType == 'form'):
#             date = request.POST['forms_on_date']
#             return redirect('mainsite:get_forms_on_date',date)
#         if(requestType == 'relative'):
#             date = request.POST['relatives_on_date']
#             return redirect('mainsite:get_relatives_on_date',date)


# @login_required(login_url = "/home/swimming_admin_login")
# def get_relatives_on_date(request,date):
#     if(request.method == "GET"):
#         required_date = datetime(int(date[0:4]),int(date[5:7]),int(date[8:10]))
#         data = {}
#         data['relatives'] = swimmingRelative.objects.filter(date = required_date)
#         data['unverifiedCount'] = swimmingRelative.objects.filter(date = required_date).filter(approvedStatus = False).filter(disapprovedStatus = False).count()
#         return render(request,'MainSite/Swimming Portal/relatives_responses.html',data)
#     else:
#         email = request.POST['email']
#         relativeName = request.POST['relativeName']
#         action = request.POST['action']
#         relativeCode = request.POST['relativeCode']
#         obj = swimmingRelative.objects.filter(email = email).get(relativeCode = relativeCode)
#         if(action == 'approve'):
#             if(obj.approvedStatus==False):
#                 obj.approvedStatus = True
#                 obj.disapprovedStatus = False
#                 msg = "Your request to register the following relative uploaded on "+date+" has been approved.\nRelatives's Name : "+relativeName+"\nRelative's Code : "+relativeCode+"\nUse the above code while booking slots"
#                 send_mail("IITD Swimming Relative Registration Approved",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
#         else:
#             if(obj.disapprovedStatus==False):
#                 obj.approvedStatus = False
#                 obj.disapprovedStatus = True
#                 msg = "Your request to register the following relative uploaded on "+date+" has been disapproved.\nRelatives's Name : "+relativeName+"\nYou are requested to reupload a correct relation proof"
#                 send_mail("IITD Swimming Relative Registration Disapproved",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
#         obj.save()

#         return redirect('mainsite:get_relatives_on_date',date)

# @login_required(login_url = "/home/swimming_admin_login")
# def get_forms_on_date(request,date):
#     if(request.method == "GET"):
#         required_date = datetime(int(date[0:4]),int(date[5:7]),int(date[8:10]))
#         data = {}
#         # data['abc'] = ReimbursementForms.objects.filter()
#         data['forms'] = swimmingForm.objects.filter(date = required_date)
#         data['unverifiedCount'] = swimmingForm.objects.filter(date = required_date).filter(approvedStatus = False).filter(disapprovedStatus = False).count()
#         return render(request,'MainSite/Swimming Portal/forms_responses.html',data)
#     else:
#         email = request.POST['email']
#         action = request.POST['action']
#         name = request.POST['name']
#         relativeCode = request.POST['relativeCode']
#         obj = swimmingForm.objects.filter(email = email).get(relativeCode = relativeCode)
#         if(action == 'approve'):
#             if(obj.approvedStatus==False):
#                 obj.approvedStatus = True
#                 obj.disapprovedStatus = False
#                 msg = "Your Swimming form uploaded on "+date+" for the following person has been approved.\nYou can now book slots on the portal.\nPerson's Name : "+name
#                 send_mail("IITD Swimming Registration Form Approved",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
#         else:
#             if(obj.disapprovedStatus==False):
#                 obj.approvedStatus = False
#                 obj.disapprovedStatus = True
#                 msg = "Your Swimming form uploaded on "+date+" for the following person has been disapproved.\nYou are requested to reupload a correct one.\nPerson's Name : "+name
#                 send_mail("IITD Swimming Registration Form Disapproved",msg,settings.EMAIL_HOST_USER,[email],fail_silently=True)
#         obj.save()

#         return redirect('mainsite:get_forms_on_date',date)


# def swimming_steps(request):
#     return render(request,'MainSite/Swimming Portal/swimming_steps.html')
    

# def export(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="Slots.xls"'

#     wb = xlwt.Workbook(encoding='utf-8')

#     list_of_sheets = []

#     for s in slots:
#         list_of_sheets.append(wb.add_sheet(s))


#     for i in range(len(slots)):

#         ws = list_of_sheets[i]
#         sl = slots[i]
#         slot_name = getSlotName(slots[i])

#         # Sheet header, first row
#         row_num = 0

#         font_style = xlwt.XFStyle()
#         font_style.font.bold = True

#         columns = ['Name', 'Entry No','Hostel','Mobile No','Email','Gender','Pic','Slot' ]

#         for col_num in range(len(columns)):
#             ws.write(row_num, col_num, columns[col_num], font_style)

#         # Sheet body, remaining rows
#         font_style = xlwt.XFStyle()

#         rows = swimmingUser.objects.filter(slot=sl).values_list('name', 'entryno','hostel','mobileno','email','gender' )
#         for row in rows:
#             row_num += 1
#             for col_num in range(len(row)):
#                 ws.write(row_num, col_num, row[col_num], font_style)
#             # ws.insert_image(row_num, len(row), 'python.png', {'x_offset': 15, 'y_offset': 10})
#             # ws.write(row_num, len(row), slot_name, font_style)

#     wb.save(response)
#     return response

# def getSlotName(s):
#     if(s == "slotTTS_67AM"):
#          return "Tue./Thu./Sat.6:00to7:00 AM" 
#     if(s == "slotTTS_78AM"):
#          return "Tue./Thu./Sat.7:00to8:00 AM" 
#     if(s == "slotTTS_89AM"):
#          return "Tue./Thu./Sat.8:00to9:00 AM" 
#     if(s == "slotTTS_56PM"):
#          return "Tue./Thu./Sat.5:00to6:00 PM" 
#     if(s == "slotTTS_67PM"):
#          return "Tue./Thu./Sat.6:00to7:00 PM" 
#     if(s == "slotTTS_78PM"):
#          return "Tue./Thu./Sat.7:00to8:00 PM" 
#     if(s == "slotWFS_67AM"):
#          return "Wed./Fri./Sun.6:00to7:00 AM" 
#     if(s == "slotWFS_78AM"):
#          return "Wed./Fri./Sun.7:00to8:00 AM" 
#     if(s == "slotWFS_89AM"):
#          return "Wed./Fri./Sun.8:00to9:00 AM" 
#     if(s == "slotWFS_56PM"):
#          return "Wed./Fri./Sun.5:00to6:00 PM" 
#     if(s == "slotWFS_67PM"):
#          return "Wed./Fri./Sun.6:00to7:00 PM" 
#     if(s == "slotWFS_78PM"):
#          return "Wed./Fri./Sun.7:00to8:00 PM" 



def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL # Typically /static/
    sRoot = STATIC_ROOT = os.path.join(settings.BASE_DIR, 'static') # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL # Typically /static/media/
    mRoot = settings.MEDIA_ROOT # Typically /home/userX/project_static/media/
    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri # handle absolute uri (ie: http://some.tld/foo.png)
    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

def getSlotPdf(slot,det):
    template_path = 'MainSite/Swimming Portal/pdf_template_responses.html'
    data={}
    td = datetime.today()
    data['slot'] = swimmingUser.objects.filter(date = td).filter(slot=slot).values()
    data['today'] = td.strftime("%d/%m/%Y") +"  "+ det
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    fname = '"' + data['today'] + '.pdf"'
    response['Content-Disposition'] = 'attachment; filename='+fname
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(data)
    # create a pdf
    pisaStatus = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def render_pdf_view_AM67(request):
    return getSlotPdf("AM67",'6:00 to 7:00 AM')



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()

    #This part will create the pdf.
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def yearbook_pdf(request):
    template_path = 'MainSite/yearbook_pdf_template.html'
    data = {}
    people = yearBookPeople.objects.all()
    data['peoples'] = people
    data['comments'] = yearBookComments.objects.all()
    pdf = render_to_pdf(template_path, data)
    return HttpResponse(pdf, content_type='application/pdf')



def yearbook_pdf2(request):
    template_path = 'MainSite/yearbook_pdf_template.html'
    data = {}
    people = yearBookPeople.objects.all()
    data['peoples'] = people
    data['comments'] = yearBookComments.objects.all()
    return render(request, 'MainSite/yearBook_pdf_template.html', data)




# def render_pdf_view_AM78(request):
#     return getSlotPdf("AM78",'7:00 to 8:00 AM')

# def render_pdf_view_AM89(request):
#     return getSlotPdf("AM89",'8:00 to 9:00 AM')

# def render_pdf_view_PM56(request):
#     return getSlotPdf("PM56",'5:00 to 6:00 PM')

# def render_pdf_view_PM67(request):
#     return getSlotPdf("PM67",'6:00 to 7:00 PM')

# def render_pdf_view_PM78(request):
#     return getSlotPdf("PM78",'7:00 to 8:00 PM')

# def render_pdf_view_all(request):
#     data = getBookableSlots(datetime.now(),datetime.today())

#     displayList = []
#     user_list = []

#     for name,display in data['slots']:
#         displayList.append(display)
#         dt = getDate(name)
#         slot = name[10:14]
#         lst = swimmingUser.objects.filter(date = dt).filter(slot=slot).values()
#         user_list.append(lst)

#     data['zipped_data'] = zip(displayList,user_list) 

#     template_path = 'MainSite/Swimming Portal/pdf_template_responses2.html'

#         # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="All_slots.pdf"'
#         # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(data)
#         # create a pdf
#     pisaStatus = pisa.CreatePDF(
#         html, dest=response, link_callback=link_callback)
#         # if error then show some funy view
#     if pisaStatus.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response
