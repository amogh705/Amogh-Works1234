#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tkinter import Tk, Button, Entry, StringVar, Label
import math

# Create main application window
root = Tk()
root.title("Scientific Calculator")
root.geometry("400x500")
root.resizable(False, False)
root.configure(bg="#222")  # Dark background

# Entry widget for display
expression = StringVar()
entry = Entry(root, textvariable=expression, font=("Arial", 20), bg="#333", fg="white", 
              borderwidth=5, relief="ridge", justify="right")
entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10, ipadx=8, ipady=8)

# Function to handle button clicks
def button_click(value):
    current = expression.get()
    expression.set(current + str(value))

# Function to clear entry field
def clear_entry():
    expression.set("")

# Function to evaluate expression
def calculate():
    try:
        expr = expression.get()
        expr = expr.replace("^", "**")  # Allow power operation

        # Convert function names to Python equivalents
        expr = expr.replace("sin(", "math.sin(math.radians(")
        expr = expr.replace("cos(", "math.cos(math.radians(")
        expr = expr.replace("tan(", "math.tan(math.radians(")
        expr = expr.replace("log(", "math.log10(")
        expr = expr.replace("sqrt(", "math.sqrt(")

        # Fix missing closing parentheses issue
        open_brackets = expr.count("(")
        close_brackets = expr.count(")")
        expr += ")" * (open_brackets - close_brackets)  # Add missing ')'

        # Handling tan(90) explicitly
        if "math.tan(math.radians(90))" in expr:
            expression.set("Undefined")
        else:
            result = eval(expr, {"math": math})  # Secure eval with math library only
            if isinstance(result, float):  
                result = round(result, 6)  # Round decimal values
            expression.set(result)

        history_label["text"] = f"History: {expr} = {result}"
    except Exception as e:
        expression.set("Error")  # Show general error

# Standard Calculator Buttons
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
]

for (text, row, col) in buttons:
    btn = Button(root, text=text, width=5, height=2, bg="#444", fg="white",
                 command=lambda t=text: button_click(t) if t != "=" else calculate())
    btn.grid(row=row, column=col, padx=5, pady=5)

# Scientific Functions Buttons
scientific_buttons = [
    ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('log', 5, 3),
    ('sqrt', 6, 0), ('^', 6, 1), ('C', 6, 2),
    ('(', 6, 3), (')', 6, 4)  # Parentheses added here
]

for text, row, col in scientific_buttons:
    btn = Button(root, text=text, width=5, height=2, bg="#666", fg="white",
                 command=lambda t=text: button_click(t) if t != "C" else clear_entry())
    btn.grid(row=row, column=col, padx=5, pady=5)

# History Label
history_label = Label(root, text="History: None", bg="#222", fg="lightgray", font=("Arial", 12))
history_label.grid(row=7, column=0, columnspan=5, pady=10)

# Run the application
root.mainloop()

