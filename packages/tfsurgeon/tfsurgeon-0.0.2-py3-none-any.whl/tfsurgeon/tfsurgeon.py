if __name__ == "__main__":
    import os

    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from .utils.replace_type_editor import replace_layers_by_types_in_model
from .utils.remove_type_editor import remove_layers_by_types_in_model
from .utils.replace_by_counter import replace_layers_by_counterparts_in_model
from .utils.remove_by_names import remove_layers_by_names_or_indices_in_model
import tensorflow as tf
from typing import Optional, List, Tuple, Type, Dict, Union, Any


def edit_model(
    model: tf.keras.Model,
    remove_by_name: Optional[List[Union[str, int]]] = None,
    replace_layers_by_provided_counter_parts: Optional[
        Dict[str, tf.keras.layers.Layer]
    ] = None,
    replace_layers_by_types: Optional[List[Tuple[Type, Type]]] = None,
    remove_layer_by_types: Optional[List[Type]] = None,
    extra_args: Dict[str, Any] = None,
    verbose: bool = False,
) -> tf.keras.Model:
    """
    The purpose of this project is to provide an easy way to replace or remove layes in a tensorflow model.
    Note: this method will not apply pruning or tensor decomposition.


    Examples:

    >>> model = tf.keras.applications.MobileNetV2(weights=None)
    >>> new_model = edit_model(
    ...     model=model,
    ...     remove_by_name=[2, -3, "block_16_depthwise_BN"],
    ...     verbose=True,
    ... )
    [RemoveLayersByName] [===============]
    +---------------------------------------+
    |          mobilenetv2_1.00_224         |
    +---------------------------------------+
    | removed layers              | 3       |
    | kept layers                 | 153     |
    +---------------------------------------+


    >>> model = tf.keras.applications.MobileNetV2(weights=None)
    >>> new_model = edit_model(
    ...     model=model,
    ...     replace_layers_by_types=[
    ...         [tf.keras.layers.BatchNormalization, tf.keras.layers.LayerNormalization]
    ...     ],
    ...     verbose=True,
    ... )
    [ReplaceLayersByType] [===============]
    +---------------------------------------+
    |          mobilenetv2_1.00_224         |
    +---------------------------------------+
    | modified layers             | 52      |
    | unmodified layers           | 104     |
    +---------------------------------------+

    >>> model = tf.keras.applications.MobileNetV2(weights=None)
    >>> new_model = edit_model(
    ...     model=model,
    ...     remove_layer_by_types=[tf.keras.layers.BatchNormalization],
    ...     verbose=True,
    ... )
    [RemoveLayersByType] [===============]
    +---------------------------------------+
    |          mobilenetv2_1.00_224         |
    +---------------------------------------+
    | removed layers              | 52      |
    | kept layers                 | 104     |
    +---------------------------------------+

    >>> model = tf.keras.applications.MobileNetV2(weights=None)
    >>> new_model = edit_model(
    ...     model=model,
    ...     replace_layers_by_provided_counter_parts={
    ...         "Conv_1": tf.keras.layers.Conv2D(
    ...             filters=1280, kernel_size=5, padding="same"
    ...         )
    ...     },
    ...     verbose=True,
    ... )
    [ReplaceLayersByCounterparts] [===============]
    +---------------------------------------+
    |          mobilenetv2_1.00_224         |
    +---------------------------------------+
    | modified layers             | 1       |
    | unmodified layers           | 155     |
    +---------------------------------------+

    Args:
        model: model to edit
        remove_by_name: list of names (or indices) of layers to remove
        replace_layers_by_provided_counter_parts: Dict of pairs (layer name, new layer) and we replace
            the layer with correct name by the provided new layer
        replace_layers_by_types: list of pairs (old layer type, new layer type)
        remove_layer_by_types: list of types of layers to remove
        extra_args: extra arguments for new layers in replace by types.
        verbose: verbatim level
    """
    if replace_layers_by_types is not None:
        return replace_layers_by_types_in_model(
            model=model,
            replace_layers=replace_layers_by_types,
            extra_args=extra_args,
            verbose=verbose,
        )
    elif remove_layer_by_types is not None:
        return remove_layers_by_types_in_model(
            model=model,
            remove_layer=remove_layer_by_types,
            verbose=verbose,
        )
    elif replace_layers_by_provided_counter_parts is not None:
        return replace_layers_by_counterparts_in_model(
            model=model,
            replace_layers_by_provided_counter_parts=replace_layers_by_provided_counter_parts,
            verbose=verbose,
        )
    elif remove_by_name is not None:
        return remove_layers_by_names_or_indices_in_model(
            model=model, remove_layer=remove_by_name, verbose=verbose
        )
    else:
        print("\r[\033[91mwarning\033[0m] called tfsurgeon without modifying the model")
        return model


if __name__ == "__main__":
    model = tf.keras.applications.MobileNetV2(weights=None)
    new_model = edit_model(
        model=model,
        replace_layers_by_types=[
            [tf.keras.layers.BatchNormalization, tf.keras.layers.LayerNormalization]
        ],
        verbose=True,
    )
    new_model = edit_model(
        model=model,
        remove_layer_by_types=[tf.keras.layers.BatchNormalization],
        verbose=True,
    )
    new_model = edit_model(
        model=model,
        replace_layers_by_provided_counter_parts={
            "Conv_1": tf.keras.layers.Conv2D(
                filters=1280, kernel_size=5, padding="same"
            )
        },
        verbose=True,
    )
    new_model = edit_model(
        model=model,
        remove_by_name=[2, -3, "block_16_depthwise_BN"],
        verbose=True,
    )
    new_model = edit_model(
        model=model,
        verbose=True,
    )
