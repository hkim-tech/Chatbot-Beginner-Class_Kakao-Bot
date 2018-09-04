# -*- coding: utf-8 -*- 

import json
from flask import Flask
from flask import request
from flask import jsonify
import requests
import operator

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/keyboard", methods=["GET"])
def keyboard():
    return jsonify(type="text")

@app.route("/message", methods=["GET", "POST"])
def message():
    data = json.loads(request.data)
    image_url = data["content"]

    subscription_key = '' # 각자 키 값을 넣으세요

    face_api_url = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0/detect'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'returnFaceId': 'true',
              'returnFaceLandmarks': 'false',
              'returnFaceAttributes': 'age,gender,emotion'}
    data = {'url': image_url}

    response = requests.post(face_api_url, params=params, headers=headers, json=data)
    faces = response.json()
    gender = faces[0]['faceAttributes']['gender']
    gender = gender.replace("female", "여자")
    gender = gender.replace("male", "남자")
    age = str(int(faces[0]['faceAttributes']['age']))

    emotion = faces[0]['faceAttributes']['emotion']



    emotion1 = sorted(emotion.items(), key=operator.itemgetter(1), reverse=True)[0][0]
    emotion1 = emotion1.replace("anger", "분노")
    emotion1 = emotion1.replace("contempt", "경멸")
    emotion1 = emotion1.replace("disgust", "역겨움")
    emotion1 = emotion1.replace("fear", "두려움")
    emotion1 = emotion1.replace("happiness", "행복")
    emotion1 = emotion1.replace("neutral", "중립")
    emotion1 = emotion1.replace("sadness", "슬픔")
    emotion1 = emotion1.replace("surprise", "놀람")
    emotion2 = sorted(emotion.items(), key=operator.itemgetter(1), reverse=True)[0][1]
    emotion3 = emotion1 + ' : ' + "{0:.0f}%".format(emotion2 * 100)

    response = {
        "message": {
            "text": gender + ', ' + age + '세' + ', ' + emotion3
        }
    }

    response = json.dumps(response, ensure_ascii=False)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # 윈도우 app.run(host="127.0.0.1", port=80)