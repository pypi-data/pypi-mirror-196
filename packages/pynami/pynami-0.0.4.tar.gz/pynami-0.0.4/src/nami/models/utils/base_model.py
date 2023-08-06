from collections import defaultdict

from transformers import PreTrainedModel, PretrainedConfig

from franky.model import BaseModel
from nami.registry import MODELS, CONFIGS


class Config(PretrainedConfig):
    pass


class HFModel(PreTrainedModel, BaseModel):
    config_class = Config

    def __init__(self, *args, init_cfg=None, **kwargs):
        if not args:
            config = defaultdict(dict)
            models = dict()
            for k, v in kwargs.items():
                model = MODELS.build(v)
                if hasattr(model, 'config'):
                    config[k]['config_type'] = v['config_type']
                    config[k]['model_type'] = v['model_type']
                    config[k]['_config'] = model.config.to_dict()
                else:
                    config[k] = v
                models[k] = model
            config = self.config_class.from_dict(config)
            super().__init__(config)
            for k, v in models.items():
                setattr(self, k, v)
            del models
        else:
            super().__init__(args[0])
            for k, v in args[0].to_dict().items():
                if not isinstance(v, dict):
                    continue
                if 'type' in v:
                    v = MODELS.build(v)
                elif 'config_type' in v and 'model_type' in v:
                    config = CONFIGS.build(dict(type=v['config_type'], **v['_config']))
                    v = MODELS.build(dict(type=v['model_type'], config=config))
                setattr(self, k, v)

    def init_weights(self):
        BaseModel.init_weights(self)

    def prepare_inputs_for_generation(self, input_ids, past_key_values=None, **kwargs):
        token_type_ids = kwargs.get("token_type_ids", None)
        # only last token for inputs_ids if past is defined in kwargs
        if past_key_values:
            input_ids = input_ids[:, -1].unsqueeze(-1)
            if token_type_ids is not None:
                token_type_ids = token_type_ids[:, -1].unsqueeze(-1)

        attention_mask = kwargs.get("attention_mask", None)
        position_ids = kwargs.get("position_ids", None)

        if attention_mask is not None and position_ids is None:
            # create position_ids on the fly for batch generation
            position_ids = attention_mask.long().cumsum(-1) - 1
            position_ids.masked_fill_(attention_mask == 0, 1)
            if past_key_values:
                position_ids = position_ids[:, -1].unsqueeze(-1)
        else:
            position_ids = None
        return {
            "input_ids": input_ids,
            "past_key_values": past_key_values,
            "use_cache": kwargs.get("use_cache"),
            "position_ids": position_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids,
        }


@MODELS.register_module()
class NamiAutoModel:
    @classmethod
    def from_config(
            cls,
            model_type='AutoModel',
            config_type='AutoConfig',
            config_pretrained=None,
            model_pretrained=None,
            **kwargs
    ):
        if model_pretrained:
            model = MODELS.build(dict(type=model_type, pretrained=model_pretrained, **kwargs))
        else:
            config = CONFIGS.build(dict(type=config_type, pretrained=config_pretrained, **kwargs))
            model = MODELS.build(dict(type=model_type, config=config))

        return model
