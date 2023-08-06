import inspect

import transformers
from transformers import AutoConfig, AutoTokenizer, PreTrainedModel, PreTrainedTokenizerBase, PretrainedConfig
from transformers.models.auto.auto_factory import _BaseAutoModelClass

from franky.logging import FrankyLogger
from nami.registry import MODELS, TOKENIZERS, CONFIGS

logger = FrankyLogger.get_current_instance()

TOKENIZERS.register_module(module=AutoTokenizer)
CONFIGS.register_module(module=AutoConfig)


def register_transformers_models():
    """Register models in ``transformers.models`` to the ``MODELS`` registry,
    register tokenizer to the ``TOKENIZERS`` registry.
    """
    for module_name in dir(transformers.models):
        if module_name.startswith('__'):
            continue
        modules = getattr(transformers.models, module_name)
        for module_name in dir(modules):
            if module_name.startswith('__'):
                continue
            try:
                model = getattr(modules, module_name)
            except AttributeError as e:
                logger.warning(e)
                continue
            if inspect.isclass(model):
                if issubclass(model, PreTrainedModel):
                    MODELS.register_module(module=model)
                elif issubclass(model, PreTrainedTokenizerBase):
                    TOKENIZERS.register_module(module=model)
                elif issubclass(model, PretrainedConfig):
                    CONFIGS.register_module(module=model)


def register_transformers_automodel():
    for module_name in dir(transformers.models.auto):
        if module_name.startswith('__'):
            continue
        module = getattr(transformers.models.auto, module_name)
        if inspect.isclass(module) and issubclass(module, _BaseAutoModelClass):
            MODELS.register_module(module=module)
