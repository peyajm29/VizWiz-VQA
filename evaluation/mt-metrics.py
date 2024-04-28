import json
from API.PythonEvaluationTools.vqaEvaluation.pycocoevalcap.tokenizer.ptbtokenizer import PTBTokenizer
from API.PythonEvaluationTools.vqaEvaluation.pycocoevalcap.bleu.bleu import Bleu
from API.PythonEvaluationTools.vqaEvaluation.pycocoevalcap.rouge.rouge import Rouge
from API.PythonEvaluationTools.vqaEvaluation.pycocoevalcap.cider.cider import Cider

def evaluate(gts, res):
    tokenizer = PTBTokenizer()
    gts  = tokenizer.tokenize(gts)
    res = tokenizer.tokenize(res)
    scorers = [
        (Bleu(4), ["Bleu_1", "Bleu_2", "Bleu_3", "Bleu_4"]),
        (Rouge(), "ROUGE_L"),
        (Cider(), "CIDEr")
    ]
    for scorer, method in scorers:
        score, scores = scorer.compute_score(gts, res)
        if type(method) == list:
            for sc, scs, m in zip(score, scores, method):
                print("%s: %0.3f"%(m, sc))
        else:
            print("%s: %0.3f"%(method, score))

def setEval(score, method):
    eval[method] = score

def main():
    # update values here
    gt_file = '/Users/peyamowar/Downloads/MLProject/Annotations/val.json'
    test_file = '/Users/peyamowar/Downloads/MLProject/Annotations/result_val_100.json'

    with open(gt_file) as f:
        train_data = json.load(f)

    with open(test_file) as f:
        results_data = json.load(f)

    results_dict = {item['image']: item['answer'] for item in results_data}
    train_dict = {item['image']: item['answers'] for item in train_data}

    image_id = []
    answers = []
    for img_id, sentences in train_dict.items():
        if (img_id not in results_dict):
            continue
        image_id.append(img_id)
        answer = []
        for sentence in sentences:
            answer.append(sentence['answer'])
        answers.append(answer)

    gts = {img_id: [{'caption': a} for a in answer] for img_id, answer in zip(image_id, answers)}
    res = {img_id: [{'caption': sentences}] for img_id, sentences in results_dict.items()}

    print(evaluate(gts, res))

if __name__ == '__main__':
    main()