# celery-sentinel

Celery broker for [Redis Sentinel](http://redis.io/topics/sentinel)

## Installation

As simple as possible:

```pip install celery-sentinel```

## Usage

Setup celery broker:

```python
#  settings.py

BROKER_URL='redis-sentinel://redis-sentinel:26379/0'

BROKER_TRANSPORT_OPTIONS = {
    'sentinels': [('192.168.1.1', 26379),
                  ('192.168.1.2', 26379),
                  ('192.168.1.3', 26379)],
    'service_name': 'master',
    'socket_timeout': 0.1,
}
```

Configure celery app:

```python
# celery_app.py
import os

from celery_sentinel import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("your-project")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
```

Then use the celery as usual.