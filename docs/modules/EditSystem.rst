Editing Tracktivity Pets
===========================

In this section extending the system will be discussed. This includes where to start for release 3 features, as well as adding new pets, scenery, items, and challenges. One of the features that Django has built in is an admin view that allows developers to easily access the database and add/edit/remove entries in the database. Some time was spent on setting up specific models in here so that certain things could easily be modified, though it should be noted that this was not a requirement and as such does not work perfectly.

Accessing the Admin Page
-----------------------------

To add new pets, scenery, items, and challenges, you simply log navigate to <domain name>/admin and log in as an administrator. By default this is set to a username:password pair of administrator:admin (though may be different if you have changed this). From this section you can see a range of headings such as ‘Authentication and Authorization’, ‘Djcelery’, ‘Fitapp’, and ‘Tracktivitypetswebsite’. Under these are specific subheadings which directly correlate with the models defined.

Adding Pets
-----------------------------

From the admin page, adding a new pet is as simple as clicking on ‘Pets’ under ‘Tracktivitypetswebsite’. 

Here you will be presented with a list of currently existing pets, and by clicking the button at the top right labelled ‘Add pet’, you will be taken to a form to create a new pet. Similarly, clicking on an existing pet’s name will take you to an already filled out form where you can edit and save changes.

Upon clicking on the ‘Add pet’ button, an administrator will be presented with the blank form to fill out. Clicking on the ‘Starter level’ dropdown list, you can select what level this pet will start at when purchased from the store or selected from the pet selection page. The default name plays two major roles: first off it will be what the user will see the pet called on the pet selection page and store, and what it is referred to throughout the admin page, and secondly (which is a very important step) is that any images for the pet or pet’s items MUST be in the desired spot under an identical (even including capitals) folder. 

Using an example of a pet called ‘Peter’, all images related to the silhouette, default picture, and evolution/mood images for Peter would go in <project folder>/tracktivityPetsWebsite/static/trackivityPetsWebsite/images/pets/Peter and any cosmetic items for Peter would go in <project folder>/tracktivityPetsWebsite/static/trackivityPetsWebsite/images/items/Peter. To get proper results for this, the development team made all pets 1024x1024 pixels, with a transparent background. Items are also the same dimension, and were simply positioned in Photoshop so that they were in the correct position, with a very large amount of whitespace. If you do not do this, unwanted results may occur. 

‘Experience to unlock’ in this form is how much experience is needed (across all pets) for user’s to be able to purchase this pet, otherwise it will appear locked. ‘Cost’ is how many pet pennies the user must have in order to be able to purchase an unlocked pet. 

Next in the form is how to set up the images for the pet. Setting the level to 1, the happiness to -1, will set up the required default picture for this pet. This default picture is used in the pet selection page and in the store, and should be used to represent what the pet is like to a user. The image location is relative to the pet’s image folder, as described above. 

As such, an image entered into this field as default_picture.png would need to exist in the file structure as <project folder>/tracktivityPetsWebsite/static/trackivityPetsWebsite/images/pets/Peter/default_picture.png. Next to this image location field is a description, this will be used later on to set the mood for the pet, so try name these something meaningful, such as default picture, silhouette, evolution 1 sad, etc. 

To set up a pet entirely, after the admin has set a default picture, they also need to set a silhouette, which is done much the same way as the default picture, but for this the happiness is set to -2. From here it is time to set the happiness and evolution images for the pet. The way this works is quite simple, the level indicates what level is required for the image should be shown, and the happiness indicates how much happiness is needed for this image. 

The system will then pick the closest (without going above) image based on the level and happiness the pet has. For example, if two images are present, a level 1 and 0 happiness, and a level 5 and 50 happiness, but the pet is level 3 and has 70 happiness, the requirements for the second image will not be met, so the first image will instead be used. If the pet was level 5 however, the second image would be selected. For best practice, the development team used three evolutions (at level 1, level 5, and level 10), with three moods each (at happiness 0, happiness 35, and happiness 70). 

