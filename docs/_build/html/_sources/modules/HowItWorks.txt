How Tracktivity Pets Works
===========================

Dependencies
-----------------------------

* Ubuntu 14.04 LTS (May work on other operating systems however)
* Python3
* pip3
* Nginx (We used version 1.9)
* mySQL or mariaDB server 
* Python libraries
* django
* fitbit
* django-fitbit
* django-celery
* mysqlclient
* gunicorn
* Virtualenv
* RabbitMQ
* Celery

Installation
-----------------------------

1. Install Ubuntu server and install any updates available.
2. Install python3 - apt-get install python3
3. Install pip3 - apt-get install python3-pip
4. Install virtualenv - pip3 install virtualenv
5. Install the mysql client libraries - apt-get install libmysqlient-dev python3-dev
6. Install mySQL - apt-get install mysql
7. Log into mysql and create a database called “tracktivitypets”
8. Create a mySQL user called “tracktivitypets” with the password “tracktivitypets”
9. The username can be changes in the settings.py of Tracktivity Pets
10. Give the tracktivitypets user all privileges on the tracktivitypets database
11. Create a user called “django” with a default home directory - useradd django
12. Gives the user django a password - passwd django 
13. Create a directory for logs - mkdir /var/log/TracktivityPets
14. Give django ownership of /var/log/TracktivityPets - chown django:django /var/log/TracktivityPets
15. Login as the user - su django
16. cd to the home directory - cd ~
17. Create a Python virtual environment - virtualenv init
18. Copy TracktivityPets folder into the home directory of the user django
19. In the settings.py file, change the hostname or IP address of the database to the location of your database instance (localhost if mysql is installed on the same server)
20. Make sure the django user owns the files and directories within the TracktivityPets directory - chown -R django:django TracktivityPets
21. Activate the Python virtual environment - source ./init/bin/activate
22. Install the following python libraries using pip3:
	
	- django
	- fitbit
	- django-fitbit
	- django-celery
	- mysqlclient
	- gunicorn
	
23. Get django to create the tables in the database - python3 manage makemigrations, python3 manage migrate
24. Load the initial data into the database - python3 manage loaddata initdata.json
25. Install RabbitMQ server - apt-get install rabbitmq-server
26. Install nginx - apt-get install nginx
27. Create a file /etc/nginx/sites-enabled/tracktivitypets.conf
28. Define a server block to communicate to the gunicorn UNIX socket. (Below is an example server block config)
29. Set up gunicorn to run on the servers start-up using Upstart. (Below is an example configuration script)
30. In the settings.py file, you will need to configure the SMTP settings so that they work with your server. This is for the feedback functionality of the application.
	below is an example:
	
	- EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	- EMAIL_USE_TLS = True (Should be True)
	- EMAIL_HOST = 'SMTP HOSTNAME HERE'
	- EMAIL_HOST_USER = 'SMTP USERNAME'
	- EMAIL_HOST_PASSWORD = 'SMTP PASSWORD'
	- EMAIL_PORT = 587

31. In the settings.py, you will also need to change the hostname and Fitbit fields so that they correspond with your details

	- HOST_NAME = "YOUR HOSTNAME HERE"
	
	- FITAPP_CONSUMER_KEY = 'FITBIT CONSUMER KEY HERE'
	- FITAPP_CONSUMER_SECRET = 'FITBIT CONSUMER PRIVATE KEY HERE'
	- FITAPP_SUBSCRIBE = SET TO True FOR SUBSCRIPTION (ASYNC) FITBIT RESULTS 
	- FITAPP_SUBSCRIBER_ID = "FITBIT SUBSCRIBER ID HERE"

Nginx configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: nginx.txt


Gunicorn configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: upstart.txt

Structure
-----------------------------

Main Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Due to the nature of our program implementing the Django framework, our project does not have a traditional style of a main method. The entry point that a developer would need to worry about <project folder>/TracktivityPets/urls.py. This basic file is structured in such a way that branches off to use multiple different Django ‘apps’. The first is the admin page, which the developer will not need to change as these are pre-built by the Django development team, the second uses the content found in <project folder>/fitapp/urls.py, and the third being the entryway into the pages we developed, which can be found in <project folder>/tracktivityPetsWebsite/urls.py.

