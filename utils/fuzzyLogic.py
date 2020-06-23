import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class fuzzyLogic:

    def __init__(self):
        # 독립변수(X1, X2): 연령, 한국 체류 기간
        self.age = ctrl.Antecedent(np.arange(0, 70, 0.5), 'age')  # 연령
        self.duration = ctrl.Antecedent(np.arange(0, 27, 0.5), 'duration')  # 체류 기간
        # 종속변수(Y): 한국어 회화 수준
        self.level = ctrl.Consequent(np.arange(0, 18, 0.5), 'level')  # 수준

        self.final_grade = "undefined"

        # 그래프 그리기
        self.age['child'] = fuzz.trimf(self.age.universe, [0, 10, 20])
        self.age['youth'] = fuzz.trimf(self.age.universe, [18, 29, 40])
        self.age['middle-age'] = fuzz.trimf(self.age.universe, [30, 40, 50])
        self.age['elderly'] = fuzz.trimf(self.age.universe, [45, 52, 60])

        self.duration['zero'] = fuzz.trimf(self.duration.universe, [0, 3, 6])
        self.duration['short'] = fuzz.trimf(self.duration.universe, [4.5, 9, 13.5])
        self.duration['medium'] = fuzz.trimf(self.duration.universe, [12, 16.5, 21.5])
        self.duration['long'] = fuzz.trimf(self.duration.universe, [17, 20.5, 24])

        self.level['A'] = fuzz.trimf(self.level.universe, [0, 2, 4])
        self.level['B'] = fuzz.trimf(self.level.universe, [3, 6, 9])
        self.level['C'] = fuzz.trimf(self.level.universe, [8, 11, 14])
        self.level['D'] = fuzz.trimf(self.level.universe, [12, 16, 16])

        # 퍼지 규칙 만들기
        rule10 = ctrl.Rule(self.age['child'] & self.duration['zero'], self.level['A'])
        rule11 = ctrl.Rule(self.age['child'] & self.duration['short'], self.level['A'])
        rule12 = ctrl.Rule(self.age['child'] & self.duration['medium'], self.level['B'])
        rule13 = ctrl.Rule(self.age['child'] & self.duration['long'], self.level['C'])

        rule20 = ctrl.Rule(self.age['youth'] & self.duration['zero'], self.level['A'])
        rule21 = ctrl.Rule(self.age['youth'] & self.duration['short'], self.level['B'])
        rule22 = ctrl.Rule(self.age['youth'] & self.duration['medium'], self.level['B'])
        rule23 = ctrl.Rule(self.age['youth'] & self.duration['long'], self.level['C'])

        rule30 = ctrl.Rule(self.age['middle-age'] & self.duration['zero'], self.level['B'])
        rule31 = ctrl.Rule(self.age['middle-age'] & self.duration['short'], self.level['C'])
        rule32 = ctrl.Rule(self.age['middle-age'] & self.duration['medium'], self.level['C'])
        rule33 = ctrl.Rule(self.age['middle-age'] & self.duration['long'], self.level['D'])

        rule40 = ctrl.Rule(self.age['elderly'] & self.duration['zero'], self.level['B'])
        rule41 = ctrl.Rule(self.age['elderly'] & self.duration['short'], self.level['C'])
        rule42 = ctrl.Rule(self.age['elderly'] & self.duration['medium'], self.level['D'])
        rule43 = ctrl.Rule(self.age['elderly'] & self.duration['long'], self.level['D'])

        # 퍼지 규칙 모두 입력하기
        level_ctrl = ctrl.ControlSystem([rule10, rule11, rule12, rule13,
                                         rule20, rule21, rule22, rule23,
                                         rule30, rule31, rule32, rule33,
                                         rule40, rule41, rule42, rule43])

        self.level_grading = ctrl.ControlSystemSimulation(level_ctrl)

    # membership function으로 가장 큰 값의 등급으로 출력
    def final_level_decision(self, age, duration):

        # 입력받은 연령대, 체류 기간
        self.level_grading.input['age'] = age
        self.level_grading.input['duration'] = duration

        try:
            self.level_grading.compute()
        except:
            #역퍼지 에러 발생했을 때
            print('error')
            self.final_grade = 'F'
            return self.final_grade

        max_val = 0
        for grades in self.level.terms:
            mval = np.interp(self.level_grading.output['level'], self.level.universe, self.level[grades].mf)
            if mval >= max_val:
                max_val = mval
                # print("max값:",max_val)
                self.final_grade = grades
            # print(grades, mval)
        #print("Your Korean Speaking Level is", self.final_grade)

        return self.final_grade
