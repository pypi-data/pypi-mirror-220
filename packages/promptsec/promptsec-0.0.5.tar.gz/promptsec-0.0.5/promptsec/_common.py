import requests
import json
import langchain.schema.output
from langchain.chains.base import Chain as BaseChainClass
import inspect

from typing import (
    AbstractSet,
    Any,
)
import logging
logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)

_monkey_patched_flag = False

g_api_key = ''
def _set_api_key(api_key):
    global g_api_key
    logging.info(f"PSEC: register api_key='{api_key}'")
    g_api_key = api_key

def _send_siem(log):
    url = "https://dash2.prompt-security.com/api/log-sdk/v1"
    request_body = json.dumps(log)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=request_body, headers=headers)
    if response.status_code != 200:
        logging.info("PSEC: send failed:", response.status_code)

def _before_generate(self, *args : Any, **kwargs : Any):
    # Collect list of chain objects from the call stack
    llm_inputs = None
    chains = []
    call_stack = inspect.stack()
    run_id = None
    run_seq = None
    for frame in call_stack:
        # check that the frame represents a call to function named _call which is a method of a class (has 'self')
        if frame[3] != '_call' or 'self' not in frame[0].f_locals: continue
        chain = frame[0].f_locals['self']
        # only consider classes that inherit from the abstract base class "Chain"
        if not (issubclass(type(chain), BaseChainClass)): continue
        if 'inputs' in frame[0].f_locals and llm_inputs == None:
            llm_inputs = frame[0].f_locals['inputs']
        chains.append(chain)
        if 'run_manager' in frame[0].f_locals:
            run_manager = frame[0].f_locals['run_manager']
            if '__psec_seq' not in run_manager.__dict__:
                run_manager.__dict__['__psec_seq'] = 1
            else:
                run_manager.__dict__['__psec_seq'] += 1
            run_seq = run_manager.__dict__['__psec_seq']
            run_id = run_manager.run_id.hex

    # Collect chain_path and prompt_info
    prompt_info = None
    chain_path = []
    last_chain = None
    for chain in chains:
        chainClassName = chain.__class__.__name__
        if isinstance(chain, langchain.chains.llm.LLMChain):
            prompt = chain.prompt
            llm_type = chain.llm.__class__.__name__
            chain_path.insert(0, f"{chainClassName}({llm_type})")

            # Add prompt details
            if prompt_info == None:
                prompt_info = {}
                if 'input_variables' in prompt.__dict__ and type(prompt.input_variables) is list:
                    prompt_info["input_variables"] = prompt.input_variables
                if 'template' in prompt.__dict__ and type(prompt.template) is str:
                    prompt_info["template"]=prompt.template
                if 'template_format' in prompt.__dict__ and type(prompt.template_format) is str:
                    prompt_info["template_format"] = prompt.template_format
        elif isinstance(chain, langchain.chains.transform.TransformChain):
            transform_id = id(chain.transform)
            chain_path.insert(0, f"{chainClassName}({transform_id})")
        elif isinstance(chain, langchain.chains.sequential.SequentialChain) or isinstance(chain, langchain.chains.sequential.SimpleSequentialChain):
            lastChainIndex = chain.chains.index(last_chain) if last_chain in chain.chains else -1
            chain_path.insert(0, f"{chainClassName}[{lastChainIndex}]")
        elif isinstance(chain, langchain.chains.llm_requests.LLMRequestsChain):
            url = chain.input_key
            chain_path.insert(0, f"{chainClassName}(url={url})")
        elif isinstance(chain, langchain.chains.moderation.OpenAIModerationChain):
            input_key = chain.input_key
            chain_path.insert(0, f"{chainClassName}(input_key={input_key})")
        else:
            # all other LLM chain types treated generically
            chain_path.insert(0, f"{chainClassName}")
        # Remember last chain
        last_chain = chain

    prompts, stop, run_manager = args
    self.__dict__['__psec_log_data'] = {
        'api_key': g_api_key,
        'llm_provider': self.__class__.__name__,
        'temperature': getattr(self, 'temperature', -1),
        'prompts': prompts[:],
        'response': '',
        'chain_path': '->'.join(chain_path),
    }
    if prompt_info:
        self.__dict__['__psec_log_data']['prompt_info'] = prompt_info
    if llm_inputs != None:
        self.__dict__['__psec_log_data']['inputs'] = json.dumps(llm_inputs)
    if run_id:
        self.__dict__['__psec_log_data']['run_id'] = run_id
    if run_seq:
        self.__dict__['__psec_log_data']['run_seq'] = run_seq

def _after_generate(self, r : langchain.schema.output.LLMResult):
    #logging.info(f"PSEC: Hook after generate: generations={r.generations}")
    #logging.info(f"PSEC: Hook after generate: llm_output={r.llm_output}")
    #logging.info(f"PSEC: Hook after generate: run={r.run}")
    self.__dict__['__psec_log_data']['model_name'] = r.llm_output['model_name']
    self.__dict__['__psec_log_data']['token_usage'] = json.dumps(r.llm_output['token_usage'])
    for generationList in r.generations:
        for generation in generationList:
            gen_text = getattr(generation, 'text', '')
            self.__dict__['__psec_log_data']['response'] += gen_text
    # Send log to SIEM
    #print(json.dumps(self.__dict__['__psec_log_data'], indent=2))
    _send_siem(self.__dict__['__psec_log_data'])

def _set_monkey_patched():
    global _monkey_patched_flag
    logging.info(f"Monkey patch installed.")
    _monkey_patched_flag = True

def _is_monkey_patched():
    return _monkey_patched_flag
