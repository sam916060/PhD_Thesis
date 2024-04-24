# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 14:03:04 2023

@author: ezxsp4
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 11:27:52 2023

@author: ezxsp4
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import joblib
import pandas as pd
from PIL import Image, ImageTk

# Load the trained machine learning model
best_grid = joblib.load('C:\\Users\\ezxsp4\\Downloads\\trained_model.pkl')

# Load your dataset
dataset = pd.read_csv('C:\\Users\\ezxsp4\\Downloads\\LC-11.11.csv')

# Define the original feature names
feature_names = [
    "Slab Thickness (mm)", "Base Thickness (mm)", "Annual Average Daily Traffic",
    "Joint Spacing", "Annual Precipitation", "Average Annual Temp Range",
    "Freezing Index", "Compressive Strength", "Elastic Modulus", "Density of Concrete",
    "Modulus of Rupture", "Tensile Strength", "Age"
]

# Split the dataset into X (features) and y (target)
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Train the model
best_grid.fit(X, y)

# Your predict() function
def predict():
    try:
        independent_vars = [
            float(entry_vars[i].get()) for i in range(13)
        ]
        
        prediction = best_grid.predict([independent_vars])[0]
        prediction_in_meters_per_100_meters = prediction / 100  # Convert to meters per 100 meters
        
        # Update the label with the predicted result and color
        result_label.config(text=f"Longitudinal Cracking: {prediction_in_meters_per_100_meters:.2f} meters/100m")
        result_label.configure(foreground=get_color(prediction_in_meters_per_100_meters))
    except Exception as e:
        result_label.config(text=f"An error occurred: {e}")
        result_label.configure(foreground="red")

# Define a function to determine the text color based on the prediction value
def get_color(prediction_value):
    if prediction_value < 0.5:
        return "green"
    elif 0.5 <= prediction_value < 1.0:
        return "orange"
    else:
        return "red"

# Create the main application window
app = tk.Tk()
app.title("Longitudinal Cracking Predictor")

# Add a heading for the app
heading_label = ttk.Label(app, text="Longitudinal Cracking Predictor", font=('Helvetica', 16, 'bold'))
heading_label.pack(pady=10)

# Add the definition of longitudinal cracking
definition_label = ttk.Label(app, text="Definition: Cracks parallel to the pavement’s centerline or laydown direction.", font=('Helvetica', 12))
definition_label.pack(pady=5)

# Create a frame for the input fields and image
input_frame = ttk.Frame(app)
input_frame.pack(padx=20, pady=20, fill='both', expand=True)

# Create a subframe for input fields
subframe = ttk.Frame(input_frame)
subframe.pack(side='left', padx=20, pady=20)

# Create input fields for independent variables with the original feature names and an appealing font
entry_vars = [tk.DoubleVar() for _ in range(13)]

for i in range(13):
    label = ttk.Label(subframe, text=feature_names[i], font=('Helvetica', 12))
    label.grid(row=i, column=0, padx=10, pady=5, sticky='w')
    
    entry = ttk.Entry(subframe, textvariable=entry_vars[i], font=('Helvetica', 12))
    entry.grid(row=i, column=1, padx=10, pady=5)

# Create a button to trigger the prediction
predict_button = ttk.Button(subframe, text="Predict", command=predict)
predict_button.grid(row=13, column=0, columnspan=2, pady=10)

# Create a label to display the predicted result
result_label = ttk.Label(subframe, text="Longitudinal Cracking: ", font=('Helvetica', 14, 'bold'))
result_label.grid(row=14, column=0, columnspan=2, pady=10)

# Load the image and display it on the right side
image = Image.open('C:\\Users\\ezxsp4\\Downloads\\rp.png')
image.thumbnail((450, 450))  # Resize the image to fit the frame
photo = ImageTk.PhotoImage(image)

image_label = ttk.Label(input_frame, image=photo)
image_label.image = photo  # Keep a reference to prevent image from being garbage collected
image_label.pack(side='right', padx=500)

# Start the Tkinter main loop
app.mainloop()
