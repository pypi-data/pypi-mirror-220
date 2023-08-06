Evtt
=========
Django app that use vosk library to convert voice to text.

Quick start
-----------
1.Add "evtt" to your INSTALLED_APPS in your project setting.py file:
```
INSTALLED_APPS = [
...,
'evtt',
]
```

2.Include the evtt URLconf in your project urls.py like this:

```
path('evtt/', include('evtt.urls')),
```

3.Visit http://127.0.0.1:8000/evtt/ to voice to text.
