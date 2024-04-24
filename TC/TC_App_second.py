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

# Set the window size and center it on the screen
app_width = 400
app_height = 600
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2
app.geometry(f"{app_width}x{app_height}+{x}+{y}")

# Create a style for buttons
style = ttk.Style()
style.configure("TButton", background="#008CBA", font=("Arial", 12))

# Define colors
background_color = "#F0F0F0"  # Light gray
title_color = "#333333"  # Dark gray
label_color = "#555555"  # Gray

# Set the background color for the entire app
app.configure(bg=background_color)

# Title
title_label = tk.Label(app, text="Transverse Cracking Predictor", font=("Arial", 18, "bold"), fg=title_color, bg=background_color)
title_label.pack(pady=(20, 10))

# Definition of Transverse Cracking
definition_label = tk.Label(app, text="Transverse cracking is a type of distress in pavement surfaces. This app predicts the likelihood of transverse cracking based on input parameters.", 
                             font=("Arial", 12), fg=label_color, bg=background_color, wraplength=350, padx=10, pady=10)
definition_label.pack()

# Create a frame for input fields
input_frame = tk.Frame(app, bg=background_color)
input_frame.pack(fill="both", expand=True)

# Create a canvas to hold the input fields and a scrollbar
canvas = tk.Canvas(input_frame, bg=background_color)
canvas.pack(side="left", fill="both", expand=True)

# Create a scrollbar
scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas to hold the input fields
input_fields_frame = tk.Frame(canvas, bg=background_color)
canvas.create_window((0, 0), window=input_fields_frame, anchor="nw")

# Create labels and entry fields for input variables
labels = ['ST', 'BT', 'AD', 'JS', 'AP', 'AT', 'FI', 'SC', 'EM', 'DE', 'TS', 'CT', 'AG']
entries = []

for i, label in enumerate(labels):
    label = tk.Label(input_fields_frame, text=label, font=("Arial", 12), fg=label_color, bg=background_color)
    label.grid(row=i, column=0, padx=10, pady=(5, 10), sticky="w")
    
    entry = ttk.Entry(input_fields_frame)
    entry.grid(row=i, column=1, padx=10, pady=(5, 10), sticky="ew")
    entries.append(entry)

# Update the canvas scroll region
input_fields_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Create a button to make predictions
predict_button = ttk.Button(app, text='Predict Transverse Cracking', command=predict_transverse_cracking, style="TButton")
predict_button.pack(pady=(10, 20))

# Create a label to display the prediction
result_label = tk.Label(app, text='', font=("Arial", 14, "bold"), fg=title_color, bg=background_color)
result_label.pack()

# Start the Tkinter main loop
app.mainloop()
