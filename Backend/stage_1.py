import json
import spacy
import re
from datetime import datetime
import time

nlp = spacy.load("en_core_web_lg")

file = open("stage_0.json", "r")
data = json.load(file)

# Replace the synonyms of shirt with shirt
# Sanitize input from "..." kind of symbols

pattern_l = re.compile("(top)|(t-?\s?shirt)|(tee)|(polo)")
pattern_u = re.compile("(Top)|(T-?\s?shirt)|(Tee)|(Polo)")
pattern_stop = re.compile("\.\.+")

def text_sanitizer(text):
    text = pattern_l.sub("shirt", text)
    text = pattern_u.sub("Shirt", text)
    text = pattern_stop.sub(".", text)
    return text

# To get the negation of an emotion PART
def find_neg_in_children(children):
    for child in children:
        if child.dep_ == "neg" :
            return child
        elif child.dep_ != "conj":
            # Often it happens PART <- ADV (not conjugated) <- ADJ,
            # handle these cases
            neg = find_neg_in_children(child.lefts)
            if neg is not None:
                return neg

# To find all adjectives in the child (ADJ)+

def find_adj_in_children(children) :
    # Adjs under current verb
    adjs = []

    for child in children :
        if child.pos_ == "ADJ" :
            # Check for negation
            neg = find_neg_in_children(child.lefts)

            # No neg child? Recheck!
            if neg is None and child.head.pos_ == "AUX" and child.head:
                neg = find_neg_in_children(child.head.rights)
            
            adjs.append((neg, child))
    
    # Now recurse again to find associated adjectives
    more_adjs = []

    for adj in adjs:
        more_adjs += find_adj_in_children(adj[1].children)
    
    return adjs + more_adjs

# form the adjectives from the core and the part
def form_adj_texts(adjs) :
    adj_texts = []

    for adj in adjs :
        adj_text = ""
        if adj[0] is not None :
            adj_text += adj[0].text + " "
        adj_text += adj[1].text
        adj_texts.append(adj_text)
    
    return adj_texts

# find the nearest Noun in the token children NOUN
def find_noun_in_children(children) :
    for child in children :
        if child.pos_ == "NOUN" or child.pos_ == "PROPN":
            return child

# find conjugate nouns in the children (NOUN)+ ->
def find_conj_noun_in_children(children) :
    nouns = []
    for child in children :
        if child.pos_ == "NOUN" and child.dep_ == "conj" :
            nouns.append(child)
    
    more_nouns = []
    for noun in nouns :
        more_nouns += find_conj_noun_in_children(noun.rights)
    
    return nouns + more_nouns

# To form compound nouns, get the compound nouns (NOUN)+ <-
def find_comp_noun_in_head(head) :
    nouns = []
    while head.pos_ == "NOUN" or head.pos_ == "PROPN" :
        nouns.append(head)
        if head.head == head:
            break
        head = head.head
        
    return nouns

# Find adverbs in the children ADV
def find_adv_in_children(children) :
    for child in children :
        if child.pos_ == "ADV" :
            return child

# Find pronouns in the children PRON
def find_pron_in_children(children) :
    for child in children :
        if child.pos_ == "PRON" :
            return child

# Find determiners in the children DET
def find_det_in_children(children) :
    for child in children :
        if child.pos_ == "DET" :
            return child

# Find a phrase matching the rule PRON <- VERB -> ADV
def rule_1(verb) :
    if verb.pos_ == "VERB":
        pron = find_pron_in_children(verb.lefts)
        if pron is None:
            return None

        if pron.text.lower().rstrip() != "it" :
            return None

        adv = find_adv_in_children(verb.rights)
        if adv is None :
            return None
        part = find_neg_in_children(adv.lefts)
        text = ""
        if part is not None:
            text = part.text
        
        keyword = {
            "aspect"  : "shirt",
            "opinion" : [verb.text + " " + text + " " + adv.text] 
        }

        return keyword

