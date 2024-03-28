#from __future__ import division, print_function
#import tensorflow as tf
#import logging as log
import os
import math
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template

app = Flask(__name__)

# model = #laoding model
MODEL_PATH = 'models/CNN_model.h5'
model = load_model(MODEL_PATH)
#model._make_predict_function()



def model_predict(img_path, model):
    # Decoding and pre-processing base64 image
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    pred = model.predict(x)
    return pred



@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        
        # Save the file to ./uploads
        #basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            './uploads', secure_filename(f.filename))
        print(file_path)
        f.save(file_path)

     
        predict = model_predict(file_path,model)
        prediction = ''
        if predict[0][0] < predict[0][1]:
            prediction = 'The Patient has ' + str(math.ceil(predict[0][1]*100)) +'% Chances of Pneumonia'
        else:
            prediction = 'The Patient is Normal with ' + str(math.ceil(predict[0][1]*100)) + '% Chances of Pneumonia'

        return prediction
    return None



@app.route('/')
def index():
# Main page
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)




