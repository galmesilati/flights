from django.db import models
from rest_framework.authtoken.admin import User
from rest_framework.exceptions import ValidationError



# Create your models here.
# Flights:

class Flights(models.Model):
    class Meta:
        db_table = 'flights'
        ordering = ['id']

    # flight:

    flight_number = models.TextField(db_column='flight_number', null=False, blank=False)
    total_seats = models.IntegerField(db_column='total_seats', null=False, blank=False)
    seats_left = models.IntegerField(db_column='seats_left', null=False, blank=False)
    is_cancelled = models.BooleanField(db_column='is_cancelled', null=True,blank=True)
    price = models.FloatField(db_column='price', null=False, blank=False)
    # origin:

    origin_country = models.CharField(max_length=256, db_column='origin_country', null=False, blank=False)
    origin_city = models.CharField(max_length=256, db_column='origin_city', null=False, blank=False)
    origin_airport_code = models.IntegerField(db_column='origin_airport_code', null=False, blank=False)
    origin_date_time = models.DateTimeField(db_column='origin_date_time', null=True, blank=True)
    # destination:

    destination_country = models.CharField(max_length=256, db_column='destination_country', null=False, blank=False)
    destination_city = models.CharField(max_length=256, db_column='destination_city', null=False, blank=False)
    destination_airport_code = models.IntegerField(db_column='destination_airport_code', null=False, blank=False)
    destination_date_time = models.DateTimeField(db_column='destination_date_time', null=True, blank=True)

    def __str__(self):
        return f"Flight number: {self.flight_number}, from: {self.origin_country} to {self.destination_country}"


    # orders:

class Orders(models.Model):
    class Meta:
        db_table = 'orders'

    def seats_number_validate(self):
        seats_of_plan = Flights.objects.get(id=self.flight_id).seats_left
        if seats_of_plan < self.seats_number:
            raise ValidationError(f'There are not enough seats left on the plane, {seats_of_plan} seats are left')

    flight_id = models.ForeignKey(Flights, on_delete=models.RESTRICT, related_name='orders')
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='orders')
    seats_number = models.IntegerField(db_column='seats_number', null=False, blank=False, validators=[seats_number_validate])
    order_date = models.DateTimeField(db_column='order_date', null=False, blank=False)
    total_price = models.FloatField(db_column='total_price', null=False, blank=False)

    def __str__(self):
        return f"Your flight  has been successfully. date: {self.order_date}," \
               f" seats_number: {self.seats_number}, " \
               f"total price: {self.total_price}"










