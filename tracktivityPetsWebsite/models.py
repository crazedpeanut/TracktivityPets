from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
import datetime
from django.utils import timezone
from collections import OrderedDict

#TODO add helper functions and __name__

STEPS_IN_DURATION = 'steps_in_duration'

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
    
    def get_owned_scenery(self):
        return CollectedScenery.objects.filter(inventory=self)
    
    def get_owned_scenery_in_queryset(self, set):
        return CollectedScenery.objects.filter(inventory=self, scenery__in=set)
    
    def get_collected_items_for_pet(self, pet):
        all = self.get_owned_items()
        data = []
        for collected_item in all:
            if collected_item.item.belongs_to.pk == pet.pk:
                data.append(collected_item)
        return data
    
    def is_item_owned_by_pet(self, pet, item):
        owned = self.get_collected_items_for_pet(pet)
        for i in owned:
            if i.item == item:
                return True
        return False
    
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
    
    def calculate_unpurchased_scenery(self, all_scenery, owned_scenery):
        unpurchased_scenery = []
        for scenery in all_scenery:#remove any scenery in all_scenery that exist in owned_scenery, to get the ones that are unpurchased
            found = False
            for i in owned_scenery:
                if i.scenery.name == scenery.name:
                    found=True
                    break
            if not found:
                unpurchased_scenery.append(scenery)
        return unpurchased_scenery         

class Level(models.Model):
    level = models.IntegerField(unique=True)
    experience_needed = models.IntegerField(default=0)
    
    def __str__(self):             
        return str(self.level) + ": " + str(self.experience_needed)
    
class Scenery(models.Model):
    experience_to_unlock = models.IntegerField()
    image_location = models.TextField(default="")
    description = models.TextField(default="")
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    
    def __str__(self):             
        return self.name
    
    def image_tag(self):
        start_url = static('tracktivityPetsWebsite/images')
        return u'<img src="{url}/scenery/{location}" />'.format(url=start_url, location=self.image_location)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    
    def get_image_path(self):
        start_url = static('tracktivityPetsWebsite/images')
        return "{url}/scenery/{location}".format(url=start_url, location=self.image_location)
    
class CollectedScenery(models.Model):
    scenery = models.ForeignKey(Scenery)
    inventory = models.ForeignKey(Inventory)
    
    def __str__(self):             
        return self.scenery.name

class Pet(models.Model):
    starter_level = models.ForeignKey(Level)
    default_name = models.CharField(max_length=100)
    experience_to_unlock = models.IntegerField()
    cost = models.IntegerField()
    
    def __str__(self):             
        return self.default_name
    
    def get_default_image_path(self):
        image_location = self.mood_set.filter(happiness_needed=-1)[0].image_location
        start_url = static('tracktivityPetsWebsite/images')
        return '{url}/pets/{name}/{location}'.format(url=start_url, name=self.default_name, location=image_location)

class CollectedPet(models.Model):
    pet = models.ForeignKey(Pet)
    inventory = models.ForeignKey(Inventory)
    level = models.ForeignKey(Level)
    name = models.CharField(max_length=100, default=pet.name)
    date_created = models.DateTimeField()
    scenery = models.ForeignKey(CollectedScenery, null=True)
    
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

    def get_current_scenery_image(self):
        start_url = static('tracktivityPetsWebsite/images')
        try:
            image_location = self.scenery.scenery.image_location
        except:
            image_location = ""
        return '{url}/scenery/{location}'.format(url=start_url, location=image_location)
    
    def get_default_image_path(self):
        self.pet.get_default_image_path()
        
    def get_all_equipped_items_image_paths(self):
        images = []
        all_items = self.inventory.get_collected_items_for_pet(self.pet)
        for item in all_items:
            if item.equipped:
                images.append(item.item.get_image_path())
        return images
        
    
class BodyPart(models.Model):
    name = models.CharField(max_length=100)
        
    def __str__(self):             
        return self.name
    
class Item(models.Model):
    experience_to_unlock = models.IntegerField()
    image_location = models.TextField(default="")
    description = models.TextField(default="")
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    belongs_to = models.ForeignKey(Pet, null=True)
    body_part = models.ForeignKey(BodyPart)
    
    def __str__(self):             
        return self.belongs_to.default_name + ": " + self.name
    
    def get_image_path(self):
        start_url = static('tracktivityPetsWebsite/images')
        return '{url}/items/{location}'.format(url=start_url, location=self.image_location)

class CollectedItem(models.Model):
    item = models.ForeignKey(Item)
    inventory = models.ForeignKey(Inventory)
    #equipped_on = models.ForeignKey(CollectedPet, null=True, blank=True)
    equipped = models.BooleanField(default=False)
    
    def __str__(self):             
        return self.item.name
    
class Profile(models.Model):
    user = models.OneToOneField(User)
    inventory = models.OneToOneField(Inventory)  
    current_pet = models.OneToOneField(CollectedPet, null=True)
    total_pet_pennies = models.IntegerField(default=0)
    last_fitbit_sync = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):             
        return self.user.email + " profile"
    
    def get_total_xp(self):
        collected_pets = self.inventory.get_owned_pets()
        total_xp = 0
        for pet in collected_pets:
            total_xp += pet.get_total_experience()
        return total_xp
    
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

MicroChallengeTypes = (
    (STEPS_IN_DURATION,'STEPS_IN_DURATION'),
)

class MicroChallenge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    overview = models.TextField(default="")
    challenge_type = models.CharField(choices=MicroChallengeTypes, max_length=100, null=True)
    duration_mins = models.IntegerField(default=0)

    def __str__(self):
        return "Micro Challenge: " + self.name

class MicroChallengeMedal(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MicroChallengeState(models.Model):
    steps = models.IntegerField()

    def __str__(self):
        return "Micro Challenge State. Steps: " + str(self.steps)

class UserMicroChallengeState(models.Model):
    state = models.ForeignKey(MicroChallengeState)

class UserMicroChallenge(models.Model):
    micro_challenge = models.ForeignKey(MicroChallenge)
    state = models.ForeignKey(UserMicroChallengeState)
    profile = models.ForeignKey(Profile, null=True)
    complete = models.BooleanField(default=False)
    date_started = models.DateTimeField(default=datetime.datetime.now, null=True)
    date_end = models.DateTimeField(null=True)
    date_completed = models.DateTimeField(null=True)

class PetSwap(models.Model):
    from_pet = models.ForeignKey(CollectedPet, related_name='from_pet')
    to_pet = models.ForeignKey(CollectedPet, related_name='to_pet')
    time_swapped = models.DateTimeField(default=datetime.datetime.now)

class MicroChallengeGoal(models.Model):
    micro_challenge = models.ForeignKey(MicroChallenge)
    medal = models.ForeignKey(MicroChallengeMedal)
    description = models.TextField(default="")
    pet_pennies_reward = models.IntegerField()
    goal_state = models.ForeignKey(MicroChallengeState)
    achieved = models.BooleanField()

    def __str__(self):
        return "Micro Challenge Goal: " + self.micro_challenge.name + ", medal: " + self.medal.name
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
