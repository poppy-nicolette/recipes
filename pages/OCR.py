import pandas as pd
import streamlit as st
import pytesseract
# Import receipt_reader module to convert an image to a string
#receipt_reader has one function, ocr()
#nothing is passed to ocr() - it looks for any image file in the working dir

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\ tesseract'
print("Starting OCR...")

#import receipt_reader
from receipt_reader import ocr

# Call function
textlist = ocr().split('\n')
st.write("Finished reading receipt")

#clean up text of numbers, punctuation, and blank lines
from cleanup import cleanup

cleaned_list = cleanup(textlist)
#print(cleaned_list)
st.write("Finished cleaning receipt items")

#fuzzy matching - fuzzymatch returns a pandas dataframe
from fuzzymatch import fuzzymatch

df_matched = fuzzymatch(cleaned_list)
st.write("Finished identifying food items")

#concat temporary inventory df_matched with inventory
#concat will add items to inventory, whereas df_matched is overwritten each time
#future version - should save out inventory and read in so that it can be added to but not overwritten
inventory = pd.DataFrame(columns=['item', 'matches', 'date'])
inventory = pd.concat([inventory, df_matched])

st.write("These are the food items you purchased:")
inventory["matches"]