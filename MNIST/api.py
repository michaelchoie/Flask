import os
from webapp import app

if __name__ == "__main__":
    if not os.path.exists("mnist.model.best.hdf5"):
        os.system("python model.py")
    app.run(debug=True)