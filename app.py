# application file
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import tensorflow
from tensorflow.keras.preprocessing import image
import cv2
import numpy
import os

#insitalize the app
app = Flask(__name__)

#load the model
model = None
#tensorflow.keras.models.load_model("Cat_Dog_Classifier_97.h5")
@app.route('/')
def upload_file():
   return render_template('form.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file'] 

        filepath = secure_filename(f.filename) # save file 
        f.save(filepath)
        predictive_path = os.getcwd()
        #predictive_path = "C:\\Learnbay\\DeploymentLearnbay\\CNN_Cat_vs_Dog\\Flask_app"
        image_path1 = f'{predictive_path}\\{filepath}'
        print(image_path1)
        test_image = image.load_img(f'{predictive_path}\\{filepath}', target_size=(64,64))
        
        test_image = image.img_to_array(test_image)
        test_image = test_image.reshape(1,64,64,3)

        load_model = tensorflow.keras.models.load_model('Cat_Dog_Classifier_97.h5')
        result = load_model.predict(test_image)

        if result[0][0] == 1:
            out = "DOG"
        else:
            out = "CAT"
        return render_template('predict.html', data=f"It's a {out}", image_path = filepath)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)