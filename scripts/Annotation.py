import pandas as pd
from typing import List
import os

class Annotation:
    BASE_DIR = '../data/AL'
    text : List[str]
    filename : str
    def __init__(self, filename, text):
        self.text = text
        self.filename = filename
    def iterate_over_files(path : str):
        for document in os.listdir(path):
            yield document
    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame(data = {'SampleId' : [str(i+1) for i,_ in enumerate(self.text)],'Sample' : self.text})
    def process(self):
        for line in self.text:
            print(line)
            

class Document:
    BASE_DIR = '../data/texts'
    text : List[str]
    filename : str
    def __init__(self, filename, text):
        self.text = text
        self.filename = filename
    def iterate_over_files(path : str):
        for document in os.listdir(path):
            yield document
    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame(data = {'SampleId' : [str(i+1) for i,_ in enumerate(self.text)],'Sample' : self.text})

