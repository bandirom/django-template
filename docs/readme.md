* Install dependencies
```shell
pipenv install -r docs/requirements.txt --dev
```

* doc8 style checks
```shell
doc8 docs/source/ --config web/pyproject.toml
```

* Generate documentation
```shell
make -C docs html
```

* Check spelling
```shell
make -C docs spelling
```
