from transformers import GPT2LMHeadModel, AutoTokenizer
import torch
import argparse
import numpy as np
from torch.nn import functional as F

# Calculates the conditional perplexity score on the quest descriptions from the provided .txt file (see the 'train_text' folder for examples)

parser = argparse.ArgumentParser()
parser.add_argument("model")
parser.add_argument("file")
parser.add_argument("format")
args = parser.parse_args()

model = GPT2LMHeadModel.from_pretrained(args.model)
tokenizer = AutoTokenizer.from_pretrained("gpt2")

model.eval()

supported_formats = ["simple", "xml", "narrative"]

def softmax(x):
    exps = [np.exp(i) for i in x]
    tot = np.sum(exps)
    return [i/tot for i in exps]

def score(ingredients, description):
    encoded_input = tokenizer.encode(ingredients)
    encoded_quest = tokenizer.encode(ingredients + description)
    
    encoded_desc = encoded_quest[len(encoded_input):]   
    tensor_input = torch.tensor([encoded_quest])
    
    with torch.no_grad():
        outputs = model(tensor_input)
        predictions = outputs.logits
        
    logprobs = []
    start = -1 - len(encoded_desc)
    for j in range(start, -1, 1):
        raw_output = []
        for i in predictions[-1][j]:
            raw_output.append(i.item())  
        logprobs.append(np.log(softmax(raw_output)))
    
    conditional_probs = []
    for desc_word, prob in zip(encoded_desc, logprobs):
        conditional_probs.append(prob[desc_word])
    
    return np.exp(-np.sum(conditional_probs)/len(encoded_desc))

if args.format in supported_formats:
    f = open(args.file)
else:
    print("Format not specified correctly!")
    quit()

quest_data = f.read().split("<|endoftext|>")
f.close()

if args.format == "simple":
    desc_start = "Quest description, the quest-giver explaining the quest to the player:\n"
elif args.format == "narrative":
    desc_start = "This is the quest description, the quest-giver explaining the quest to the player:\n\""
    desc_end = "\""
else:
    desc_start = "<|begin_description|>\n"
    desc_end = "\n<|end_description|>\n<|end_quest|>"

scores_sum = 0
i = 0
for quest in quest_data:
    quest = quest.strip()
    if not quest:
        continue
    
    i += 1 
        
    ingredients, description = quest.split(desc_start)
    ingredients += desc_start

    if (args.format == "narrative" or args.format == "xml") and description.endswith(desc_end):
        description = description[:-len(desc_end)]
    
    quest_score = score(ingredients, description)
    print(quest_score)
    scores_sum += quest_score
    
print("Avg. perplexity: " + str(scores_sum/i))