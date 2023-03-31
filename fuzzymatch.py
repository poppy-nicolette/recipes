from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
from cleanup import cleanup

#function to pass in cleaned_list
def fuzzymatch(x):

    #import food items into a list to extract only food items
    df2 = pd.read_csv("food_list.csv")
    
    #import nonfood_item_list.csv
    df_nonfood = pd.read_csv("nonfood_list.csv")
    list3 = df_nonfood["nonFoodItems"].tolist()
    
    # convert to list...why? just following the example so far...
    list1 = x
    list2 = df2["Food Type"].tolist()

    #cleanup list2 which is our imported food_thesaurus
    list2 = cleanup(list2)

    # empty lists for storing the matches later
    mat1 = []
    mat2 = []


    # fuzzymatch from list2
    mat1 = []
    for i in list1:
        mat1.append(process.extract(i, list2, limit=1))
    
    df1 = pd.DataFrame(list1)
    df1.rename(columns = {0:'item'}, inplace = True)
    df1['matches'] = mat1
    
    #fuzzymatch for nonfoods
    mat3 = []
    for i in list1:
        mat3.append(process.extract(i, list3, limit=1))
    df1['nonfoods'] = mat3

    #keep only items above threshold in matches
    #threshold can be adjusted to values between 0 and 100
    threshold = 90

    for j in df1['matches']:
        p = []
        for k in j:
            if k[1] >= threshold:
                p.append(k[0])       
        mat2.append(",".join(p))

    df1['matches'] = mat2
    
    #keep only nonfood items above threshold
    #filter for nonfood items
    threshold2 = 90
    mat3=[]
    for j in df1['nonfoods']:
        p = []
        for k in j:
            if k[1] >= threshold2:
                p.append(k[0])
            else:
                pass
        mat3.append(",".join(p))

    df1['nonfoods'] = mat3
    #remove empty matches
    df1 = df1.replace("", "NaN")
    df3 = df1[df1.filter(['matches']).matches.str.contains('NaN') == False]
    
    #remove nonfood_list items from df3
    df3 = df3.loc[df3["nonfoods"] == "NaN"]
    df3 = df3.drop('nonfoods', axis=1)
    
    #reset index just to make it tidy
    df3.reset_index(drop=True, inplace=True)

    #add system date
    date = pd.Timestamp.today().strftime('%Y-%m-%d')
    df3 = df3.assign(date=date)
    return df3
