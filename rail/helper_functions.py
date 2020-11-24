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
    

def berthTableCreator():
    slType = ["LB", "MB", "UB", "LB", "MB", "UB", "SL", "SU"]
    acType = ["LB", "LB", "UB", "UB", "SL", "SU"]
    for i in range(1 , 25):
        berth = Berth(berthNumber = i, coachType = "SL", berthType = slType[(i - 1)%8])
        berth.save()
    for i in range(1 , 18):
        berth = Berth(berthNumber = i, coachType = "AC", berthType = acType[(i - 1)%6])
        berth.save()

