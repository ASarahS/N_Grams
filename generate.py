
from pathlib import Path
import tkinter as tk
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from pandastable import Table, TableModel
from PIL import ImageTk, Image

import sys,os
import pm4py
import pandas as pd

from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.statistics.traces.log import case_statistics
from collections import Counter
from collections import defaultdict
import main as mainFile

def start():
    window = Tk()
    main = tk.Frame(window)

    window.title('Predictive Process Mining using N_Grams')

    window.geometry("729x499")

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    #Import event log data
    log = xes_importer.apply(str(sys.argv[1]))

    def getOptions(datas):
        data_list = []
        for data in datas:
            for value in data.split(","):
                data_list.append(value);
        options = set(data_list)
        return options;

    finalText = ""
    #Get event sequence details out of log
    total_variants = case_statistics.get_variant_statistics(log)
    variants_count = {i['variant']:i['count']for i in total_variants} #Which variant occurs how many times?
    variants_list = list(variants_count.keys()) #List of events in variants

    get_trace_lengths = [len(i['variant'].split(',')) for i in total_variants]
    max_trace_length = max(get_trace_lengths)

    from collections import Counter

    ngrams = [] #initialize list for ngrams (has 2-n grams with their count)

    for gram_length in range(2, max_trace_length):
      temp_gram = []
      grams = Counter()

      for variant in variants_list:
        trace_list = variant.split(',') #Getting trace list for n grams (from 2 to n)
        n_gram_trace_list = [trace_list[j:] for j in range(gram_length)]
        temp_gram.append(dict(Counter(list(zip(*(n_gram_trace_list)))))) #Count sequence (of length 2 to n) in each unique variant.

      for i, j in zip(temp_gram, variants_count.values()):
        for k in i.keys():
          i[k] = i[k] * j #Multiply sequence count with variant count (gives sequence count in variant)

      for i in temp_gram:
        for j in i.keys():
          grams[j] += i[j] #Get count of a sequence in whole log
      ngrams.append(dict(grams))

    events = getOptions(variants_list)

    def get_predictions(pattern, ngrams):
      pattern = tuple(pattern.split(','))
      probs = defaultdict(list) #Will contain probabilities of next states and gram number

      #Calculate probabilities for 1 gram
      #total occurences of 2 grams
      gram2 = {i:j for i,j in ngrams[0].items() if i[0]==pattern[-1]}
      total_occurences = sum(gram2.values())
      [probs[i[-1]].append(j/total_occurences) for i,j in gram2.items() if i[0]==pattern[-1]]
      #get probability of next activity
      probs['grams'].append('1-gram')

      #Calculate probabilities for 2 to n gram
      for i in range(1, len(pattern)):
        probs['grams'].append(str(i+1)+'-gram') #
        gram_n = {j:k for j,k in ngrams[i].items() if j[0:i+1]==pattern[-i-1:]}
        total_occurences = sum(gram_n.values())
        for j,k in gram_n.items():
          if j[0:i+1]==pattern[-i-1:]:
            probs[j[-1]].append(k/total_occurences)

      df = pd.DataFrame.from_dict(probs, orient='index').transpose().fillna(0)
      return df


    def generate(text):
        finalText = text.get()[:-1];
        window = TestApp(tk.Frame,finalText)

    class TestApp(tk.Frame):
        """Basic test frame for the table"""
        def __init__(self, parent,finalText):
            self.parent = parent
            tk.Frame.__init__(self)
            self.main = self.master
            f = tk.Frame(self.main)
            f.grid(column=1,row=7,columnspan=4)
            df = get_predictions(finalText, ngrams)
            self.table = pt = Table(f, dataframe=df)
            pt.show()
            return

    # Entry Box
    text = Entry(window, bg='White',width=60)
    text.grid(columnspan=3,column=1,row=4,padx=10, pady=10,ipady=10)

    browse_text = tk.StringVar()
    browse_btn = tk.Button(window, textvariable = browse_text,command = lambda: generate(text), font = "Raleway", bg = "#52b69a", fg="white", height = 1, width = 8)
    browse_text.set("Generate")
    browse_btn.grid(column = 3, row=4,columnspan=2);

    clear_text = tk.StringVar()
    clear_btn = tk.Button(window, textvariable = clear_text,command = lambda: clearText(), font = "Raleway", bg = "white", fg="black", height = 1, width = 6)
    clear_text.set("Clear")
    clear_btn.grid(column = 4, row=4,columnspan=2);
    # create buttons
    button_dict = {}
    col=1

    def text_updation(language):
        text.insert('end', str(language)+",")

    def goBack():
        window.destroy()
        mainFile.start()

    def clearText():
        text.delete(0, "end")
        generate(text)

    button3 = Button(window, text = "< Back ",command = lambda:goBack(), font = "Raleway", fg="#0077b6", height = 1, width = 8,borderwidth=0)
    button3.grid(column=0, row=0,columnspan=2,sticky = 'nw',pady=3)

    for lang in events:
        # pass each button's text to a function
        def action(x = lang):
            return text_updation(x)

        # create the buttons
        button_dict[lang] = Button(window, text = lang,command = action,font = "Raleway", bg = "#0077b6", fg="white", height = 2, width = 15)
        button_dict[lang].grid(column=col, row=3,padx=10,pady=10)
        col+=1

    window.mainloop()
