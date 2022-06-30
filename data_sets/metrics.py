import json

import spacy
import textdescriptives as td
from lexicalrichness import LexicalRichness

# Calculates some commonly used NLP metrics on the quest data sets

files = ["BG/quests_BG.json", "BG/quests_BGII.json", "MC/quests_MC.json", "TES/quests_oblivion.json", "TES/quests_skyrim.json", "TL2/quests_TL2.json"]

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('textdescriptives')


total_readability = 0
total_complexity = 0
total_richness = 0
total_words = 0
total_quests = 0
for file in files:
    f = open(file)
    quest_data = json.load(f)
    
    readability = 0
    complexity = 0
    richness = 0
    words = 0
    for quest in quest_data:
        quest_description = quest['description']
        
        doc = nlp(quest_description)
        readability += doc._.readability['flesch_kincaid_grade']
        complexity += doc._.dependency_distance['dependency_distance_mean']
        
        lex = LexicalRichness(quest_description)
        richness += lex.ttr
        words += lex.words
        
    quests = len(quest_data)
    
    total_quests += quests
    total_readability += readability
    total_complexity += complexity
    total_richness += richness
    total_words += words
    
    print("Quest file: " + file)    
    print("Avg. readability (Flesch-Kincaid grade): " + str(readability / quests))
    print("Avg. syntactics complexity (dependency distance): " + str(complexity / quests))
    print("Avg. lexical richness (Type-Token Ratio): " + str(richness / quests))
    print("Avg. words: " + str(words / quests))
    print(".........")
    
print("Overall:")    
print("Avg. readability (Flesch-Kincaid grade): " + str(total_readability / total_quests))
print("Avg. syntactics complexity (dependency distance): " + str(total_complexity / total_quests))
print("Avg. lexical richness (Type-Token Ratio): " + str(total_richness / total_quests))
print("Avg. words: " + str(total_words / total_quests))
print(".........")