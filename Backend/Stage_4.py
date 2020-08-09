import json
import math


# In[41]:


file = open("./stage_3.json", "r")
data = json.load(file)


# In[32]:


detail_stats = {}
rev_summ_stats = {}


# In[33]:


def calculate_trendiness(rating_div, oldest_rev, newest_rev):
    if len(rating_div) == 0:
        return None
    
    # Assuming weightage scale [-2, -1, 0, 0.5, 1]
    score = rating_div['5'] * 1 + rating_div['4']*0.5 + rating_div['3']*0.1
    score += rating_div['2'] * (-1) + rating_div['1']*-2
     
    if oldest_rev is None:
        # Since, generally the newest product have few ratings
        time_diff = 5
    else :
        # time_diff is the number of days since introduction of the product
        time_diff = (newest_rev - oldest_rev)/86400
    
    # More rating in less time means more trendy
    score /= time_diff
    
    return score    


# In[91]:


def calculate_score(data) :
    modified_json = []
    for item in data:
        # Copy everything except oldest_rev, newest_rev, 
        # rating_div
        item_new = {}

        item_new["id"] = item["id"]
        item_new["title"] = item["title"]
        item_new["image"] = item["image"]
        item_new["rev_summ"] = item["rev_summ"]
        item_new["detail"] = item["detail"]

        rating_div = item["rating_div"]
        oldest_rev = item["oldest_rev"]
        newest_rev = item["newest_rev"]

        score = calculate_trendiness(rating_div, oldest_rev, newest_rev)
        if score is None :
            continue
        item_new["score"] = score
        modified_json.append(item_new)
    
    return modified_json


# In[92]:


def func(elem) :
    return elem[1]

def most_used_elements(data) :
    most_used_elems = {}
    for item in data:
        for element in item["detail"]:
            if element not in most_used_elems :
                most_used_elems[element] = {}
            specifics = item["detail"][element]
            for specific in specifics:
                if specific not in most_used_elems[element]:
                    most_used_elems[element][specific] = 0
                most_used_elems[element][specific] += 1
    inference = {}
    for element in most_used_elems:
        array = sorted(most_used_elems[element].items(), reverse = True, key = func)
        inference[element] = []
        for i in range(min(len(array), 3)):
            inference[element].append(array[i])
    return inference
    


# In[93]:


def most_concern(data) :
    most_talked = {}
    for item in data:
        for rev in item["rev_summ"] :
            if rev not in most_talked:
                most_talked[rev] = 0
            most_talked[rev] += 1
    array = sorted(most_talked.items(), reverse=True, key = func)
    
    inference = []
    
    for i in range(min(len(array), 7)) :
        inference.append(array[i])
    
    return inference


# In[94]:


def sort_data(item):
    return item['score']


# In[95]:


# Calculate score of each item
modified_data = calculate_score(data)

# Sort data on the basis of score
modified_data.sort(key=sort_data, reverse=True)

# Create a new json
stage_4_json = {}

stage_4_json["items"] = modified_data
stage_4_json["most_used_elements"] = most_used_elements(modified_data)
stage_4_json["most_concern"] = most_concern(modified_data)

file = open("./stage_4.json", "w")
json.dump(stage_4_json, file, indent=4)
file.close()


# In[ ]:




