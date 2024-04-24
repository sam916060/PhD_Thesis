import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import joblib
import pandas as pd
from PIL import Image, ImageTk

# Load all the trained machine learning models and datasets
models = {
    "Longitudinal Cracking": joblib.load('C:\\Users\\ezxsp4\\Downloads\\LC_RFR_model.pkl'),
    "Transverse Cracking": joblib.load('C:\\Users\\ezxsp4\\Downloads\\TC_model_XGB.pkl'),
    "Faulting": joblib.load('C:\\Users\\ezxsp4\\Downloads\\Faulting_model1.pkl'),
    "IRI": joblib.load('C:\\Users\\ezxsp4\\Downloads\\xgboost_model.pkl')
}

datasets = {
    "Longitudinal Cracking": pd.read_csv('C:\\Users\\ezxsp4\\Downloads\\LC-12.09.csv'),
    "Transverse Cracking": pd.read_csv('C:\\Users\\ezxsp4\\Downloads\\TC-08.09 (1).csv'),
    "Faulting":pd.read_csv('C:\\Users\\ezxsp4\\Downloads\\Fault_14.02.23.csv'),
    "IRI": pd.read_csv('C:\\Users\\ezxsp4\\Downloads\\IRI_11-07.csv'),
}

# Define feature names for each distress
feature_names = {
    "Longitudinal Cracking": [
        "Slab Thickness (mm)", "Base Thickness (mm)", "Annual Average Daily Traffic",
        "Joint Spacing (mm)", "Annual Precipitation (mm)", "Average Annual Temp Range",
        "Freezing Index", "Compressive Strength (MPa)", "Elastic Modulus (MPa)", "Density of Concrete (kg/m3)",
        "Modulus of Rupture (MPa)", "Tensile Strength (MPa)", "Age"
    ],
    "Transverse Cracking": [
        "ST", "BT", "AD", "JS", "AP", "AT", "FI", "SC", "EM", "DE", "TS", "CT", "AG"
    ],
    "Faulting": [
        "ST", "BT", "AD", "JS", "AP", "AT", "FI", "P200"
    ],
    "IRI": [
        "IRI_initial", "TC", "SPALL", "PATCH", "FAULT", "AGE", "FI", "P200"
    ],
}

# Define the main function to predict distress
def predict_distress():
    distress = distress_var.get()
    model = models[distress]
    dataset = datasets[distress]
    feature_name = feature_names[distress]
    
    try:
        independent_vars = [
            float(entry_vars[i].get()) for i in range(len(feature_name))
        ]
        
        min_values = dataset.min(axis=0)
        max_values = dataset.max(axis=0)
        
        for i in range(len(feature_name)):
            if independent_vars[i] < min_values[i] or independent_vars[i] > max_values[i]:
                messagebox.showerror("Error", f"Enter valid values for {feature_name[i]}.")
                return
        
        prediction = model.predict([independent_vars])[0]
        
        if distress == "IRI":
            if prediction < 1.5:
                result_label.config(text=f"IRI Prediction: {prediction:.2f}", foreground="green")
            elif 1.5 <= prediction < 3.0:
                result_label.config(text=f"IRI Prediction: {prediction:.2f}", foreground="orange")
            else:
                result_label.config(text=f"IRI Prediction: {prediction:.2f}", foreground="red")
        else:
            result_label.config(text=f"Predicted {distress}: {prediction:.2f}")
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main application window
app = tk.Tk()
app.title("Distress Predictor")

# Create a frame for the distress selection
distress_frame = ttk.Frame(app)
distress_frame.pack(pady=10)

# Create a label and dropdown box for selecting the distress
distress_label = ttk.Label(distress_frame, text="Select Distress:")
distress_label.grid(row=0, column=0, padx=5)

distress_var = tk.StringVar()
distress_dropdown = ttk.Combobox(distress_frame, textvariable=distress_var, values=list(models.keys()))
distress_dropdown.grid(row=0, column=1, padx=5)
distress_dropdown.current(0)

# Create a frame for input fields
input_frame = ttk.Frame(app)
input_frame.pack(pady=10)

# Create input fields based on the selected distress
entry_vars = [tk.DoubleVar() for _ in range(16)]  # Maximum number of input fields

# Function to clear entry fields when distress selection changes
def clear_entry_fields(event):
    for entry in entry_fields:
        entry.delete(0, "end")

def create_entry_fields(distress):
    feature_name = feature_names[distress]
    num_rows = len(feature_name)
    
    for i, name in enumerate(feature_name):
        label = ttk.Label(input_frame, text=name)
        label.grid(row=i, column=0, padx=5, pady=2)
    
        entry = ttk.Entry(input_frame, textvariable=entry_vars[i])
        entry.grid(row=i, column=1, padx=5, pady=2)
    
        entry_fields.append(entry)

d# Corrected distress_dropdown binding
distress_dropdown.bind("<<ComboboxSelected>>", lambda event: (clear_entry_fields(event), create_entry_fields(distress_var.get())))


# Create a button to trigger the prediction
predict_button = ttk.Button(app, text="Predict", command=predict_distress)
predict_button.pack(pady=10)

# Create a label to display the predicted result
result_label = ttk.Label(app, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Create input fields based on the selected distress
entry_fields = []

# Start the Tkinter main loop
app.mainloop()
