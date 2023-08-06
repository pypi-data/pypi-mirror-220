# mlflowops Util
**MLOps utils with MLFlow**


## Setup

### Quick Install

```shell
python -m pip install mlflowops
```

### Build from source

Clone the repository

```shell
git clone https://github.com/Broomva/mlflowops.git
```

Install the package

``` shell
cd mlflowops && make install
```

### Build manually

After cloning, create a virtual environment

```shell
conda create -n mlflowops python=3.10
conda activate mlflowops
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

The deployment requires a .env file created under local folder:

```shell
touch .env
```

It should have a schema like this:

```toml
databricks_experiment_name=''
databricks_experiment_id=''
databricks_host=''
databricks_token=''
databricks_username=''
databricks_password=''
databricks_cluster_id=''
```

```python
import mlflowops 
```