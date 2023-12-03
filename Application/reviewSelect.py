from restaurant import Restaurant
class reviewData:
    def __init__(self, review, score, count, date):
        self.score = score
        self.date = date
        self.review = review
        self.count = count
        
    def __str__(self):
        return f"Count:{self.count} {self.score} {self.review}"
    

def reviewPreprocess(restaurant : Restaurant):
    rev = restaurant.review
    reviewList = rev.split('|')
    positive = [4,5]
    negative = [1,2] 
    reviewListWithScore = []
    for review in reviewList:
        print(review)
        if(len(review.split('^')) < 3):
            continue
        scoreCount = 0
        scoreText = review.split('^')[0]
        score = scoreText.split(',')
        reviewScore = [0,0,0,0,0]
        if(scoreText == ''):
            break
        for scind in range(len(score)):

            if(int(score[scind]) == 0):
                continue
            elif(int(score[scind]) in positive):
                reviewScore[scind] = 3
            elif (int(score[scind]) in negative):
                reviewScore[scind] = 1
            else:
                reviewScore[scind] = 2

            scoreCount+=1
        #print(review.split('^')[2])
        timeText = review.split('^')[1]
        try:
            number = int(review.split('^')[1].split()[0])
        except:
            print(review)
            continue
        unit = review.split('^')[1].split(' ')[1]
        day = 0
        if("分鐘" in unit):
            day = 0
        elif("小時" in unit):
            day = 0
        elif("天" in unit):
            day = number
        elif("週" in unit):
            day = number*7
        elif("個月" in unit):
            day = number*30
        elif("年" in unit):
            day = number*365

        reviewListWithScore.append(reviewData(review.split('^')[2],reviewScore,scoreCount, day))
    return reviewListWithScore

def reviewClassify(reviewListWithScore):
    NEWDAY = 365
    reviewListCount3NEW = []
    reviewListCount2NEW = []
    reviewListCount3 = []
    reviewListCount2 = []
    reviewListCount1 = []

    for review in reviewListWithScore:
        if(review.count == 3):
            if(review.date <= NEWDAY):
                reviewListCount3NEW.append(review)
            else:
                reviewListCount3.append(review)
        elif(review.count == 2):
            if(review.date <= NEWDAY):
                reviewListCount2NEW.append(review)
            else:
                reviewListCount2.append(review)
        elif(review.count == 1):
            reviewListCount1.append(review)
    pendingList = [reviewListCount3NEW, reviewListCount2NEW, reviewListCount3, reviewListCount2, reviewListCount1]
    return pendingList

def reviewPick(pendingList):
    MAXNEED = 2
    reviewPick = []
    currentPositive = [0,0,0,0,0]
    currentNature = [0,0,0,0,0]
    currentNegative = [0,0,0,0,0]

    for List in pendingList:
        doneFlag = False
        #print(f"gellp{review}")
        for review in List:

            pickFlag = False
            tempPositive = currentPositive.copy()
            tempNature = currentNature.copy()
            tempNegative = currentNegative.copy()

            for scoreInd in range(len(review.score)):

                score = review.score[scoreInd]
                if(score == 3):
                    if(currentPositive[scoreInd] < MAXNEED):
                        pickFlag = True
                    tempPositive[scoreInd] += 1
                elif(score == 2):
                    tempNature[scoreInd] += 1
                elif(score == 1):
                    if(currentNegative[scoreInd] < MAXNEED):
                        pickFlag = True
                    tempNegative[scoreInd] += 1

            if(pickFlag):
                currentPositive = tempPositive.copy()
                currentNature = tempNature.copy()
                currentNegative = tempNegative.copy()
                reviewPick.append(f"{len(reviewPick)}. {review.review}")
                #print("picked")
                #print(f"{len(reviewPick)}. {review.review}")
                #print(currentPositive)
                #print(currentNegative)
            
            if (min(currentPositive) >= MAXNEED and min(currentNegative) >= MAXNEED):
                doneFlag = True
                break
        if(doneFlag):
            break
    return reviewPick