Below all of this, is the ‘Stories’ section. A default story for the pet should be set up, this is used in the pet selection page, the store, and many other places throughout. To set this up, simply select the level as 1, and write in a story. To add more stories, simply add a new level at whatever level you wish, and enter a story. Once all this is done, simply click the save button at the bottom right hand corner (note: you should probably click ‘save and continue editing’ throughout, as this can be time consuming, and you do not want to lose work). At this stage, it is assumed that a default picture, silhouette, and multiple evolutions/happiness images have been setup, as well as at least a default story for the pet.

Next up is setting the phrases for the pet, which will be spoken depending on the mood of the pet. To do this, navigate back to the original admin page, and click on ‘Moods’ under ‘Tracktivitypetswebsite’. Here you will be presented with every mood that exists for every single pet, for ease of finding the pet’s name is displayed first, followed by the description you set for each image while setting up the pet (so name them something useful!). 

To add new phrases, simply click on the mood you wish the pet to state these phrases as, and type away! Do note that a phrase for each pet does need to be set, otherwise the website will give an error if this mood if ever reached by a user (and again, this is an easy way to access the database, not a perfectly working solution). At this stage, the pet should be fully set up and ready to use by users, throughout, if any help is needed simply refer to already existing pets/stories/moods. 

Adding Scenery
-----------------------------

Adding a new scenery is extremely simple, far more simple than adding a pet. To add a new scenery, simply navigate to the admin page as described earlier, then press on ‘Scenerys’ under ‘Trackitivtypetswebsite’. Here you will be presented with a list of currently existing scenery, and just like ‘Pets’, you can either modify an existing scenery, or add a new scenery by clicking ‘Add scenery’. 

Upon clicking ‘Add scenery’, an admin will be presented with a fresh form. The ‘name’ section is what the scenery will be called, and will be displayed in the store and inventory. ‘Experience to unlock’ is the amount of experience that is required (across all pets) to unlock this scenery. ‘Cost’ is how many pet pennies are required in order to purchase this scenery once unlocked. ‘Description’ is the description/story of the scenery, and will be displayed to users in the store and inventory. Image location is a relative path from <project folder>/tracktivityPetsWebsite/static/trackivityPetsWebsite/images/scenery such that a scenery with the image name of beach.jpg would be found in <project folder>/tracktivityPetsWebsite/static/trackivityPetsWebsite/images/scenery/beach.jpg. 

It should also be noted that there is a CSS rule that zooms in on part of the scenery, which is done so to get more of the center of the image based on screen size, so the image may look slightly cropped on certain screen sizes. Clicking on save should now make this scenery live on the website.

Adding Items
-----------------------------

Adding items are very similar to adding scenery, though slightly different. To add a new item, simply navigate to the admin page as described earlier and press ‘Items’ under ‘Tracktivitypetswebsite’. Here you will be presented with a list of items, that starts with a pets name, followed by the item name. Just like scenery and pets, you can either click one of these to modify an existing item, or press the ‘Add item’ at the top right hand corner to add a new item. Upon clicking on ‘Add item’ you will be presented with a fresh form. ‘Name’ refers to what the item should be called, and will be displayed to the user in the store and inventory. ‘Experience to unlock’ is how much experience is needed by this pet in order to unlock this item. ‘Cost’ refers to the amount of pet pennies required in order to purchase this item once unlocked. ‘Belongs to’ is a drop down box with a list of all pets that exist (and is updated automatically with new pets), and indicates which pet this item is usable on (only one pet per item). 

‘Body part’ is used to indicate which body part this item goes on, and is used by the system to detect other items on this body part, so that a warning can be given to the user to unequip the other item. If the body part does not exist, you can simply press the + next to this which should take you to a form that simply takes the name of the body part so you can add your own. ‘Description’ is the description/story for this item, and is displayed to the user in the store and inventory. 

