import re
import json

terms = {
    "crop(ped).top" : ["cropped", "top"],
    "tank" : ["tank", "top"]
    "top" : ["top", "shirt"],
    "polo" : ["polo", "shirt"],
    "tee" : ["tee", "shirt"],
    "cotton" : ["cotton", "fabric"],
    "stretch.?knit" : ["stretch", "knit"],
    "curve(d)?.hem" : ["curved", "hem"],
    "graphic" : ["graphic", "design"],
    "ribbed" : ["ribbed", "design"],
    "baggy" : ["baggy", "fit"],
    "ringer" : ["ringer", "design"],
    "v.neck" : ["v-neck", "neckline"],
    "t.shirt" : ["tee", "shirt"],
    "slub" : ["slub", "knit"],
    "jersey" : ["jersey", "knit"],
    "crew.?neck" : ["crewneck", "neckline"],
    "knot(ted)?.hem" : ["knotted","hem"],
    "rib.knit" : ["rib-knit", "knit"],
    "modal" : ["modal", "fabric"],
    "spandex" : ["spandex", "fabric"],
    "polyester" : ["polyester", "fabric"],
    "rayon" : ["rayon", "fabric"],
    "ruch" : ["ruch", "design"],
    "curve(d)?.hem" : ["curved", "hem"],
    "pattern" : ["pattern", "design"],
    "pintuck" : ["pintuck", "design"],
    "pleat" : ["pleat", "design"],
    "lace" : ["lace", "design"],
    "ruffle" : ["ruffle", "design"],
    "pima.?cotton" : ["pima", "fabric"],
    "scoop.neck" : ["scoop", "neckline"],
    "raw.edge" : ["raw edge", "design"],
    "tie.front" : ["tie front", "hem"],
    "square(d)?.neck" : ["square", "neckline"],
    "mesh" : ["mesh", "design"],
    "print" : ["print", "design"],
    "logo" : ["logo", "design"],
    "long.sleeve" : ["long", "sleeve"],
    "turtle.?neck" : ["turtle", "neckline"],
    "camo" : ["camo", "design"],
    "linen" : ["linen", "fabric"],
    "short.sleeve" : ["short", "sleeve"],
    "stripe" : ["stripe", "design"],
    "theme" : ["themed", "design"],
    "twist(ed)?.cuff" : ["twisted", "cuff"],
    "slogan" : ["slogan", "design"],
    "ruffle(d)?.cuff" : ["ruffle", "cuff"],
    "triblend" : ["triblend", "fabric"],
    "racerback" : ["racerback", "shirt"]
}

# Compile the regex in the terms
def compile_terms(terms):
    compiled_terms = {}

    for term in terms:
        pattern = re.compile(term)

        compiled_terms[pattern] = {
            "element" : terms[term][1],
            "specific" : terms[term][0]
        }
    
    return compiled_terms

uploaded = files.upload()

file = open("stage_1.json")
data = json.load(file)

#Compile the terms
compiled_terms = compile_terms(terms)

stage_2_json = []

for item in data:
    # Copy the json except details
    item_new = {}

    item_new["id"] = item["id"]
    item_new["title"] = item["title"]
    item_new["rating_div"] = item["rating_div"]
    item_new["image"] = item["image"]
    item_new["rev_summ"] = item["rev_summ"]
    item_new["oldest_rev"] = item["oldest_rev"]
    item_new["newest_rev"] = item["newest_rev"]

    detail = {}

    for det in item["details"] :
        det = det.lower()
        for term in compiled_terms :
            if term.search(det):
                entry = compiled_terms[term]
                if entry["element"] not in detail:
                    detail[entry["element"]] = set()
                detail[entry["element"]].add(entry["specific"])
    
    for attr in detail:
        detail[attr] = list(detail[attr])
    item_new["detail"] = detail

    stage_2_json.append(item_new)

file = open("stage_2.json", "w")
json.dump(stage_2_json, file, indent=4)
file.close()
