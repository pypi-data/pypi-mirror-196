import tensorflow as tf
from typing import Dict, Tuple


def get_graph_as_dict(model: tf.keras.Model) -> Tuple[Dict[str, Dict[str, list]], bool]:
    """
    This function returns a dictionnary of the layers and their corresponding
    input layers. This serves the purpose of re-defining the graph with
    new layers.
    """
    istransformer = False
    network_dict = {"input": {}, "new_output": {}}
    for layer in model.layers:
        for node in layer._outbound_nodes:
            layer_name = node.outbound_layer.name
            if layer_name not in network_dict["input"]:
                network_dict["input"].update({layer_name: [layer.name]})
            else:
                if layer.name not in network_dict["input"][layer_name]:
                    network_dict["input"][layer_name].append(layer.name)
    if network_dict == {"input": {}, "new_output": {}}:
        print("[\033[91mWARNING\033[00m] not supported architecture")
    if isinstance(model.input, (list, tuple)):
        istransformer = True
        for inputs in model.input:
            network_dict["new_output"][inputs.name] = inputs
    else:
        network_dict["new_output"].update({model.layers[0].name: model.input})
    for layer in model.layers:
        if layer.name not in network_dict["input"]:
            network_dict["input"][layer.name] = []
    return network_dict, istransformer


def reverse_graph(graph: Dict[str, list]) -> Dict[str, list]:
    """
    This function fetches the output layers of each layer of the DNN
    """
    output_dict = {}
    all_keys = []
    for key_1 in list(graph.keys()):
        for key_2 in graph[key_1]:
            if key_2 not in output_dict:
                output_dict.update({key_2: [key_1]})
            else:
                if key_1 not in output_dict[key_2]:
                    output_dict[key_2].append(key_1)
            if key_2 not in all_keys:
                all_keys.append(key_2)
        if key_1 not in all_keys:
            all_keys.append(key_1)
    for key in all_keys:
        if key not in output_dict:
            output_dict[key] = []
    return output_dict
