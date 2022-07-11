import json
import statistics

import spacy
import textdescriptives as td
from lexicalrichness import LexicalRichness

# Calculates some commonly used NLP metrics on the quest data sets

files = ["BG/quests_BG.json", "BG/quests_BGII.json", "MC/quests_MC.json", "TES/quests_oblivion.json", "TES/quests_skyrim.json", "TL2/quests_TL2.json"]

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('textdescriptives')

total_readability = []
total_complexity = []
total_richness = []
total_words = []
for file in files:
    f = open(file)
    quest_data = json.load(f)
    
    readability = []
    complexity = []
    richness = []
    words = []
    for quest in quest_data:
        quest_description = quest['description']
        
        doc = nlp(quest_description)
        readability.append(doc._.readability['flesch_kincaid_grade'])
        complexity.append(doc._.dependency_distance['dependency_distance_mean'])
        
        lex = LexicalRichness(quest_description)
        richness.append(lex.ttr)
        words.append(lex.words)

    total_readability.extend(readability)
    total_complexity.extend(complexity)
    total_richness.extend(richness)
    total_words.extend(words)
    
    print("Quest file: " + file)    
    print("Avg. readability (Flesch-Kincaid grade): " + str(statistics.mean(readability)) + " (stdev: " + str(statistics.stdev(readability)) + ")")
    print("Avg. syntactics complexity (dependency distance): " + str(statistics.mean(complexity))  + " (stdev: " + str(statistics.stdev(complexity)) + ")")
    print("Avg. lexical richness (Type-Token Ratio): " + str(statistics.mean(richness))  + " (stdev: " + str(statistics.stdev(richness)) + ")")
    print("Avg. words: " + str(statistics.mean(words)) +  " (stdev: " + str(statistics.stdev(words)) + ")")
    print(".........")
    
print("Overall:")    
print("Avg. readability (Flesch-Kincaid grade): " + str(statistics.mean(total_readability))  + " (stdev: " + str(statistics.stdev(total_readability)) + ")")
print("Avg. syntactics complexity (dependency distance): " + str(statistics.mean(total_complexity))  + " (stdev: " + str(statistics.stdev(total_complexity)) + ")")
print("Avg. lexical richness (Type-Token Ratio): " + str(statistics.mean(total_richness))  + " (stdev: " + str(statistics.stdev(total_richness)) + ")")
print("Avg. words: " + str(statistics.mean(total_words))  + " (stdev: " + str(statistics.stdev(total_words)) + ")")
print(".........")