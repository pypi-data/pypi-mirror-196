from typing import Optional

import franky.dist as dist
from nami.registry import DATASETS
from .base_dataset import BaseDataset


@DATASETS.register_module()
class GPTDataset(BaseDataset):
    def __init__(self,
                 ann_file: str,
                 test_mode: bool,
                 metainfo: Optional[dict] = None,
                 data_root: str = '',
                 **kwargs):
        super().__init__(
            ann_file=ann_file,
            metainfo=metainfo,
            data_root=data_root,
            test_mode=test_mode,
            **kwargs)

    def load_data_list(self):
        file = self.ann_file

        dist.barrier()

        texts = []
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                texts.append(line)

        data_list = []
        for text in texts:
            info = {'text': text}
            data_list.append(info)
        return data_list
