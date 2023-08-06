# jupyterlab-theme

A theme extension for JupyterLab with the NayaOne logo and colors

## Prerequisites

* JupyterLab >= 3.0.0

## Installation

```bash
jupyter labextension install @nayaone/jupyterlab-theme
```

## Development

For a development install (requires npm version 4 or later), do the following in the repository directory:

```bash
npm install
jupyter labextension link .
jupyter labextension install .
```

To rebuild the package and the JupyterLab app:

```bash
npm run build
jupyter lab build
```


## Building and Uploading a new Package
python3 -m build
python3 -m twine upload --repository jupyterlab-theme dist/*
