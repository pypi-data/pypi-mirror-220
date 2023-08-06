from .._common import _before_generate, _after_generate, _is_monkey_patched
from langchain.llms import OpenAI as _orig_OpenAI
from typing import (
    Any,
    Optional,
    List
)
from langchain.callbacks.manager import (
    CallbackManagerForLLMRun
)

_orig_generate = _orig_OpenAI._generate
def _custom_ps_generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ):
    if not _is_monkey_patched(): # if monkey patched - the hook would already be called
        _before_generate(self, prompts, stop, run_manager, **kwargs)
    r = _orig_generate(self, prompts, stop, run_manager, **kwargs)
    if not _is_monkey_patched(): # if monkey patched - the hook would already be called
        _after_generate(self, r)
    return r

class OpenAI(_orig_OpenAI):
    pass

OpenAI._generate = _custom_ps_generate
