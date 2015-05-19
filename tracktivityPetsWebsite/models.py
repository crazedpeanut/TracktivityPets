from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
import datetime
from django.utils import timezone
from collections import OrderedDict

#TODO add helper functions and __name__

class Inventory(models.Model): #need to look up how to get a model with only an ID (automatically done for all models)
    def __str__(self):    
        try:         
            return str(self.profile.user.email) + " inventory"
        except:
            return "DELETE ME" #crappy self fix, deleting a user doesnt delete inventory, TODO

class Level(models.Model):
    level = models.IntegerField(unique=True)
    experience_needed = models.IntegerField(default=0)
    
    def __str__(self):             
        return str(self.level) + ": " + str(self.experience_needed)

class Pet(models.Model):
    starter_level = models.ForeignKey(Level)
    default_name = models.CharField(max_length=100)
    experience_to_unlock = models.IntegerField()
    cost = models.IntegerField()
    
    def __str__(self):             
        return self.default_name

class CollectedPet(models.Model):
    pet = models.ForeignKey(Pet)
    inventory = models.ForeignKey(Inventory)
    level = models.ForeignKey(Level)
    name = models.CharField(max_length=100, default=pet.name)
    date_created = models.DateTimeField()
    
    def __str__(self):             
        return self.pet.default_name + ": " + self.name
    
    def get_current_mood_image_location(self):
        start_url = static('tracktivityPetsWebsite/images')
        image_location = self.get_current_mood().image_location
        return '{url}/pets/{name}/{location}'.format(url=start_url, name=self.pet.default_name, location=image_location)
    
    #this method is pretty much pointless...
    def get_total_happiness(self):
        data = self.happiness_set.all()
        total = 0
        for h in data:
            data += h.amount
        return total
    
    def get_total_experience(self):
        data = self.experience_set.all()
        total = 0
        for e in data:
            total += e.amount
        return total
    
    def get_happiness_last_seven_days(self):
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        dates = self.happiness_set.filter(date__gt=seven_days_ago).order_by('date')
        values = OrderedDict()
        for d in dates:
            date = d.date.strftime('%d-%m')
            values[date] = OrderedDict()
            values[date]['date'] = date
            values[date]['happiness'] = d.amount/100
        return values
    
    def get_todays_happiness_value(self):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        try:
            return self.happiness_set.get(date=today).amount
        except:
            return 0 #might not have synced today, so its currently 0
    
    def get_experience_last_seven_days(self):
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        dates = self.experience_set.filter(date__gt=seven_days_ago).order_by('date')
        values = OrderedDict()
        largest_number = 0
        for d in dates:
            date = d.date.strftime('%d-%m')
            values[date] = OrderedDict()
            values[date]['date'] = date
            values[date]['experience'] = d.amount
            
            if d.amount > largest_number:
                largest_number = d.amount
        return largest_number, values
    
    def get_all_accumulative_experience(self):
        pass
        dates = self.experience_set.all().order_by('date')
        values = OrderedDict()
        accumulative = 0 
        for d in dates:
            date = d.date.strftime('%d-%m')
            values[date] = OrderedDict()
            values[date]['date'] = date
            accumulative += d.amount
            values[date]['experience'] = accumulative
            
        return values
    
    def get_age_in_days(self):
        return (timezone.now() - self.date_created).days
    
    def get_next_level(self):
        try:
            return Level.objects.get(level = self.level.level + 1)
        except:
            return None
        
    def get_current_mood(self):
        happiness = self.get_todays_happiness_value()
         #TODO: this compares keys, levels are already in order, but if you deleted level 1, then added it again, it would then be greater than the others and this would fail
        return self.pet.mood_set.filter(happiness_needed__lte=happiness, level__lte=self.level).order_by('-level', '-happiness_needed')[0]
    
    def get_random_current_phrase_by_mood(self, mood):
        return mood.phrase_set.all().order_by('?')[0]
    
    def get_unlocked_stories(self):
        return Story.objects.filter(pet=self.pet, level_unlocked__lte=self.level).order_by('level_unlocked')
    
    def get_stories_available(self):
        return Story.objects.filter(pet=self.pet)

class Profile(models.Model):
    user = models.OneToOneField(User)
    inventory = models.OneToOneField(Inventory)  
    current_pet = models.OneToOneField(CollectedPet, null=True)
    total_pet_pennies = models.IntegerField(default=0)
    last_fitbit_sync = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):             
        return self.user.email + " profile"
    
class Happiness(models.Model):
    pet = models.ForeignKey(CollectedPet)
    amount = models.IntegerField()
    date = models.DateTimeField()
    
    def __str__(self):             
        return self.pet.name + " " + str(self.date) + " " + str(self.amount)

class Experience(models.Model):
    pet = models.ForeignKey(CollectedPet)
    amount = models.IntegerField()
    date = models.DateTimeField()
    
    def __str__(self):             
        return self.pet.name + " " + str(self.date) + " " + str(self.amount)
 
class Mood(models.Model):
    pet = models.ForeignKey(Pet)
    level = models.ForeignKey(Level) #different images depending on level
    happiness_needed = models.IntegerField()
    image_location = models.TextField()
    description = models.TextField()
    
    def image_tag(self):
        start_url = static('tracktivityPetsWebsite/images')
        return u'<img src="{url}/pets/{name}/{location}" />'.format(url=start_url, name=self.pet.default_name, location=self.image_location)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    
    def __str__(self):             
        return self.description

class Phrase(models.Model):
    mood = models.ForeignKey(Mood)
    text = models.TextField()
    
    def __str__(self): 
        return self.text[0:20]

class Story(models.Model):
    level_unlocked = models.ForeignKey(Level)
    pet = models.ForeignKey(Pet)
    text = models.TextField()

#release 2 models below


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    