from keras_core.src.backend import Variable
from keras_core.src.layers.layer import Layer


class TorchModule(Layer):
    def __init__(self, module, name=None):
        super().__init__(name=name)
        self.module = module

    def parameters(self, recurse=True):
        return self.module.parameters(recurse=recurse)

    def build(self, _):
        if not self.built:
            for param in self.module.parameters():
                variable = Variable(value=param, trainable=param.requires_grad)
                self._track_variable(variable)
        self.built = True

    def call(self, *args, **kwargs):
        return self.module.forward(*args, **kwargs)

