import tkinter as tk
from tkinter import ttk
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('C:\\Users\\ezxsp4\\Downloads\\Faulting_model1.pkl')

# Load the dataset to get the minimum and maximum values
dataset = pd.read_csv('C:\\Users\\ezxsp4\\Downloads\\Fault_14.02.23.csv')
min_max_values = dataset.describe().loc[['min', 'max']].to_dict()

# Create a function to make predictions
def predict_fault():
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
    result_label.config(text=f'Predicted Fault: {prediction[0]:.2f}')

# Create the main application window
app = tk.Tk()
app.title('Stepping Predictor')

# Add some padding and set the window size
app.geometry("400x400")
app.configure(bg="#f0f0f0")

# Create a style for labels and buttons
style = ttk.Style()
style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
style.configure("TButton", background="#008CBA", foreground="white", font=("Arial", 12))

# Create labels and entry fields for input variables
labels = ['ST', 'BT', 'AD', 'JS', 'AP', 'AT', 'FI', 'CS', 'EM', 'DE', 'MR', 'TS', 'CT', 'AG', 'PN', 'PL']
entries = []

for i, label in enumerate(labels):
    label = ttk.Label(app, text=label)
    label.grid(column=0, row=i, padx=10, pady=5, sticky="w")
    
    entry = ttk.Entry(app)
    entry.grid(column=1, row=i, padx=10, pady=5)
    entries.append(entry)

# Create a button to make predictions
predict_button = ttk.Button(app, text='Predict Fault', command=predict_fault)
predict_button.grid(column=0, columnspan=2, row=len(labels), pady=10)

# Create a label to display the prediction
result_label = ttk.Label(app, text='', font=("Arial", 14, "bold"))
result_label.grid(column=0, columnspan=2, row=len(labels)+1)

# Start the Tkinter main loop
app.mainloop()
