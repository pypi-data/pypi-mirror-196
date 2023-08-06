
__version__ = "0.0.0a"

def get_provider_info():
    return {
        "package-name": "airflow-provider-mlflow",  # Required
        "name": "airflow-provider-mlflow",  # Required
        "description": "A short description of the package",  # Required
        "versions": [__version__],  # Required
    }
