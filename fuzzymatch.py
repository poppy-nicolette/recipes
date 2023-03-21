from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
from cleanup import cleanup


# function to pass in cleaned_list
def fuzzymatch(x):
    # import food items into a list to extract only food items
    df2 = pd.read_csv("food_list.csv")

    # convert to list...why? just following the example so far...
    list1 = x
    list2 = df2["Food Type"].tolist()

    # cleanup list2 which is our imported food_thesaurus
    list2 = cleanup(list2)

    # empty lists for storing the matches later
    mat1 = []
    mat2 = []

    # iterating through list1 to extract
    # it's closest match from list2
    for i in list1:
        mat1.append(process.extract(i, list2, limit=2))

    df1 = pd.DataFrame(list1)
    df1.rename(columns={0: 'item'}, inplace=True)
    df1['matches'] = mat1

    # iterating through the closest
    # matches to filter out the
    # maximum closest match
    # taking the threshold as 80
    threshold = 90

    for j in df1['matches']:
        p = []
        for k in j:
            if k[1] >= threshold:
                p.append(k[0])

        mat2.append(",".join(p))

    # storing the resultant matches
    # back to dframe1
    df1['matches'] = mat2

    df1 = df1.replace("", "NaN")
    df3 = df1[df1.filter(['matches']).matches.str.contains('NaN') == False]
    df3.reset_index(drop=True, inplace=True)

    # add system date
    date = pd.Timestamp.today().strftime('%Y-%m-%d')
    df3 = df3.assign(date=date)
    return df3
