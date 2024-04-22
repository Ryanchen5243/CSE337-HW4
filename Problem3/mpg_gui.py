#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

class MyFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.pack()

        # Define string variables for text entry fields
        self.miles_driven = tk.StringVar()
        self.gallons_of_gas_used = tk.StringVar()
        self.miles_per_gallon = tk.StringVar()

        # Display the grid of components
        ttk.Label(self, text="Miles Driven:").grid(
            column=0, row=0, sticky=tk.E)
        ttk.Entry(self, width=30, textvariable=self.miles_driven).grid(
            column=1, row=0)
        ttk.Label(self, text="Gallons of Gas Used:").grid(
            column=0, row=1, sticky=tk.E)
        ttk.Entry(self, width=30, textvariable=self.gallons_of_gas_used).grid(
            column=1, row=1)
        ttk.Label(self, text="Miles Per Gallon:").grid(
            column=0, row=2, sticky=tk.E)
        ttk.Entry(self, width=30, textvariable=self.miles_per_gallon, state="readonly").grid(
            column=1, row=2)
        ttk.Button(self,text="Calculate",command=self.calculate_mpg).grid(row=3,column=1,sticky=tk.E)

        # Add padding to all components
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)
    def calculate_mpg(self):
        try:
            miles_driven = float(self.miles_driven.get())
            gallons_used = float(self.gallons_of_gas_used.get())
            result = round(miles_driven / gallons_used,2)
            self.miles_per_gallon.set(str(result))
        except:
            self.miles_per_gallon.set("Invalid Input")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Miles Per Gallon Calculator")
    MyFrame(root)
    root.mainloop()
