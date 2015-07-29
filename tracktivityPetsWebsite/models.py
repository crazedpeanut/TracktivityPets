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
        
    def get_owned_items(self):
        return CollectedItem.objects.filter(inventory=self)
        
    def get_owned_items_in_queryset(self, set):
        return CollectedItem.objects.filter(inventory=self, item__in=set)
    
    def get_owned_pets(self):
        return CollectedPet.objects.filter(inventory=self)
     
    def get_owned_pets_in_queryset(self, set):
        return CollectedPet.objects.filter(inventory=self, pet__in=set) 
    
    def calculate_unpurchased_items(self, usable_items, owned_items):
        unpurchased_items = []
        for item in usable_items:#remove any items in usable_items that exist in owned_items, to get the ones that are unpurchased
            found = False
            for i in owned_items:
                if i.item.name == item.name:
                    found=True
                    break
            if not found:
                unpurchased_items.append(item)
        return unpurchased_items
    
    def calculate_unpurchased_pets(self, all_pets, owned_pets):
        unpurchased_pet = []
        for pet in all_pets:#remove any pets in all_pets that exist in owned_pets, to get the ones that are unpurchased
            found = False
            for i in owned_pets:
                if i.pet.default_name == pet.default_name:
                    found=True
                    break
            if not found:
                unpurchased_pet.append(pet)
        return unpurchased_pet

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

    def get_usable_items(self):
        return Item.objects.filter(usable__pet_usable_on=self.pet)
    
    def set_name(self, name):
        self.name = name

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
    image_location = models.TextField(default="")
    description = models.TextField(default="")
    
    def image_tag(self):
        start_url = static('tracktivityPetsWebsite/images')
        return u'<img src="{url}/pets/{name}/{location}" />'.format(url=start_url, name=self.pet.default_name, location=self.image_location)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    
    def __str__(self):             
        return self.description

class Phrase(models.Model):
    mood = models.ForeignKey(Mood)
    text = models.TextField(default="")
    
    def __str__(self): 
        return self.text[0:20]

class Story(models.Model):
    level_unlocked = models.ForeignKey(Level)
    pet = models.ForeignKey(Pet)
    text = models.TextField(default="")

#release 2 models below

class Item(models.Model):
    experience_to_unlock = models.IntegerField()
    image_location = models.TextField(default="")
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    
    def __str__(self):             
        return self.name

class CollectedItem(models.Model):
    item = models.ForeignKey(Item)
    inventory = models.ForeignKey(Inventory)
    equipped_on = models.ForeignKey(CollectedPet, null=True)
    
    def __str__(self):             
        return self.item.name

class Usable(models.Model):
    pet_usable_on = models.ForeignKey(Pet)
    item_to_use = models.ForeignKey(Item)

class MicroChallenge(models.Model):
    name = models.CharField(max_length=100)
    overview = models.TextField(default="")
    
class UserMicroChallengeState(models.Model):
    state = models.CharField(max_length=100)

class UserMicroChallenge(models.Model):
    micro_challenge = models.ForeignKey(MicroChallenge)
    state = models.ForeignKey(UserMicroChallengeState)
    user = models.OneToOneField(User)
    
class MicroChallengeMedal(models.Model):
    name = models.CharField(max_length=100)

class MicroChallengeGoal(models.Model):
    micro_challenge = models.ForeignKey(MicroChallenge)
    medal = models.ForeignKey(MicroChallengeMedal)
    description = models.TextField(default="")
    pet_pennies_reward = models.IntegerField()
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    