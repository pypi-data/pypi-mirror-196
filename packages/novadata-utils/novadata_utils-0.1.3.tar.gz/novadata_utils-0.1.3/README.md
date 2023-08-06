# novadata utils
Pacote para facilitar o seu dia a dia como programador Django.

## Getting Started

### Dependências
Django
Django Rest Framework

#### Installation
```shell
pip install novadata-utils
```

Settings.py:
```python
INSTALLED_APPS = [
    ...
    'advanced_filters',
    'import_export',
    'novadata_utils',
    'rest_framework',
    ...
]
```

Urls.py:
```python
urlpatterns = [
    ...
    path("advanced_filters/", include("advanced_filters.urls")),
    ...
]
```


## Features
