from keras.models import load_model
from modules import app

model = load_model("D:/coffee_server/modules\model/mobilenet_model.hdf5")
print("model loading .... plaese wait this might take a while")
app.run(debug=False,host='192.168.1.103',port=5000)