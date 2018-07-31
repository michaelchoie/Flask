import cv2
import numpy as np
import os
from flask import render_template, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
from webapp import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image']
        if not file:
            return render_template('home.html', label='No file')

        # Read in model
        model = load_model('best_model.hdf5')

        # Read in image and preprocess for CNN input
        filestr = file.read()
        npimg = np.fromstring(filestr, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        # Predict class and render web page with the value
        dog_breed = os.listdir('./dog_images/train')
        pred = model.predict(x)
        index = np.argmax(pred)
        prob = round(np.asscalar(np.max(pred)), 2)

        return jsonify({
            'prediction_result': {
                'Dog Breed': dog_breed[index],
                'Probability': prob
            }
        })
