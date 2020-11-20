from django.db import models


class Train(models.Model):
    trainNumber = models.IntegerField(primary_key = True, help_text= "Train number should be of 4-5 characters and should be unique")
    starts = models.CharField(max_length = 20)
    ends = models.CharField(max_length = 20)
    name = models.CharField(max_length = 30)

    def __str__(self):
        return str(self.trainNumber)


class ReleasedTrain(models.Model):
    train = models.ForeignKey('Train', on_delete=models.CASCADE, related_query_name='released_trains', verbose_name = 'Train Number')
    departureDate = models.DateField()
    departureTime = models.TimeField()
    AcNumber = models.IntegerField()
    SlNumber = models.IntegerField()
    releasedDate = models.DateField()
    releasedTime = models.TimeField()

    def __str__(self):
        return "{} , {}".format(self.train, self.releasedDate)


