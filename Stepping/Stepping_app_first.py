# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 14:08:20 2023

@author: ezxsp4
"""

import tkinter as tk
from tkinter import ttk
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('C:\\Users\\ezxsp4\\Downloads\\Faulting_model1.pkl')

# Create a function to make predictions
def predict_fault():
    # Get input values from the user
    input_values = []
    for entry in entries:
        value = entry.get()
        if value == "":
            result_label.config(text="Please enter values for all variables.")
            return
        input_values.append(float(value))
    
    # Create a DataFrame with the input values
    input_data = pd.DataFrame([input_values], columns=['ST', 'BT', 'AD', 'JS', 'AP', 'AT', 'FI', 'CS', 'EM', 'DE', 'MR', 'TS', 'CT', 'AG', 'PN', 'PL'])
    
    # Use the model to make a prediction
    prediction = model.predict(input_data)
    
    # Display the prediction
    result_label.config(text=f'Predicted Fault: {prediction[0]:.2f}')

# Create the main application window
app = tk.Tk()
app.title('Stepping Predictor')

# Create labels and entry fields for input variables
labels = ['ST', 'BT', 'AD', 'JS', 'AP', 'AT', 'FI', 'CS', 'EM', 'DE', 'MR', 'TS', 'CT', 'AG', 'PN', 'PL']
entries = []

for i, label in enumerate(labels):
    label = ttk.Label(app, text=label)
    label.grid(column=0, row=i)
    
    entry = ttk.Entry(app)
    entry.grid(column=1, row=i)
    entries.append(entry)

# Create a button to make predictions
predict_button = ttk.Button(app, text='Predict Fault', command=predict_fault)
predict_button.grid(column=0, row=len(labels))

# Create a label to display the prediction
result_label = ttk.Label(app, text='')
result_label.grid(column=1, row=len(labels))

# Start the Tkinter main loop
app.mainloop()
