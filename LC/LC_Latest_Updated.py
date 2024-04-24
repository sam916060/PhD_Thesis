# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 01:30:04 2023

@author: ezxsp4
"""

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
best_grid = joblib.load('C:\\Users\\ezxsp4\\Downloads\\LC_RFR_model.pkl')

# Load your dataset
dataset = pd.read_csv('C:\\Users\\ezxsp4\\Downloads\\LC-12.09.csv')

# Define the original feature names
feature_names = [
    "Slab Thickness (mm)", "Base Thickness (mm)", "Annual Average Daily Traffic",
    "Joint Spacing (mm)", "Annual Precipitation (mm)", "Average Annual Temp Range",
    "Freezing Index", "Compressive Strength (MPa)", "Elastic Modulus (MPa)", "Density of Concrete (kg/m3)",
    "Modulus of Rupture (MPa)", "Tensile Strength (MPa)", "Age"
]

# Split the dataset into X (features) and y (target)
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Train the model
best_grid.fit(X, y)

# Calculate the minimum and maximum values for each input variable
min_values = X.min(axis=0)
max_values = X.max(axis=0)

# Define a function to determine the color based on the predicted value
def get_color(value):
    if value < 10:  # You can adjust this threshold as needed
        return "green"
    elif value < 20:
        return "orange"
    else:
        return "red"

# Modify the predict function to include range validation
def predict():
    try:
        independent_vars = [
            float(entry_vars[i].get()) for i in range(13)
        ]
        
        # Check if input values are within the acceptable range
        for i in range(13):
            if independent_vars[i] < min_values[i] or independent_vars[i] > max_values[i]:
                result_label.config(text=f"Enter valid values for {feature_names[i]}.")
                result_label.configure(foreground="red")
                return
        
        prediction = best_grid.predict([independent_vars])[0]
        prediction_in_meters_per_100_meters = prediction  # Convert to meters per 100 meters
        
        # Update the label with the predicted result and color
        result_label.config(text=f"Longitudinal Cracking: {prediction_in_meters_per_100_meters:.2f} ")
        result_label.configure(foreground=get_color(prediction_in_meters_per_100_meters))
    except Exception as e:
        result_label.config(text=f"An error occurred: {e}")
        result_label.configure(foreground="red")


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
