from .base_model import HFModel, NamiAutoModel, Config
from .builder import register_transformers_automodel, register_transformers_models

register_transformers_automodel()
register_transformers_models()
