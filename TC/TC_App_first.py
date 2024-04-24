# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 15:00:11 2023

@author: ezxsp4
"""

import tkinter as tk
from tkinter import ttk
import joblib
import pandas as pd

# Load the trained model for transverse cracking
model = joblib.load('C:\\Users\\ezxsp4\\Downloads\\TC_model_XGB.pkl')

# Load the dataset to get the minimum and maximum values
dataset = pd.read_csv('C:\\Users\\ezxsp4\\Downloads\\TC-08.09 (1).csv')
min_max_values = dataset.describe().loc[['min', 'max']].to_dict()

# Create a function to make predictions
def predict_transverse_cracking():
    # Get input values from the user
    input_values = []
    for i, entry in enumerate(entries):
        value = entry.get()
        try:
            # Convert the input to float
            float_value = float(value)
            
            # Check if the value is within the range
            if float_value < min_max_values[labels[i]]['min'] or float_value > min_max_values[labels[i]]['max']:
                result_label.config(text=f"{labels[i]} value not in range. Please enter a correct value.")
                return
            
            input_values.append(float_value)
        except ValueError:
            result_label.config(text=f"Invalid value for {labels[i]}. Please enter a valid number.")
            return
    
    # Create a DataFrame with the input values
    input_data = pd.DataFrame([input_values], columns=labels)
    
    # Use the model to make a prediction
    prediction = model.predict(input_data)
    
    # Display the prediction
    result_label.config(text=f'Predicted Transverse Cracking: {prediction[0]:.2f}')

# Create the main application window
app = tk.Tk()
app.title('Transverse Cracking Predictor')

# Add some padding and set the window size
app.geometry("400x600")  # Increased height to accommodate definition text
app.configure(bg="#f0f0f0")

# Create a style for buttons
style = ttk.Style()
style.configure("TButton", background="#008CBA", foreground="white", font=("Arial", 12))

# ... (previous code)

# Definition of Transverse Cracking
definition_label = tk.Label(app, text="Transverse Cracking Predictor:\n"
                                      "Transverse cracking is a type of distress in pavement surfaces.\n"
                                      "This app predicts the likelihood of transverse cracking based on input parameters.", 
                             font=("Arial", 12), wraplength=350, padx=10, pady=10)
definition_label.grid(column=0, columnspan=2)

# ... (rest of the code)


# Create labels and entry fields for input variables
labels = ['ST', 'BT', 'AD', 'JS', 'AP', 'AT', 'FI', 'SC', 'EM', 'DE', 'TS', 'CT', 'AG']
entries = []

for i, label in enumerate(labels):
    label = tk.Label(app, text=label)
    label.grid(column=0, row=i+1, pady=(5, 5), sticky="w")
    
    entry = ttk.Entry(app)
    entry.grid(column=1, row=i+1, padx=(5, 10), pady=(5, 10))
    entries.append(entry)

# Create a button to make predictions
predict_button = ttk.Button(app, text='Predict Transverse Cracking', command=predict_transverse_cracking)
predict_button.grid(column=0, columnspan=2, row=len(labels)+1, pady=10)

# Create a label to display the prediction
result_label = ttk.Label(app, text='', font=("Arial", 14, "bold"))
result_label.grid(column=0, columnspan=2, row=len(labels)+2)

# Start the Tkinter main loop
app.mainloop()
