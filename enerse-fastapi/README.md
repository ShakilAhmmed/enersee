### Enersee FastApi Application

### Copy .env.example to .env
```bash
cp .env.example .env
```
#### [Note: Do not use @ in DB_PASSWORD]

### Run Containers
```bash
 sudo docker-compose up -d 
```
### Execute Commands
```bash
sudo docker exec -it enerse-fastapi-enersee_fastapi_backend-1 bash 
```

### Migrations using alembic

#### If you have mismatching tables with alembic versions
```bash
alembic stamp head
```
#### After Changing property in src/models
```bash
 alembic revision --autogenerate -m "Description of changes"
 alembic upgrade head
```

#### Fresh Migrations
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```
#### Check for pending migrations
```bash
alembic current
alembic history --verbose
alembic heads
```
### Run test 
```bash
pytest -v
```