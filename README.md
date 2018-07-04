# django_football_stats

- heroku login
- heroku create
- heroku config:set DISABLE_COLLECTSTATIC=1
- git push heroku master
- heroku run python manage.py migrate
- heroku ps:scale web=1
- heroku open
- heroku logs --tail

## test

python manage.py test record


coverage run --source='.' manage.py test record && coverage report


coverage html

