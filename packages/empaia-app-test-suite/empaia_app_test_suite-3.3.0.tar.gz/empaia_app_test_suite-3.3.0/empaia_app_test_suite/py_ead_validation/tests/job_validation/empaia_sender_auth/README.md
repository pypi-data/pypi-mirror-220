# EMPAIA Sender Auth

The AioHttpClient class implements JWT-based authorization for EMPAIA Python FastAPI services, that send outgoing requests to other services.

A reference usage of the the AioHttpClient class can be found in the App Service, where this repository is integrated as a git submodule.

## Code Checks

Check your code before committing.

* always format code with `black` and `isort`
* check code quality using `pycodestyle` and `pylint`

```bash
python -m venv .venv
source .venv/bin/activate
poetry install
```

```bash
black .
isort .
pycodestyle *.py
pylint *.py
```

## Usage

1. Create AioHttpClient object
2. Run async task in FastAPI app for regular token updates

```python
import asyncio
from .empaia_sender_auth import AioHttpClient, AuthSettings

logger = None  # change this
app = None  # change this
settings = None  # change this

auth_settings = AuthSettings(
    idp_url=settings.idp_url,
    client_id=settings.client_id,
    client_secret=settings.client_secret,
)

http_client = AioHttpClient(
    logger=logger,
    timeout=settings.app_service_timeout,
    auth_settings=auth_settings,
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(http_client.update_token_routine())
```
