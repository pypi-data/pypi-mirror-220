import requests
import json
import langchain.schema.output
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
    prompts, stop, run_manager = args
    self.__dict__['__psec_log_data'] = {
        'api_key': g_api_key,
        'llm_provider': self.__class__.__name__,
        'temperature': getattr(self, 'temperature', -1),
        'prompts': prompts[:],
        'response': ''
    }

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
