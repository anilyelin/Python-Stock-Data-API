# author: anil yelin
# version 1.0
import tkinter as tk 
import json
import urllib.request
from datetime import datetime
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
import datetime
from tkinter import messagebox
from matplotlib import pyplot as plt
import csv
import sqlite3
import sys

NASDAQ_CODES = ['CMCSA','MSFT','HBAN','INTC','CSCO','NVAX','AAPL','SIRI',
                'QCOM','EBAY','AMAT','ATVI','MRVL','NVDA','BIOS','PLUG',
                'MHLD','SBUX','ADBE','GILD','IMGN','CELG','FITB','MYL',
                'FLEX','NFLX','PAAS','MNKD','GPOR','AMZN','BBBY','AMGN',
                'NUAN','SYMC','NTAP','LRCX','JBLU','PCBT','MXIM','FOLD',
                'FISV','LBTYK']

company_dict = {"CMCSA":"Comcast","MSFT":"Microsoft","HBAN":"Hungtington Banc.",
                "INTC":"Intel Corp.","CSCO":"Cisco","NVAX":"Novavax",
                "AAPL":"Apple Inc.","SIRI":"Sirius","QCOM":"Qualcomm","EBAY":"Ebay",
                "AMAT":"Applied Mat","ATVI":"Activision Blizzard","MRVL":"Marvel",
                "NVDA":"Nvidia","BIOS":"BioScrip Inc","PLUG":"Plug Power","MHLD":"Maiden Holdings",
                "SBUX":"Starbucks","ADBE":"Adobe","GILD":"Gilead Sciences","IMGN":"ImmunoGen",
                "CELG":"Celgene","FITB":"Fifth Third Bancorp","MYL":"Mylan","FLEX":"Flex","NFLX":"Netflix",
                "PAAS":"Pan American Silver","MNKD":"MannKind Corp","GPOR":"Gulfport Energy Corp","AMZN":"Amazon",
                "BBBY":"Bed Bath & Beyond","AMGN":"Amgen","NUAN":"Nuance Communications",
                "SYMC":"Symantec","NTAP":"Net App","LRCX":"Lam Research Corp","JBLU":"Jet Blue Airways",
                "PCBT":"P.C.B. Technologies","MXIM":"Maxim Integrated","FOLD":"Amicus Therapeutics","FISV":"Fiserv","LBTYK":"Liberty Glo."}

recent_dates = []
for i in range(20):
    #retrieving the past 20 days
    date = datetime.date.fromordinal(datetime.date.today().toordinal()-i).strftime("%F")
    recent_dates.append(date)

# IMPORTANT: to get this program working you have to get an API key at
# https://www.alphavantage.co/support/#api-key
# it is free
# WARNING: if the API key remains as an empty string to program will not work and will terminate itself
API_KEY = ''

