from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

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
    
    def total_happiness(self):
        data = self.happiness_set.all()
        total = 0
        for h in data:
            data += h.amount
        return total
    
    def total_experience(self):
        data = self.experience_set.all()
        total = 0
        for e in data:
            data += e.amount
        return total

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

class UserStory(models.Model):
    story = models.ForeignKey(Story)
    collected_pet = models.ForeignKey(CollectedPet)
    is_viewed = models.BooleanField(default=False)

#release 2 models below


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    