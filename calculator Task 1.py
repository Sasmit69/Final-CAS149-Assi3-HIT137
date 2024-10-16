#This is a calculator that uses tkinter and a advance calculator, it has all the function that calculator needs
#It has seprate buutton with seprate colour i.e. red denoting basic mode and yellow denoting sifi 
# All the calculation can be done without any error  
#this calculator lets you type from your krybord itself to peform a calculation
import tkinter as tk
import math

class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculator grp CAS149")
        self.root.configure(bg="#2E4053")  #  background for better look

        self.entry = tk.Entry(self.root, width=30, font=("Arial", 16), bd=5, relief=tk.GROOVE, justify="right")
        self.entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)  # columnspan adjusted

        # going from default to basic mode
        self.is_scientific_mode = False
        self.create_buttons()

        # Creating mode buttons at the bottom
        self.create_mode_buttons()

        self.root.mainloop()

    def create_mode_buttons(self):
        # creating Button for Basic Calculator
        basic_button = tk.Button(self.root, text="Basic Mode", font=("Arial", 14), bg="#FF5733", fg="white", height=2, width=15, command=self.set_basic_mode)
        basic_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # creating Button for Scientific Calculator
        sci_button = tk.Button(self.root, text="Scientific Mode", font=("Arial", 14), bg="#FFC300", fg="white", height=2, width=15, command=self.set_scientific_mode)
        sci_button.grid(row=8, column=3, columnspan=2, padx=10, pady=10)  # column adjusted

    def create_buttons(self):
        # Defining button configurations for both modes
        self.basic_buttons = {
            "7": (1, 0), "8": (1, 1), "9": (1, 2), "/": (1, 3),
            "4": (2, 0), "5": (2, 1), "6": (2, 2), "*": (2, 3),
            "1": (3, 0), "2": (3, 1), "3": (3, 2), "-": (3, 3),
            "0": (4, 0), ".": (4, 1), "=": (4, 2), "+": (4, 3),
            "C": (5, 0), "⌫": (5, 1), "AC": (5, 2)
        }

        self.scientific_buttons = { 
            "7": (1, 0), "8": (1, 1), "9": (1, 2), "/": (1, 3), "x²": (1, 4),
            "4": (2, 0), "5": (2, 1), "6": (2, 2), "*": (2, 3), "x³": (2, 4),
            "1": (3, 0), "2": (3, 1), "3": (3, 2), "-": (3, 3), "√": (3, 4),
            "0": (4, 0), ".": (4, 1), "=": (4, 2), "+": (4, 3), "log": (4, 4),
            "C": (5, 0), "⌫": (5, 1), "AC": (5, 2), "sin": (5, 3), "cos": (5, 4), 
            "tan": (6, 3), "π": (6, 4), "e": (7, 4)
        }

        # Creating basic buttons to have seprate option for sifi mode and basic mode
        self.create_basic_buttons()

    def create_basic_buttons(self):
        for button_text, grid_pos in self.basic_buttons.items():
            button = tk.Button(
                self.root, text=button_text, font=("Arial", 14),
                command=lambda text=button_text: self.handle_button_click(text),
                bg="#3498DB", fg="white", height=2, width=5, bd=2, relief=tk.RAISED
            )
            button.grid(row=grid_pos[0], column=grid_pos[1], padx=5, pady=5)

    def create_scientific_buttons(self):
        for button_text, grid_pos in self.scientific_buttons.items():
            button = tk.Button(
                self.root, text=button_text, font=("Arial", 14),
                command=lambda text=button_text: self.handle_button_click(text),
                bg="#3498DB", fg="white", height=2, width=5, bd=2, relief=tk.RAISED
            )
            button.grid(row=grid_pos[0], column=grid_pos[1], padx=5, pady=5)

    def handle_button_click(self, text):
        if text == "=":
            try:
                expression = self.entry.get()
                expression = expression.replace("^", "**")
                expression = expression.replace("√", "math.sqrt")

                # More handling of trigonometric functions
                expression = expression.replace("sin(", "math.sin(math.radians(")
                expression = expression.replace("cos(", "math.cos(math.radians(")
                expression = expression.replace("tan(", "math.tan(math.radians(")
                expression = expression.replace("log(", "math.log10(")

                # Ensure correct parentheses for functions
                open_paren_count = expression.count("(")
                close_paren_count = expression.count(")")
                if open_paren_count > close_paren_count:
                    expression += ")" * (open_paren_count - close_paren_count)

                result = eval(expression)
                self.entry.delete(0, tk.END)
                self.entry.insert(0, str(result))
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, "Error")
        elif text == "C":
            self.entry.delete(0, tk.END)
        elif text == "⌫":
            current_text = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current_text[:-1])
        elif text == "AC":
            self.entry.delete(0, tk.END)
        elif text == "π":
            self.entry.insert(tk.END, str(math.pi))
        elif text == "e":
            self.entry.insert(tk.END, str(math.e))
        elif text in ["sin", "cos", "tan", "log", "√"]:
            self.entry.insert(tk.END, text + "(")
        elif text == "x²":
            self.entry.insert(tk.END, "**2")
        elif text == "x³":
            self.entry.insert(tk.END, "**3")
        else:
            self.entry.insert(tk.END, text)

    def set_basic_mode(self):
        self.is_scientific_mode = False
        self.clear_scientific_buttons()
        self.create_basic_buttons()

    def set_scientific_mode(self):
        self.is_scientific_mode = True
        self.clear_basic_buttons()
        self.create_scientific_buttons()

    def clear_basic_buttons(self):
        for button_text in self.basic_buttons:
            for widget in self.root.grid_slaves():
                if widget.cget("text") == button_text:
                    widget.grid_forget()  # Remove basic buttons

    def clear_scientific_buttons(self):
        for button_text in self.scientific_buttons:
            for widget in self.root.grid_slaves():
                if widget.cget("text") == button_text:
                    widget.grid_forget()  # Remove scientific buttons

if __name__ == "__main__":
    calculator = Calculator()