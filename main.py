import os
import csv
import copy
import speech_recognition as sr
import time
import pyaudio
import pyttsx3
from imageai.Detection import ObjectDetection

# Object Detection --------------------------------------
execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
custom = detector.CustomObjects(backpack=True, umbrella=True, handbag=True, tie=True, suitcase=True, frisbee=True,
                                skis=True, snowboard=True, sports_ball=True, kite=True, baseball_bat=True,
                                baseball_glove=True, skateboard=True, surfboard=True, tennis_racket=True,
                                bottle=True, wine_glass=True, cup=True, fork=True, knife=True, spoon=True,
                                bowl=True, banana=True, apple=True, sandwich=True, orange=True, broccoli=True,
                                carrot=True, hot_dog=True, pizza=True, donut=True, cake=True, chair=True,
                                couch=True, potted_plant=True, bed=True, dining_table=True, toilet=True,
                                tv=True, laptop=True, mouse=True, remote=True, keyboard=True, cell_phone=True,
                                microwave=True, oven=True, toaster=True, sink=True, refrigerator=True, book=True,
                                clock=True, scissors=True, teddy_bear=True, hair_dryer=True, toothbrush=True)
image = "image2"
input_image = "Images/" + image + ".jpg"
output_image = "Images/" + image + "_detected.jpg"
detections = detector.detectCustomObjectsFromImage(custom_objects=custom, input_image=input_image,
                                                   output_image_path=output_image,
                                                   minimum_percentage_probability=35)


# End: Object Detection     ~   ~

# Speech Recognition ------------------------------------
# Source: https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py
#
# r = sr.Recognizer()
# m = sr.Microphone()
#
#
# def say(text):
#     return subprocess.call("espeak -s 155 -a 200 '" + text + "'", shell=True)
#
#
# try:
#     print("A moment of silence, please...")
#     with m as source:
#         # r.adjust_for_ambient_noise(source)
#         r.adjust_for_ambient_noise(source, duration=5)
#         print("Set minimum energy threshold to {}".format(r.energy_threshold))
#         while True:
#             print("Say something!")
#             audio = r.listen(source)
#             print("Got it! Now to recognize it...")
#             try:
#                 # recognize speech using Google Speech Recognition
#                 value = r.recognize_google(audio)
#
#                 # we need some special handling here to correctly print unicode characters to standard output
#                 if str is bytes:  # this version of Python uses bytes for strings (Python 2)
#                     say(u"You said {}".format(value).encode("utf-8"))
#                 else:  # this version of Python uses unicode for strings (Python 3+)
#                     say("You said {}".format(value))
#             except sr.UnknownValueError:
#                 print("Oops! Didn't catch that")
#             except sr.RequestError as e:
#                 print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
# except KeyboardInterrupt:
#     pass

# End: Speech Recognition   ~   ~

# Speech Processing ------------------------------------------------

def in_items(item, list):
    for i in list:
        if i['name'] == item:
            return True
    return False


def occurs_once(list, item):
    count = 0
    for i in list:
        if i['name'] == item:
            count += 1
    return count == 1


def is_plural(name):
    plural = False
    if name[-1] == 's':
        if not name[-2:] == 'ss':
            plural = True
    return plural


def naming_convention(name):
    if not (name[-1] == 's'):
        name += 's'
    if name[-2:] == 'ch':
        name += 'es'
    return name


def speech_processing(message):
    words = message.split()
    print(words)
    count = 0
    while count < len(words) - 1:
        if in_items(words[count], detections):
            break
        if in_items(words[count] + " " + words[count + 1], detections):
            words[count] = words[count] + " " + words.pop(count + 1)
            break
        count += 1

    if words[0] == "where":
        if in_items(words[3], detections):
            return look_for(words[3])
        else:
            return "the item you asked for cannot be found."
    elif words[0] == "list":
        if words[1] + " " + words[2] == "all items":
            return list_items()

    if words[0] == "what":
        if words[2] + " " + words[3] == "next to":
            return inv_horizontal_neighbours(words[5])
        if words[2] + " " + words[3] + " " + words[4] == "on top of":
            return inv_neighbours(words[6], "on top of")
        if words[2] + " " + words[3] + " " + words[4] == "in front of":
            return inv_neighbours(words[6], "in front of")
        if words[2] == "behind":
            return inv_neighbours(words[4], "behind")
        if words[2] == "the":
            if in_items(words[3], detections):
                if words[4] + " " + words[5] == "next to":
                    return horizontal_neighbours(words[3])
                if words[4] + " " + words[5] + " " + words[6] == "on top of":
                    return neighbours(words[3], "on top of")
                if words[4] + " " + words[5] + " " + words[6] == "in front of":
                    return neighbours(words[3], "in front of")
                if words[4] == "behind":
                    return neighbours(words[3], "behind")

    return "Sorry, I couldn't understand the question..."


