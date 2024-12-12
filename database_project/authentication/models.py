from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    account_money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # If user_type is needed (based on register form), uncomment:
    # user_type = models.IntegerField(default=1) 

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username