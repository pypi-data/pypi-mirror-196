# Lingua-SDK
A user toolkit for analyzing and interfacing with Large Language Models (LLMs)

<!--
[![PyPI]()]()
[![code checks]()]()
[![integration tests]()]()
[![docs]()]()
[![codecov]()
[![license]()]()
-->

## Overview

``lingua-sdk`` is a Python module used to interact with large language models
hosted via the Lingua service (available at https://github.com/VectorInstitute/lingua).
It provides a simple interface launch LLMs on an HPC cluster, ask them to
perform basic features like text generation, but also retrieve intermediate
information from inside the model such as log probabilities and activations.
These features are exposed via a few high-level APIs, namely:

* `generate` - Returns an LLM text generation based on prompt input
* `module_names` - Returns all modules in the LLM neural network
* `model_instances` - Returns all active LLMs instantiated and avaiable to use
* `get_activations` - Retrieves all activations for a set of modules

Full documentation and API reference are available at
http://lingua-sdk.readthedocs.io.

## Getting Started

### Install

```bash
python3 -m pip install pylingua
```
or install from source:

```bash
pip install git+https://github.com/VectorInstitute/lingua-sdk.git
```

### Authentication

In order to submit generation jobs, a designated Vector Institute cluster account is required. Please contact the
[AI Engineering Team](mailto:ai_engineering@vectorinstitute.ai?subject=[Github]%20Lingua)
in charge of Lingua for more information.

### Sample Workflow

The following workflow shows how to load and interact with an OPT-175B model
on the Vector Institute Vaughan cluster.

```python
import lingua
import time
# Establish a client connection to the Lingua service
# If you have not previously authenticated with the service, you will be prompted to now
client = lingua.Client(gateway_host="llm.cluster.local", gateway_port=3001)

# See which models are available to use
print(client.models)

# Get a handle to a model. If this model is not actively running, it will get launched in the background.
# In this example we want to use the OPT-175B model
opt_model = client.load_model("OPT-175B")

# If not the was not actively running, this it could take several minutes to load. Wait for it come online.
while opt_model.state != "ACTIVE":
    time.sleep(1)

# Sample text generation w/ input parameters
text_gen = opt_model.generate("What is the answer to life, the universe, and everything?", {'max_tokens': 5, 'top_k': 4, 'top_p': 3, 'rep_penalty': 1, 'temperature': 0.5})
dir(text_gen) # display methods associated with generated text object
text_gen.generation['text'] # display only text
text_gen.generation['logprobs'] # display logprobs
text_gen.generation['tokens'] # display tokens

# Now let's retrieve some activations from the model
# First, show a list of modules in the neural network
print(opt_model.module_names)

# Setup a request for module acivations for a certain module layer
requested_activations = ['_fsdp_wrapped_module._fpw_module.decoder.layers.0._fsdp_wrapped_module._fpw_module']
activations = opt_model.get_activations("What are activations?", requested_activations)
print(activations)
```

## [Documentation](https://lingua-sdk.readthedocs.io/)
More information can be found on the Lingua documentation site.

## Contributing
Contributing to lingua is welcomed. See [Contributing](https://github.com/VectorInstitute/lingua-sdk/blob/main/doc/CONTRIBUTING.md) for
guidelines.

## License
[MIT](LICENSE)

## Citation
Reference to cite when you use Lingua in a project or a research paper:
```
Sivaloganathan, J., Coatsworth, M., Willes, J., Choi, M., & Shen, G. (2022). Lingua. http://VectorInstitute.github.io/lingua. computer software, Vector Institute for Artificial Intelligence. Retrieved from https://github.com/VectorInstitute/lingua-sdk.git.
```
