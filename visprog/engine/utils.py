import os
from PIL import Image
# from openai import OpenAI
import numpy as np
import copy
import openai

from .step_interpreters import register_step_interpreters, parse_step


class Program:
    def __init__(self,prog_str,init_state=None):
        self.prog_str = prog_str
        self.state = init_state if init_state is not None else dict()
        self.instructions = self.prog_str.split('\n')


class ProgramInterpreter:
    def __init__(self,dataset='nlvr'):
        self.step_interpreters = register_step_interpreters(dataset)

    def execute_step(self,prog_step,inspect):
        print('Here is the program step string name: ', prog_step.prog_str)
        step_name = parse_step(prog_step.prog_str,partial=True)['step_name']
        print('Here is the parsed program step name: ', step_name)
        return self.step_interpreters[step_name].execute(prog_step,inspect)

    def execute(self,prog,init_state,inspect=False):
        if isinstance(prog,str):
            prog = Program(prog,init_state)
        else:
            assert(isinstance(prog,Program))

        prog_steps = [Program(instruction,init_state=prog.state) \
            for instruction in prog.instructions]

        html_str = '<hr>'
        for prog_step in prog_steps:
            if inspect:
                step_output, step_html = self.execute_step(prog_step,inspect)
                html_str += step_html + '<hr>'
            else:
                step_output = self.execute_step(prog_step,inspect)

        if inspect:
            return step_output, prog.state, html_str

        return step_output, prog.state


class ProgramGenerator():
    def __init__(self,prompter,temperature=0.7,top_p=0.5,prob_agg='mean'):
        # openai.api_key = os.getenv("OPENAI_API_KEY")

        # Addd Your Own API Key Here
        API_KEY = ""
        openai.api_key = API_KEY

        self.prompter = prompter
        self.temperature = temperature
        self.top_p = top_p
        self.prob_agg = prob_agg

    def compute_prob(self,response):
        eos = '<|endoftext|>'

        for i, token_info in enumerate(response.choices[0]['logprobs']['content']):
            token = token_info['token']
            if token == eos:
                break

        if self.prob_agg == 'mean':
            agg_fn = np.mean
        elif self.prob_agg == 'sum':
            agg_fn = np.sum
        else:
            raise NotImplementedError

        token_logprobs = [token_info['logprob'] for token_info in response.choices[0]['logprobs']['content']]
        return np.exp(agg_fn(token_logprobs[:i]))

    def custom_prompter(self, inputs):
        # This method should prepare the chat message from the inputs
        return [{"role": "system", "content": "You are generating code program instructions to run modules that will understand and segment images to answer a visual question. You will be given multiple examples of a question followed by a program instruction by the user. Use the same naming conventions for the variables in the code. If a question is repeated from the given examples, provide the same program instructions anyways. Also note that the resulting answer from following the programming instructions may possibly be 'unanswerable' depending on the given question"},
                {"role": "user", "content": self.prompter(inputs)}]

    def generate(self, inputs):
        # See the following reference: https://stackoverflow.com/questions/77789886/openai-api-error-the-model-text-davinci-003-has-been-deprecated

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=self.custom_prompter(inputs),
            temperature=self.temperature,
            max_tokens=512,
            top_p=self.top_p,
            frequency_penalty=0,
            presence_penalty=0,
            n=1,
            logprobs=True
        )

        prob = self.compute_prob(response)
        prog = response['choices'][0]['message']['content'].strip()
        return prog, prob
    
    

    