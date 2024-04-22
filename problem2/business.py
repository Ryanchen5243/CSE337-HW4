import tkinter as tk
from tkinter import ttk
import locale

class Investment():
    def __init__(self):
        self.monthlyInvestment = 0
        self.yearlyInterestRate = 0
        self.years = 0

    def calculateFutureValue(self):
        monthlyInterestRate = self.yearlyInterestRate / 12 / 100
        months = self.years * 12

        futureValue = 0
        for i in range(months):
            futureValue += self.monthlyInvestment
            monthlyInterestAmount = futureValue * monthlyInterestRate
            futureValue += monthlyInterestAmount

        return futureValue

class FutureValueFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent
        self.investment = Investment()
        result = locale.setlocale(locale.LC_ALL, '')
        if result == 'C':
            locale.setlocale(locale.LC_ALL, 'en_US')        

        # Define string variables for text entry fields
        self.monthlyInvestment = tk.StringVar()
        self.yearlyInterestRate = tk.StringVar()
        self.years = tk.StringVar()
        self.futureValue = tk.StringVar()

        self.initComponents()

    def initComponents(self):
        self.pack()

        # Display the grid of labels and text entry fields
        ttk.Label(self, text="Monthly Investment:").grid(
            column=0, row=0, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.monthlyInvestment).grid(
            column=1, row=0)

        ttk.Label(self, text="Yearly Interest Rate:").grid(
            column=0, row=1, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.yearlyInterestRate).grid(
            column=1, row=1)

        ttk.Label(self, text="Years:").grid(
            column=0, row=2, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.years).grid(
            column=1, row=2)

        ttk.Label(self, text="Future Value:").grid(
            column=0, row=3, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.futureValue,
                  state="readonly").grid(
            column=1, row=3)

        self.makeButtons()

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    def makeButtons(self):
        # Create a frame to store the two buttons
        buttonFrame = ttk.Frame(self)

        # Add the button frame to the bottom row of the main grid
        buttonFrame.grid(column=0, row=4, columnspan=2, sticky=tk.E)

        # Add two buttons to the button frame
        ttk.Button(buttonFrame, text="Calculate", command=self.calculate) \
            .grid(column=1, row=0, padx=5)
        ttk.Button(buttonFrame, text="Clear", command=self.clearFields) \
            .grid(column=0, row=0)

    def calculate(self):
        self.investment.monthlyInvestment = float(
            self.monthlyInvestment.get())
        self.investment.yearlyInterestRate = float(
            self.yearlyInterestRate.get())
        self.investment.years = int(
            self.years.get())

        self.futureValue.set(locale.currency(
                self.investment.calculateFutureValue(), grouping=True))
    
    def clearFields(self):
        self.monthlyInvestment.set("")
        self.yearlyInterestRate.set("")
        self.years.set("")
        self.futureValue.set("")

def configureTwoFutureValueFrames(parent):
    # create left and right frames and store FutureValueFrames in each
    topFrame=tk.Frame(parent)
    topFrame.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
    botFrame=tk.Frame(parent)
    botFrame.pack(side=tk.BOTTOM,fill=tk.X,padx=5,pady=5)

    leftTopFrame=tk.Frame(topFrame)
    leftTopFrame.pack(side=tk.LEFT)
    rightTopFrame=tk.Frame(topFrame)
    rightTopFrame.pack(side=tk.RIGHT)
    FutureValueFrame(leftTopFrame)
    FutureValueFrame(rightTopFrame)

    exitButtonWidget = ttk.Button(botFrame,text="Exit",command=parent.destroy)
    exitButtonWidget.pack(side=tk.RIGHT)



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Future Value Calculator")
    configureTwoFutureValueFrames(root)
    root.mainloop()