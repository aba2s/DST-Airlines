from django.db import models


# Create your models here.
class Flights(models.Model):
    hex = models.CharField(max_length=80, null=True, blank=True,
                           help_text='CAO24 Hex address')
    reg_number = models.CharField(max_length=80, null=True, blank=True,
                                  help_text='Aircraft Registration Number')
    flag = models.CharField(max_length=80, null=True, blank=True,
                            help_text='ISO 2 country code from Countries DB.\
                                       Available in the Free plan.')
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    alt = models.IntegerField(null=True)
    dir = models.IntegerField(null=True)
    speed = models.IntegerField(null=True, blank=True)
    v_speed = models.FloatField(null=True)
    squaw = models.FloatField(null=True)
    flight_number = models.CharField(max_length=300, null=True, blank=True)
    flight_icao = models.CharField(max_length=300, null=True, blank=True)
    flight_iata = models.CharField(max_length=300, null=True, blank=True)
    dep_icao = models.CharField(max_length=300, null=True, blank=True)
    dep_iata = models.CharField(max_length=300, null=True, blank=True)
    arr_icao = models.CharField(max_length=300, null=True, blank=True)
    arr_iata = models.CharField(max_length=300, null=True, blank=True)
    airline_icao = models.CharField(max_length=300, null=True, blank=True)
    airline_iata = models.CharField(max_length=300, null=True, blank=True)
    aircraft_icao = models.CharField(max_length=300, null=True, blank=True)
    updated = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=300)

    class Meta:
        db_table = 'Flights'

    def __str__(self):
        return "flight: Departure {}  --> Arrival {}".format(
            self.dep_iata, self.arr_iata)
