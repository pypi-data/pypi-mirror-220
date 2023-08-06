# Hyperopt Prophet

**Integration of prophet forecasting with hyperopt, mlflow**
This implementation is based on the [Databricks AutoML](https://github.com/databricks/automl) repository.

## Setup

### Quick Install

```shell
python -m pip install hyperopt_prophet
```

### Build from source

Clone the repository

```shell
git clone https://github.com/Broomva/hyperopt_prophet.git
```

Install the package

``` shell
cd hyperopt_prophet && make install
```

### Build manually

After cloning, create a virtual environment

```shell
conda create -n hyperopt_prophet python=3.9
conda activate hyperopt_prophet
```

Install the requirements

```shell
pip install -r requirements.txt
```

Run the python installation

```shell
python setup.py install
```

## Usage

```python
import hyperopt_prophet 
```

## Attribution

Hyperopt Prophet builds upon the hard work of others. Here are the original leveraged repositories:

- [Databricks AutoML](https://github.com/databricks/automl)
