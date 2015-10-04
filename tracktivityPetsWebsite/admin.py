from django.contrib import admin

from tracktivityPetsWebsite.models import Pet, Mood, Level, Phrase, Story, Profile, CollectedPet, Inventory, \
    Item, Scenery, CollectedItem, CollectedScenery, BodyPart, MicroChallenge, MicroChallengeGoal,\
    MicroChallengeState, UserMicroChallenge, UserMicroChallengeState, MicroChallengeMedal,\
    UserMicroChallengeGoalStatus, UserNotification

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib import admin
from django import forms
from django.contrib.auth import admin as upstream
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext, ugettext_lazy as _

######################################
class PhraseInline(admin.TabularInline):
    model = Phrase
    extra = 1
    
class MoodAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['description']}),
    ] 
    inlines = [PhraseInline]
###############################
class LevelAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['level', 'experience_needed']}),
    ]
########################################
class StoryInline(admin.TabularInline):
    model = Story
    extra = 1

class MoodInline(admin.TabularInline):
    model = Mood
    readonly_fields = ('image_tag',)
    extra = 1
    search_fields = ['level']
    
class PetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['starter_level', 'default_name', 'experience_to_unlock', 'cost']}),
    ]
    inlines = [MoodInline, StoryInline]
    
########################################
class CollectedPetsInline(admin.TabularInline):
    model = CollectedPet
    extra = 1
    
class CollectedItemsInline(admin.TabularInline):
    model = CollectedItem
    extra = 1 
    
class CollectedScenerysInLine(admin.TabularInline):
    model = CollectedScenery
    extra = 1
        
class InventoryAdmin(admin.ModelAdmin):
    inlines = [CollectedPetsInline, CollectedItemsInline, CollectedScenerysInLine]

#########################################
class ProfileInline(admin.StackedInline):
    model = Profile
    
class UserAdmin(upstream.UserAdmin):
    inlines = [ProfileInline]
    fieldsets = (
        (None, {'fields': ('username', 'password','email')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email')}
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    
    def save_model(self, request, user, form, change):
        if change:
            user.save()
        else:
            user.save()
            inventory = Inventory.objects.create()
            inventory.save()
            profile = Profile.objects.create(user=user, inventory=inventory)
            profile.save()
            inventory.save()
            user.save()
        
''' #TODO: need to actually delete everything, such as pets etc...
None of this code seems to work
    def delete_model(request, user):
        profile = Profile.objects.get(user=user)
        inventory = profile.inventory
        inventory = delete()
        profile.delete()
        #user.delete()'''
        
    
#########################################
    
class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'experience_to_unlock', 'cost', "belongs_to", "body_part", "description", "image_location"]}),
    ] 
    
#########################################

class SceneryAdmin(admin.ModelAdmin):
    fields = ('name', 'experience_to_unlock', 'cost', 'description', 'image_location')
    readonly_fields = ('image_tag',)
    
#########################################

class BodyPartAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
    ] 

#########################################

class CollectedItemAdmin(admin.ModelAdmin):
    fields = ('item', 'inventory', 'equipped')
    
#########################################

class CollectedPetAdmin(admin.ModelAdmin):
    fields = ('pet', 'inventory')
    
#########################################

class CollectedSceneryAdmin(admin.ModelAdmin):
    fields = ('scenery', 'inventory')
    
#########################################

class MicroChallengeAdmin(admin.ModelAdmin):
    fields = ('name', 'overview', 'challenge_type', 'duration_mins')

#########################################

class MicroChallengeGoalAdmin(admin.ModelAdmin):
    fields = ('micro_challenge', 'medal', 'description', 'pet_pennies_reward', 'goal_state')


#########################################

class MicroChallengeStateAdmin(admin.ModelAdmin):
    fields = ('steps',)

#########################################

class UserMicroChallengeStateAdmin(admin.ModelAdmin):
    fields = ('state',)

#########################################

class UserMicroChallengeAdmin(admin.ModelAdmin):
    fields = ('micro_challenge', 'state', 'profile', 'complete', 'date_end', 'date_completed', 'date_started')

#########################################


class MicroChallengeMedalAdmin(admin.ModelAdmin):
    fields = ('name',)

#########################################

class UserMicroChallengeGoalStatusAdmin(admin.ModelAdmin):
    fields = ('complete', 'user_micro_chal', 'micro_chal_goal')

#########################################

class UserNotificationAdmin(admin.ModelAdmin):
    fields = ('userProfile', 'dateAdded', 'message','acknowledged','notificationType')


##################################

class ExperienceAdmin(admin.ModelAdmin):
    fields = ('pet', 'amount', 'date')

admin.site.register(UserNotification, UserNotificationAdmin)
admin.site.register(UserMicroChallengeGoalStatus, UserMicroChallengeGoalStatusAdmin)
admin.site.register(MicroChallengeMedal, MicroChallengeMedalAdmin)
admin.site.register(UserMicroChallengeState, UserMicroChallengeStateAdmin)
admin.site.register(UserMicroChallenge, UserMicroChallengeAdmin)
admin.site.register(MicroChallengeState, MicroChallengeStateAdmin)
admin.site.register(Pet, PetAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Mood, MoodAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Scenery, SceneryAdmin)
admin.site.register(BodyPart, BodyPartAdmin)
admin.site.register(MicroChallenge, MicroChallengeAdmin)
admin.site.register(MicroChallengeGoal, MicroChallengeGoalAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

##### below are for TEST purposes only in admin, they can screw up if people link the wrong stuff
admin.site.register(CollectedItem, CollectedItemAdmin)
admin.site.register(CollectedScenery, CollectedSceneryAdmin)
admin.site.register(CollectedPet, CollectedPetAdmin)


