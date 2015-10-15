Troubleshooting Tracktivity Pets / Known Problems
========================================================

- The Scenery called Oak Tree Park required to create a pet, if you delete this it will not work. Can change the default scenery by going to line   252 of utils.py in tracktivityPetsWebsite and changing the name to whatever default scenery you want (as named in admin page)
- Pets need a phrase for each mood otherwise whenever the user logs while their current pet is at the mood without a phrase, they will be greeted with an exception.
- Django superusers are not automatically created a Tracktivity Pets profile. So if they try to visit the website logged in, they will be greeted with an exception.
- Users can only have one account linked to a fitbit account (the latest linked one), so if a user registers a Fitbit account that already  exists, the old Tracktivity Pets account will not be updated.

