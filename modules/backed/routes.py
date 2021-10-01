import os
import tensorflow as tf
from keras.models import load_model
from tensorflow.keras.preprocessing import image as img
from keras.preprocessing.image import img_to_array
import numpy as np
from datetime import datetime
from flask import Blueprint, request, render_template, jsonify
from modules.dataBase import collection as db

mod = Blueprint('backend', __name__, template_folder='templates', static_folder='./static')
UPLOAD_URL = 'http://192.168.1.103:5000/static/'
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

            image = img.load_img(path, target_size=(224, 224))
            img_array = img_to_array(image)
            img_array = np.expand_dims(img_array, axis=0)
            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])
            
            class_name = class_names[np.argmax(score)]
            score = np.max(score)


            db.addNewImage(
                user_file.filename,
                class_name,
                str(score),
                datetime.now(),
                UPLOAD_URL + user_file.filename)

            return jsonify({
                "status": "success",
                "class": class_name,
                "score": str(score),
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
