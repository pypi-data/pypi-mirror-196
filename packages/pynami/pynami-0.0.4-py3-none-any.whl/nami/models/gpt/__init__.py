from transformers import AutoConfig, AutoModelForCausalLM

from .modeling_gpt import GPTModel, GPTConfig

AutoConfig.register("nami_gpt", GPTConfig)
AutoModelForCausalLM.register(GPTConfig, GPTModel)
