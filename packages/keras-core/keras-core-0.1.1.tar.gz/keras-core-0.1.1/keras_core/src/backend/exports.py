from keras_core.src import backend
from keras_core.src.api_export import keras_core_export

if backend.backend() == "tensorflow":
    BackendVariable = backend.tensorflow.core.Variable
elif backend.backend() == "jax":
    BackendVariable = backend.jax.core.Variable
elif backend.backend() == "torch":
    BackendVariable = backend.torch.core.Variable
else:
    raise RuntimeError("Invalid backend.")


@keras_core_export("keras_core.backend.Variable")
class Variable(BackendVariable):
    pass

