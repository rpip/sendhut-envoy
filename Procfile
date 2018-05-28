#release: python manage.py migrate --no-input
#web: honcho -f ProcfileHoncho start
web: newrelic-admin run-program gunicorn -b "0.0.0.0:$PORT" -w 3 sendhut.wsgi
