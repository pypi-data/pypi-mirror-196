
__version__ = "0.0.0a"

def get_provider_info():
    return {
        "package-name": "airflow-provider-zenml",  # Required
        "name": "airflow-provider-zenml",  # Required
        "description": "A short description of the package",  # Required
        "versions": [__version__],  # Required
    }
