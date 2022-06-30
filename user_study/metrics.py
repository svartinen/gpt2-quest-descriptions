import pandas as pd

import spacy
import textdescriptives as td
from lexicalrichness import LexicalRichness

# Computes some commonly used NLP metrics on the generated descriptions

file = "generated_descriptions.csv"

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('textdescriptives')

quest_data = pd.read_csv(file).to_dict('records')

readability = {}
complexity = {}
richness = {}
words = {}

quests_per_game = {}
for quest in quest_data:
    quest_description = quest['description_text']
    quest_description = quest_description.replace('\\n', '\n')
    
    game = quest['game']

    doc = nlp(quest_description)
    readability[game] = readability.get(game, 0) + doc._.readability['flesch_kincaid_grade']
    complexity[game] = complexity.get(game, 0) + doc._.dependency_distance['dependency_distance_mean']

    lex = LexicalRichness(quest_description)
    richness[game] = richness.get(game, 0) + lex.ttr
    words[game] = words.get(game, 0) + lex.words

    quests_per_game[game] = quests_per_game.get(game, 0) + 1


total_readability = 0
total_complexity = 0
total_richness = 0
total_words = 0
total_quests = 0
for key, value in quests_per_game.items():
    total_readability += readability[key]
    total_complexity += complexity[key]
    total_richness += richness[key]
    total_words += words[key]
    total_quests += value
    
    readability[key] = readability[key]/value
    complexity[key] = complexity[key]/value
    richness[key] = richness[key]/value
    words[key] = words[key]/value
    
quests = len(quest_data)
print("Quest file: " + file)    
print("Avg. readability (Flesch-Kincaid grade): " + str(readability))
print("Avg. syntactics complexity (dependency distance): " + str(complexity))
print("Avg. lexical richness (Type-Token Ratio): " + str(richness))
print("Avg. words: " + str(words))
print(".........")

print("Overall:")    
print("Avg. readability (Flesch-Kincaid grade): " + str(total_readability / total_quests))
print("Avg. syntactics complexity (dependency distance): " + str(total_complexity / total_quests))
print("Avg. lexical richness (Type-Token Ratio): " + str(total_richness / total_quests))
print("Avg. words: " + str(total_words / total_quests))
print(".........")