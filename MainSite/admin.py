from django.contrib import admin
from .models import yearBookPeople, yearBookComments, People, Event, Announcement, LiveMatch, Comment, Gallery, Pride, JuniorExe, FantasyLeagueMatch, FantasyLeaguePlayer, FantasyLeagueSubmission, FantasyLeaguePoints, DailyFantasyLeaguePoints ,swimmingUser,swimmingForm, swimmingRelative, Hof,coachFeedback, ReimbursementForms

# Register your models here.

admin.site.register(People)
admin.site.register(Event)
admin.site.register(Gallery)
admin.site.register(Announcement)
admin.site.register(LiveMatch)
admin.site.register(Comment)
admin.site.register(JuniorExe)
admin.site.register(Pride)
admin.site.register(FantasyLeagueMatch)
admin.site.register(FantasyLeaguePlayer)
admin.site.register(FantasyLeagueSubmission)
admin.site.register(FantasyLeaguePoints)
admin.site.register(DailyFantasyLeaguePoints)
admin.site.register(swimmingUser)
admin.site.register(swimmingForm)
admin.site.register(swimmingRelative)
admin.site.register(Hof)
admin.site.register(coachFeedback)
admin.site.register(ReimbursementForms)
admin.site.register(yearBookPeople)
admin.site.register(yearBookComments)





