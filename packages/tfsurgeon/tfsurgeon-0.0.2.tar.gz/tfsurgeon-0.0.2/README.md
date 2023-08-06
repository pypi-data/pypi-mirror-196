# TFSurgeon

Allows for dynamic tensorflow keras model edition.
You can install this package with pip and call it as `from tfsurgeon import edit_model`.

## How to use

- [x] remove layers based on layer type
- [x] remove layers based on name or index
- [x] replace layers from one type to another
- [x] replace specific layer (name) by another layer (callable)

see docstring for examples in `src/tfsurgeon/tfsurgeon.py`.

### import

```
from tfsurgeon import edit_model
import tensorflow as tf

model = tf.keras.applications.MobileNetV2(weights=None)
new_model = edit_model(
    model=model,
    replace_layers_by_types=[
        [tf.keras.layers.BatchNormalization, tf.keras.layers.LayerNormalization]
    ],
    verbose=True,
)
```

### CLI

no supported yet