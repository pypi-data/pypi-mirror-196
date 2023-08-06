=================
Django Chat App
=================

if you need to a chat application in your django project, you can use from this package.
this package powered by channels and vuejs technologies.

Prerequisites: your project must use asgi engine. you can use from channels package.


Quick start
-----------
1. Add "chatapp" to your INSTALLED_APPS in settings.py

2. Include the chatapp URLconf in your project urls.py like this:

from chatapp.views import supporter_homepage

path('django-chat-app/chat/supporter/', supporter_homepage),
path('', include('chatapp.urls')),

3. Run `python manage.py migrate` to create the chatapp models.

4. at now, you can include chatapp section to your templates:
{% load chatapp %}
{% include_chatapp %}
