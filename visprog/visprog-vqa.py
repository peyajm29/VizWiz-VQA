import os
import sys
import json

import sys
from pathlib import Path

# Add the parent directory to sys.path
parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)

from PIL import Image
from IPython.core.display import HTML
from functools import partial

from engine.utils import ProgramGenerator, ProgramInterpreter
from prompts.gqa import create_prompt

from io import BytesIO
import requests
import re

gqa_step_interpreters = set([
            'LOC(',
            'COUNT(',
            'CROP(',
            'CROP_RIGHTOF(',
            'CROP_LEFTOF(',
            'CROP_FRONTOF(',
            'CROP_INFRONTOF(',
            'CROP_INFRONT(',
            'CROP_BEHIND(',
            'CROP_AHEAD(',
            'CROP_BELOW(',
            'CROP_ABOVE(',
            'VQA(',
            'EVAL(',
            'RESULT(']
        )

def extract_image_names(json_file_path):
    image_names = []  # List to store image names

    # Read JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract image names from each item in the JSON data
    for item in data:
        image_names.append(item['image'])

    return image_names

def extract_index(image_name):
    # Split the string at the underscore and take the last part
    index_part = image_name.rsplit('_', 1)[-1]
    # Remove the file extension and convert the index part to an integer
    index = int(index_part.split('.')[0])
    return index

def filter_instructions(prog_instruction, gqa_step_interpreters):
    # Split the input string into lines
    lines = prog_instruction.split('\n')
    
    # Filter lines that contain any of the keywords
    filtered_lines = [line for line in lines if any(keyword in line for keyword in gqa_step_interpreters)]

    for line in filtered_lines:
        if 'LOC' in line:
            line = line.replace('IMAGE0', 'IMAGE')

    # Join the filtered lines back into a string
    filtered_string = '\n'.join(filtered_lines)
    
    return filtered_string

def generate_default_prog(question):
    default_prog = "ANSWER0=VQA(image=IMAGE,question='" + question + "')\nFINAL_RESULT=RESULT(var=[ANSWER0])"
    return default_prog

if __name__ == '__main__':

    module_path = os.path.abspath(os.path.join('..'))
    if module_path not in sys.path:
        sys.path.append(module_path)

    interpreter = ProgramInterpreter(dataset='gqa')
    prompter = partial(create_prompt,method='all')
    generator = ProgramGenerator(prompter=prompter)


    ###########################################################
    ##### Gathering filnames from datasets
    ###########################################################
    path = Path(os.getcwd())
    root = path.parent.absolute()
    root_directory  = os.path.join(root, "gpt4-turbo-vision/outputs/")

    # Train Names
    train_filenames = os.path.join(root_directory, 'results-train.json')
    train_names = extract_image_names(train_filenames)
    train_names = list(set(train_names))

    train_yesno_filenames = os.path.join(root_directory, 'results-train-yesno.json')
    train_yesno_names = extract_image_names(train_yesno_filenames)

    train_number_filenames = os.path.join(root_directory, 'results-train-number.json')
    train_number_names = extract_image_names(train_number_filenames)

    for item in train_number_names:
        if item in train_names:
            train_names.remove(item)

    for item in train_yesno_names:
        if item in train_names:
            train_names.remove(item)

    # Val Names
    val_filenames = os.path.join(root_directory, 'results-val.json')
    val_names = extract_image_names(val_filenames)
    val_names = list(set(val_names))

    val_yesno_filenames = os.path.join(root_directory, 'results-val-yesno.json')
    val_yesno_names = extract_image_names(val_yesno_filenames)

    val_number_filenames = os.path.join(root_directory, 'results-val-number.json')
    val_number_names = extract_image_names(val_number_filenames)

    for item in val_number_names:
        if item in val_names:
            val_names.remove(item)

    for item in val_yesno_names:
        if item in val_names:
            val_names.remove(item)

    # Test Names
    test_filenames = os.path.join(root_directory, 'results-test.json')
    test_names = extract_image_names(test_filenames)

    # Concatenating Val and Train Names
    val_names = val_yesno_names + val_number_names + val_names
    train_names = train_yesno_names + train_number_names + train_names

    ###########################################################
    ##### Gathering image objects from hosted image urls
    ###########################################################

    # val_names can also be train_names or test_names depending on purpose

    num_images = min(100, len(val_names))
    counter = 0
    print("\n\nLoading images from hosted url")
    print("Loading ", num_images, " images", "\n\n")

    image_names = val_names

    image_objects = []
    image_url_prefix = "https://vizwiz.cs.colorado.edu/VizWiz_visualization_img/"

    # Loop through all filenames in the list
    for filename in image_names:
        if counter == num_images: break
        # Check if the filename is valid (you can add more conditions if needed)
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            # Construct the URL for the image
            image_url = image_url_prefix + filename
            
            # Fetch the image data from the URL
            response = requests.get(image_url)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Open the image data as an image object
                with Image.open(BytesIO(response.content)) as image:
                    # Resize the image
                    image.thumbnail((640, 640), Image.LANCZOS)
                    # Append the image object to the list along with the filename
                    image_objects.append((image, filename))
                    counter += 1
                    print("Number of images loaded: ", counter)
            else:
                print(f"Failed to fetch image '{filename}' from URL: {image_url}")

    # Example usage:
    for image, filename in image_objects:
        print(f"Loaded image '{filename}' with size: {image.size}")


    ###########################################################
    ##### Generating Image Question Pairs
    ###########################################################

    # Modify depending on which annotations you're referencing 
    # to compare against a particular dataset 
    data_folder = os.path.join(root, "data")
    with open(os.path.join(data_folder, "val.json"), 'r') as file:
        data = json.load(file)
    # with open(os.path.join(data_folder, "test.json"), 'r') as file:
    #     data = json.load(file)
    # with open(os.path.join(data_folder, "train.json"), 'r') as file:
    #     data = json.load(file)

    image_question_pairs = []

    for image_object in image_objects:
        (image, filename) = image_object
        image_index = extract_index(filename)
        image_json = data[image_index]

        question = image_json["question"]
        image_question_pairs.append((image, question, filename))

    
    ###########################################################
    ##### Generating JSON File of Results
    ###########################################################

    results = []

    for pair in image_question_pairs:
        (image, question, filename) = pair
        prog,_ = generator.generate(dict(question=question))
        prog = filter_instructions(prog, gqa_step_interpreters)
        
        init_state = dict(IMAGE=image.convert('RGB'))

        print('\n\nHere is the image name and question we are currently on: ', (filename, question), '')
        if prog:
            print('Here is the program instructions:\n ', prog, '\n\n')
        else: 
            print('Here is the default program instructions generated:\n ', prog, '\n\n')
            prog = generate_default_prog(question)


        answer, prog_state, html_str = interpreter.execute(prog,init_state,inspect=True)
        
        result = {
            "image": filename,
            "answer": answer
        }
        results.append(result)


    # Change to whatever name you'd like the results json file to be generated as. 
    output_file_name = 'final_val_100_answers.json'

    output_dir = os.path.join(root, "visprog/outputs")
    output_file_path = os.path.join(output_dir, output_file_name)
    with open(output_file_path, 'w') as file:
        json.dump(results, file, indent=4)

    