# Find a phrase matching the rule PRON <- (VERB|AUX) -> (ADJ)+
def rule_2(verb) :
    if verb.pos_ == "VERB"  or verb.pos_ == "AUX" :
        pron = find_pron_in_children(verb.lefts)
        if pron is None:
            return None

        adjs = find_adj_in_children(token.rights)
        if len(adjs) == 0 :
            return None

        text = pron.text.lower().rstrip()

        if text == "it" or text == "they":
            text = "shirt"
        else :
            return None

        keyword = {
            "aspect" : text,
            "opinion" : form_adj_texts(adjs)
        }

        if verb.pos_ == "VERB" :
            for i in range(len(keyword["opinion"])) :
                keyword["opinion"][i] = verb.text + " " +  keyword["opinion"][i]
        
        return keyword

# Find the phrases matching the rule (NOUN)+ <- (AUX | VERB) -> (ADJ)+
def rule_3(verb) :
    if verb.pos_ == "AUX" or verb.pos_ == "VERB" and verb.pos_ == "ROOT" :
        noun = find_noun_in_children(verb.lefts)
        if noun is None :
            return None

        nouns = []
        nouns.append(noun)

        nouns += find_conj_noun_in_children(noun.rights)
        
        adjs = find_adj_in_children(verb.rights)
        if len(adjs) == 0 :
            return None
        
        keywords = []
        adj_texts = form_adj_texts(adjs)

        if verb.pos_ == "VERB" :
            for i in range(len(adj_texts)) :
                adj_texts[i] = verb.text + " " + adj_texts[i]

        for noun in nouns:
            keyword = {
                "aspect" : noun.text,
                "opinion" : adj_texts
            }

            keywords.append(keyword)
        
        return keywords

# Find a phrase matching the rule NOUN <- AUX -> NOUN <- ADJ
def rule_4(aux):
    if aux.pos_ == "AUX" :
        noun = find_noun_in_children(aux.lefts)
        if noun is None:
            return noun

        opine_noun = find_noun_in_children(aux.rights)
        if opine_noun is None:
            return
        
        adjs = find_adj_in_children(opine_noun.lefts)
        if len(adjs) == 0:
            return None

        adj_texts = form_adj_texts(adjs)
        for i in range(len(adj_texts)):
            adj_texts[i] += " " + opine_noun.text

        keyword = {
            "aspect" : noun.text,
            "opinion" : adj_texts
        }
        
        return keyword

# Find the phrases matching the rule ADJ <- NOUN
def rule_5(noun) :
    valid_deps  = {"ROOT", "attr", "nsubj"}
    if noun.pos_ == "NOUN" and noun.dep_ in valid_deps :
        adjs = find_adj_in_children(noun.lefts)
        if len(adjs) == 0 :
            return None
        
        keyword = {
            "aspect" : noun.text,
            "opinion" : form_adj_texts(adjs)
        }

        return keyword

# Find adjectives in sentences containing only adjectives (ADJ)+
def rule_6 (adj) :
    if adj.pos_ == "ADJ" and adj.dep_ == "ROOT" :
        adjs = find_adj_in_children(adj.children)
        part = find_neg_in_children(adj.children)
        adjs.append((part, adj))

        if len(adjs) == 0:
            return None
        
        keyword = {
            "aspect" : "shirt",
            "opinion" : form_adj_texts(adjs)
        }

        return keyword

# Find the phrases matching the rule  (ADJ)+ <- (NOUN)+
def rule_7(noun) :
    if noun.pos_ == "NOUN" and noun.dep_ == "compound" :
        adjs = find_adj_in_children(noun.lefts)
        if len(adjs) == 0 :
            return None
        
        n_heads = find_comp_noun_in_head(noun.head)
        n_heads.insert(0, noun)
        text = n_heads[-1].text
        n_heads = n_heads[:-1]
        opinion = form_adj_texts(adjs)[0]
        for n_head in n_heads:
            opinion += " " + n_head.text

        keyword = {
            "aspect" : text,
            "opinion" : [opinion]
        }

        return keyword

