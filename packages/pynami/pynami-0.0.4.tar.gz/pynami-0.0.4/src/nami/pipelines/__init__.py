from transformers import AutoModelForCausalLM
from transformers.pipelines import PIPELINE_REGISTRY, TextGenerationPipeline


SUPPORTED_TASKS = {
    "text-generation": {
        "pipeline_class": TextGenerationPipeline,
        "pt_model": AutoModelForCausalLM,
        "type": "text",  # current support type: text, audio, image, multimodal
    }
}

for task, pipeline in SUPPORTED_TASKS.items():
    PIPELINE_REGISTRY.register_pipeline(task, **pipeline)
