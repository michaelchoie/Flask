import os
from webapp import app


if __name__ == "__main__":

    # Get and clean the data
    if not os.path.exists("dog_images"):
        if os.path.exists("downloads"):
            print("Downloading images...")
            os.system("python web_scraper.py")
        print("Organizing files")
        os.system("python data_prep.py")

    # Create and train the model
    if not os.path.exists("best_model.hdf5"):
        print("Creating and training model...")
        os.system("python model.py")

    app.run(debug=True)
