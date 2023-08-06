import langchain.schema.output
from typing import (
    AbstractSet,
    Any,
)
import logging
logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)

_monkey_patched_flag = False

def _before_generate(*args : Any, **kwargs : Any):
    prompts, stop, run_manager = args
    logging.info(f"PSEC: Hook before generate: prompts: {', '.join(prompts)}")

def _after_generate(r : langchain.schema.output.LLMResult):
    logging.info(f"PSEC: Hook after generate: generations={r.generations}")
    logging.info(f"PSEC: Hook after generate: llm_output={r.llm_output}")
    logging.info(f"PSEC: Hook after generate: run={r.run}")

def _set_monkey_patched():
    global _monkey_patched_flag
    logging.info(f"Monkey patch installed.")
    _monkey_patched_flag = True

def _is_monkey_patched():
    return _monkey_patched_flag

