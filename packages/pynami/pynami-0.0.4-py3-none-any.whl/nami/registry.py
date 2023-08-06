from franky.registry import COLLATE as FRANKY_COLLATE
from franky.registry import DATASETS as FRANKY_DATASETS
from franky.registry import DATA_SAMPLERS as FRANKY_DATA_SAMPLERS
from franky.registry import EVALUATOR as FRANKY_EVALUATOR
from franky.registry import HOOKS as FRANKY_HOOKS
from franky.registry import LOG_PROCESSORS as FRANKY_LOG_PROCESSORS
from franky.registry import LOOPS as FRANKY_LOOPS
from franky.registry import METRICS as FRANKY_METRICS
from franky.registry import MODELS as FRANKY_MODELS
from franky.registry import MODEL_WRAPPERS as FRANKY_MODEL_WRAPPERS
from franky.registry import OPTIMIZERS as FRANKY_OPTIMIZERS
from franky.registry import OPTIM_WRAPPERS as FRANKY_OPTIM_WRAPPERS
from franky.registry import OPTIM_WRAPPER_CONSTRUCTORS as FRANKY_OPTIM_WRAPPER_CONSTRUCTORS
from franky.registry import PARAM_SCHEDULERS as FRANKY_PARAM_SCHEDULERS
from franky.registry import RUNNERS as FRANKY_RUNNERS
from franky.registry import RUNNER_CONSTRUCTORS as FRANKY_RUNNER_CONSTRUCTORS
from franky.registry import Registry
from franky.registry import TASK_UTILS as FRANKY_TASK_UTILS
from franky.registry import TRANSFORMS as FRANKY_TRANSFORMS
from franky.registry import VISBACKENDS as FRANKY_VISBACKENDS
from franky.registry import VISUALIZERS as FRANKY_VISUALIZERS
from franky.registry import WEIGHT_INITIALIZERS as FRANKY_WEIGHT_INITIALIZERS

#######################################################################
#                            nami.engine                             #
#######################################################################
# Runners like `EpochBasedRunner` and `IterBasedRunner`
RUNNERS = Registry(
    'runner',
    parent=FRANKY_RUNNERS,
    locations=['nami.engine'],
)
# Runner constructors that define how to initialize runners
RUNNER_CONSTRUCTORS = Registry(
    'runner constructor',
    parent=FRANKY_RUNNER_CONSTRUCTORS,
    locations=['nami.engine'],
)
# Loops which define the training or test process, like `EpochBasedTrainLoop`
LOOPS = Registry(
    'loop',
    parent=FRANKY_LOOPS,
    locations=['nami.engine'],
)
# Hooks to add additional functions during running, like `CheckpointHook`
HOOKS = Registry(
    'hook',
    parent=FRANKY_HOOKS,
    locations=['nami.hooks'],
)
# Log processors to process the scalar log data.
LOG_PROCESSORS = Registry(
    'log processor',
    parent=FRANKY_LOG_PROCESSORS,
    locations=['nami.engine'],
)
# Optimizers to optimize the model weights, like `SGD` and `Adam`.
OPTIMIZERS = Registry(
    'optimizer',
    parent=FRANKY_OPTIMIZERS,
    locations=['nami.engine'],
)
# Optimizer wrappers to enhance the optimization process.
OPTIM_WRAPPERS = Registry(
    'optimizer_wrapper',
    parent=FRANKY_OPTIM_WRAPPERS,
    locations=['nami.engine'],
)
# Optimizer constructors to customize the hyperparameters of optimizers.
OPTIM_WRAPPER_CONSTRUCTORS = Registry(
    'optimizer wrapper constructor',
    parent=FRANKY_OPTIM_WRAPPER_CONSTRUCTORS,
    locations=['nami.engine'],
)
# Parameter schedulers to dynamically adjust optimization parameters.
PARAM_SCHEDULERS = Registry(
    'parameter scheduler',
    parent=FRANKY_PARAM_SCHEDULERS,
    locations=['nami.engine'],
)

#######################################################################
#                           nami.datasets                             #
#######################################################################

# Datasets like `ImageNet` and `CIFAR10`.
DATASETS = Registry(
    'dataset',
    parent=FRANKY_DATASETS,
    locations=['nami.datasets'],
)
# Samplers to sample the dataset.
DATA_SAMPLERS = Registry(
    'data sampler',
    parent=FRANKY_DATA_SAMPLERS,
    locations=['nami.datasets'],
)
# Transforms to process the samples from the dataset.
TRANSFORMS = Registry(
    'transform',
    parent=FRANKY_TRANSFORMS,
    locations=['nami.datasets'],
)
COLLATE = Registry(
    'collate',
    parent=FRANKY_COLLATE,
    locations=['nami.datasets'],
)

#######################################################################
#                            nami.models                             #
#######################################################################
# Configs
CONFIGS = Registry(
    'configs',
    locations=['nami.models']
)
# Tokenizers
TOKENIZERS = Registry(
    'tokenizer',
    locations=['nami.models'],
)
# Neural network modules inheriting `nn.Module`.
MODELS = Registry(
    'model',
    parent=FRANKY_MODELS,
    locations=['nami.models', 'nami.losses'],
)
# Model wrappers like 'MMDistributedDataParallel'
MODEL_WRAPPERS = Registry(
    'model_wrapper',
    parent=FRANKY_MODEL_WRAPPERS,
    locations=['nami.models'],
)
# Weight initialization methods like uniform, xavier.
WEIGHT_INITIALIZERS = Registry(
    'weight initializer',
    parent=FRANKY_WEIGHT_INITIALIZERS,
    locations=['nami.models'],
)
# Batch augmentations like `Mixup` and `CutMix`.
BATCH_AUGMENTS = Registry(
    'batch augment',
    locations=['nami.models'],
)
# Task-specific modules like anchor generators and box coders
TASK_UTILS = Registry(
    'task util',
    parent=FRANKY_TASK_UTILS,
    locations=['nami.models'],
)

#######################################################################
#                          nami.evaluation                           #
#######################################################################

# Metrics to evaluate the model prediction results.
METRICS = Registry(
    'metric',
    parent=FRANKY_METRICS,
    locations=['nami.evaluation'],
)
# Evaluators to define the evaluation process.
EVALUATORS = Registry(
    'evaluator',
    parent=FRANKY_EVALUATOR,
    locations=['nami.evaluation'],
)

#######################################################################
#                         nami.visualization                         #
#######################################################################

# Visualizers to display task-specific results.
VISUALIZERS = Registry(
    'visualizer',
    parent=FRANKY_VISUALIZERS,
    locations=['nami.visualization'],
)
# Backends to save the visualization results, like TensorBoard, WandB.
VISBACKENDS = Registry(
    'vis_backend',
    parent=FRANKY_VISBACKENDS,
    locations=['nami.visualization'],
)
