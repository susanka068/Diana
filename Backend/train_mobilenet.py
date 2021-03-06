#global imports
import os
import PIL
import pathlib

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import tensorflow as tf
import tensorflow_hub as hub

# For downloading the image.
import matplotlib.pyplot as plt
import tempfile
from six.moves.urllib.request import urlopen
from six import BytesIO

# For drawing onto the image.
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

# For measuring the inference time.
import time

# Print Tensorflow version
print(tf.__version__)

# Check available GPU devices.
print("The following GPU devices are available: %s" % tf.test.gpu_device_name())

#loading and precoesing the csv which contains training data
import pandas as pd
csv_url = "https://raw.githubusercontent.com/subashgandyer/Myntra-Tshirt-Classification/master/vidai8_new.csv"
document = pd.read_csv(csv_url , error_bad_lines=False) 
document.head()

class_names = np.unique(document['Sub_category'])
class_names
num_classes = len(class_names)
num_classes

#to decode a jpg image to RGB channel
def load_img(path):
  img = tf.io.read_file(path)
  img = tf.image.decode_jpeg(img, channels=3)
  return img

#display an image
def display_image(image):
  fig = plt.figure(figsize=(20, 15))
  plt.grid(False)
  plt.imshow(image)



#to download and resize an image from an url
def download_and_resize_image(url, tag , id ,  new_width=224, new_height=224,
                              display=False):
  try:
    parent_dir = './data/'
    foldername = parent_dir + tag
    try:
      os.mkdir(foldername)   
    except OSError as error: 
      pass
    filename = parent_dir + tag + '/tshirt_' + str(id) + '_' + tag + '.jpg'
    print(filename)
    response = urlopen(url)
    image_data = response.read()
    image_data = BytesIO(image_data)
    pil_image = Image.open(image_data)
    pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
    pil_image_rgb = pil_image.convert("RGB")
    pil_image_rgb.save(filename, format="JPEG", quality=90)
    print("Image downloaded to %s." % filename)
    if display:
      display_image(pil_image)
    return filename
  except:
    pass

#to download and split the training and validation data
for i in range(len(document['Link_to_the_image'])):
  image_url , tag , color = document['Link_to_the_image'][i] , document['Sub_category'][i] , document['Color'][i]
  download_and_resize_image(str(image_url) , str(tag) , i ,224, 224,display=False)

root_dir = pathlib.Path('Diana')
root_dir

#get the total count of images downloaded and initialize project directory and data_dir
data_dir = './data/'
data_dir = pathlib.Path(data_dir)
image_count = len(list(data_dir.glob('*/*.jpg')))
print(image_count)

#self-explanatory contants
batch_size = 32
img_height = 224
img_width = 224

#preparing training and validation data with high-level keras api 
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

#converting image to input tensors 
IMAGE_SHAPE = (224, 224)

image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
image_data = image_generator.flow_from_directory(str(data_dir), target_size=IMAGE_SHAPE)

#separating image batch and label_batch from image_data
for image_batch, label_batch in image_data:
  print("Image batch shape: ", image_batch.shape)
  print("Label batch shape: ", label_batch.shape)
  break

#mobilet classifier to download the classifier
classifier_url ="https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2"

IMAGE_SHAPE = (224, 224)

classifier = tf.keras.Sequential([
    hub.KerasLayer(classifier_url, input_shape=IMAGE_SHAPE+(3,))
])

result_batch = classifier.predict(image_batch)
result_batch.shape

