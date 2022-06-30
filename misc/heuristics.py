import string
import re

# Extracts individual quest ingredients from the 'xml-like' quest metadata format
def get_ingredients_xml(text):
    lines = text.splitlines()
    
    i = 0
    ingredients = {}
    
    while i < len(lines):
        line = lines[i]
        
        if "<|begin_objective|>" in line:
            i += 1
            
            if lines[i][0:1] == "<|" and "<|end_objective|>" not in lines[i]:
                raise ValueError('Incorrect formating: found <|begin_objective|>, but could not find matching <|end_objective|>')
            elif "<|end_objective|>" not in lines[i]:
                ingredients['objective'] = [lines[i]]
            
            i += 1
                
        elif "<|begin_tasks|>" in line:
            i += 1
            
            tasks = []
            line = lines[i]
            while "<|end_tasks|>" not in line and i < len(lines):
            
                if lines[i][0:1] == "<|":
                    raise ValueError('Incorrect formating: found <|begin_tasks|>, but could not find matching <|end_objective|>')
                
                tasks.append(line)
                i += 1
                line = lines[i]
            
            if tasks:
                ingredients['tasks'] = tasks
            
        elif "<|begin_task_locations|>" in line:
            i += 1
            
            task_locations = []
            line = lines[i]
            while "<|end_task_locations|>" not in line and i < len(lines):
                
                if lines[i][0:1] == "<|":
                    raise ValueError('Incorrect formating: found <|begin_task_locations|>, but could not find matching <|end_task_locations|>')
                
                task_locations.append(line)
                i += 1
                line = lines[i]
            
            if task_locations:
                ingredients['task_locations'] = task_locations
            
        elif "<|begin_quest_giver|>" in line:
            i += 1
            
            if lines[i][0:1] == "<|" and "<|end_quest_giver|>" not in lines[i]:
                raise ValueError('Incorrect formating: found <|begin_quest_giver|>, but could not find matching <|end_quest_giver|>')
            elif "<|end_quest_giver|>" not in lines[i]:
                ingredients['quest_giver'] = [lines[i]]
            
            i += 1
        
        elif "<|begin_rewards|>" in line:
            i += 1
            
            rewards = []
            line = lines[i]
            while "<|end_rewards|>" not in line and i < len(lines):
                
                if lines[i][0:1] == "<|":
                    raise ValueError('Incorrect formating: found <|begin_rewards|>, but could not find matching <|end_rewards|>')
                
                rewards.append(line)
                i += 1
                line = lines[i]
            
            if rewards:
                ingredients['rewards'] = rewards
                
        elif "<|begin_characters|>" in line:
            i += 1
            
            characters = []
            line = lines[i]
            while "<|end_characters|>" not in line and i < len(lines):
                
                if lines[i][0:1] == "<|":
                    raise ValueError('Incorrect formating: found <|begin_characters|>, but could not find matching <|end_characters|>')
                
                characters.append(line)
                i += 1
                line = lines[i]
            
            if characters:
                ingredients['characters'] = characters
                
        elif "<|begin_locations|>" in line:
            i += 1
            
            locations = []
            line = lines[i]
            while "<|end_locations|>" not in line and i < len(lines):
                
                if lines[i][0:1] == "<|":
                    raise ValueError('Incorrect formating: found <|begin_locations|>, but could not find matching <|end_locations|>')
                
                locations.append(line)
                i += 1
                line = lines[i]
            
            if locations:
                ingredients['locations'] = locations
                
        elif "<|begin_items|>" in line:
            i += 1
            
            items = []
            line = lines[i]
            while "<|end_items|>" not in line and i < len(lines):
                
                if lines[i][0:1] == "<|":
                    raise ValueError('Incorrect formating: found <|begin_items|>, but could not find matching <|end_items|>')
                
                items.append(line)
                i += 1
                line = lines[i]
            
            if items:
                ingredients['items'] = items
                
        elif "<|begin_groups|>" in line:
            i += 1
            
            groups = []
            line = lines[i]
            while "<|end_groups|>" not in line and i < len(lines):
                
                if lines[i][0:1] == "<|":
                    raise ValueError('Incorrect formating: found <|begin_groups|>, but could not find matching <|end_groups|>')
                
                groups.append(line)
                i += 1
                line = lines[i]
            
            if groups:
                ingredients['groups'] = groups
                
        elif "<|begin_enemies|>" in line:
            i += 1
            
            enemies = []
            line = lines[i]
            while "<|end_enemies|>" not in line and i < len(lines):
                
                if lines[i][0:1] == "<|":
                    raise ValueError('Incorrect formating: found <|begin_enemies|>, but could not find matching <|end_enemies|>')
                
                enemies.append(line)
                i += 1
                line = lines[i]
            
            if enemies:
                ingredients['enemies'] = enemies
                
        elif "<|begin_tools|>" in line:
            i += 1
            
            tools = []
            line = lines[i]
            while "<|end_tools|>" not in line and i < len(lines):
                
                if lines[i][0:1] == "<|":
                    raise ValueError('Incorrect formating: found <|begin_tools|>, but could not find matching <|end_tools|>')
                
                tools.append(line)
                i += 1
                line = lines[i]
            
            if tools:
                ingredients['tools'] = tools
        i += 1
    return ingredients

