# Import required libraries
import pandas as pd
from tkinter import *
from tkinter import messagebox, simpledialog
from profanity_check import predict_prob  # For language detection
import os

# Check if required packages are installed
try:
    import pandas
except ImportError:
    print("Install pandas: pip install pandas")
    
try:
    from profanity_check import predict_prob
except ImportError:
    print("Install profanity-check: pip install profanity-check")

# Add these imports
import re
from collections import Counter

def is_bot_enhanced(response):
    # Check for gibberish (repeating characters)
    if re.match(r'^(.)\1{3,}$', response):
        return True
        
    # Check for random character sequences
    if re.match(r'^[^\w\s]{5,}$', response):
        return True
        
    return False
# Initialize main window
root = Tk()
root.title("Response Analyzer")
root.geometry("400x300")

# Create list to store responses and analysis results
responses = []

# Function to save responses with analysis
def save_response():
    response = entry.get().strip()
    
    if response:
        # Detect inappropriate language
        is_inappropriate = predict_prob([response])[0] > 0.5
        
        # Detect bot-like patterns (simple version: repeated responses)
        is_bot = any(resp['Response'] == response for resp in responses)
        
        responses.append({
            "Response": response,
            "Inappropriate Language": is_inappropriate,
            "Possible Bot": is_bot
        })
        
        status_label.config(text=f"Responses collected: {len(responses)}")
        entry.delete(0, END)
    else:
        messagebox.showwarning("Empty Input", "Please enter a response")

# Function to export to Excel
def export_to_excel():
    if not responses:
        messagebox.showwarning("No Data", "No responses to export")
        return
    
    df = pd.DataFrame(responses)
    
    try:
        # Create filename with dialog box
        filename = simpledialog.askstring("Save File", 
                                         "Enter filename (without extension):",
                                         parent=root)
        if filename:
            df.to_excel(f"{filename}.xlsx", index=False)
            messagebox.showinfo("Success", f"File saved as {filename}.xlsx")
            # Clear data after export
            responses.clear()
            status_label.config(text="Responses collected: 0")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed: {str(e)}")

# GUI Layout
Label(root, text="Enter Response:").pack(pady=5)
entry = Entry(root, width=50)
entry.pack(pady=5)

Button(root, text="Save Response", command=save_response).pack(pady=5)
Button(root, text="Export to Excel", command=export_to_excel).pack(pady=5)
status_label = Label(root, text="Responses collected: 0")
status_label.pack(pady=10)

# Start the application
root.mainloop()