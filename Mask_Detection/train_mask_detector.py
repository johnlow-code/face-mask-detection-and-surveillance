# -*- coding: utf-8 -*-
"""
Created on Sun May 30 17:21:01 2021

@author: John Low
"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import os

INIT_LR = 1e-4  # Initial Learning Rate
EPOCHS = 15    # How many runs of trainings
BS = 64         # Batch Size of the training
DIRECTORY = "/Mask Detection/dataset"
CATEGORIES = ["with mask", "without mask"]

#  Images

print("[INFO] loading images")

data = []   #Image arrays are appended in it
labels = [] #Appends image labels

for category in CATEGORIES:
    path = os.path.join(DIRECTORY, category)
    for img in os.listdir(path):
        img_path = os.path.join(path, img)  #specific path of one img
        # LOAD IMAGE AND CONVERT SIZE TO 1024 X 1024
        image = load_img(img_path,target_size=(256,256))
        image = img_to_array(image) #KERAS: convert image to array
        image = preprocess_input(image) #MobileNetV2
        
        # Append Image to data list
        data.append(image)
        
        # Appends labels to label list
        labels.append(category)
        

# Encoding the labels as 0 and 1
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
labels = to_categorical(labels)

data = np.array(data, dtype="float32")
labels = np.array(labels)

(trainX, testX, trainY, testY) = train_test_split(data, labels,
      test_size = 0.30, stratify=labels, random_state=53)
# Refer to the diagram in the report for the meaning of x train, y train etc

# Construct the training image generator for data augmentation
aug = ImageDataGenerator(
    rotation_range=20,
    zoom_range=0.15, #Randomly zoom with tange of 0.15
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
    fill_mode="nearest"
    )

# load the MobileNetV2 network, ensuring head fc layer sets are left off.
# imagenet is used as the predefined weights for images
# 3 for 3 channels, RGB
baseModel = MobileNetV2(weights="imagenet", include_top=False,
                        input_tensor=Input(shape=(256, 256, 3)))

# construct the head of the model that will be placed on top of the base mmodel
headModel = baseModel.output
headModel = AveragePooling2D(pool_size=(7,7))(headModel)
headModel = Flatten(name="flatten")(headModel)
headModel = Dense(128, activation="relu")(headModel) #non linear, for images
headModel = Dropout(0.3)(headModel) # Dropout rate, careful of overfitting
headModel = Dense(2, activation="softmax")(headModel) #number of categories

# place head FC model on top of base model
# This is the ACTUAL model we will train
model = Model(inputs=baseModel.input, outputs=headModel)

# loop over all layers in the base model and freeze them so they will not
# be updated during the first training
for layer in baseModel.layers:
    layer.trainable = False

# Compile Mdoel
print("[INFO] Compiling model...")
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt,
              metrics=["accuracy"])

# Train the head of the NN
print("[INFO] Training head!")
H = model.fit(
    aug.flow(trainX, trainY, batch_size=BS),
    steps_per_epoch=len(trainX) // BS,
    validation_data=(testX,testY),
    validation_steps=len(testX) // BS,
    epochs=EPOCHS)
    
# make predictions on the testing set
print("[INFO] evaluating network...")
predIdxs = model.predict(testX, batch_size=BS)

# for each image in the testing set we need to find the index of the label with
# corresponding largest predicted probability
predIdxs = np.argmax(predIdxs, axis=1)

# show a nicely formatted classification report
print(classification_report(testY.argmax(axis=1), predIdxs, 
                            target_names=lb.classes_))

# SERIALIZE model to the disk
print("[INFO] saving mask detector model...")
model.save("mask_detector.model", save_format="h5")

# Plot training loss and accuracy
N = EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), N.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), N.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), N.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), N.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig("plot.png")




    
        
