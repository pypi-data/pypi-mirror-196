from nami.registry import MODELS
from ..utils import HFModel, Config


class GPTConfig(Config):
    model_type = 'nami_gpt'


@MODELS.register_module()
class GPTModel(HFModel):
    config_class = GPTConfig

    def forward(
            self,
            input_ids=None,
            past_key_values=None,
            attention_mask=None,
            token_type_ids=None,
            position_ids=None,
            head_mask=None,
            inputs_embeds=None,
            encoder_hidden_states=None,
            encoder_attention_mask=None,
            labels=None,
            use_cache=None,
            output_attentions=None,
            output_hidden_states=None,
            return_dict=None,
            mode: str = 'pred', **kwargs):
        output = self.gpt(
            input_ids=input_ids,
            past_key_values=past_key_values,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            encoder_attention_mask=encoder_attention_mask,
            labels=None,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict
        )
        self.input_ids = input_ids
        self.labels = labels
        if mode == 'train':
            loss = self._get_loss(output, input_ids, labels)
            return dict(loss=loss)
        elif mode == 'eval':
            loss = self._get_loss(output, input_ids, labels)
            return dict(loss=loss),
        else:
            return output

    def _get_loss(self, output, input_ids, labels):
        shift_logits = output.logits[..., :-1, :].contiguous()
        if labels is None:
            labels = input_ids
        shift_labels = labels[..., 1:].contiguous()
        loss = self.loss(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))

        return loss
