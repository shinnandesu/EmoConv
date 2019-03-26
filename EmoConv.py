# 'dog-bark':0,
# 'drill':1,
# 'hazard-alarm':2,
# 'phone-ring':3,
# 'speech':4,
# 'vacuum':5,
# 'baby-cry':6,
# 'chopping':7,
# 'cough':8,
# 'door':9,
# 'water-running':10,
# 'knock':11,
# 'microwave':12,
# 'shaver':13,
# 'toothbrush':14,
# 'blender':15,
# 'dishwasher':16,
# 'doorbell':17,
# 'flush':18,
# 'hair-dryer':19,
# 'laugh':20,
# 'snore':21,
# 'typing':22,
# 'hammer':23,
# 'car-horn':24,
# 'engine':25,
# 'saw':26,
# 'cat-meow':27,
# 'alarm-clock':28,
# 'cooking':29,


#0 dummy = ['snore', 'saw']
#1 bathroom = ['water-running','flush','toothbrush','shaver','hair-dryer']
#2 kitchen = ['water-running','chopping','cooking','microwave','blender','hazard-alarm','dishwasher','speech']
#3 bedroom = ['alarm-clock','snore','cough','baby-cry','speech']
#4 office = ['knock','typing','phone-ring','door','cough','speech']
#5 entrance = ['knock','door','doorbell','speech','laugh']
#6 workshop = ['hammer','saw','drill','vacuum','hazard-alarm','speech']
#7 outdoor = ['dog-bark','cat-meow','engine','car-horn','speech','hazard-alarm']

everything = {
0:[7],
1:[6],
2:[2,6,7],
3:[4],
4:[2,3,4,5,6,7],
5:[6],
6:[3],
7:[2],
8:[3,4],
9:[4,5],
10:[1,2],
11:[4,5],
12:[2],
13:[1],
14:[1],
15:[2],
16:[2],
17:[5],
18:[1],
19:[1],
20:[5],
21:[0,3],
22:[4],
23:[6],
24:[7],
25:[7],
26:[0,6],
27:[7],
28:[3],
29:[2]
}


home_expressions = {
    0:"",
    1:"GoodNews",
    2:"Supportive",
    3:"Supportive",
    4:""
}

public_expressions = {
    0:"",
    1:"GoodNews",
    2:"",
    3:"",
    4:""
}


alone_expressions = {
    0:"",
    1:"GoodNews",
    2:"Supportive",
    3:"Supportive",
    4:""
}


group_expressions = {
    0:"",
    1:"GoodNews",
    2:"",
    3:"",
    4:""
}


expressions = {
    0:"",
    1:"Supportive",
    2:"GoodNews",
    3:"Apology",
    4:"Angry"
}


detect_emotion_mapping = {
    0:'Neutral', 
    1:'Happy', 
    2:'Upset', 
    3:'Angry',
    4:'Others'
}
reply_emotion_mapping={
    "":"Neutral",
    "GoodNews":"Happy",
    "Supportive":"Supportive",
    "Angry":"Angry",
    "Apology":"Sad" 
}

context_mapping = {
    0: home_expressions, #dummy
    1: home_expressions, #bathroom 
    2: home_expressions, #kitchen
    3: home_expressions, #bedroom
    4: public_expressions, #office
    5: home_expressions, #entrance
    6: public_expressions, #workshop
    7: public_expressions #outdoor
}
scenario_context_mapping = {
    0: home_expressions, #home
    1: public_expressions, #public
    2: alone_expressions, #alone
    3: group_expressions, #group
}
detect_context_mapping= {
    0:'dummy',
    1:'bathroom', 
    2:'kitchen', 
    3:'bedroom', 
    4:'office', 
    5:'office', 
    6:'workshop', 
    7:'outdoor'
}

scenario_context_mapping_word  = {
    0:"Home",
    1:"Public",
    2:"Alone",
    3:"Group"
}

import numpy as np
import random
import time
import csv

class Converter:
    def __init__(self,context,emotion):
        self.count_context = np.array([0]*8)
        self.scenario_context = context
        self.scenario_emotion = emotion
            
    def convertEmotion(self,real_emotion,context,pattern,reply):
        for i in context:
            for n in (everything[i]):
                self.count_context[n]+=1
        real_context = self.count_context.argmax()
        target_expression = scenario_context_mapping[self.scenario_context]
        print("Emotion Prediction: "+detect_emotion_mapping[real_emotion])
        print("Context Prediction: "+detect_context_mapping[real_context])
        print("="*40)
        print("Emotion Scenario: "+detect_emotion_mapping[self.scenario_emotion])
        print("Context Scenario: "+scenario_context_mapping_word[self.scenario_context])
        print("="*40)
        target_emotion = ""
        if(pattern== 0):
            target_emotion = ""
        elif(pattern== 1):
            target_emotion = expressions[random.randint(0,4)]
        elif(pattern== 2):
            target_emotion = target_expression[self.scenario_emotion]
        elif(pattern== 3):
            target_emotion = expressions[int(reply)]

        data = [time.time(),pattern,detect_context_mapping[real_context],scenario_context_mapping_word[self.scenario_context],detect_emotion_mapping[real_emotion],detect_emotion_mapping[self.scenario_emotion],reply_emotion_mapping[target_emotion]]
        with open('result.csv','a') as f:
            writer = csv.writer(f, lineterminator='\n') # 行末は改行
            writer.writerow(data)

        # target_emotion = "Neutral" if target_emotion == "" else target_emotion
        print("Reply Emotion is '{}'".format(reply_emotion_mapping[target_emotion]))

        return target_emotion