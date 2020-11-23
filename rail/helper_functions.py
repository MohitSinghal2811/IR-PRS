from .models import ReleasedTrain, Coach, Berth


def coachExtractor(trainNumber, coachType):
    train = ReleasedTrain.objects.filter(trainNumber = trainNumber)[0]
    if(coachType == "SL"):
        ma = train.currSL
        coach = Coach.objects.filter(train = train).filter(coachType = "SL").filter(coachNumber = (ma - 1) / 24 + 1)
        train.currSL = ma + 1
        return coach
    else:
        ma = train.currAC
        coach = Coach.objects.filter(train = train).filter(coachType = "AC").filter(coachNumber = (ma - 1) / 18 + 1)
        train.currAC = ma + 1
        return coach


def berthExtractor(trainNumber, CoachType):
    train = ReleasedTrain.objects.filter(trainNumber = trainNumber)[0]
    if(CoachType == "SL"):
        ma = train.currSL
        berth = Berth.objects.filter(CoachType = "SL").filter(berthNumber = (ma - 1) % 24 + 1)[0]
        return berth
    else:
        ma = train.currAC
        berth = Berth.objects.filter(CoachType = "AC").filter(berthNumber = (ma - 1) % 18 + 1)[0]
        return berth
    
