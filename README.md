# DevOps Interview Service

## Database setup:

```
# requires that a postgresql database already exists
# called 'simpleenergy_dev'

# may not need this instruction
# python manage.py db init

python manage.py db migrate
python manage.py db upgrade
```

## Running the service:

```python run.py```
