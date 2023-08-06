# Moonhub Logger

## Use the mh_logger package

### 1. Install

```
python3 -m pip install mh_logger
```

### 2. Import and use

```
from mh_logger import LoggingManager
logger = LoggingManager(__name__)
logger.info("This is a sample log", hello="world")
```

Output:
```
2023-03-16 20:22:36,561 [INFO] - TestLogger: this is a sample log - JSON Payload: {'hello': 'world'}
```

Set following environment variable if you want to push logs to GCP Cloud Logging service while testing locally.
```
GCP_SERVICE_KEY=google-service-key.json
```

## Create and upload the mh_logger package
https://packaging.python.org/en/latest/tutorials/packaging-projects/
```
