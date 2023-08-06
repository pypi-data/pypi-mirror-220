from .._common import _before_generate, _after_generate, _set_monkey_patched
from langchain.llms import OpenAI as _orig_OpenAI
from typing import (
    Any,
    Optional,
    List
)
from langchain.callbacks.manager import (
    CallbackManagerForLLMRun
)
# TODO: also patch the async method _agenerate()
orig_generate = _orig_OpenAI._generate
def _custom_ps_generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ):
    _before_generate(self, prompts, stop, run_manager, **kwargs)
    r = orig_generate(self, prompts, stop, run_manager, **kwargs)
    _after_generate(self, r)
    return r

_orig_OpenAI._generate = _custom_ps_generate
_set_monkey_patched()
