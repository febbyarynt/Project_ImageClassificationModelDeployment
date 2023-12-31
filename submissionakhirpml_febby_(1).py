# -*- coding: utf-8 -*-
"""SubmissionAkhirPML_Febby (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18qofQbr0P4gjXGSq-g7ty_Y5T2l6kdKf

## Data Diri
* Nama : Febby Ariyanti Herdiana
* Grup : M06
"""

!pip install -q kaggle

from google.colab import files
files.upload()

!mkdir ~/.kaggle
!cp kaggle.json ~/.kaggle/

import os, zipfile, shutil

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras_preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import MaxPooling2D, Dense, Dropout, Conv2D

import matplotlib.pyplot as plt

!kaggle datasets download -d viratkothari/animal10

local_zip = '/content/animal_class.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/content')
zip_ref.close()

main_dir = os.path.join('/content/Animals-10')
print(os.listdir(main_dir))

from PIL import Image
samples = 0

for x in os.listdir(main_dir):
  dir = os.path.join('/content/Animals-10', x)
  y = len(os.listdir(dir))
  print(x+' :', y)
  samples = samples + y
  
  image_name = os.listdir(dir)
  for z in range(3):
    image_path = os.path.join(dir, image_name[z])
    image = Image.open(image_path)
    print(image.size)
  print()


print('Total Sample : ', samples)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = image.load_img('/content/Animals-10/butterfly/butterfly (1).jpeg')
imgplot = plt.imshow(img)

ignore_dir = ['butterfly', 'sheep', 'dog', 'cat', 'cow', 'squirrel', 'elephant']

for dir in ignore_dir:
  path = os.path.join(main_dir, dir)
  shutil.rmtree(path)

print(os.listdir(main_dir))

from PIL import Image
samples = 0

for x in os.listdir(main_dir):
  dir = os.path.join('/content/Animals-10', x)
  y = len(os.listdir(dir))
  print(x+' :', y)
  samples = samples + y
  
  image_name = os.listdir(dir)
  for z in range(3):
    image_path = os.path.join(dir, image_name[z])
    image = Image.open(image_path)
    print(image.size)
  print()


print('Total Sample : ', samples)

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    horizontal_flip=True,
    shear_range = 0.2,
    zoom_range = 0.2,
    fill_mode = 'nearest',
    validation_split = 0.2)

train_generator = train_datagen.flow_from_directory(
    main_dir,
    target_size=(150, 150),
    batch_size=128,
    class_mode='categorical',
    subset='training')
 
validation_generator = train_datagen.flow_from_directory(
    main_dir,
    target_size=(150, 150),
    batch_size=128,
    class_mode='categorical',
    subset='validation')

model = Sequential()

model.add(Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3))),
model.add(MaxPooling2D(2, 2)),
model.add(Conv2D(64, (3,3), activation='relu')),
model.add(MaxPooling2D(2,2)),
model.add(Conv2D(128, (3,3), activation='relu')),
model.add(MaxPooling2D(2,2)),
model.add(Conv2D(128, (3,3), activation='relu')),
model.add(MaxPooling2D(2,2)),
model.add(Flatten()),
model.add(Dense(512, activation='relu')),
model.add(Dense(3, activation='softmax')),

model.summary()

class Callback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy') and logs.get('val_accuracy') > 0.92):
      print("\n The accuracy rate was above 92%!")
      self.model.stop_training = True
callbacks = Callback()

model.compile(optimizer=tf.optimizers.Adam(),
              loss='categorical_crossentropy',
              metrics = ['accuracy'])

history = model.fit(
    train_generator,
    epochs=50,
    validation_data=validation_generator,
    verbose=2,
    callbacks=[callbacks])

figure = plt.figure(figsize = (15, 5))

figure.add_subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Accuracy Plot')
plt.xlabel('Value')
plt.ylabel('Epoch')
plt.legend(['Train', 'Validation'], loc = 'lower right')

figure.add_subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss Plot')
plt.xlabel('Value')
plt.ylabel('Epoch')
plt.legend(['Train', 'Validation'], loc = 'upper right')

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('model.tflite', 'wb') as f:
  f.write(tflite_model)