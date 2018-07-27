from flask import render_template, request
from keras.models import load_model
from webapp import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


'''
@app.route("/predict", methods=['POST'])
def predict()
    if request.method == 'POST':
        file = request.files['image']
        if not file:
            return render_template('home.html', label='No file')

        # Read in model
        model = load_model('best_model.hdf5')

        # Read in image and preprocess for CNN input

        # Predict class and render web page with the value
        label = str(model.predict_classes(img))

        return render_template("predict.html", label=label)
'''