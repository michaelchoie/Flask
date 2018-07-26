from webapp import app
from flask import render_template, request

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


def breed_detector(img_path):
    breed, confidence = resnet50_predict_breed(img_path)

    img = cv2.imread(img_path)
    cv_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(cv_rgb)
    plt.show()

    if dog_detector(img_path):
        print("Prediction: Dog \nBreed: %s \nConfidence level: %.4f%%" % (str(breed), confidence))
    elif face_detector(img_path):
        print("Prediction: Human \nMost similar dog breed: %s \nConfidence level of breed similarity: %.4f%%" % (str(breed), confidence))
    else:
        print("CNN cannot predict what that is. \nMost similar dog breed: %s \nConfidence level of breed similarity: %.4f%%" % (str(breed), confidence))
