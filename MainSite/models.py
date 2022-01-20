from django.db import models
from django.utils.timezone import now
import datetime

# Create your models here.
STATIC_DIR = 'static'
TEAMS = (
    ('', 'None'),
    ('Athletics (Men)', 'Athletics (Men)'),
    ('Athletics (Women)', 'Athletics (Women)'),
    ('Aquatics (Men)', 'Aquatics (Men)'),
    ('Aquatics (Women)', 'Aquatics (Women)'),
    ('Badminton (Men)', 'Badminton (Men)'),
    ('Badminton (Women)', 'Badminton (Women)'),
    ('Basketball (Men)', 'Basketball (Men)'),
    ('Basketball (Women)', 'Basketball (Women)'),
    ('Cricket', 'Cricket'),
    ('Football', 'Football'),
    ('Hockey', 'Hockey'),
    ('ISC', 'ISC'),
    ('Lawn Tennis (Men)', 'Lawn Tennis (Men)'),
    ('Lawn Tennis (Women)', 'Lawn Tennis (Women)'),
    ('Squash (Men)', 'Squash (Men)'),
    ('Squash (Women)', 'Squash (Women)'),
    ('Table Tennis (Men)', 'Table Tennis (Men)'),
    ('Table Tennis (Women)', 'Table Tennis (Women)'),
    ('Volleyball (Men)', 'Volleyball (Men)'),
    ('Volleyball (Women)', 'Volleyball (Women)'),
    ('Weight-lifting', 'Weight-lifting')
)

SPORTS = (
    ('', 'None'),
    ('Athletics', 'Athletics'),
    ('Aquatics', 'Aquatics'),
    ('Badminton', 'Badminton'),
    ('Basketball', 'Basketball'),
    ('Cricket', 'Cricket'),
    ('Football', 'Football'),
    ('Hockey', 'Hockey'),
    ('ISC', 'ISC'),
    ('Lawn-Tennis', 'Lawn-Tennis'),
    ('Squash', 'Squash'),
    ('Table-Tennis', 'Table-Tennis'),
    ('Volleyball', 'Volleyball'),
    ('Weight-lifting', 'Weight-lifting')
)


class People(models.Model):
    Secretary = 'Secretary'
    Executive = 'Executive'
    JuniorExecutive = 'Junior Executive'
    Faculty = 'Faculty'
    Captain = 'Captain'
    ViceCaptain = 'Vice-Captain'
    GeneralSecretary = 'General Secretary'
    DeputyGeneralSecretary = 'Deputy General Secretary'
    people_types = (
        (Secretary, 'Secretary'),
        (Executive, 'Executive'),
        (JuniorExecutive,'Junior Executive'),
        (Faculty, 'Faculty'),
        (Captain, 'Captain'),
        (ViceCaptain, 'Vice-Captain'),
        (GeneralSecretary, 'General Secretary'),
        (DeputyGeneralSecretary, 'Deputy General Secretary'),
    )
    type = models.CharField(blank=False, max_length=40, choices=people_types, default=Secretary)
    team = models.CharField(blank=True, max_length=20, choices=TEAMS, default='', help_text="Leave blank if not capn or vice-capn")
    name = models.CharField(blank=False, max_length=30, help_text="Full Name")
    entryno = models.CharField(blank=True, max_length=15, help_text="Leave Blank if faculty")
    mobileno = models.CharField(blank=True, max_length=15, help_text="Mobile Number")
    email = models.CharField(blank=False, max_length=30, help_text="Email ID")
    hostel = models.CharField(blank=True, max_length=15, help_text="Leave Blank if faculty")
    fb = models.CharField(blank=True, max_length=200, help_text="Not required")
    image_link = models.CharField(blank=False, max_length=500)

class Hof(models.Model):
    InterIITBestPlayer = 'Inter IIT Best Player'
    people_types = (
        (InterIITBestPlayer, 'Inter IIT Best Player'),
    )
    type = models.CharField(blank=False, max_length=40, choices=people_types, default=InterIITBestPlayer)
    team = models.CharField(blank=True, max_length=20, choices=TEAMS, default='', help_text="Leave blank if not capn or vice-capn")
    name = models.CharField(blank=False, max_length=30, help_text="Full Name")
    year = models.IntegerField(default=0, help_text="Year")
    image_link = models.CharField(blank=True, max_length=500)


