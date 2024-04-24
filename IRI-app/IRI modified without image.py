import tkinter as tk
from tkinter import ttk
import numpy as np
import joblib
import pandas as pd
from PIL import Image, ImageTk

# Load the trained machine learning model
best_grid = joblib.load('/Users/sampathkumar/Downloads/xgboost_model.pkl')

# Load your dataset
dataset = pd.read_csv('/Users/sampathkumar/Downloads/IRI_11-07.csv')

# Define the original feature names
feature_names = [
    "IRI_initial", "TC", "SPALL", "PATCH",
    "FAULT", "AGE", 
    "FI", "P200" 
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

# Define functions for tooltips
def show_tooltip(event, text):
    tooltip = tk.Toplevel()
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{event.x_root + 15}+{event.y_root + 10}")
    label = ttk.Label(tooltip, text=text, background="lightyellow", font=('Helvetica', 10))
    label.pack()

def hide_tooltip(event):
    event.widget.master.destroy()

# Modify the predict function to include range validation
def predict():
    try:
        independent_vars = [
            float(entry_vars[i].get()) for i in range(8)
        ]
        
        # Check if input values are within the acceptable range
        for i in range(8):
            if independent_vars[i] < min_values[i] or independent_vars[i] > max_values[i]:
                result_label.config(text=f"Enter valid values for {feature_names[i]}.")
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
app.iconbitmap('path_to_icon.ico')  # Set the window icon

# Add a heading for the app
heading_label = ttk.Label(app, text="IRI Predictor", font=('Helvetica', 16, 'bold'))
heading_label.pack(pady=10)

# Create a frame for the input fields
input_frame = ttk.Frame(app)
input_frame.pack(padx=20, pady=20, fill='both', expand=True)

# Create a subframe for input fields
subframe = ttk.Frame(input_frame)
subframe.pack(side='left', padx=20, pady=20)

# Add descriptions for input fields
descriptions = [
    "Initial IRI (m/km)",
    "Traffic Count (vehicles/day)",
    "Spalling Index",
    "Patching Index",
    "Faulting Index",
    "Age of Road (years)",
    "Frost Index",
    "Precipitation (mm/year)",
]

# Create input fields with labels and descriptions
entry_vars = [tk.DoubleVar() for _ in range(8)]

for i in range(8):
    label = ttk.Label(subframe, text=feature_names[i], font=('Helvetica', 12))
    label.grid(row=i, column=0, padx=10, pady=5, sticky='w')
    
    entry = ttk.Entry(subframe, textvariable=entry_vars[i], font=('Helvetica', 12))
    entry.grid(row=i, column=1, padx=10, pady=5)

    # Add descriptions as tooltips
    label.bind("<Enter>", lambda event, desc=descriptions[i]: show_tooltip(event, desc))
    label.bind("<Leave>", hide_tooltip)

# Create a button to trigger the prediction
predict_button = ttk.Button(subframe, text="Predict", command=predict)
predict_button.grid(row=8, column=0, columnspan=2, pady=10)

# Create a label to display the predicted result
result_label = ttk.Label(subframe, text="IRI: ", font=('Helvetica', 14, 'bold'))
result_label.grid(row=9, column=0, columnspan=2, pady=10)

# Start the Tkinter main loop
app.mainloop()
