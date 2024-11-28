# Backend development

> Central development is done against Python 3.12

First, prepare your `.env` file using appropriate values for your development
environment.

```shell
cp template.env .env
vim .env
```

Now, make sure you have a working environment by running the unit tests.

```shell
pip install -r requirements.txt
pip install -r requirements-dev.txt

python -m pytest
```

