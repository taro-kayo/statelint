export python_version="$1"

docker run --rm -it -v $(pwd):/statelint python:$python_version-slim sh -e -x -c "
cd /statelint

python -m pip install --upgrade pip setuptools
python -m pip install wheel pytest
python setup.py bdist_wheel
export whl_path=$(echo dist/*.whl)
python -m pip install $whl_path[yaml]
python -m pytest tests
"