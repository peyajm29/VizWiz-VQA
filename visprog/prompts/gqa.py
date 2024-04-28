import random

GQA_CURATED_EXAMPLES=[
"""Question: Is the vehicle in the top of the image?
Program:
BOX0=LOC(image=IMAGE,object='TOP')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='vehicle')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Are there trains or fences in this scene?
Program:
BOX0=LOC(image=IMAGE,object='train')
BOX1=LOC(image=IMAGE,object='fence')
ANSWER0=COUNT(box=BOX0)
ANSWER1=COUNT(box=BOX1)
ANSWER2=EVAL(expr="'yes' if {ANSWER0} + {ANSWER1} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER)
""",
"""Question: Who is carrying the umbrella?
Program:
BOX0=LOC(image=IMAGE,object='umbrella')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='Who is carrying the umbrella?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Which place is it?
Program:
ANSWER0=VQA(image=IMAGE,question='Which place is it?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: What color is the curtain that is to the right of the mirror?
Program:
BOX0=LOC(image=IMAGE,object='mirror')
IMAGE0=CROP_RIGHTOF(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='What color is the curtain?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Is the pillow in the top part or in the bottom of the picture?
Program:
BOX0=LOC(image=IMAGE,object='TOP')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='pillow')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'top' if {ANSWER0} > 0 else 'bottom'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Question: Do you see bottles to the right of the wine on the left of the picture?
Program:
BOX0=LOC(image=IMAGE,object='LEFT')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='wine')
IMAGE1=CROP_RIGHTOF(image=IMAGE0,box=BOX1)
BOX2=LOC(image=IMAGE1,object='bottles')
ANSWER0=COUNT(box=BOX2)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Is the street light standing behind a truck?
Program:
BOX0=LOC(image=IMAGE,object='truck')
IMAGE0=CROP_BEHIND(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='street light')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Which side is the food on?
Program:
BOX0=LOC(image=IMAGE,object='RIGHT')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='food')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'right' if {ANSWER0} > 0 else 'left'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: What do the wetsuit and the sky have in common?
Program:
ANSWER0=VQA(image=IMAGE,question='What do the wetsuit and the sky have in common?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Do the post and the sign have a different colors?
Program:
BOX0=LOC(image=IMAGE,object='post')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE,object='sign')
IMAGE1=CROP(image=IMAGE,box=BOX1)
ANSWER0=VQA(image=IMAGE0,question='What color is the post?')
ANSWER1=VQA(image=IMAGE1,question='What color is the sign?')
ANSWER2=EVAL(expr="'yes' if {ANSWER0} != {ANSWER1} else 'no'")
FINAL_RESULT=RESULT(var=ANSWER2)
""",
"""Question: Does the traffic cone have white color?
Program:
BOX0=LOC(image=IMAGE,object='traffic cone')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='What color is the traffic cone?')
ANSWER1=EVAL(expr="'yes' if {ANSWER0} == 'white' else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Are these animals of different species?
Program:
ANSWER0=VQA(image=IMAGE,question='Are these animals of different species?')
FINAL_RESULT=RESULT(var=ANSWER0)
""",
"""Question: Which side of the image is the chair on?
Program:
BOX0=LOC(image=IMAGE,object='RIGHT')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='chair')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'right' if {ANSWER0} > 0 else 'left'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Do you see any drawers to the left of the plate?
Program:
BOX0=LOC(image=IMAGE,object='plate')
IMAGE0=CROP_LEFTOF(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='drawers')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Does the mat have the same color as the sky?
Program:
BOX0=LOC(image=IMAGE,object='sky')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE,object='mat')
IMAGE1=CROP(image=IMAGE,box=BOX1)
ANSWER0=VQA(image=IMAGE0,question='What color is the sky?')
ANSWER1=VQA(image=IMAGE1,question='What color is the mat?')
ANSWER2=EVAL(expr="'yes' if {ANSWER0} == {ANSWER1} else 'no'")
FINAL_RESULT=RESULT(var=ANSWER2)
""",
"""Question: Is a cat above the mat?
Program:
BOX0=LOC(image=IMAGE,object='mat')
IMAGE0=CROP_ABOVE(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='cat')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
"""
"""Question: Is the cat above a mat?
Program:
BOX0=LOC(image=IMAGE,object='cat')
IMAGE0=CROP_BELOW(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='mat')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 and else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Is the mat below a cat?
Program:
BOX0=LOC(image=IMAGE,object='mat')
IMAGE0=CROP_ABOVE(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='cat')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",
"""Question: Is a mat below the cat?
Program:
BOX0=LOC(image=IMAGE,object='cat')
IMAGE0=CROP_BELOW(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE0,object='mat')
ANSWER0=COUNT(box=BOX1)
ANSWER1=EVAL(expr="'yes' if {ANSWER0} > 0 and else 'no'")
FINAL_RESULT=RESULT(var=ANSWER1)
""",

# Adding My Own Examples:
# """Question: Is this shampoo or conditioner?
# Program:
# BOX0=LOC(image=IMAGE,object='shampoo')
# BOX1=LOC(image=IMAGE,object='conditioner')
# ANSWER0=COUNT(box=BOX0)
# ANSWER1=COUNT(box=BOX1)
# ANSWER2=EVAL(expr="'shampoo' if {ANSWER0} > 0 'conditioner' if {ANSWER1} > 0 else 'neither'")
# FINAL_RESULT=RESULT(var=ANSWER2) 
# """

"""Question: Is this shampoo or conditioner?
Program:
BOX0=LOC(image=IMAGE,object='shampoo')
BOX1=LOC(image=IMAGE,object='conditioner')
ANSWER0=COUNT(box=BOX0)
ANSWER1=COUNT(box=BOX1)
ANSWER2=EVAL(expr="'unanswerable' if {ANSWER0} == {ANSWER1} else 'shampoo'")
ANSWER3=EVAL(expr="'shampoo' if {ANSWER0} > {ANSWER1} else 'conditioner'")
ANSWER4=EVAL(expr="'unanswerable' if {ANSWER2} == 'unanswerable' else {ANSWER3}")
FINAL_RESULT=RESULT(var=ANSWER4) 
"""

"""Question: Okay I think I got it this time. Can you read the model and serial number for me? Thanks.
Program:
BOX0=LOC(image=IMAGE,object='model number')
IMAGE0=CROP(image=IMAGE,box=BOX0)
BOX1=LOC(image=IMAGE,object='serial number')
IMAGE1=CROP(image=IMAGE,box=BOX1)
ANSWER0=VQA(image=IMAGE0,question='What is the model number?')
ANSWER1=VQA(image=IMAGE1,question='What is the serial number?')
FINAL_RESULT=RESULT(var=ANSWER0, var=ANSWER1) 
"""

"""Question: Which one of the three images is the Google logo?
Program:
ANSWER0=VQA(image=IMAGE,question='Which one of the three images is the Google logo?')
FINAL_RESULT=RESULT(var=ANSWER0) 
"""

"""Question: Where do you think I could get a power cord?
Program:
BOX0=LOC(image=IMAGE,object='location')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER1=EVAL(expr="'store' if {ANSWER0} > 0 else 'unanswerable'")
FINAL_RESULT=RESULT(var=ANSWER1) 
"""

"""Question: Can you tell me what type of sports jersey this is please. If its celtics, lakers, or nets, something like that."
Program:
BOX0=LOC(image=IMAGE,object='sports jersey')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='Is this a celtics, lakers, or nets jersey or is it unanswerable?')
FINAL_RESULT=RESULT(var=ANSWER0) 
"""

"""Question: Please rate the surface"
Program:
BOX0=LOC(image=IMAGE,object='surface')
IMAGE0=CROP(image=IMAGE,box=BOX0)
ANSWER0=VQA(image=IMAGE0,question='What is a rating of the surface?')
FINAL_RESULT=RESULT(var=ANSWER0) 
"""

"""Question: Ok. There is another photograph I hope it is a better one"
Program:
BOX0=LOC(image=IMAGE,object='photograph')
ANSWER0=COUNT(box=BOX0)
ANSWER1=EVAL(expr="'unanswerable' if {BOX0} > 1 else 'yes'")
FINAL_RESULT=RESULT(var=ANSWER1) 
"""

]

def create_prompt(inputs,num_prompts=8,method='random',seed=42,group=0):
    if method=='all':
        prompt_examples = GQA_CURATED_EXAMPLES
    elif method=='random':
        random.seed(seed)
        prompt_examples = random.sample(GQA_CURATED_EXAMPLES,num_prompts)
    else:
        raise NotImplementedError

    prompt_examples = '\n'.join(prompt_examples)
    prompt_examples = f'Think step by step to answer the question.\n\n{prompt_examples}'


    return prompt_examples + "\nQuestion: {question}\nProgram:".format(**inputs)