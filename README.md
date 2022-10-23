# interview-public
public information for interviews @ PatternResearch

# Backend
Written in FastAPI, using SQLAlchemy over SQLite as a DB, Pydantic for model formatting

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