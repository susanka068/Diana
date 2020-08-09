#global imports
import tensorflow as tf
import json
import numpy as np 
import PIL.Image as Image

root_dir = './' #directory name of there the project is stored in your local device

#class_names denoe the abstract classes used for this classification
class_names = ['Abstract', 'Biker', 'Camouflage', 'Checked', 'Colourblocked', 'Conversational', 'Floral', 'Geometric', 'Graphic', 'Humour and Comic', 'Music', 'People and Places', 'Polka Dots', 'Self Design', 'Solid', 'Sports', 'Sports and Team Jersey', 'Striped', 'Superhero', 'Tie and Dye', 'Tribal', 'Typography', 'Varsity']

#load the trained model and cjeck the baseline
loaded_model = tf.keras.models.load_model(root_dir + 'DianaSaved_model/t-shirt-classifier')
loaded_model.summary()

#load and preprocess stage_3.json as the input in data
file = open(root_dir + 'stage_2.json')

#downloads the resizes an image from a given url according to our needs
def download_and_resize(url , id , image_height=224 , image_width = 224 , display = False):
  downloaded_image = tf.keras.utils.get_file('/tmp/image_' + str(id) + '.jpg',url)
  downloaded_image = Image.open(downloaded_image).resize((image_height,image_width))
  downloaded_image = np.array(downloaded_image)/255.0
  return downloaded_image

#predict the class_names used on the downloaded image batch
def predict_type_string(image):
  result = loaded_model.predict(image[np.newaxis, ...])
  predicted_class = np.argmax(result[0], axis=-1)
  return class_names[predicted_class]

#main functon starts here t runs a for loop for all the elements in stage_2.json and adds the color attribue 
for item in data:
    color_type_string =  predict_type_string(download_and_resize(item['image'],item['id']))
    if 'pattern' not in item['detail'] :
        item['detail']['pattern'] = []
    item['detail']['pattern'].append(color_type_string)
    #print( predict_type_string(download_and_resize(item['image'],item['id'])))

#save the updated json
with open(root_dir + 'stage_3.json' , 'w') as file_upload:
  json.dump(data,file_upload, indent= 4)
  file.close()