# End: Speech Processing    ~   ~

# Object Detection ----------------------------------------------
sort_d = []

for eachObject in detections:
    x1, y1, x2, y2 = eachObject['box_points']
    area = (x2 - x1) * (y2 - y1)
    sort_d.append({'name': eachObject['name'], 'box_points': eachObject['box_points'], 'area': area})

    # print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
sort_d = sorted(sort_d, key=lambda k: k['area'])
# print(detections)
# print(sort_d)

# prepro = copy.deepcopy(sort_d)
# print(prepro)

prepro = []

# maxx1 = 10000
# maxy1 = 10000
# maxx2 = 0
# maxy2 = 0
once = True

while sort_d:
    item1 = sort_d.pop()
    name1 = item1['name']
    same = False
    x11, y11, x12, y12 = item1['box_points']
    temp = copy.deepcopy(sort_d)
    while temp:
        item2 = temp.pop()
        name2 = item2['name']
        # if they have the same name
        if name1 == name2:
            same = True
            x21, y21, x22, y22 = item2['box_points']
            y1half = int((y12 - y11) / 2)  # Halfway point of y in item1
            if once:
                maxx1 = x11
                maxy1 = y11
                maxx2 = x12
                maxy2 = y12
                once = False
            # print('x11, y11, x12, y12:', x11, y11, x12, y12)
            # print('max:', maxx1, maxy1, maxx2, maxy2)
            # if the ys of the second item is within the extended y of the first
            if ((y11 - y1half) < y22) or (y21 < (y12 + y1half)):
                # and the xs of the second item is within the x of the first
                if (x11 < x22) or (x21 < x12):
                    # Set the boundaries of the group
                    if x21 < maxx1:
                        maxx1 = x21
                    if y21 < maxy1:
                        maxy1 = y21
                    if x22 > maxx2:
                        maxx2 = x22
                    if y22 > maxy2:
                        maxy2 = y22
                    if occurs_once(sort_d, name1):
                        name1 = naming_convention(name1)
                        area = (maxx2 - maxx1) * (maxy2 - maxy1)
                        prepro.append({'name': name1, 'box_points': [maxx1, maxy1, maxx2, maxy2], 'area': area})
                        # print({'name': name1, 'box_points': [maxx1, maxy1, maxx2, maxy2], 'area': area})

    if (not in_items(name1, prepro)) & (not in_items(name1 + 's', prepro)):
        if occurs_once(detections, name1):
            area = (x12 - x11) * (y12 - y11)
            prepro.append({'name': name1, 'box_points': [x11, y11, x12, y12], 'area': area})
            # print({'name': name1, 'box_points': [x11, y11, x12, y12], 'area': area})

prepro = sorted(prepro, key=lambda k: k['area'])
# print(prepro)
detections = copy.deepcopy(prepro)
detections = sorted(detections, key=lambda k: k['area'], reverse=True)

with open('preset.csv', mode='r') as f:
    reader = csv.reader(f)
    ontology = {(rows[0], rows[1]): (rows[2], rows[3]) for rows in reader}
    # print(ontology)


def check_ontology(item1, item2):
    # print('Check ontology for: ', item1, ',', item2)
    position = None
    weight = 0
    if (item1, item2) in ontology:
        # print('found')
        position, weight = ontology[item1, item2]

    # print('Position:', pos, ' Weight:', wei)
    return position, float(weight)


