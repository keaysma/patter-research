# interview-public
public information for interviews @ PatternResearch

# Backend
Written in FastAPI, using SQLAlchemy over SQLite as a DB, Pydantic for model formatting

## Setup
Setup venv
```bash
pythom -m venv .
source bin/activate
```

Install dependences
```bash
pip install -r requirements.txt
```


## Run
```bash
uvicorn app.main:app
```

## Test
```bash
# Get one order
curl -L "localhost:8000/fills/1666019586564769"

# Get orders over a time range
curl -L "localhost:8000/fills?start=1666019586564768&end=1666019586964769"
```

# Frontend
Written in React using Mantine, and Chart.JS

## nginx
nginx is used as a request broker to simulate a production environment (and also assist in CORS handling)

From the frontend folder, run
```bash
sudo nginx -c $(pwd)/nginx.conf
```

## hosts
The nginx config is setup to run this site from pattern.test, please add the following entry to your hosts file
```bash
sudo echo "127.0.0.1       pattern.test api.pattern.test" >> /etc/hosts
```

## Setup
Install dependencies
```bash
npm i
```

## Run
Simple as
```bash
npm start
```