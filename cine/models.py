from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def get_nickname(self):
        return self.name
    
    def set_nickname(self, name):
        self.name = name

    def get_email(self):
        return self.email
    
    def set_email(self, email):
        self.email = email

    def get_password(self):
        return self.name
    
    def set_password(self, name):
        self.name = name