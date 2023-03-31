import os 
os.system('sudo pip install scikit-learn')
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd
import streamlit as st
import pytesseract
from receipt_reader import ocr
from cleanup import cleanup

from fuzzymatch import fuzzymatch

import nltk
import string
from pages.OCR import inventory

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

st.title("Welcome to the Recipe Recommendation System")
st.write("Starting OCR...")

#import receipt_reader


# Call function
textlist = ocr().split('\n')
st.write("Finished reading receipt")

#clean up text of numbers, punctuation, and blank lines


cleaned_list = cleanup(textlist)
#print(cleaned_list)
st.write("Finished cleaning receipt items")



#fuzzy matching - fuzzymatch returns a pandas dataframe


df_matched = fuzzymatch(cleaned_list)
st.write("Finished identifying food items")

#concat temporary inventory df_matched with inventory
#concat will add items to inventory, whereas df_matched is overwritten each time
#future version - should save out inventory and read in so that it can be added to but not overwritten


inventory = pd.DataFrame(columns=['item', 'matches', 'date'])
inventory = pd.concat([inventory, df_matched])

st.write("These are the food items you purchased:")

inventory["item"]
recipe_list = inventory["item"].values.tolist()





#reads the csv file from the system
data = pd.read_csv("recipe.csv")

#performs data cleaning by checking it if it has null values
data.isnull().sum()
data.dropna(inplace=True)


#checks for duplicate values and removes
recommendation=data
recommendation.duplicated().sum()
recommendation.drop_duplicates(inplace=True)
#resets the index after dropping duplicats and null values if any
recommendation.reset_index(drop=True,inplace=True)

#reassign the dataset to a new variable
recNew=recommendation

def convert_to_list(data):
    a = data.replace("-","").replace("[","").replace("]","")
#     a = ''.join([i for i in a if not i.isdigit()])
    a = a.translate(str.maketrans('', '', string.punctuation))
    return a

recNew["ingredients"] = recNew["ingredients"].apply(lambda x: convert_to_list(x))

recNew = recNew[~recNew.duplicated("name")]
recNew.reset_index(drop=True,inplace=True)

vectorizer = TfidfVectorizer()
ingredient_tfidf = vectorizer.fit_transform(recNew["ingredients"])
ingredient_consin_sim = cosine_similarity(ingredient_tfidf, ingredient_tfidf)

# method for our recipe recommendation system
data_indices = pd.Series(recNew.index, index=recNew['name'])


def recipe_recommendation(data, sim):
    re_li = []
    # df = pd.DataFrame([])
    ind = data_indices[data]
    #     ind = rec[rec["name"]==data].index[0]
    sim_score = list(enumerate(sim[ind]))
    sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)
    sim_score = sim_score[0:5]
    rec_indices = [i[0] for i in sim_score]
    max_sim_score = max(sim_score)

    for i in rec_indices:
        re_li.append(recNew.iloc[i]["name"])

    return re_li


# prints the recommended meals based on ingredient and also prints the number of steps if a user chooses a particular meal.
my_count = 1
my_meal = []


def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1


# Driver code
recipe_list_str=listToString(recipe_list)


ingred = recNew['ingredients'][3]
steps = recNew['steps'][3]
meals_rec = recipe_recommendation(recNew["name"][3], ingredient_consin_sim)
np.array(steps).tolist()
 #displayed when the button is clicked
#st.write(recipe_list)

def makeMeal():
    st.write("Meals recommendation for the above ingredients include:")
    my_count = 1
    for j in meals_rec:
        st.write(my_count, ":", j)
        my_count = my_count + 1
    #st.write("Select a particular number you wish to prepare", "")
    number = st.text_input("Select a particular number you wish to prepare")
    if number:
        my_choice = int(number)

        if my_choice >= 1:
            def switch(n):
                count = 1
                # prints the required number of steps
                if n == 1 & n <= my_count:
                    first_item_steps = recNew.loc[recNew['name'] == meals_rec[n - 1], 'steps'].item()
                    a = first_item_steps.split(",")
                    st.write("The steps to prepare the meals for item ", n, "include:")
                    for i in a:
                        st.write("Step ", count, ":", i)
                        count = count + 1

                elif n == 2:
                    second_item_steps = recNew.loc[recNew['name'] == meals_rec[n - 1], 'steps'].item()
                    b = second_item_steps.split(",")
                    st.write("The steps to prepare the meals for item ", n, "include:")
                    for i in b:
                        st.write("Step ", count, ":", i)
                        count = count + 1
                elif n == 3 & n <= my_count:
                    third_item_steps = recNew.loc[recNew['name'] == meals_rec[n - 1], 'steps'].item()
                    c = third_item_steps.split(",")
                    st.write("The steps to prepare the meals for item ", n, "include:")
                    for i in c:
                        st.write("Step ", count, ":", i)
                        count = count + 1
                elif n == 4 & n <= my_count:
                    fourth_item_steps = recNew.loc[recNew['name'] == meals_rec[n - 1], 'steps'].item()
                    d = fourth_item_steps.split(",")
                    st.write("The steps to prepare the meals for item ", n, "include:")
                    for i in d:
                        st.write("Step ", count, ":", i)
                        count = count + 1
                elif n == 5 & n <= my_count:
                    fifth_item_steps = recNew.loc[recNew['name'] == meals_rec[n - 1], 'steps'].item()
                    e = fifth_item_steps.split(",")
                    st.write("The steps to prepare the meals for item ", n, "include:")
                    for i in e:
                        st.write("Step ", count, ":", i)
                        count = count + 1

            st.write(switch(my_choice))
            # User enters invalid input
        else:
            st.write("wrong input detected or input is out or range. Please try again")
    else:
        st.write("Please enter input")
#adding a button

makeMeal()




