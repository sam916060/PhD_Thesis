# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 23:25:22 2024

@author: ezxsp4
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 23:19:35 2023

@author: sampathkumar
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 23:07:52 2023

@author: sampathkumar
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import joblib
import pandas as pd
from PIL import Image, ImageTk

# Load the trained machine learning model
best_grid = joblib.load('C:\\Users\\ezxsp4\\Downloads\\xgboost_model.pkl')

# Load your dataset
# dataset = pd.read_csv('/Users/sampathkumar/Downloads/IRI_11-07.csv')
dataset = pd.read_csv('C:\\Users\\ezxsp4\\Downloads\\IRI_11-07.csv')

# Define the original feature names
feature_names = [
    ("IRI_initial", "International Roughness Index", "m/km"),
    ("TC", "Percentage of slabs with Transverse Cracking (all severities)", "%"),
    ("SPALL", "Percentage of slabs with spalling (all severities)", "%"),
    ("PATCH", "Pavement surface area with flexible and rigid patching (all severities)", "%"),
    ("FAULT", "Total joint faulting cumulated per kilometre", "mm"),
    ("AGE", "Age of the pavement", "number"),
    ("FI", "Freezing Index", "°C"),
    ("P200", "Percent subgrade material passing the 75-micron sieve", "%")
]

# Split the dataset into X (features) and y (target)
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Train the model
best_grid.fit(X, y)

# Calculate the minimum and maximum values for each input variable
min_values = X.min(axis=0)
max_values = X.max(axis=0)

# Define a function to determine the text color based on the prediction value
def get_color(prediction_value):
    if prediction_value < 1.5:
        return "green"
    elif 1.5 <= prediction_value < 3.0:
        return "orange"
    else:
        return "red"

# Modify the predict function to include range validation
def predict():
    try:
        independent_vars = [
            float(entry_vars[i].get()) for i in range(8)
        ]
        
        # Check if input values are within the acceptable range
        for i in range(8):
            if independent_vars[i] < min_values[i] or independent_vars[i] > max_values[i]:
                result_label.config(text=f"Enter valid values for {feature_names[i][1]}.")
                result_label.configure(foreground="red")
                return
        
        prediction = best_grid.predict([independent_vars])[0]
        prediction_IRI = prediction
        
        # Update the label with the predicted result and color
        result_label.config(text=f"IRI Prediction: {prediction_IRI:.2f}")
        result_label.configure(foreground=get_color(prediction_IRI))
    except Exception as e:
        result_label.config(text=f"An error occurred: {e}")
        result_label.configure(foreground="red")

# Create the main application window
app = tk.Tk()
app.title("IRI Predictor")

# Load and resize the first logo (Notts-logo.png)
notts_logo = Image.open('C:\\Users\\ezxsp4\\Downloads\\Notts-logo.png')
notts_logo = notts_logo.resize((100, 50), Image.ANTIALIAS)
notts_logo_photo = ImageTk.PhotoImage(notts_logo)

# Load and resize the second logo (NH-logo.jpeg)
nh_logo = Image.open('C:\\Users\\ezxsp4\\Downloads\\NH-logo.jpeg')
nh_logo = nh_logo.resize((100, 50), Image.ANTIALIAS)
nh_logo_photo = ImageTk.PhotoImage(nh_logo)

# Create labels for the logos and place them in the top left and top right corners
notts_logo_label = ttk.Label(app, image=notts_logo_photo)
notts_logo_label.photo = notts_logo_photo
notts_logo_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

nh_logo_label = ttk.Label(app, image=nh_logo_photo)
nh_logo_label.photo = nh_logo_photo
nh_logo_label.grid(row=0, column=1, padx=10, pady=10, sticky='e')

# Create a heading for the app
heading_label = ttk.Label(app, text="IRI Predictor", font=('Helvetica', 16, 'bold'))
heading_label.grid(row=1, column=0, columnspan=2, pady=10)

# Create a frame for the input fields
input_frame = ttk.Frame(app)
input_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

# Create input fields with labels and units
entry_vars = [tk.DoubleVar() for _ in range(8)]

for i in range(8):
    label = ttk.Label(input_frame, text=f"{feature_names[i][1]} ({feature_names[i][2]})", font=('Helvetica', 12))
    label.grid(row=i, column=0, padx=10, pady=5, sticky='w')
    
    entry = ttk.Entry(input_frame, textvariable=entry_vars[i], font=('Helvetica', 12))
    entry.grid(row=i, column=1, padx=10, pady=5)

# Create a button to trigger the prediction
predict_button = ttk.Button(input_frame, text="Predict", command=predict)
predict_button.grid(row=8, column=0, columnspan=2, pady=10)

# Create a label to display the predicted result
result_label = ttk.Label(input_frame, text="IRI: ", font=('Helvetica', 14, 'bold'))
result_label.grid(row=9, column=0, columnspan=2, pady=10)

# Start the Tkinter main loop
app.mainloop()
