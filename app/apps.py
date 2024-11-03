from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

def ready(self):
    import app.signals  

# apps.py
# from django.apps import AppConfig

# class YourAppConfig(AppConfig):
#     name = 'your_app'

#     def ready(self):
#         import your_app.signals  # Import the signals