def vertical_check(y11, y12, y21, y22):
    # Connection = weak : 0.25 most likely not on top
    # Connection = average : 0.5 on top, only if ontology supports it
    # Connection = strong : 0.75 definitely on top, unless ontology doesn't support it
    strength = 0.5
    yhalf = int(y11 + ((y12 - y11) / 2))  # Halfway point of y in item1
    # print('y11: ', y11, 'y12: ', y12, 'y21: ', y21, 'y22: ', y22)
    # Case 1
    if y22 <= y11:
        strength = 0.25
    # Case 2
    if (y21 <= y11) & (y11 <= y22 & y22 <= yhalf):
        strength = 0.5
    # Case 3
    if (y11 <= y21 & y21 <= yhalf) & (y11 <= y22 & y22 <= yhalf):
        strength = 0.75
    # Case 4
    if (yhalf <= y21 & y21 <= y12) & (yhalf <= y22 & y22 <= y12):
        strength = 0.5
    # Case 5
    if (yhalf <= y21) & (y21 <= y12 & y12 <= y22):
        strength = 0.25
    # Case 6
    if y12 <= y21:
        strength = 0.25
    # print('Vertical connection: ', connection)
    return strength


def horizontal_check(x11, x12, x21, x22):
    # Relation = left : to the left
    # Relation = in front : in front
    # Relation = right : to the right
    rel = ''
    xhalf = int(x11 + ((x12 - x11) / 2))  # Halfway point of x in item1
    xql = int(x11 + ((x12 - x11) * 0.25))  # Left Quarter of x in item1
    xqr = int(x11 + ((x12 - x11) * 0.75))  # Right Quarter of x in item1
    if x22 <= x11:
        rel = 'to the left'
    if (x21 <= x11) & (x11 <= x22 & x22 <= xql):
        rel = 'to the left'
    if (xql <= x21 & x21 <= xqr) or (xql <= x22 & x22 <= xqr):
        rel = 'in front'
    if (xqr <= x21 & x21 <= x12) & (x12 <= x22):
        rel = 'to the right'
    if x12 <= x21:
        rel = 'to the right'

    # print('Relation:', relation)
    return rel


connections = []

while prepro:
    item1 = prepro.pop()
    # print('1', item1)
    x11, y11, x12, y12 = item1['box_points']
    # print('1:', item1)
    temp = copy.deepcopy(prepro)
    # print('---------------------------------------------')
    while temp:
        item2 = temp.pop()
        # print('2', item2)
        name1 = item1['name']
        name2 = item2['name']
        x21, y21, x22, y22 = item2['box_points']
        x1half = int((x12 - x11) / 2)  # Halfway point of x in item1
        y1half = int((y12 - y11) / 2)  # Halfway point of y in item1
        xel = x11 - x1half
        strength = 0
        wei = 0
        pos = None
        relation = None
        # print('1:', item1['name'], '2:', item2['name'])
        # if (((y11 - y1half) < y22) & (y22 < y1half)) or ((y1half < y21) & (y21 < (y12 + y1half))):
        # print('x11: ', x11, 'x21: ', x21, 'x22: ', x22, 'x12: ', x12)
        # Make sure item2 is within the border of item1 (x coordinates)
        if ((y11 - y1half) < y22) & (y22 < y1half):
            if (x11 < x21) & (x22 < x12):
                # print('Checking vertical for ', name1, ' and ', name2)
                connection = vertical_check(y11, y12, y21, y22)
                pos, wei = check_ontology(name1, name2)
                strength = connection + wei
                # print('Strength:', strength)

        if (((x11 - x1half) < x22) & (x22 < x1half)) or ((x1half < x21) & (x21 < (x12 + x1half))):
            if ((y11 < y22) & (y22 < y1half)) or ((y1half < y21) & (y21 < y12)):
                # print('Checking horizontal for ', name1, ' and ', name2)
                relation = horizontal_check(x11, x12, x21, x22)

        if strength >= 1:
            # print('The', name2, 'is', pos, 'of the', name1)
            connections.append({'1': name1, '2': name2, 'Strength': strength, 'Relation': 'underneath'})
            connections.append({'1': name2, '2': name1, 'Strength': strength, 'Relation': 'on top of'})
            # G.add_edge(name1, name2, weight=strength, relation='bellow')
            # G.add_edge(name2, name1, weight=strength, relation='on top')
        else:
            if relation == 'to the left':
                # print('The', name2, 'is', relation, 'of the', name1)
                connections.append({'1': name1, '2': name2, 'Strength': 0.75, 'Relation': 'to the right of'})
                connections.append({'1': name2, '2': name1, 'Strength': 0.75, 'Relation': 'to the left of'})
                # G.add_edge(name1, name2, weight=0.75, relation='to the right')
                # G.add_edge(name2, name1, weight=0.75, relation='to the left')
            if relation == 'to the right':
                connections.append({'1': name1, '2': name2, 'Strength': 0.75, 'Relation': 'to the left of'})
                connections.append({'1': name2, '2': name1, 'Strength': 0.75, 'Relation': 'to the right of'})
                # G.add_edge(name1, name2, weight=0.75, relation='to the left')
                # G.add_edge(name2, name1, weight=0.75, relation='to the right')
            if relation == 'in front':
                connections.append({'1': name1, '2': name2, 'Strength': 0.75, 'Relation': 'in front of'})
                connections.append({'1': name2, '2': name1, 'Strength': 0.75, 'Relation': 'behind'})
                # G.add_edge(name1, name2, weight=0.75, relation='behind')
                # G.add_edge(name2, name1, weight=0.75, relation='in front')