From here a logical representation of the url a user has entered is converted into a regex and is then matched to a function found within a view. Take for example the following code found in <project folder>/tracktivityPetsWebsite/urls.py:

    url(r'^login/$', views.user_login, name='user_login')

This means anytime a user enters <domain name>/login, the function called user_login found in <project folder>/tracktivityPetsWebsite/views/__init__.py will be called. The same works for all the other views. It is recommended to familiarise yourself with regex as to understand the symbols within the more complicated urls.

Program Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django is referred to as a model-view-controller (MVC) framework, however it is slightly different to traditional MVC frameworks, and appears to be more of a model-view-controller-template.
Traditionally views are used to represent how something should look, but Django takes a different approach and uses views to describe which data is shown. Views in Django are page-specific functions that are passed a HttpResponse object, which allows access to user data, session data, and more. Using this, the view uses logic and queries the database through the use of models, similar to the controller of traditional MVC patterns. Templates are similar to traditional views, in that they are given data and decide how to display the information. Models in Django are basically the same as traditional MVC patterns.
 
The controller portion of Django is not so much what is shown (like in MVC), but rather the system logic for following through to the correct view. This is done by looking at urls.py, defined in the project’s folder, which uses regular expression (regex) pattern matching on the URL entered by the user (as described above). It attempts to match the regex to a view, and if it is found it will then go to that view to perform the logic and querying as described above. Partial matches can be found, and will look further into other Django app’s urls.py files, if specified. If no matches are found the user is redirected to a “404 page not found” page.

Using this logic, and the explanation of the main method to indicate what function should be run, we can look further into how a page is delivered to the user. So we can assume that the system has now selected a function that is defined in <project folder>/views/__init__.py. This imports functions from other files, as clearly indicated in this file. If you then select one of the files listed there (which are found in the same folder, which is called views), you can see the logic behind how data is retrieved from the database. 

QuerySet objects are used to create an object-oriented style query that Django will change into it’s own query for the database, depending on the database used. This will then fetch the data, and return it in an object-oriented class. Logic can then be applied, such as for loops and if statements. Further down, a HttpResponse may be seen, which will return exactly the string that is found to the user’s web browser, or will call a render function, that takes a request object, a dictionary with key/value pairs, and a template to render. The request object is passed into the function automatically from when Django matches a URL, and contains HTTP specific variables, such as the ip address, cookies, and other information. For the return function, at this point in time the program should now have a set of key/value pairs that contain variables that have had logic applied to them, such as retrieving the user’s current pet, how much experience that pet, and so on. The third variable will have a Django specific path, that uses a shortcut to find templates that are (by default, and such in this software), found in <project folder>/tracktivityPetsWebsite/templates.


A URL of tracktivityPetsWebsite/pet_selection.py would in fact be referring to <project folder>/tracktivityPetsWebsite/templates/pet_selection.py due to this shortcut. What this now means is that the dictionary full of variables will have been passed to this template in order to render it. Throughout this HTML file will be brackets indicated as either {{ <variable> }} or {% <logic> %}. These are Jinja2 specific tags, and knowledge on such language will be required to understand what is happening here. All variables inside {{ <variable> }} will be named appropriately so that they reflect the same key as was passed into this template from the python file previously discussed. Once Jinja2 has completed filling in these variables and using it’s logic, the now completed HTML file will be delivered to the user’s device for viewing.

Below is a flow diagram that shows the process that Django takes, as described above.

.. image:: ../images/overview.png

Database Design and Class Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: ../images/erdiagram.png

Above is an Entity-Relationship (ER) diagram showing the final version of the database. This is a direct representation of the models found in <project folder>/tracktivityPetsWebsite/models.py. The external user model represents the built-in User model provided by Django, and the external Fitbit model represents the models found in <project folder>/fitapp/models.py from the Fitbit app. Due to how Django models work, this ER diagram is also a direct representation of the class model used (excluding functions, which can be found in the corresponding models.py files), and will be translated into QuerySet objects upon querying.