Image location is a relative path, and is expected to be found in the images folder, under the name of the pet. For example, if an item is called blue_hat.png and belongs to a pet called Peter, it should be found in <project folder>/tracktivityPetsWebsite/static/trackivityPetsWebsite/images/items/Peter/blue_hat.png. Clicking on save should now make this item be live on the website. 

Adding Challenges
-----------------------------

To add a new challenge to Tracktivity Pets, the first step is to navigate to the Tracktivity Pets administration panel (<hostname>/admin) and log in with a django superuser account. In the Tracktivitypetswebsite section, click the Micro challenges model. Click the 'Add micro challenge' button on the right hand side of the page, which will take you to a form.

Fill out your challenge details in the form. The fields should be fairly self explanitory. Here is a brief explanation of all of them:

- Name - This is the name of your challenge. 
- Overview - This is just some text to describe what your challenge is and what the user has to do to complete it.
- Challenge Type - This is used by the backend to determine how to calculate if the user has completed the challenge or not. The only type of   challenge implemented so far is STEPS_IN_DURATION.
- Duration mins - This is how long the challenge goes for, or how much time the user has to complete the challenge.

Once the form is filled out, click the 'Save' button.

Next up, we need to create the goals for the challenge. These are essentially how many steps the user has to take and the reward they get for accomplishing it. To create your goals go back to the administration panel home page and click 'Micro challenge goals'.

Click the 'Add micro challenge goal' on the right hand side of the screen. You should now see a form. Here is a description of the fields in this form:

- Micro challenge - This is the micro challenge this goal refers to.
- Medal - This is the medal that the user receives for achieving this challenge. The current medals are gold, silver and bronze, but you can    add more if you would like.
- Description - A textfield for describing how the user can achieve this goal.
- Pet pennies reward - How many pet pennies the user receives for completing this goal.
- Goal state - This is the state that has to be achieved in order to complete this goal. At the moment a goal state only contains the amount    of steps.

If things have gone well, you should have a new challenge for your users to try out. Hooray!
 
Extending For Release 3
-----------------------------

There were two features stated as being in “release three” for this project (multiplayer challenges and a statistics view), and this section will provide a brief overview of where to start looking to implement said features.

First and foremost, to get any new pages to work, you need to setup a url in urls.py to tell Django what view to call when the user enters a specific url (maybe /statistics or /multiplayer_challenge). Also any new view will need to be added to __init__.py in the format as described in the backend (tracktivityPetsWebsite) section. 

To implement the multiplayer challenges, a model for ‘Friend’ will need to be added, which simply requires a one-to-many relationship field to other ‘User’ models. An extension of ‘Profile’ may also want to be made to add more social aspects such as a user profile picture, or some statistics such as sex, age, etc. This could be further added by adding a ‘Status’ model for users to be able to make posts or something, if you wish to go down that route. It should also be noted that a unique username currently exists for every user, though is not used, which could be used as a screen name for multiplayer challenges/friends as so avoid giving them an email address. A page would need to be setup so that users can browse people, or add/delete friends somehow. Another page would be needed for the actual multiplayer challenges, and could be based off of the current ‘Challenge’ view and template, though would need a way to select a friend to invite. To implement the actual multiplayer challenges, minimal changes would need to be made to the existing models. A new model could be created that takes the ID of both users and the datetime the challenge is to be started. Once the opponent accepts the challenge, a new UserMicroChallenge instance would be created for both users. Once the duration of the challenge is over, a mechanism would need to be implemented so that the users are notified of the results of the challenge.

The statistics page should be very straight forward. Lots of the data already exists, and it is simply a matter of looking through the models to see what data there is. This can include stuff such as a pet’s happiness for a given day, experience earned on that day, total experience for a pet, etc. All of this is searchable via queries and can be ordered. Other aspects such as rewards from challenges can be used. Further statistics would be as simple as modifying the existing models to add new data fields to track. A statistics page would then need to be created and simply render a template to fill in the HTML with fields retrieved from the database. 

