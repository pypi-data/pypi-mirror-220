# What is Waffle Box.
Waffle Box는 기존 Autocare App을 Waffle로 만든 모델로 교체해 새로운 App을 생성해 줍니다.

# Build
Waffle Box는 python package 관리자인 Poetry를 기반으로 빌드 및 배포합니다.  
Install poetry: https://python-poetry.org/docs/

``` bash
poetry build
```

# Dependency
- python
  - 3.10

# Install
## Install from code
```bash
poetry install
```

## Install from PyPI
```bash
pip install waffle-box
```

# Usage
## Pull Waffle Maker Image
```bash
wb --dx-version 1.6.2 pull --login
```

## Convert App
```bash
wb --dx-version 1.6.2 convert safety_app_1.0.0.zip -o safety_app_1.0.1.zip
```
