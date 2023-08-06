from franky.hooks import Hook
from nami.registry import HOOKS


@HOOKS.register_module()
class SavePretrainedHook(Hook):
    priority = 'BELOW_NORMAL'

    def before_load_checkpoint(self, runner, ckpt_dir) -> None:
        runner._has_loaded = True

    def before_save_checkpoint(self, runner, checkpoint, ckpt_dir):
        checkpoint.pop('state_dict')
        runner.model.save_pretrained(ckpt_dir)
        for val in runner.train_dataloader.collate_fn.__dict__.values():
            if hasattr(val, 'save_pretrained'):
                val.save_pretrained(ckpt_dir)
