from .models import ReleasedTrain, Coach, Berth, Train
import csv


def coachExtractor(releasedTrain, coachType):
    if(coachType == "SL"):
        ma = releasedTrain.currSL
        coach = Coach.objects.filter(releasedTrain = releasedTrain).filter(coachType = "SL").filter(coachNumber = (ma - 1) / 24 + 1)[0]
        releasedTrain.currSL = ma + 1
        releasedTrain.save()
        return coach
    else:
        ma = releasedTrain.currAC
        coach = Coach.objects.filter(releasedTrain = releasedTrain).filter(coachType = "AC").filter(coachNumber = (ma - 1) / 18 + 1)[0]
        releasedTrain.currAC = ma + 1
        releasedTrain.save()
        return coach


def berthExtractor(releasedTrain, CoachType):
    if(CoachType == "SL"):
        ma = releasedTrain.currSL
        berth = Berth.objects.filter(coachType = "SL").filter(berthNumber = (ma - 1) % 24 + 1)[0]
        return berth
    else:
        ma = releasedTrain.currAC
        berth = Berth.objects.filter(coachType = "AC").filter(berthNumber = (ma - 1) % 18 + 1)[0]
        return berth
    

def berthTableCreator():
    slType = ["LB", "MB", "UB", "LB", "MB", "UB", "SL", "SU"]
    acType = ["LB", "LB", "UB", "UB", "SL", "SU"]
    for i in range(1 , 25):
        berth = Berth(berthNumber = i, coachType = "SL", berthType = slType[(i - 1)%8])
        berth.save()
    for i in range(1 , 19):
        berth = Berth(berthNumber = i, coachType = "AC", berthType = acType[(i - 1)%6])
        berth.save()



def trainsCreator():
    with open('All_Indian_Trains.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            train = Train(trainNumber = row[1], name = row[2], starts = row[3], ends = row[4])
            train.save()