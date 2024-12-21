from django.db import models

# Create your models here.

class Pokemon(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, default='')
    height = models.IntegerField()
    weight = models.IntegerField()
    is_default = models.BooleanField(default=True)
    sprite_url = models.URLField(default='')


    def set_types(self, types):
        # Set the 'type' attribute by joining the provided list of types
        self.type = ', '.join(types)

    def get_types(self):
        # Get a list of types by splitting the 'type' attribute
        return [t.strip() for t in self.type.split(',') if t.strip()]
    
    def height_in_meters(self):
        # Convert height from decimeters to meters
        return self.height / 10.0

    def weight_in_kilograms(self):
        # Convert weight from decigrams to kilograms
        return self.weight / 10.0
    
    def __str__(self):
        return self.name