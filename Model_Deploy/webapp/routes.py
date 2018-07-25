import cv2
import numpy as np
import os
from flask import render_template, request
from keras.models import load_model
from webapp import app

# Route tells Flask what URL should trigger the function
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/predict", methods=['POST'])
def predict():
    # request object gives you access to parsed request data
    if request.method == "POST":
        file = request.files['image']
        if not file:
            return render_template("home.html", label="No file")

        # Read in the model
        model = load_model(os.path.abspath("mnist.model.best.hdf5"))

        # Image file read in as file storage object - must preprocess
        filestr = file.read()
        npimg = np.fromstring(filestr, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
        img = img.astype("float32") / 255
        img = img.reshape(1, 28, 28)

        # Predict class and render web page with the value
        label = str(model.predict_classes(img))

        return render_template("predict.html", label=label)
