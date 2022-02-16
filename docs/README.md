# Welcome to the Jizt docs!

You can find the docs at [docs.jizt.it](https://docs.jizt.it). Besides, you can
always compile the documentation locally. For that, simply follow the steps below.

## Prerequisites

First of all, create a virtual environment, activate it, and install the
necessary requirements.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Compiling the docs

Once the requirements have been installed, execute the following in the
`/docs` directory:

```bash
make html
```

A new directory `_build/html` will have been created. You can then open
`_build/html/index.html` to open the compiled docs on your browser.

**Note**: if you've made any changes to the docs source files, it is recommended
that you clean-build by running:

```bash
make clean && make html
```
