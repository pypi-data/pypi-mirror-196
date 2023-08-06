from nami.registry import COLLATE
from nami.registry import TOKENIZERS


@COLLATE.register_module()
class GPTCollate:
    def __init__(self, tokenizer, max_length=512, ignore_index=-100, **kwargs):
        self.tokenizer = TOKENIZERS.build(tokenizer)
        self.max_length = max_length
        self.ignore_index = ignore_index

    def _align(self, texts):
        tokens = self.tokenizer(texts, padding=True, truncation=True, max_length=self.max_length, return_tensors="pt")

        return tokens

    def __call__(self, data_batch):
        # list of dict to dict of list
        data = {k: [dic[k] for dic in data_batch] for k in data_batch[0]}
        tokens = self._align(data['text'])

        return tokens