def ending(message):
    if len(message) > 1:
        counter = len(message) - 1
        temp_m = message[counter][:-1]
        message[counter] = 'and ' + temp_m + "."

    message = ' '.join(message)

    return message


def list_items():
    message = []
    vowels = ['a', 'e', 'o', 'i', 'u']
    for i in detections:
        if i['name'][0] in vowels:
            message.append('there is an ' + i['name'] + ',')
        elif is_plural(i['name']):
            message.append('there are ' + i['name'] + ',')
        else:
            message.append('there is a ' + i['name'] + ',')

    message = ending(message)

    return message


def format_relations(item, items):
    if is_plural(item):
        message = ['The ' + item + ' are']
    else:
        message = ['The ' + item + ' is']

    for each in items:
        message.append(each['Relation'] + ' the ' + each['2'] + ',')

    message = ending(message)

    return message


def inv_format_relations(item, items):
    message = []
    for each in items:
        if is_plural(each['1']):
            message.append('the ' + each['1'] + ' are ' + each['Relation'] + ' the ' + each['2'] + ',')
        else:
            message.append('the ' + each['1'] + ' is ' + each['Relation'] + ' the ' + each['2'] + ',')

    message = ending(message)

    return message


def look_for(item):
    temp_list = []
    print('Looking for:', item)
    for i in connections:
        # print(i['1'], '==', item)
        if i['1'] == item:
            temp_list.append(i)
    # print(temp_list)
    if not temp_list:
        return 'The item cannot be found.'

    items = sorted(temp_list, key=lambda k: k['Strength'], reverse=True)

    return format_relations(item, items)


def neighbours(item, rel):
    temp_list = []
    for i in connections:
        # print(i['1'], '==', item)
        if i['1'] == item:
            if i['Relation'] == rel:
                temp_list.append(i)
    # print(temp_list)
    if not temp_list:
        return 'No item is ' + rel + ' the ' + item

    return format_relations(item, temp_list)


def inv_neighbours(item, rel):
    temp_list = []
    for i in connections:
        if i['2'] == item:
            if i['Relation'] == rel:
                temp_list.append(i)
    if not temp_list:
        return 'No item is ' + rel + ' the ' + item

    return inv_format_relations(item, temp_list)


def horizontal_neighbours(item):
    temp_list = []
    for i in connections:
        if i['1'] == item:
            # if i['Relation'] == 'to the right of' or i['Relation'] == 'to the left of':
            temp_list.append(i)
    if not temp_list:
        return 'No item is next to the ' + item

    return format_relations(item, temp_list)


def inv_horizontal_neighbours(item):
    temp_list = []
    for i in connections:
        if i['2'] == item:
            # if i['Relation'] == 'to the right of' or i['Relation'] == 'to the left of':
            temp_list.append(i)
    if not temp_list:
        return 'No item is next to the ' + item

    return inv_format_relations(item, temp_list)


engine = pyttsx3.init()
engine.setProperty('rate', 180)  # setting up new voice rate

# print(look_for('laptop'))
exit_messages = ["stop", "that's all for now", "ok thanks", "exit"]

while True:
    query = input("Ask a question:\n")
    query = query.lower()
    if query in exit_messages:
        break
    answer = speech_processing(query)
    print(answer)
    engine.say(answer)
    engine.runAndWait()
engine.stop()
