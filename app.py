from keras.models import load_model
from modules import app

model = load_model("modules/model/mobilenet_model.hdf5")
print("model loading .... plaese wait this might take a while")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port="5000", debug=False)
