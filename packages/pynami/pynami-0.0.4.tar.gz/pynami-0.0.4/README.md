* nami = not an mmlab implementation
* 原先基于mmengine，现fork了mmengine并改为franky
* 安装：pip install pynami
* 模型需要继承自：HFModel，并实现forward方法
* 预训练的模型使用pretrained关键字
* 当子模块模型基于transformers时需要：
  * type为NamiAutoModel
  * model_type和config_type必须
  * config_pretrained和model_pretrained优先级
    1. model_pretrained
    2. config_pretrained
    3. None
* 新增transformers保存模型和预处理对应钩子

