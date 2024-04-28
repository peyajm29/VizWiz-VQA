import json
import numpy as np
import re

contractions = {"aint": "ain't", "arent": "aren't", "cant": "can't", "couldve": "could've", "couldnt": "couldn't", \
							 "couldn'tve": "couldn’t’ve", "couldnt’ve": "couldn’t’ve", "didnt": "didn’t", "doesnt": "doesn’t", "dont": "don’t", "hadnt": "hadn’t", \
							 "hadnt’ve": "hadn’t’ve", "hadn'tve": "hadn’t’ve", "hasnt": "hasn’t", "havent": "haven’t", "hed": "he’d", "hed’ve": "he’d’ve", \
							 "he’dve": "he’d’ve", "hes": "he’s", "howd": "how’d", "howll": "how’ll", "hows": "how’s", "Id’ve": "I’d’ve", "I’dve": "I’d’ve", \
							 "Im": "I’m", "Ive": "I’ve", "isnt": "isn’t", "itd": "it’d", "itd’ve": "it’d’ve", "it’dve": "it’d’ve", "itll": "it’ll", "let’s": "let’s", \
							 "maam": "ma’am", "mightnt": "mightn’t", "mightnt’ve": "mightn’t’ve", "mightn’tve": "mightn’t’ve", "mightve": "might’ve", \
							 "mustnt": "mustn’t", "mustve": "must’ve", "neednt": "needn’t", "notve": "not’ve", "oclock": "o’clock", "oughtnt": "oughtn’t", \
							 "ow’s’at": "’ow’s’at", "’ows’at": "’ow’s’at", "’ow’sat": "’ow’s’at", "shant": "shan’t", "shed’ve": "she’d’ve", "she’dve": "she’d’ve", \
							 "she’s": "she’s", "shouldve": "should’ve", "shouldnt": "shouldn’t", "shouldnt’ve": "shouldn’t’ve", "shouldn’tve": "shouldn’t’ve", \
							 "somebody’d": "somebodyd", "somebodyd’ve": "somebody’d’ve", "somebody’dve": "somebody’d’ve", "somebodyll": "somebody’ll", \
							 "somebodys": "somebody’s", "someoned": "someone’d", "someoned’ve": "someone’d’ve", "someone’dve": "someone’d’ve", \
							 "someonell": "someone’ll", "someones": "someone’s", "somethingd": "something’d", "somethingd’ve": "something’d’ve", \
							 "something’dve": "something’d’ve", "somethingll": "something’ll", "thats": "that’s", "thered": "there’d", "thered’ve": "there’d’ve", \
							 "there’dve": "there’d’ve", "therere": "there’re", "theres": "there’s", "theyd": "they’d", "theyd’ve": "they’d’ve", \
							 "they’dve": "they’d’ve", "theyll": "they’ll", "theyre": "they’re", "theyve": "they’ve", "twas": "’twas", "wasnt": "wasn’t", \
							 "wed’ve": "we’d’ve", "we’dve": "we’d’ve", "weve": "we've", "werent": "weren’t", "whatll": "what’ll", "whatre": "what’re", \
							 "whats": "what’s", "whatve": "what’ve", "whens": "when’s", "whered": "where’d", "wheres": "where's", "whereve": "where’ve", \
							 "whod": "who’d", "whod’ve": "who’d’ve", "who’dve": "who’d’ve", "wholl": "who’ll", "whos": "who’s", "whove": "who've", "whyll": "why’ll", \
							 "whyre": "why’re", "whys": "why’s", "wont": "won’t", "wouldve": "would’ve", "wouldnt": "wouldn’t", "wouldnt’ve": "wouldn’t’ve", \
							 "wouldn’tve": "wouldn’t’ve", "yall": "y’all", "yall’ll": "y’all’ll", "y’allll": "y’all’ll", "yall’d’ve": "y’all’d’ve", \
							 "y’alld’ve": "y’all’d’ve", "y’all’dve": "y’all’d’ve", "youd": "you’d", "youd’ve": "you’d’ve", "you’dve": "you’d’ve", \
							 "youll": "you’ll", "youre": "you’re", "youve": "you’ve"}
manualMap    = { 'none': '0',
							  'zero': '0',
							  'one': '1',
							  'two': '2',
							  'three': '3',
							  'four': '4',
							  'five': '5',
							  'six': '6',
							  'seven': '7',
							  'eight': '8',
							  'nine': '9',
							  'ten': '10'
							}
articles     = ['a',
							 'an',
							 'the'
							]
 

periodStrip  = re.compile("(?!<=\d)(\.)(?!\d)")
commaStrip   = re.compile("(\d)(\,)(\d)")
punct        = [';', r"/", '[', ']', '"', '{', '}',
							 '(', ')', '=', '+', '\\', '_', '-',
							 '>', '<', '@', '`', ',', '?', '!']

