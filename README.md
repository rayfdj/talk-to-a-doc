# Talk To A Doc(ument)

This is a very simple Python script that asks you to pick a file, and then allows you to ask questions about the file. 

It uses the great & powerful [LangChain](https://langchain.com/) to do the heavy lifting :muscle:.

## Pre-requisites
### OpenAI API Key
You need to have an OpenAI API key. You can get one [here](https://platform.openai.com/account/api-keys).

Set it as an environment variable called `OPENAI_API_KEY`.

### Python & Dependencies
I'm using Python 3.9, but [detectron2](https://github.com/facebookresearch/detectron2) works with Python ≥ 3.7, so any 
version of Python 3.7 or higher should work.

[pyenv](https://github.com/pyenv/pyenv) and the [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) plugin are 
highly recommended to keep your Python versions and environments cleanly separated.

Once you have them installed and have the virtual environment activated, then install the following dependencies (the 
below is for Mac):

```bash
brew install poppler
brew install tesseract
pip install langchain
pip install "unstructured[local-inference]"
pip install openai
pip install chromadb
pip install "detectron2@git+https://github.com/facebookresearch/detectron2.git@v0.6#egg=detectron2"
```

## Usage

Simply run the script:

```bash
python main.py
```

And start asking questions! Ctrl + C to stop the session.