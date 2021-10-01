import os
from tensorflow.keras.preprocessing import image as img
from keras.preprocessing.image import img_to_array
import numpy as np
from keras.applications.mobilenet import MobileNet, decode_predictions, preprocess_input
from datetime import datetime
from flask import Blueprint, request, render_template, jsonify
from modules.dataBase import collection as db

mod = Blueprint('backend', __name__, template_folder='templates', static_folder='./static')
UPLOAD_URL = 'http://192.168.1.103:5000/static/'
model = MobileNet()
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
        temp = request.files['file']
        if user_file.filename == '':
            return "file name not found ..."

        else:
            path = os.path.join(os.getcwd() + '\\modules\\static\\' + user_file.filename)
            user_file.save(path)
            classes = identifyImage(path)
            db.addNewImage(
                user_file.filename,
                classes[0][0][1],
                str(classes[0][0][2]),
                datetime.now(),
                UPLOAD_URL + user_file.filename)

            return jsonify({
                "status": "success",
                "prediction": classes[0][0][1],
                "confidence": str(classes[0][0][2]),
                "upload_time": datetime.now()
            })


def identifyImage(img_path):
    img
    image = img.load_img(img_path, target_size=(224, 224))
    x = img_to_array(image)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    preds = decode_predictions(preds, top=1)
    print(preds)
    return preds