class Pride(models.Model):
    sport = models.CharField(blank=True, max_length=20, help_text="Leave blank if not applicable")
    name = models.CharField(blank=False, max_length=30, help_text="Full Name")
    entryno = models.CharField(blank=True, max_length=15, help_text="Leave Blank if faculty")
    mobileno = models.CharField(blank=True, max_length=15, help_text="Mobile Number")
    email = models.CharField(blank=False, max_length=30, help_text="Email ID")
    hostel = models.CharField(blank=True, max_length=15, help_text="Leave Blank if faculty")
    fb = models.CharField(blank=True, max_length=200, help_text="Not required")
    image_link = models.CharField(blank=False, max_length=500)

class JuniorExe(models.Model):
    team = models.CharField(blank=True, max_length=20, choices=TEAMS, default='', help_text="Leave blank if not capn or vice-capn")
    name = models.CharField(blank=False, max_length=30, help_text="Full Name")
    entryno = models.CharField(blank=True, max_length=15, help_text="Leave Blank if faculty")
    mobileno = models.CharField(blank=True, max_length=15, help_text="Mobile Number")
    email = models.CharField(blank=False, max_length=30, help_text="Email ID")
    hostel = models.CharField(blank=True, max_length=15, help_text="Leave Blank if faculty")
    fb = models.CharField(blank=True, max_length=200, help_text="Not required")
    image_link = models.CharField(blank=False, max_length=500)


class Event(models.Model):
    name = models.CharField(blank=False, max_length=50)
    date = models.DateField(blank=False)
    time = models.TimeField(blank=True)
    short_des = models.CharField(blank=True, max_length=300)
    long_des = models.CharField(blank=True, max_length=2000)
    logo_link = models.CharField(blank=True, max_length=500)
    image_link = models.CharField(blank=True, max_length=500)


class Gallery(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    path_to_images = models.CharField(blank=False, max_length=500)


class Announcement(models.Model):
    desc = models.CharField(blank=False, max_length=300)
    link = models.CharField(blank=True, max_length=500)


class LiveMatch(models.Model):
    score = models.CharField(blank=False, max_length=100)
    start_time = models.DateTimeField('time started')
    duration = models.TimeField
    header = models.CharField(blank=False, max_length=500)
    end_text = models.CharField(blank=True, max_length=500)


class Comment(models.Model):
    LiveMatch = models.ForeignKey(LiveMatch, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

class FantasyLeagueMatch(models.Model):
    
    matchCode = models.IntegerField(default=0, help_text="Unique Match Code")
    team1 = models.CharField(blank=False, max_length=30, help_text="Team 1")
    team2 = models.CharField(blank=False, max_length=30, help_text="Team 2")
    startTime = models.DateTimeField(default=now, blank=True)
    activationTime = models.DateTimeField(default=now, blank=True)
    deactivationTime = models.DateTimeField(default=now, blank=True)
    image_link = models.CharField(default="def", max_length=500)

class FantasyLeaguePlayer(models.Model):
    
    matchCode = models.IntegerField(default=0, help_text="Unique Match Code")
    name = models.CharField(blank=False, max_length=30, help_text="Player Name")
    team = models.CharField(blank=False, max_length=30, help_text="Team")
    Batsman = 'Batsman'
    Bowler = 'Bowler'
    AllRounder = 'AllRounder'
    position = (
        (Batsman, 'Batsman'),
        (Bowler, 'Bowler'),
        (AllRounder,'AllRounder'),
    )
    playerType = models.CharField(blank=False, max_length=40, choices=position, default=Batsman)
    
class FantasyLeagueSubmission(models.Model):
    
    matchCode = models.IntegerField(default=0, help_text="Unique Match Code")
    name = models.CharField(blank=True, max_length=30)
    entryno = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=False, max_length=30, help_text="Email ID")
    submittedString = models.CharField(blank=False, max_length=1000)

class FantasyLeaguePoints(models.Model):
    
    name = models.CharField(blank=True, max_length=30)
    entryno = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=False, max_length=30, help_text="Email ID")
    points = models.IntegerField(default=0, help_text="User points")

class DailyFantasyLeaguePoints(models.Model):
    
    name = models.CharField(blank=True, max_length=30)
    entryno = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=False, max_length=30, help_text="Email ID")
    points = models.IntegerField(default=0, help_text="User points")

