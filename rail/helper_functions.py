from .models import ReleasedTrain, Coach, Berth


def coachExtractor(releasedTrain, coachType):
    if(coachType == "SL"):
        ma = releasedTrain.currSL
        coach = Coach.objects.filter(releasedTrain = releasedTrain).filter(coachType = "SL").filter(coachNumber = (ma - 1) / 24 + 1)
        releasedTrain.currSL = ma + 1
        releasedTrain.save()
        return coach
    else:
        ma = releasedTrain.currAC
        coach = Coach.objects.filter(releasedTrain = releasedTrain).filter(coachType = "AC").filter(coachNumber = (ma - 1) / 18 + 1)
        releasedTrain.currAC = ma + 1
        releasedTrain.save()
        return coach


def berthExtractor(releasedTrain, CoachType):
    if(CoachType == "SL"):
        ma = releasedTrain.currSL
        berth = Berth.objects.filter(CoachType = "SL").filter(berthNumber = (ma - 1) % 24 + 1)[0]
        return berth
    else:
        ma = releasedTrain.currAC
        berth = Berth.objects.filter(CoachType = "AC").filter(berthNumber = (ma - 1) % 18 + 1)[0]
        return berth
    
