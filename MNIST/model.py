import numpy as np
from keras.callbacks import ModelCheckpoint
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.utils import np_utils

# Load data
(X_Train, Y_Train), (X_Test, Y_Test) = mnist.load_data()

# Rescale images to (0,1) so higher valued pixels don't have more importance
# Also allows us to use a typical learning rate
X_Train = X_Train.astype("float32") / 255
X_Test = X_Test.astype("float32") / 255

# Encode categorical variables via one hot encoding
Y_Train = np_utils.to_categorical(Y_Train, 10)
Y_Test = np_utils.to_categorical(Y_Test, 10)

# Create the model
model = Sequential()
model.add(Flatten(input_shape=X_Train.shape[1:]))
model.add(Dense(512, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(512, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(10, activation="softmax"))

# Compile the model
model.compile(loss="categorical_crossentropy", optimizer="adam",
              metrics=["accuracy"])

# Train the model
checkpointer = ModelCheckpoint(filepath="mnist.model.best.hdf5", verbose=1,
                               save_best_only=True)
hist = model.fit(X_Train, Y_Train, batch_size=128, epochs=10,
                 validation_split=0.2, callbacks=[checkpointer], verbose=1,
                 shuffle=True)

# Score the model
score = model.evaluate(X_Test, Y_Test, verbose=1)
accuracy = 100 * score[1]

# Save the model
model.load_weights("mnist.model.best.hdf5")
