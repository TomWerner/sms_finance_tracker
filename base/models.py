""" Basic models, such as user profile """
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AccountHolder(models.Model):
	user = models.ForeignKey(User, unique=True)
	phone_number = models.CharField(max_length=11)
	
	def __unicode__(self):
		return self.phone_number
	
class MoneyAccount(models.Model):
	user = models.ForeignKey(AccountHolder)
	account_name = models.CharField(max_length=200)
	account_tag = models.CharField(max_length=10)
	account_description = models.CharField(max_length=1000)
	balance = models.DecimalField(max_digits=100,decimal_places=2)
	
	def __unicode__(self):
		return unicode(self.account_name) + " : $" + unicode(self.balance)
	
class AccountEntry(models.Model):
	account = models.ForeignKey(MoneyAccount)
	date = models.DateTimeField()
	amount = models.DecimalField(max_digits=50,decimal_places=2)
	tag = models.CharField(max_length=50)
	comment = models.CharField(max_length=300)
	balance = models.DecimalField(max_digits=100,decimal_places=2)
	
	def __unicode__(self):
		return unicode(self.account) + ": " + unicode(self.amount) + " ( " + unicode(self.comment) + ")"
		