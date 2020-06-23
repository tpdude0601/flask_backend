from utils.fuzzyLogic import *
import random


def getLevel(age, stay_duration):
    initRecommendation = fuzzyLogic()
    final_grade = initRecommendation.final_level_decision(age, stay_duration)
    return final_grade

def recommendInterest(final_grade):
    if final_grade == 'A':
        return 3
    elif final_grade == 'B':
        return random.choice([5, 6])
    elif final_grade == 'C':
        return random.choice([1, 2, 4])
    elif final_grade == 'D':
        return 7
    elif final_grade == 'F':
        # 역퍼지 오류 났을 때는, 그냥 랜덤으로 추천 띄우기
        return random.choice([1, 2, 3, 4, 5, 6, 7])
