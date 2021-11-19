import os
import tensorflow as tf
from keras.models import load_model
import numpy as np
from datetime import datetime
from flask import Blueprint, request, render_template, jsonify
from modules.dataBase import collection as db
import cv2

mod = Blueprint('backend', __name__, template_folder='templates', static_folder='./static')
UPLOAD_URL = 'http://0.0.0.0:8400/static/'
model = load_model("modules/model/mobilenet_model.hdf5")
class_names = ['Dark', 'Green', 'Light', 'Medium']
model.make_predict_function()


@mod.route('/')
def home():
    return render_template('index.html')


@mod.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "someting went wrong 1"

        user_file = request.files['file']
        if user_file.filename == '':
            return "file name not found ..."

        else:
            path = os.path.join(os.getcwd() + '\\modules\\static\\' + user_file.filename)
            user_file.save(path)

            image = cv2.resize(cv2.imread(path), (224, 224))
            # Use gaussian blur
            blurImg = cv2.GaussianBlur(image, (5, 5), 0)

            # Convert to HSV image
            hsvImg = cv2.cvtColor(blurImg, cv2.COLOR_BGR2HSV)

            # Create mask (parameters - green color range)
            lower_green = (25, 40, 50)
            upper_green = (75, 255, 255)
            mask = cv2.inRange(hsvImg, lower_green, upper_green)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # Create bool mask
            bMask = mask > 0

            # Apply the mask
            clear = np.zeros_like(image, np.uint8)  # Create empty image
            clear[bMask] = image[bMask]  # Apply boolean mask to the origin image
            clearTestImg = clear / 255
            clearTestImg = tf.expand_dims(clearTestImg, 0)
            predictions = model.predict(clearTestImg)
            score = tf.nn.softmax(predictions)

            class_name = class_names[np.argmax(score)]
            score = np.max(score) * 100

            db.addNewImage(
                user_file.filename,
                class_name,
                str(round(score, 2)),
                datetime.now(),
                UPLOAD_URL + user_file.filename)

            return jsonify({
                "status": "success",
                "class": class_name,
                "score": str(round(score, 2)),
                "upload_time": datetime.now()
            })

# def identifyImage(img_path):
#     image = img.load_img(img_path, target_size=(224, 224))
#     x = img_to_array(image)
#     x = np.expand_dims(x, axis=0)
#     preds = model.predict(x)
#     score = tf.nn.softmax(preds[0])
#     class_name = class_names[np.argmax(score)]
#     print(preds, score, class_name)
#     return preds, score, class_name