class App:
    def __init__(self,main):
        """initializing the GUI of our stock app"""
        self.main=main
        self.banner = tk.Label(main,bg='black',text="Stock API App v1.0",font=('Futura',16),fg='white')
        self.banner.grid(column=0,row=0,columnspan=3,sticky=('N','S','E','W'),padx=10,pady=10)
        self.first = tk.StringVar()
        self.first_label = tk.Label(main,textvariable=self.first).grid(row=1,column=0)
        str_data = "Stock info for "
        self.first.set(str_data)
        self.dateLabel = tk.Label(main,text="Actual date").grid(row=3,column=0)
        self.dateLabel_source = tk.StringVar()
        self.actualDate_label = tk.Label(main,textvariable=self.dateLabel_source,foreground='blue').grid(row=3,column=1)
        self.dateLabel_source.set(datetime.date.fromordinal(datetime.date.today().toordinal()).strftime("%F"))
        self.text_label_changes = tk.Label(main,text="Changes").grid(row=3,column=2)
        ####
        self.company_name_source = tk.StringVar()
        self.company_name_label = tk.Label(main,textvariable=self.company_name_source,fg='blue').grid(row=1,column=1)
        self.company_name_source.set('')
        #####
        self.choose_date_label = tk.Label(main,text="Choose a date").grid(row=2,column=0)
        self.date_combo = ttk.Combobox(main,values=recent_dates,width=10)
        self.date_combo.current(0)
        self.date_combo.grid(row=2,column=1)
        #####
        self.line = ttk.Separator(main, orient='horizontal').grid(column=0, row=4,columnspan=2, sticky='we')
        self.day_open = tk.Label(main,text="Day open").grid(row=4,column=0)
        self.dayOpen_source = tk.StringVar()
        self.dayOpen_label = tk.Label(main,textvariable=self.dayOpen_source).grid(row=4,column=1)
        self.dayOpen_source.set('')
        self.day_open_percentage_source = tk.StringVar()
        self.day_open_percentage_label = tk.Label(main,textvariable=self.day_open_percentage_source)
        self.day_open_percentage_label.grid(row=4,column=2)
        self.day_open_percentage_source.set('')
        #####
        self.line1 = ttk.Separator(main, orient='horizontal').grid(column=0, row=5,columnspan=2, sticky='we')
        self.day_high = tk.Label(main,text="Day high").grid(row=5,column=0)
        self.dayHigh_source = tk.StringVar()
        self.dayHigh_label = tk.Label(main,textvariable=self.dayHigh_source).grid(row=5,column=1)
        self.dayHigh_source.set('')
        self.day_high_percentage_source = tk.StringVar()
        self.day_high_percentage_label = tk.Label(main,textvariable=self.day_high_percentage_source)
        self.day_high_percentage_label.grid(row=5,column=2)
        self.day_high_percentage_source.set('')
        #####
        self.line2 = ttk.Separator(main, orient='horizontal').grid(column=0, row=6,columnspan=2, sticky='we')
        self.dayLow = tk.Label(main,text="Day low").grid(row=6,column=0)
        self.dayLow_source= tk.StringVar()
        self.dayLow_label = tk.Label(main,textvariable=self.dayLow_source).grid(row=6,column=1)
        self.dayLow_source.set('')
        self.day_low_percentage_source = tk.StringVar()
        self.day_low_percentage_label = tk.Label(main,textvariable=self.day_low_percentage_source)
        self.day_low_percentage_label.grid(row=6,column=2)
        self.day_low_percentage_source.set('')
        #####
        self.line3 = ttk.Separator(main, orient='horizontal').grid(column=0, row=7,columnspan=2, sticky='we')   
        self.dayClose = tk.Label(main,text="Day close").grid(row=7,column=0)
        self.dayClose_source = tk.StringVar()
        self.dayClose_label = tk.Label(main,textvariable=self.dayClose_source)
        self.dayClose_label.grid(row=7,column=1)
        self.dayClose_source.set('')
        self.day_close_percentage_source = tk.StringVar()
        self.day_close_percentage_label = tk.Label(main,textvariable=self.day_close_percentage_source)
        self.day_close_percentage_label.grid(row=7,column=2)
        self.day_close_percentage_source.set('')
        #####
        self.line4 = ttk.Separator(main, orient='horizontal').grid(column=0, row=8,columnspan=2, sticky='we')
        self.volume = tk.Label(main,text="Volume").grid(row=8,column=0)
        self.volumeSource = tk.StringVar()
        self.volume_label = tk.Label(main,textvariable=self.volumeSource,foreground='purple').grid(row=8,column=1)
        self.volumeSource.set('')
        #####
        self.combo_text = tk.Label(main,text="Choose a NASDAQ Code")
        self.combo_text.grid(row=9,column=0)
        self.combobox = ttk.Combobox(main,values=NASDAQ_CODES,width=10)
        self.combobox.current(0)
        self.combobox.grid(row=9,column=1)
        self.space = tk.Label(main).grid(column=0,row=10)
        self.user_text = tk.Label(main,text="Show history of company").grid(row=11,column=0)
        self.user_text_entry = tk.Entry(main,width=10)
        self.user_text_entry.grid(row=11,column=1)
        self.submit_button = tk.Button(main,text="Submit",command=self.showDB).grid(row=11,column=2)

        self.freeLabel = tk.Label(main,text='').grid(row=13,column=0)
        self.showButton = tk.Button(main,text="show data",command=self.show_data,width=10).grid(row=15,column=0,sticky='w')
        self.GraphButton = tk.Button(main,text="show graph",command=self.openGraph,width=10).grid(row=15,column=1,sticky='w')
        self.CloseButton = tk.Button(main,text="close",command=self.close,foreground='red',width=10).grid(row=15,column=2,sticky='w')

    def showDB(self):
        """writing all the stock data into sqlite3 file and showing 
           them in a pop up window"""
        def closePopUp():
            new.destroy()

        companyName = self.user_text_entry.get()
        if companyName not in NASDAQ_CODES:
            messagebox.showinfo("Info","This company does not exist")
            return None
        else:
            pass
        new = tk.Tk()
        new.geometry("380x200")
        listbox = tk.Listbox(new,bg='black',fg='white',width=42)
        listbox.pack()
        quitButton = tk.Button(new,text='Close',command=closePopUp).pack()

        self.user_text_entry.delete(0,'end')
        data_source = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+companyName+'&apikey='+API_KEY
        response = urllib.request.urlopen(data_source)
        data = json.load(response)
        new.title(companyName+" history")
        day_close = float(data['Time Series (Daily)'][self.date_combo.get()]['4. close'])
        # creating for each NASDAQ company a sepate sqlite3 file 
        path = companyName+'.sqlite'
        self.dataBase_object = Database(path)
        try:
            self.dataBase_object.create_table()
        except:
            self.dataBase_object.execute("INSERT INTO testing values (?,?,?)",(companyName,day_close,self.date_combo.get()))
        self.dataBase_object.commit()
        rows = self.dataBase_object.cur.execute("SELECT * FROM testing;")
        for row in rows:
                listbox.insert('end',row)
        self.dataBase_object.close()

    def openGraph(self):
        """will create a popup windows with the graph of the day close values 
            of the selected NASDAQ company using matplotlib"""
        user_input = self.combobox.get()
        data_source = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+user_input+'&apikey='+API_KEY
        response = urllib.request.urlopen(data_source)
        data = json.load(response)
        
        main = tk.Tk()
        main.geometry('900x600')
        title = self.combobox.get()
        main.title(title+' graph')
        fig = Figure(figsize = (9, 6),dpi=80, facecolor = "black")
        plt.style.use('dark_background')
        axis = fig.add_subplot(111)

        close=[]
        new_dates=[]
        for date in recent_dates:
            try:
                day_close = data['Time Series (Daily)'][date]['4. close']
                close.append(day_close)
                new_dates.append(date)
            except:
                pass
    
        axis.tick_params(axis='x', rotation=45)
        axis.plot(new_dates,close, label='Test')
  
        canvas = FigureCanvasTkAgg(fig, master = main)
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
    
    def close(self):
        """function to quit the app"""
        self.main.destroy()

    def show_data(self):
        """this function will get the stock
        data for a specific stock data and 
        calculates the difference between two days"""
        user_input = self.combobox.get()
        self.first.set("Stock info for "+user_input)
        # if there is no API Key provided the program terminate itself
        if API_KEY == '':
            sys.exit(0)
        else:
            pass
        data_source = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+user_input+'&apikey='+API_KEY
        response = urllib.request.urlopen(data_source)
        data = json.load(response)
        dateCombo = self.date_combo.get()
        try:
            day_open = data['Time Series (Daily)'][dateCombo]['1. open']
            day_high = data['Time Series (Daily)'][dateCombo]['2. high']
            day_low  = data['Time Series (Daily)'][dateCombo]['3. low']
            day_close = data['Time Series (Daily)'][dateCombo]['4. close']
            volume    = data['Time Series (Daily)'][dateCombo]['5. volume']
        except:
            messagebox.showinfo('Info','No stock data available. Please choose another date')
        self.dayOpen_source.set(day_open)
        self.dayHigh_source.set(day_high)
        self.dayClose_source.set(day_close)
        self.dayLow_source.set(day_low)
        self.volumeSource.set(volume)
        value = company_dict[user_input]
        self.company_name_source.set(value)
    
        actual_date = self.date_combo.get()
        for i in range(len(recent_dates)):
            if actual_date == recent_dates[i]:
                yesterday = recent_dates[i+1]
        try:
            day_low = float(data['Time Series (Daily)'][actual_date]['3. low'])
            day_low_before = float(data['Time Series (Daily)'][yesterday]['3. low'])
            day_close = float(data['Time Series (Daily)'][actual_date]['4. close'])
            day_close_before = float(data['Time Series (Daily)'][yesterday]['4. close'])
            day_high = float(data['Time Series (Daily)'][actual_date]['2. high'])
            day_high_before = float(data['Time Series (Daily)'][yesterday]['2. high'])
            day_open = float(data['Time Series (Daily)'][actual_date]['1. open'])
            day_open_before = float(data['Time Series (Daily)'][yesterday]['1. open'])
            percentage = round(1-(day_close_before/day_close),4)
            percentage_low = round(1-(day_low_before/day_low),4)
            percentage_high = round(1-(day_high_before/day_high),4)
            percentage_open = round(1-(day_open_before/day_open),4)

            if percentage > 0:
                self.day_close_percentage_label.configure(fg='green')
                self.day_close_percentage_source.set('+'+str(percentage)+'%')
            else:
                self.day_close_percentage_label.configure(fg='red')
                self.day_close_percentage_source.set(str(percentage)+'%')

            if percentage_low > 0:
                self.day_low_percentage_label.configure(fg='green')
                self.day_low_percentage_source.set('+'+str(percentage_low)+'%')
            else:
                self.day_low_percentage_label.configure(fg='red')
                self.day_low_percentage_source.set(str(percentage_low)+'%')

            if percentage_high > 0:
                self.day_high_percentage_label.configure(fg='green')
                self.day_high_percentage_source.set('+'+str(percentage_high)+'%')
            else:
                self.day_high_percentage_label.configure(fg='red')
                self.day_high_percentage_source.set(str(percentage_high)+'%')

            if percentage_open > 0:
                self.day_open_percentage_label.configure(fg='green')
                self.day_open_percentage_source.set('+'+str(percentage_open)+'%')
            else:
                self.day_open_percentage_label.configure(fg='red')
                self.day_open_percentage_source.set(str(percentage_open)+'%')

        except:
            messagebox.showinfo('Info','No stock info for today available')
            pass

class Database(object):
    """simple sqlite3 wrapper to do basic db operations"""
    def __init__(self,db_location):
        if db_location is not None:
            self.connection = sqlite3.connect(db_location)
        else:
            self.connection = sqlite3.connect(self.db_location)
        self.cur = self.connection.cursor()
    def execute(self,d1,d2):
        self.cur.execute(d1,d2)
    def create_table(self):
        self.cur.execute('''CREATE TABLE testing(comp text, day_close real,stock_date date)''')
    def getAll(self):
        self.cur.fetchall()
    def close(self):
        self.connection.close()
    def commit(self):
        self.connection.commit()

def main():
    root = tk.Tk()
    my_gui = App(root)
    root.geometry("380x390")
    root.title("stock api v1.0")
    root.mainloop()

if __name__=="__main__":
    main()