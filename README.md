# statelint

An PyPI package providing a validator for [Amazon States Language](https://states-language.net/spec.html) JSON/YAML files.

This package is based on Amazon Web Services Labs' [awslabs/statelint](https://github.com/awslabs/statelint).

## Installation

```shell
pip install statelint
```

## Usage

```shell
statelint fancy-state-machine-spec.json
```

If you prefer YAML, you need to install [PyYaml](https://pypi.org/project/PyYAML/).

```shell
pip install PyYAML
```

Then, run command with a `--yaml` parameter.

```shell
statelint --yaml fancy-state-machine-spec.yaml
```

If you don't like to be complained that `BackoffRate` doesn't end with ".0",
pass a `--ignore=FLOAT` parameter.

```shell
statelint --ignore=FLOAT fancy-state-machine-spec.json
```

If your `Resource` doesn't contain URI string,
pass a `--ignore=URI` parameter.

```shell
statelint --ignore=URI fancy-state-machine-spec.json
```

You can pass both parameters at the same time.

```shell
statelint --ignore=FLOAT,URI fancy-state-machine-spec.json
```

## TODO

- [reference path with dash doesn't validate](https://github.com/awslabs/statelint/issues/17)
- [Reference Path with unicode doesn't validate](https://github.com/awslabs/statelint/issues/23)
- [Does not catch Duplicated State names](https://github.com/awslabs/statelint/issues/39)
