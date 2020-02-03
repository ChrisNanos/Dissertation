import os
from imageai.Detection import ObjectDetection

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
                                clock=True, vase=True, scissors=True, teddy_bear=True, hair_dryer=True, toothbrush=True)

detections = detector.detectCustomObjectsFromImage(custom_objects=custom, input_image="Images/image5.jpg",
                                             output_image_path="Images/image5_detected.jpg",
                                             minimum_percentage_probability=35)

sort_d = []

for eachObject in detections:
    x1, y1, x2, y2 = eachObject['box_points']
    area = (x2 - x1) * (y2 - y1)
    sort_d.append({'name': eachObject['name'], 'box_points': eachObject['box_points'], 'area': area})


    # print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
sort_d = sorted(sort_d, key=lambda k: k['area'])
print(detections)
print(sort_d)

while sort_d:
    item = sort_d.pop()
    x11, y11, x21, y21 = item['box_points']
    print(x11, y11, x21, y21)
    for each in sort_d:
        # Check ontology:

