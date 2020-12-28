## Local development
--- 

#### Initial
```bash
virtualenv --python=/usr/bin/python3.6 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Each time

```bash
source .venv/bin/activate
```

#### For starting the server;
```bash
uvicorn main:app --reload --host=0.0.0.0
```

#### For more about fastapi
https://fastapi.tiangolo.com/

### Swagger

http://localhost:8000/v1/analytics/docs

