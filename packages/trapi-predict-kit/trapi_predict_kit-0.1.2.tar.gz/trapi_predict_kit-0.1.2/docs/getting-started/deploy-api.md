## Define the API

You will need to instantiate a `TRAPI` class to deploy a Translator Reasoner API serving a list of prediction functions that have been decorated with `@trapi_predict`. For example:

```python
import logging

from trapi_predict_kit import TRAPI, settings
from my_model.predict import get_predictions


log_level = logging.ERROR
if settings.DEV_MODE:
    log_level = logging.INFO
logging.basicConfig(level=log_level)

predict_endpoints = [ get_predictions ]

openapi_info = {
    "contact": {
        "name": "Firstname Lastname",
        "email": "email@example.com",
        # "x-id": "https://orcid.org/0000-0000-0000-0000",
        "x-role": "responsible developer",
    },
    "license": {
        "name": "MIT license",
        "url": "https://opensource.org/licenses/MIT",
    },
    "termsOfService": 'https://github.com/your-org-or-username/my-model/blob/main/LICENSE.txt',

    "x-translator": {
        "component": 'KP',
        # TODO: update the Translator team to yours
        "team": [ "Clinical Data Provider" ],
        "biolink-version": settings.BIOLINK_VERSION,
        "infores": 'infores:openpredict',
        "externalDocs": {
            "description": "The values for component and team are restricted according to this external JSON schema. See schema and examples at url",
            "url": "https://github.com/NCATSTranslator/translator_extensions/blob/production/x-translator/",
        },
    },
    "x-trapi": {
        "version": settings.TRAPI_VERSION,
        "asyncquery": False,
        "operations": [
            "lookup",
        ],
        "externalDocs": {
            "description": "The values for version are restricted according to the regex in this external JSON schema. See schema and examples at url",
            "url": "https://github.com/NCATSTranslator/translator_extensions/blob/production/x-trapi/",
        },
    }
}

servers = []
if settings.VIRTUAL_HOST:
    servers = [
        {
            "url": f"https://{settings.VIRTUAL_HOST}",
            "description": 'TRAPI ITRB Production Server',
            "x-maturity": 'production'
        },
    ]

app = TRAPI(
    predict_endpoints=predict_endpoints,
    servers=servers,
    info=openapi_info,
    title='My model TRAPI',
    version='1.0.0',
    openapi_version='3.0.1',
    description="""Machine learning models to produce predictions that can be integrated to Translator Reasoner APIs.
\n\nService supported by the [NCATS Translator project](https://ncats.nih.gov/translator/about)""",
    dev_mode=True,
)
```

## Deploy the API

If you used the template to generate your project you can deploy the API with the `api` script defined in the `pyproject.toml` (refere to your generated project README for more details):

```bash
hatch run api
```

Otherwise you can use `uvicorn` or `gunicorn`:

```bash
uvicorn trapi.main:app --port 8808 --reload
```
