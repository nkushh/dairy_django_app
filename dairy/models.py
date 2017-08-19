from django.db import models
from datetime import date

# Create your models here.
class Cow(models.Model):
	name = models.CharField(max_length=20)
	tag_no = models.CharField(max_length=10)
	breed = models.CharField(max_length = 30)
	date_added = models.DateField(default = date.today)

	def __str__(self):
		return self.name


class Milk(models.Model):
	cow = models.ForeignKey(Cow)
	session = models.CharField(max_length=20)
	amount = models.FloatField()
	milking_date = models.DateField(default = date.today)

	def __str__(self):
		return '{}'.format(self.amount)

class MilkSale(models.Model):
	milk = models.FloatField()
	amount = models.FloatField()
	date_sold = models.DateField()

	def __str__(self):
		return "{}".format(self.milk)
