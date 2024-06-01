# statelint
<a href="https://github.com/taro-kayo/statelint/actions"><img alt="Actions Status" src="https://github.com/taro-kayo/statelint/workflows/Test/badge.svg"></a>
<a href="https://coveralls.io/github/taro-kayo/statelint?branch=main"><img alt="Coverage Status" src="https://coveralls.io/repos/github/taro-kayo/statelint/badge.svg?branch=main"></a>
<a href="https://github.com/taro-kayo/statelint/blob/main/LICENSE"><img alt="License: Apache License 2.0" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"></a>
<a href="https://pypi.org/project/statelint/"><img alt="PyPI" src="https://img.shields.io/pypi/v/statelint"></a>
[![Downloads](https://static.pepy.tech/badge/statelint/month)](https://pepy.tech/project/statelint)

A PyPI package providing a validator for [Amazon States Language](https://states-language.net/spec.html) JSON/YAML files.

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
