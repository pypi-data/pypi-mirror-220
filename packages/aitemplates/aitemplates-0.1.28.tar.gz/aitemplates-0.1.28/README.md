# aitemplates

aitemplates is a Python package designed to simplify and streamline your work with the OpenAI API. It provides automatic function calling, helper classes, Python typing support, error checking, and a usage meter to help manage API costs. Additionally, aitemplates offers built-in examples of using ChromaDB and tools for efficient prompt engineering with OpenAI.

## Features

- **Function Integration**: Quick and easy integration with OpenAI functions for automatic execution and error handling.
- **Error Checking**: Automatically catch and handle errors during API calls.
- **Usage Meter**: Keep track of your OpenAI API usage with a built-in metering system.
- **ChromaDB Integration**: Work directly with ChromaDB from the aitemplates interface.
- **Asynchronous Chat Completions**: Use the `-asnc` flag to run asynchronous chat completions. The built-in `print_every` option prints every time a completion finishes in parallel. If you'd like to maintain the order of your completions, pass in the `keep_order` boolean as `True`.
- **Prompt Engineering Examples**: Get started quickly with included examples of prompt engineering techniques.
- **Python Typing Support**: Enjoy the benefits of Python's dynamic typing system while using OpenAI API.

## Installation

You can install aitemplates directly from PyPI:

```bash
pip install aitemplates
```

To get the latest version of the package, you can also clone the repository and install the package by running `pip install -e .` in the repository directory.

## Creating Jupyter Notebook Templates

Create Jupyter notebook templates for prompt engineering with the following command:

```bash
aitemplates name_of_notebook
```

Include a Chroma database in the template with the `-db` flag:

```bash
aitemplates name_of_notebook -db
```

For asynchronous chat completions, add the `-asnc` flag:

```bash
aitemplates name_of_notebook -db -asnc
```

For chat completions with function boilerplate add the `-func` flag (async do not support functions):

```bash
aitemplates name_of_notebook -db -func
```

## Documentation

The package includes example notebooks, which provide comprehensive guides and demonstrations of the functionalities provided by aitemplates. To access these notebooks, access or clone the repository at [https://github.com/SilenNaihin/ai_templates](https://github.com/SilenNaihin/ai_templates) and navigate to the `/notebooks` directory.

Here are the available notebooks:

- `oai_examples.ipynb`: Provides examples for the OpenAI API including functions.
- `chroma_examples.ipynb`: Demonstrates usage of ChromaDB.
- `prompt_engineering_example.ipynb`: A comprehensive guide on prompt engineering, including various techniques, usage of ChromaDB and the OpenAI library together.

## Requirements

- Be sure to have a `.env` file with the `OPENAI_API_KEY` defined in the root of your project or your api key defined in some way for OpenAI. AWS env variables are for ChromaDB deployment https://docs.trychroma.com/deployment
- This library doesn't currently support text models like `text-davinci-003`. Streaming and logit_bias parameters are also not supported

## Contributing

I welcome and appreciate contributions to aitemplates. If you'd like to contribute a feature, please submit a pull request. For bugs, please open a new issue, and I'll address it promptly.

## Future?

- https://twitter.com/ItakGol/status/1668336193270865921
- Support for other LLMs
- Support for other dbs
