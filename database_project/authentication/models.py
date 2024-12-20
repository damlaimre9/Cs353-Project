from django.db import models



class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    account_money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = "users"  # Point to the existing table
        managed = False  # Prevent Django from managing the table