# Find the phrases matching the rule DET <- (VERB|AUX) -> (ADJ)+
def rule_8(verb) :
    if verb.pos_ == "VERB"  or verb.pos_ == "AUX" :
        det = find_det_in_children(verb.lefts)
        if det is None:
            return None

        adjs = find_adj_in_children(token.rights)
        if len(adjs) == 0 :
            return None

        text = det.text.lower().rstrip()

        if text == "this":
            text = "shirt"
        else :
            return None

        keyword = {
            "aspect" : text,
            "opinion" : form_adj_texts(adjs)
        }

        if verb.pos_ == "VERB" :
            for i in range(len(keyword["opinion"])) :
                keyword["opinion"][i] = verb.text + " " +  keyword["opinion"][i]
        
        return keyword

# Find the phrases matching the rule  PRON <- AUX -> NOUN <- ADJ
def rule_9(aux):
    if aux.pos_ == "AUX" :
        pron = find_pron_in_children(aux.lefts)
        if pron is None:
            return None

        text = pron.text.lower().rstrip() 
        if text == "it" :
            text = "shirt"
        else :
            return None

        opine_noun = find_noun_in_children(aux.rights)
        if opine_noun is None or opine_noun.dep_ == "attr":
            return None
        
        adjs = find_adj_in_children(opine_noun.lefts)
        if len(adjs) == 0:
            return None

        adj_texts = form_adj_texts(adjs)
        for i in range(len(adj_texts)):
            adj_texts[i] += " " + opine_noun.text

        keyword = {
            "aspect" : text,
            "opinion" : adj_texts
        }
        
        return keyword

pattern_sept = re.compile("Sept")
def sanitize_date(date) :
    date = pattern_sept.sub("September", date)
    return date

def append_keyword(keywords, keyword) :
    aspect = keyword["aspect"]
    if aspect not in keywords:
        keywords[aspect] = set()
    for op in keyword["opinion"] :
        keywords[aspect].add(op.lower())

rules = [rule_1, rule_2, rule_3, rule_4, rule_5, rule_6, rule_7, rule_8, rule_9]

# List holding list 1 json
stage_1_json = []

for item in data:
    #Copy all the json except for the comments
    item_new = {}
    item_new["id"] = item["id"]
    item_new["title"] = item["title"]
    item_new["details"] = item["details"]
    item_new["rating_div"] = item["rating_div"]
    item_new["image"] = item["image"]

    # Note the first and last date of comments
    dates = []
    for comment in item["comments"] :
        date = sanitize_date(comment["date"])
        try :
            date = datetime.strptime(date, "%b %d, %Y")
        except :
            date = datetime.strptime(date, "%B %d, %Y")
        date_to_sec = time.mktime(date.timetuple())
        dates.append(date_to_sec)

    if len(dates) != 0:
        item_new["oldest_rev"] = min(dates)
        item_new["newest_rev"] = max(dates)
    else :
        item_new["oldest_rev"] = None
        item_new["newest_rev"] = None

    keywords = {}
    
    for comment in item["comments"]:
        text = text_sanitizer(comment["body"])
        doc = nlp(text)

        for token in doc:
            for rule in rules :
                if rule == rule_3:
                    keyword_list = rule(token)
                    if keyword_list is not None:
                        for keyword in keyword_list:
                            append_keyword(keywords, keyword)
                else :
                    keyword = rule(token)
                    if keyword is not None:
                        append_keyword(keywords, keyword)

    item_new["rev_summ"] = {}

    for keyword in keywords:
        item_new["rev_summ"][keyword] = []
        for opinion in keywords[keyword] :
            item_new["rev_summ"][keyword].append(opinion)
    
    stage_1_json.append(item_new)

# Write the json to a file
file = open("stage_1.json", "w")
json.dump(stage_1_json, file, indent=4)
file.close()
