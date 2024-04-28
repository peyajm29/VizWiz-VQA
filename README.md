# vizprog
VizWiz-VQA challenge experiments 

## Install dependencies

To install the dependencies, run the following commands:

```
conda env create -f environment.yaml
conda activate vizwiz-vqa
```

## Repository Structure

Here is the structure of the repository:

```
vizprog
│   README.md
│   environment.yaml
│   gpt4-turbo-vision
│   |   gpt-vqa.py
│   |   outputs
│   |   |   results-train.json
│   |   |   results-val.json
│   |   |   results-test.json
│   |   |   results-train-number.json
│   |   |   results-val-number.json
│   |   |   results-train-yesno.json
│   |   |   results-val-yesno.json
│   visprog
|   |   visprog-vqa.py
|   |   outputs
|   |   |   result_train_100.json
|   |   |   result_val_100.json
|   |   |   result_test_100.json
|   |   engine
|   |   |   nms.py
|   |   |   step_interpreters.py
|   |   |   utils.py
|   |   |   vis_utils.py
|   |   prompts
|   |   |   gqa.py
│   evaluation
|   |   eval-accuracy.py
|   |   mt-metrics.py
|   |   API
|   |   |   PythonEvaluationTools
|   |   |   PythonHelperTools
│   data
│   |   train.json
│   |   val.json
│   |   test.json
```

## References to borrowed code and datasets:
- [VisProg](https://github.com/allenai/visprog)
- [Evaluation](https://vizwiz.org/tasks-and-datasets/vqa/)
- [Data](https://vizwiz.org/tasks-and-datasets/vqa/)

## Our Contributions

### GPT4-Turbo-Vision:
- gpt-vqa.py

### VisProg:
- visprog-vqa.py
- gqa.py (modified: added additional prompts)
- utils.py (modified: error handling, updated program generator model to gpt-3.5-turbo-0125, customised system prompt)
- step_interpreters.py (modified: added parsing functions)

### Evaluation:
- eval-accurracy.py (modified: added accuracy by question-type)