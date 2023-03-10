import joblib
from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

data = pd.read_csv("IRIS.csv")
dispatch_model = {"RF": "RF.bin", "SVM" : "SVM.bin", "XGB" : "XGB.pkl"}

#Encoding the data
le = LabelEncoder()
labels = data['species']
le.fit(labels)
labels= le.transform(labels)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
        
@app.route('/')
def home():
    return  render_template('home.html')


@app.route('/predict',methods=['POST'])
def predict():
    data = [str(x) for x in request.form.values()]
    model = (data[0]).upper()
    del data[0]

    #loading model and scaling
    Xg_model = joblib.load(dispatch_model[model])
    scaling = joblib.load("scaling.bin")

    #make predictions
    new_data = scaling.transform(np.array(data).reshape(1,-1))
    output = le.inverse_transform(Xg_model.predict(new_data))
    return render_template("home.html", prediction_model= "Called Model  {} ".format(model),prediction_flower="\n The Flower is {} ".format(output[0]))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


