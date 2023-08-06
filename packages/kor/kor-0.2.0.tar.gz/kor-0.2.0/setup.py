# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kor', 'kor.experimental', 'kor.llms']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27,<0.28']

setup_kwargs = {
    'name': 'kor',
    'version': '0.2.0',
    'description': 'Extract information with LLMs from text',
    'long_description': '**⚠ WARNING: Prototype with unstable API. 🚧**  \n\n# Kor\n\nThis is a half-baked prototype that "helps" you extract structured data from text using LLMs 🧩.\n\nSpecify the schema of what should be extracted and provide some examples.\n\nKor will generate a prompt, send it to the specified LLM and parse out the\noutput. You might even get results back.\n\nSee [documentation](https://eyurtsev.github.io/kor/).\n\n## 💡 Ideas\n\nIdeas of some things that could be done with Kor.\n\n* Extract data from text: Define what information should be extracted from a segment\n* Convert an HTML form into a Kor form and allow the user to fill it out using natural language. (Convert HTML forms -> API? Or not.)\n* Add some skills to an AI assistant\n\n## 🚧 Prototype\n\nThis a prototype and the API is not expected to be stable as it hasn\'t been\ntested against real world examples.\n\n##  ✨ does Kor excel at?  🌟 \n\n* Making mistakes! Plenty of them. Quality varies with the underlying language model, the quality of the prompt, and the number of bugs in the adapter code.\n* Slow! It uses large prompts with examples, and works best with the larger slower LLMs.\n* Crashing for long enough pieces of text! Context length window could become\n  limiting when working with large forms or long text inputs.\n* Incorrectly grouping results (see documentation section on objects).\n\n\n## Potential Changes\n\n* Adding validators\n* Built-in components to quickly assemble schema with examples\n* Add routing layer to select appropriate extraction schema for a use case when\n  many schema exist\n\n## 🎶 Why the name?\n\nFast to type and sufficiently unique.\n',
    'author': 'Eugene Yurtsev',
    'author_email': 'eyurtsev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.github.com/eyurtsev/kor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
