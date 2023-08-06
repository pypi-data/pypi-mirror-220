Erscipcard
=========
Django app that use vosk library to convert voice to text.

Quick start
-----------
1.Add "pvss" to your INSTALLED_APPS in your project setting.py file:
```
INSTALLED_APPS = [
...,
'pvss',
]
```

2.Include the pvss URLconf in your project urls.py like this:

```
path('pvss/', include('pvss.urls')),
```

3.Visit http://127.0.0.1:8000/pvss/ to voice to text.