# Extracts quest ingredients from the 'narrative' quest metadata format
def get_ingredients_narrative(text):
    ingredients = {}
    
    for line in text.splitlines():
        if line.startswith("The quest-giver is called") or line.startswith("The quest-giver is"):
            ingredients['quest_giver'] = [line]
        elif line.startswith("The quest-giver gives a quest to the player."):
            ingredients['objective'] = [line]
        elif line.startswith("The player should first"):
            tasks = re.search('The player should first (.*) to complete their objective', line).group(1)
            ingredients['tasks'] = [tasks]
            
            if "This task can be completed in the following location:" in line:
                task_locations = re.search('This task can be completed in the following location: (.*).', line).group(1)
                ingredients['task_locations'] = [task_locations]
            elif "These tasks can be completed in the following locations:" in line:
                task_locations = re.search('These tasks can be completed in the following locations: (.*).', line).group(1)
                ingredients['task_locations'] = [task_locations]
        
        elif line.startswith("The player will receive the following rewards for completing the quest objective:"):
            rewards = re.search('The player will receive the following rewards for completing the quest objective: (.*).', line).group(1)
            ingredients['rewards'] = [rewards]
        elif line.startswith("The following characters are related to this quest:"):
            characters = re.search('The following characters are related to this quest: (.*).', line).group(1)
            ingredients['characters'] = [characters]
        elif line.startswith("The following locations are related to this quest:"):        
            locations = re.search('The following locations are related to this quest: (.*).', line).group(1)
            ingredients['locations'] = [locations]
        elif line.startswith("The following items are related to this quest:"):   
            items = re.search('The following items are related to this quest: (.*).', line).group(1)
            ingredients['items'] = [items]
        elif line.startswith("The following groups are related to this quest:"):
            groups = re.search('The following groups are related to this quest: (.*).', line).group(1)
            ingredients['groups'] = [groups]
        elif line.startswith("The player will encounter the following enemies during this quest:"):
            enemies = re.search('The player will encounter the following enemies during this quest: (.*).', line).group(1)
            ingredients['enemies'] = [enemies]
        elif line.startswith("There are some important facts concerning this quest."):
            ingredients['tools'] = [line.split("quest. ", 1)[1]]
            
    return ingredients

def get_ingredients(text, format):
    if format == "xml":
        return get_ingredients_xml(text)
    elif format == "narrative":
        return get_ingredients_narrative(text)
    else:
        raise ValueError('Unrecognized format, expected "xml" or "narrative", received ' + format)

# A simple heuristic filter that checks whether the special tokens in the output also exist in the input     
def verify_tokens(input, output, format="narrative"):
    ingredients = get_ingredients(input, format)
    matcher = re.compile("[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)+") # matches all compound word tokens (snake_case)
    
    all_tokens = set()
    for ingredient in ingredients.values():
        if isinstance(ingredient, list):
            ingredient = ' '.join(ingredient) # could do something more sophisticated here...
        
        tokens = re.findall(matcher, ingredient)
        all_tokens.update(tokens)
        
    output_tokens = re.findall(matcher, output)
    
    for token in output_tokens:
        if token not in all_tokens:
            print(token + " not in input!")
            return False
        
    return True

# A simple heuristic filter that checks whether the important special tokens in the input also exist in the output  
def important_tokens_exist_in_output(input, output, not_important={"quest_giver"}, format="narrative"):
    ingredients = get_ingredients(input, format)
    matcher = re.compile("[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)+") # matches all compound word tokens (snake_case)
    
    input_tokens = set()
    for ingredient in ingredients.values():
        if isinstance(ingredient, list):
            ingredient = ' '.join(ingredient)
        
        tokens = re.findall(matcher, ingredient)
        input_tokens.update(tokens)
    
    important_tokens = set()
    for token in input_tokens:
        important = True
        for not_important_token in not_important:
            if token.startswith(not_important_token): # a lazy way to check against all different variations of tokens
                important = False
                break
        if important:
            important_tokens.add(token)
        
    output_tokens = re.findall(matcher, output)
    for token in important_tokens:
        if token not in output_tokens:
            print(token + " not in output!")
            return False
        
    return True