# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python'}

packages = \
['llamacpp']

package_data = \
{'': ['*']}

install_requires = \
['sentencepiece>=0.1.97,<0.2.0', 'torch>=1.13.1,<2.0.0']

entry_points = \
{'console_scripts': ['llamacpp-convert = llamacpp.quantize:main',
                     'llamacpp-quantize = llamacpp.quantize:main']}

setup_kwargs = {
    'name': 'llamacpp',
    'version': '0.1.3',
    'description': "Python bindings for @ggerganov's llama.cpp",
    'long_description': '## Building the Python bindings\n\n### macOS\n\n`brew install pybind11`\n\n## Install python package\n\n### From PyPI\n\n```\npip install llamacpp\n```\n\n### From source\n\n```\npoetry install\n```\n\n## Get the model weights\n\nYou will need to obtain the weights for LLaMA yourself. There are a few torrents floating around as well as some huggingface repositories (e.g https://huggingface.co/nyanko7/LLaMA-7B/). Once you have them, copy them into the models folder.\n\n```\nls ./models\n65B 30B 13B 7B tokenizer_checklist.chk tokenizer.model\n```\n\nConvert the weights to GGML format using `llamacpp-convert`. Then use `llamacpp-quantize` to quantize them into INT4. For example, for the 7B parameter model, run\n\n```\nllamacpp-convert ./models/7B/ 1\nllamacpp-quantize ./models/7B/\n```\n\n## Run demo script\n\n```\nimport llamacpp\nimport os\n\nmodel_path = "./models/7B/ggml-model-q4_0.bin"\nparams = llamacpp.gpt_params(model_path,\n"Hi, I\'m a llama.",\n4096,\n40,\n0.1,\n0.7,\n2.0)\nmodel = llamacpp.PyLLAMA(model_path, params)\nmodel.predict("Hello, I\'m a llama.", 10)\n```\n\n## ToDo\n\n- [x] Use poetry to build package\n- [x] Add command line entry point for quantize script\n- [x] Publish wheel to PyPI\n- [ ] Add chat interface based on tinygrad\n',
    'author': 'Thomas Antony',
    'author_email': 'mail@thomasantony.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
