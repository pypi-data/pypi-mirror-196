transformers_pretrained_model_dir = '/datasets/models/gpts/gpt2-chinese'

# model settings
# config_gpt2 = dict(
#     type='GPT2Config',
#     pretrained=transformers_pretrained_model_dir,
# )
#
model = dict(
    type='GPTModel',
    gpt=dict(
        type='NamiAutoModel',
        model_type='GPT2LMHeadModel',
        config_type='GPT2Config',
        config_pretrained=transformers_pretrained_model_dir,
        model_pretrained=transformers_pretrained_model_dir,
    ),
    # pretrained='/home/xxx/projects/nlp_app/x',
    loss=dict(type='CrossEntropyLoss', loss_weight=1.0),
)