labels_path = tf.keras.utils.get_file('ImageNetLabels.txt','https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
imagenet_labels = np.array(open(labels_path).read().splitlines())

predicted_class_names = imagenet_labels[np.argmax(result_batch, axis=-1)]
predicted_class_names

#headless mobilener classifier url
feature_extractor_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/2"

#download mobilenet classifier
feature_extractor_layer = hub.KerasLayer(feature_extractor_url,
                                         input_shape=(224,224,3))

#extracting the feature batch
feature_batch = feature_extractor_layer(image_batch)
print(feature_batch.shape)

#fixing all the bottom layers upto the bottleneck Flatten() layer
feature_extractor_layer.trainable = False

#add a top layer and check the model summary
model = tf.keras.Sequential([
  feature_extractor_layer,
  layers.Dense(image_data.num_classes)
])

model.summary()

predictions = model(image_batch)

predictions.shape

#compile model with 'adam' optimizer and accuracy matrices
model.compile(
  optimizer=tf.keras.optimizers.Adam(),
  loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
  metrics=['acc'])

class CollectBatchStats(tf.keras.callbacks.Callback):
  def __init__(self):
    self.batch_losses = []
    self.batch_acc = []

  def on_train_batch_end(self, batch, logs=None):
    self.batch_losses.append(logs['loss'])
    self.batch_acc.append(logs['acc'])
    self.model.reset_metrics()

#model training with newly added layers
steps_per_epoch = np.ceil(image_data.samples/image_data.batch_size)

batch_stats_callback = CollectBatchStats()

history = model.fit(image_data, epochs=5,
                    steps_per_epoch=steps_per_epoch,
                    callbacks=[batch_stats_callback])

model.summary() #new model summary

#plot the loss graph as the training progresses
plt.figure()
plt.ylabel("Loss")
plt.xlabel("Training Steps")
plt.ylim([0,2])
plt.plot(batch_stats_callback.batch_losses)

#plot the accuracy graph as the training progresses
plt.figure()
plt.ylabel("Accuracy")
plt.xlabel("Training Steps")
plt.ylim([0,1])
plt.plot(batch_stats_callback.batch_acc)

class_names = sorted(image_data.class_indices.items(), key=lambda pair:pair[1])
class_names = np.array([key.title() for key, value in class_names])
class_names
#checkout the classnames

predicted_batch = model.predict(image_batch)
predicted_id = np.argmax(predicted_batch, axis=-1)
predicted_label_batch = class_names[predicted_id]
#image and label batch

label_id = np.argmax(label_batch, axis=-1)

#visually validate how well the model predictions are
plt.figure(figsize=(10,9))
plt.subplots_adjust(hspace=0.5)
for n in range(30):
  plt.subplot(6,5,n+1)
  plt.imshow(image_batch[n])
  color = "green" if predicted_id[n] == label_id[n] else "red"
  plt.title(predicted_label_batch[n].title(), color=color)
  plt.axis('off')
_ = plt.suptitle("Model predictions (green: correct, red: incorrect)")

grace_hopper = tf.keras.utils.get_file('/tmp/image.jpg','https://n.nordstrommedia.com/id/sr3/6c18b57a-a99e-4b4c-8311-ab87b254a19b.jpeg?crop=pad&pad_color=FFF&format=jpeg&w=780&h=1196')
grace_hopper = Image.open(grace_hopper).resize((224,224))
grace_hopper
#check for a single image_prediction

grace_hopper = np.array(grace_hopper)/255.0
grace_hopper.shape
#input shape

result = model.predict(grace_hopper[np.newaxis, ...])
result.shape
#shape of result

predicted_class = np.argmax(result[0], axis=-1)
predicted_class
#check the output

class_names[predicted_class]
#map the output with original class_names

#experimantal prefetching
AUTOTUNE = tf.data.experimental.AUTOTUNE

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

print(tf.data.experimental.cardinality(train_ds).numpy())
print(tf.data.experimental.cardinality(val_ds).numpy())

#given a path to an image it returns the  ( image , label ) pair 
def process_path(file_path):
  label = get_label(file_path)
  # load the raw data from the file as a string
  img = load_img(file_path)
  return img, label

print(image_count)

#display image with label
def display_with_label(path):
  img , label = process_path(path)
  display_image(img)

# Set `num_parallel_calls` so multiple images are loaded/processed in parallel.
train_ds = train_ds.map(process_path)
val_ds = val_ds.map(process_path)

# Set `num_parallel_calls` so multiple images are loaded/processed in parallel.
train_ds = train_ds.map(process_path, num_parallel_calls=AUTOTUNE)
val_ds = val_ds.map(process_path, num_parallel_calls=AUTOTUNE)

"""for imag, label in train_ds.take(2):
  imag = tf.image.resize(imag,[224,224])
  print("Image shape: ", imag.numpy().shape)
  print("Label: ", label.numpy())
"""

print(train_ds)

# image_path = 'Diana/tshirt_9930_Colourblocked.jpg'
display_image(load_img(image_path))
print(get_label(image_path))

#configure dataset for smooth input pipeline and faster execution
def configure_for_performance(ds):
  ds = ds.cache()
  ds = ds.shuffle(buffer_size=1000)
  ds = ds.batch(200)
  ds = ds.prefetch(buffer_size=AUTOTUNE)
  return ds

train_ds = configure_for_performance(train_ds)
val_ds = configure_for_performance(val_ds)

#check first 9 image
image_batch, label_batch = next(iter(train_ds))

plt.figure(figsize=(10, 10))
for i in range(9):
  ax = plt.subplot(3, 3, i + 1)
  plt.imshow(image_batch[i].numpy().astype("uint8"))
  label = label_batch[i]
  plt.title(class_names[label])
  plt.axis("off")

# file_path = 'Diana/tshirt_9642_Sports and Team Jersey.jpg';
img = tf.io.read_file(file_path)
img = tf.image.decode_jpeg(img, channels=3)

#display_with_label('Diana/tshirt_1749_Typography.jpg')

import tensorflow_hub as hub

from tensorflow.keras import layers

feature_extractor_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/2"

feature_extractor_layer = hub.KerasLayer(feature_extractor_url,
                                         input_shape=(224,224,3))

image_batch = tf.image.resize(image_batch , [224,224])

feature_batch = feature_extractor_layer(image_batch)
print(feature_batch.shape)

feature_extractor_layer.trainable = False

for image_batch, label_batch in train_ds:
  print("Image batch shape: ", image_batch.shape)
  print("Label batch shape: ", label_batch.shape)
  break

model = tf.keras.Sequential([
  feature_extractor_layer,
  layers.Dense(num_classes)
])

model.summary()

predictions = model(image_batch)

predictions.shape

model.compile(
  optimizer=tf.keras.optimizers.Adam(),
  loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
  metrics=['acc'])

class CollectBatchStats(tf.keras.callbacks.Callback):
  def __init__(self):
    self.batch_losses = []
    self.batch_acc = []

  def on_train_batch_end(self, batch, logs=None):
    self.batch_losses.append(logs['loss'])
    self.batch_acc.append(logs['acc'])
    self.model.reset_metrics()
