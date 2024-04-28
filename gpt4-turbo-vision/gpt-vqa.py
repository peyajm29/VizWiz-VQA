from openai import OpenAI
import os
import json
from pathlib import Path
import numpy as np

API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = API_KEY)

def generate_system_prompt(condition = "zero-shot"):
    instruction = "You are a crowdsource worker answering visual questions from blind people. The answers will mostly be yes/no, number, unanswerable or other. If it is unanswerable, reply unanswerable."
    system_instruction = {"type": "text", "text": instruction}
    if (condition == "one-shot"):
        system_prompt = {
            "role": "system",
            "content": [
                system_instruction,
                {"type": "text", "text": "response example: creamy"}
            ]
        }
        return system_prompt
    elif (condition == "few-shot"):
        system_prompt = {
            "role": "system",
            "content": [
                system_instruction,
                {"type": "text", "text": "response example: creamy"},
                {"type": "text", "text": "response example: unanswerable"},
                {"type": "text", "text": "response example: stop reset start"},
                {"type": "text", "text": "response example: computer mouse"},
                {"type": "text", "text": "response example: raisin date walnut"},
                {"type": "text", "text": "response example: sticker"},
                {"type": "text", "text": "response example: yes"},
                {"type": "text", "text": "response example: eight"},
                {"type": "text", "text": "response example: no"},
                {"type": "text", "text": "response example: two"}
            ]
        }
        return system_prompt
    elif (condition == "50-few-shot"):
        system_prompt = {
            "role": "system",
            "content": [
                system_instruction,
                {"type": "text", "text": "response example: creamy"},
                {"type": "text", "text": "response example: unanswerable"},
                {"type": "text", "text": "response example: stop reset start"},
                {"type": "text", "text": "response example: computer mouse"},
                {"type": "text", "text": "response example: raisin date walnut"},
                {"type": "text", "text": "response example: sticker"},
                {"type": "text", "text": "response example: yes"},
                {"type": "text", "text": "response example: eight"},
                {"type": "text", "text": "response example: no"},
                {"type": "text", "text": "response example: two"},
                {"type": "text", "text": "response example: sloppy joe seasoning"},
                {"type": "text", "text": "response example: unsuitable"},
                {"type": "text", "text": "response example: blue"},
                {"type": "text", "text": "response example: moutain dew code red"},
                {"type": "text", "text": "response example: you going to bed"},
                {"type": "text", "text": "response example: coconut body butter"},
                {"type": "text", "text": "response example: i do not see anything on this side tin perhaps something on bottom"},
                {"type": "text", "text": "response example: on table"},
                {"type": "text", "text": "response example: living room"},
                {"type": "text", "text": "response example: no pumpkin spice coffee"},
                {"type": "text", "text": "response example: i dont know"},
                {"type": "text", "text": "response example: chicken pasta"},
                {"type": "text", "text": "response example: frog sitting on pottery dish"},
                {"type": "text", "text": "response example: shelf has trading cards"},
                {"type": "text", "text": "response example: unanswerable"},
                {"type": "text", "text": "response example: food"},
                {"type": "text", "text": "response example: nothing"},
                {"type": "text", "text": "response example: easy go"},
                {"type": "text", "text": "response example: sedan"},
                {"type": "text", "text": "response example: nutrition facts"},
                {"type": "text", "text": "response example: close to 10 inches"},
                {"type": "text", "text": "response example: description membership benefits"},
                {"type": "text", "text": "response example: solar garden light"},
                {"type": "text", "text": "response example: orange"},
                {"type": "text", "text": "response example: basil leaves"},
                {"type": "text", "text": "response example: advanced antiseptic mouthwash tartar protection citrus flavor"},
                {"type": "text", "text": "response example: remote control"},
                {"type": "text", "text": "response example: grand theft auto vice city"},
                {"type": "text", "text": "response example: apple pie spice"},
                {"type": "text", "text": "response example: sweet sour chicken"},
                {"type": "text", "text": "response example: action figure"},
                {"type": "text", "text": "response example: incredible hulk"},
                {"type": "text", "text": "response example: winney pooh stuff doll"},
                {"type": "text", "text": "response example: minute made coolers lemon"},
                {"type": "text", "text": "response example: books bookshelf pictures"},
                {"type": "text", "text": "response example: right leg"},
                {"type": "text", "text": "response example: coffee maker"},
                {"type": "text", "text": "response example: yellow coffee mug"},
                {"type": "text", "text": "response example: golden sweet whole kernel corn"},
                {"type": "text", "text": "response example: pepsi"}
            ]
        }
        return system_prompt
    else:
        system_prompt = {
            "role": "system",
            "content": [
                system_instruction
            ]
        }
        return system_prompt
    
def generate_user_prompt(image_url, question):
    user_prompt = {
      "role": "user",
      "content": [
        {"type": "text", "text": question},
        {
          "type": "image_url",
          "image_url": {
            "url": image_url,
          },
        },
      ],
    }
    return user_prompt

def main():
    # specify input dataset file here
    root_dir = Path(os.getcwd()).parent.absolute()
    data_file = os.path.join(root_dir, "data/val.json")
    with open(data_file, 'r') as file:
        parsed_data = json.load(file)
        
    # this is where the images are hosted
    base_url = "https://vizwiz.cs.colorado.edu/VizWiz_visualization_img/"

    results = []

    for item in parsed_data:

        # for testing specific question types
        # if (item["answer_type"] != "number"):
        #     continue
        
        message = [
            generate_user_prompt(base_url + item["image"], item["question"]),
            generate_system_prompt()
        ]
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages = message,
            max_tokens = 30
        )
        
        answer = response.choices[0].message.content

        result = {
            "image": item["image"],
            "answer": answer
        }

        results.append(result)

    # store predictions here in a json file
    output_file_path = os.path.join(root_dir, "gpt4-turbo-vision/outputs/results-val-number.json")

    with open(output_file_path, 'w') as output_file:
        json.dump(results, output_file, indent = 2)

