from django.contrib import admin
from tracktivityPetsWebsite.models import Pet, Mood, Level, Phrase, Story, Profile, CollectedPet, Inventory

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
class CollectedPetsInline(admin.TabularInline):
    model = CollectedPet
    extra = 1
    
class InventoryAdmin(admin.ModelAdmin):
    inlines = [CollectedPetsInline]
    
#########################################

class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user', 'inventory', 'current_pet', 'total_pet_pennies', 'last_fitbit_sync']}),
    ]
#########################################
admin.site.register(Pet, PetAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Mood, MoodAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Inventory, InventoryAdmin)