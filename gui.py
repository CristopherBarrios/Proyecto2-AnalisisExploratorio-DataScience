
import PySimpleGUI as sg
import os.path
from PIL import Image
import pandas as pd
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn import metrics

######
######
#######
#################Modelos
modelv1 = keras.models.load_model('checkpoint/model_checkpoint.h5') 
#modelv2 = keras.models.load_model('checkpoint/model2_checkpoint.h5')


# im1 = Image.open("./example.jpg")

# im1.show()
# Color palette
color_base = '#E7ECEF'
color_fondo_secundario = '#274C77'
color_secundario = '#6096BA'
color_terciario = '#A3CEF1'
color_texto = '#8B8C89'
button1text= "Classify Using model 1"
button2text= "Classify Using model 2"
globalfile=""
globalresult=""

# demoImage= Image.open(globalfile)

# Add an image file for the logo/icon
header_image_path = 'estilo/brainfly2.png'


# Layout for the header
layout_header = [
    [
        sg.Column([
            [sg.Image(filename=header_image_path, key="-HEADER-", background_color=color_base, pad=((200, 80), (0, 200)))],
        ], size=(800, 100), expand_x=True)
    ],
]

layout1 = [
    [
        sg.Text("Seleccionar Imagen"),
        sg.In(size=(21, 1), enable_events=True, key="-FILE-", background_color=color_fondo_secundario),
        sg.FileBrowse(key="-FILE-"),
    ],
    [sg.HSeparator()],
    [sg.Image(key="-IMAGE-")]
]

layout2 = [
    [sg.Text("Seleccionar el modelo")],
    [sg.Text("Modelo 1: 81% Accuracy")],
    [sg.Button(button1text)],
    [sg.Text("Modelo 2: 71% Accuracy")],
    [sg.Button(button2text)],
    [sg.Text("DIAGNOSTICO:")],
    [sg.Text("", key="-OUTPUT-")],
]

# Combine layouts
layout = [
    [
        sg.Column(layout_header),
    ],
    [
        sg.Column(layout1),
        sg.VSeparator(),
        sg.Column(layout2),
    ]
]

mywindow = sg.Window(title="Classifier", layout=layout, margins=(100,50) , background_color=color_base)


def makeprediction1(filename):
    try:
        # Open the image using PIL
        image = Image.open(filename)

        if image is not None:
            print("Image opened successfully")

            # Resize the image using the PIL .resize() method
            image = image.resize((512, 512))

            # Convert the resized PIL image to a NumPy array
            image_array = np.array(image)

            # Normalize the image by dividing by 255
            preprocessed_image = image_array / 255.0
            print("Image preprocessed successfully")

            # Expand dimensions if needed (depends on model input shape)
            if len(preprocessed_image.shape) == 2:
                preprocessed_image = np.expand_dims(preprocessed_image, axis=0)

            # Make the prediction
            prediction = modelv1.predict(preprocessed_image)
            # Extract the predicted class label
            predicted_class = np.argmax(prediction, axis=1)[0]
            class_labels = ['LAA', 'CE']
            predicted_class_label = class_labels[predicted_class]

            globalresult = predicted_class_label + str(prediction)
        else:
            globalresult = "Failed to open the image"
    except Exception as e:
        # Handle any exceptions that may occur during image loading or preprocessing
        print(f"Error: {e}")
        globalresult = "Error occurred during image loading/preprocessing"

    return globalresult



	#########################
	# prediction = modelv1.predict(Image.open(filename))
	# #print(prediction)
	# #prediction = modelv1.predict(Image.open(filename))
	# globalresult=prediction
	


def makeprediction2(filename):
    try:
        # Open the image using PIL
        image = Image.open(filename)

        if image is not None:
            print("Image opened successfully")

            # Resize the image using the PIL .resize() method
            image = image.resize((512, 512))

            # Convert the resized PIL image to a NumPy array
            image_array = np.array(image)

            # Normalize the image by dividing by 255
            preprocessed_image = image_array / 255.0
            print("Image preprocessed successfully")

            # Expand dimensions if needed (depends on model input shape)
            if len(preprocessed_image.shape) == 2:
                preprocessed_image = np.expand_dims(preprocessed_image, axis=0)

            # Make the prediction
            prediction = modelv2.predict(preprocessed_image)
            # Extract the predicted class label
            predicted_class = np.argmax(prediction, axis=1)[0]
            class_labels = ['LAA', 'CE']
            predicted_class_label = class_labels[predicted_class]

            globalresult = predicted_class_label + str(prediction)
        else:
            globalresult = "Failed to open the image"
    except Exception as e:
        # Handle any exceptions that may occur during image loading or preprocessing
        print(f"Error: {e}")
        globalresult = "Error occurred during image loading/preprocessing"

    return globalresult
	



while True:
	event, values = mywindow.read()

	if event == button1text:
		print("Boton 1 presionado")
		print("Enviare este file al modelo 1 : " +globalfile)
		globalresult = makeprediction1(globalfile)
		print(globalresult)
		mywindow["-OUTPUT-"].update(globalresult) 
	if event == button2text :
		print("Boton 2 presionado")
		print("Enviare este file al modelo 2 : " +globalfile)
		globalresult = makeprediction2(globalfile)
		mywindow["-OUTPUT-"].update(globalresult) 


	if event == "-FILE-" :
		print("Se selecciono una archivo")
		file= values["-FILE-"]
		print(file)
		globalfile=file
		demoImage= Image.open(globalfile)
		demoImage.save("demo.png")
		#mywindow["filename"].update(file)
		mywindow["-IMAGE-"].update(filename="demo.png")



	if event == sg.WIN_CLOSED:
		break

	if event == "-FOLDER-":
		folder = values ["-FOLDER-"]
		try:
			file_list = os.listdir(folder)
		except:
			file_list= []

		fnames = [
			f 
			for f in file_list
			if os.path.isfile(os.path.join(folder ,f)) and f.lower().endswith((".png",".gif"))
		]
		mywindow["-FILE_LIST-"].update(fnames)
	if event =="-FILE_LIST-":
		try:
			filename=os.path.join (values["-FOLDER-"], values["-FILE_LIST-"][0])
			filename = values["-FILE-"]
			#mywindow["filename"].update(filename)
			mywindow["-IMAGE-"].update(filename=filename)
		except:
			pass



mywindow.close()