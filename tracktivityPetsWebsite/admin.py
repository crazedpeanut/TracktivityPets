from django.contrib import admin
from tracktivityPetsWebsite.models import Pet, Mood, Level, Phrase, Story

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
    
    #search_fields = ['default_name', 'cost']
########################################

admin.site.register(Pet, PetAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Mood, MoodAdmin)