def process_text(text):
    punctuations = r"[!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~]"
    text = re.sub(punctuations, " ", text.lower())
    return re.sub(r'\s+', ' ', text).strip()

def processPunctuation(inText):
    outText = inText
    for p in punct:
        if (p + ' ' in inText or ' ' + p in inText) or (re.search(commaStrip, inText) != None):
            outText = outText.replace(p, '')
        else:
            outText = outText.replace(p, ' ')	
    outText = periodStrip.sub("", outText, re.UNICODE)
    return outText
	
def processDigitArticle(inText):
    outText = []
    tempText = inText.lower().split()
    for word in tempText:
        word = manualMap.setdefault(word, word)
        if word not in articles:
            outText.append(word)
        else:
            pass
    for wordId, word in enumerate(outText):
        if word in contractions: 
            outText[wordId] = contractions[word]
    outText = ' '.join(outText)
    return outText

def evaluate_accuracy(train_data, results_dict):
    accuracies = []
    for item in train_data:
        image_name = item['image']
        human_answers = [ans['answer'] for ans in item['answers']]
        predicted_answer = results_dict.get(image_name)
        
        if predicted_answer is None:
            continue 

        predicted_answer = predicted_answer.replace('\n', ' ')
        predicted_answer = predicted_answer.replace('\t', ' ')
        predicted_answer = predicted_answer.strip()
        predicted_answer = processPunctuation(predicted_answer)
        predicted_answer = processDigitArticle(predicted_answer)
        answer_counts = {}
        
        for ans in human_answers:
            processed_ans = process_text(ans)
            if processed_ans in answer_counts:
                answer_counts[processed_ans] += 1
            else:
                answer_counts[processed_ans] = 1

        max_match_count = answer_counts.get(predicted_answer, 0)
        accuracy = min(1, max_match_count / 3)
        accuracies.append(accuracy)

    return np.mean(accuracies)

def evaluate_accuracy_by_type(train_data, results_dict):
    accuracies = []
    type_accuracies = {}

    for item in train_data:
        image_name = item['image']
        question_type = item['answer_type']
        human_answers = [ans['answer'] for ans in item['answers']]
        predicted_answer = results_dict.get(image_name)
        
        if predicted_answer is None:
            continue  # Skip if no prediction is available for the image

        predicted_answer = process_text(predicted_answer)
        predicted_answer = predicted_answer.replace('\n', ' ')
        predicted_answer = predicted_answer.replace('\t', ' ')
        predicted_answer = predicted_answer.strip()
        predicted_answer = processPunctuation(predicted_answer)
        predicted_answer = processDigitArticle(predicted_answer)
        answer_counts = {}
        
        # Count how many times each answer appears
        for ans in human_answers:
            processed_ans = process_text(ans)
            if processed_ans in answer_counts:
                answer_counts[processed_ans] += 1
            else:
                answer_counts[processed_ans] = 1

        # Calculate accuracy for this prediction
        max_match_count = answer_counts.get(predicted_answer, 0)
        accuracy = min(1, max_match_count / 3)
        accuracies.append(accuracy)
        
        # Group accuracy by question type
        if question_type not in type_accuracies:
            type_accuracies[question_type] = []
        type_accuracies[question_type].append(accuracy)

    # Return the overall accuracy and accuracies by type
    overall_accuracy = np.mean(accuracies)
    type_accuracy_means = {k: np.mean(v) for k, v in type_accuracies.items()}
    return overall_accuracy, type_accuracy_means


def main():
    # update values here
    gt_file = '/Users/peyamowar/Downloads/MLProject/Annotations/val.json'
    test_file = '/Users/peyamowar/Downloads/MLProject/Annotations/result_val_100.json'

    with open(gt_file) as f:
        train_data = json.load(f)

    with open(test_file) as f:
        results_data = json.load(f)

    results_dict = {item['image']: item['answer'] for item in results_data}


    overall_accuracy = evaluate_accuracy(train_data, results_dict)
    print(f"Number of images answered: {len(results_dict)}")
    print(f"Overall Accuracy: {overall_accuracy * 100:.2f}%")


    answered_count_by_type = {}
    question_types = {item['image']: item['answer_type'] for item in train_data}


    for image_name in results_dict.keys():
        if image_name in question_types:
            q_type = question_types[image_name]
            if q_type in answered_count_by_type:
                answered_count_by_type[q_type] += 1
            else:
                answered_count_by_type[q_type] = 1

    # Print the counts
    for q_type, count in answered_count_by_type.items():
        print(f"Number of images answered for '{q_type}': {count}")

    # Run evaluation
    overall_accuracy, type_accuracy_means = evaluate_accuracy_by_type(train_data, results_dict)
    for q_type, acc in type_accuracy_means.items():
        print(f"Accuracy for '{q_type}': {acc * 100:.2f}%")

if __name__ == "__main__":
    main()