class swimmingUser(models.Model):
    Male = 'Male'
    Female = 'Female'
    gender = (
        (Male, 'Male'),
        (Female, 'Female'),
    )
    AM67 = "AM67"
    AM78 = "AM78"
    AM89 = "AM89"
    PM56 = "PM56"
    PM67 = "PM67"
    PM78 = "PM78"
    
    slot = (
        (AM67, "AM67"),
        (AM78, "AM78"),
        (AM89, "AM89"),
        (PM56, "PM56"),
        (PM67, "PM67"),
        (PM78, "PM78"),
    )    

    name = models.CharField(blank=False, max_length=30, help_text="Full Name")
    entryno = models.CharField(blank=True, max_length=15,default="NON-STUDENT")
    hostel = models.CharField(blank=True, max_length=30, help_text="Hostel Name",default="NON-STUDENT")
    mobileno = models.CharField(blank=True, max_length=15, help_text="Mobile Number")
    email = models.CharField(blank=False, max_length=30, help_text="Email ID")
    gender = models.CharField(blank=False, max_length=15, choices=gender)
    slot = models.CharField(blank=False, max_length=20, choices=slot,default = AM67)
    user_pic = models.ImageField(upload_to="Swimming_registrations/Users_pics",blank=True)
    weekno = models.IntegerField(default=0)
    monthno = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)
    relativeCode  = models.CharField(default="0000",blank=False, max_length=30, help_text="0000 for Non-relatives")

class swimmingUserConfirmation(models.Model):
    
    email = models.CharField(blank=False, max_length=30, help_text="Email")
    code = models.CharField(blank=False, max_length=15,help_text="Email")
    
class swimmingForm(models.Model):
    email = models.CharField(blank=False, max_length=30, help_text="Email")
    image = models.ImageField(upload_to="Swimming_registrations/Swimming_forms",blank=True)
    date = models.DateField(default=datetime.date.today)
    name = models.CharField(default="",blank=False, max_length=30, help_text="Name")
    usertype = models.CharField(default="",blank=False, max_length=30, help_text="User Type")
    relativeCode  = models.CharField(default="0000",blank=False, max_length=30, help_text="0000 for Non-relatives")
    approvedStatus = models.BooleanField(default=False, blank=False)
    disapprovedStatus  = models.BooleanField(default=False, blank=False)

class swimmingRelative(models.Model):
    email = models.CharField(blank=False, max_length=30, help_text="Email")
    relation = models.CharField(blank=True, max_length=30, help_text="Relation")
    relativeName = models.CharField(blank=True, max_length=30, help_text="Relative's Name")
    image = models.ImageField(upload_to="Swimming_registrations/Relative_proof",blank=True)
    date = models.DateField(default=datetime.date.today)
    relativeCode = models.CharField(default="0000",blank=False, max_length=30, help_text="0000 for Non-relatives")
    approvedStatus = models.BooleanField(default=False, blank=False)
    disapprovedStatus  = models.BooleanField(default=False, blank=False)

class coachFeedback(models.Model):

    name = models.CharField(blank=False, max_length=30, help_text="Full Name")
    email = models.CharField(blank=False, max_length=30, help_text="Email")
    feedback = models.CharField(default="",blank=False, max_length=500, help_text="Name")
    sports = models.CharField(blank=False, max_length=20, choices=SPORTS,default = "Athletics")

class ReimbursementForms(models.Model):

    name = models.CharField(blank=False, max_length=30, help_text="Full Name")
    image = models.ImageField(upload_to="ReimbursementForms",blank=True)
    email = models.CharField(blank=False, max_length=30, help_text="Email")
    uid = models.CharField(blank=False, max_length=30, help_text="UID")
    status = models.CharField(default = 1,blank=False, max_length=30, help_text="UID")

class yearBookPeople(models.Model):
    uid = models.CharField(blank=False, max_length=30, help_text="UID")
    name = models.CharField(blank=False, max_length=30, help_text="Full Name")
    image_link = models.CharField(blank=False, max_length=500)
    sports = models.CharField(blank=False, max_length=20, choices=SPORTS,default = "Athletics")
    entryno = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=False, max_length=30, help_text="Email")
    oneLiner = models.CharField(blank=True, max_length=1000)
    contact = models.CharField(blank=True, max_length=15)
    q1 = models.CharField(blank=True, max_length=1000)
    q2 = models.CharField(blank=True, max_length=1000)
    q3 = models.CharField(blank=True, max_length=1000)
    q4 = models.CharField(blank=True, max_length=1000)
    a1 = models.CharField(blank=True, max_length=1000)
    a2 = models.CharField(blank=True, max_length=1000)
    a3 = models.CharField(blank=True, max_length=1000)
    a4 = models.CharField(blank=True, max_length=1000)
    funFact = models.CharField(blank=True, max_length=1000)

class yearBookComments(models.Model):
    uid = models.CharField(blank=False, max_length=30, help_text="UID")
    commentedBy = models.CharField(blank=False, max_length=30, help_text="Full Name")
    comment = models.CharField(blank=False, max_length=1000, help_text="Comment")

