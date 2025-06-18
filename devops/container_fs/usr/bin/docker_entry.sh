#!/bin/bash
cat /etc/banner/dragon
cat /etc/banner/brane
cd /app/brane/
if [ $DEBUG == 'true' ]; then
  export BRANE_LOG_LEVEL='INFO'
  export ENABLE_DEBUG='true'
else
  export BRANE_LOG_LEVEL='WARNING'
  unset ENABLE_DEBUG
fi
if [ $BRANE_DB == "migrate" ]; then
  echo "•--» Bringing Database up to date (migrate/SQL files)... "
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py install_sql_files _all_
fi

if [ $BRANE_APP_MODE == 'web_devel' ]; then
    echo "•--» Web Devel Node Startup ... "
    echo "•--» Starting Statics Collecting ... "
    python3 manage.py collectstatic --noinput
    echo "•--» Configuring NGINX ... "
    rm /etc/nginx/sites-enabled/*;
    cp /etc/nginx/sites-available-devel/brane-webdev.conf /etc/nginx/sites-enabled/;
    echo "•--» Starting NGINX ... "
    /etc/init.d/nginx start
    echo "•--» Starting Daphne/Django Webdev Server ... "
    source /venv/bin/activate
    python3 manage.py runserver 127.0.0.1:8001
#
#
#elif [ $BRANE_APP_MODE == 'web_worker' ]; then
#    echo "•--» Web Worker Only Node Startup ... "
#    echo "•--» Starting Statics Collecting ... "
#    python3 manage.py collectstatic --noinput
#    echo "•--» Starting NGINX ... "
#    /etc/init.d/nginx start
#    echo "•--» Starting UWSGI ... "
#    /usr/bin/uwsgi --reload-on-exception --uid www-data --gid www-data --master --emperor /etc/uwsgi/apps-enabled/ --plugin python3 --enable-threads
#
#elif [ $BRANE_APP_MODE == 'bkg_worker' ]; then
#      echo "•--» Background Worker Only Node Startup ... "
#      echo "AQMP Server is: "
#      echo $RABBITMQ_HOST
#      echo "•--» Celery Flower Startup ... "
#      python3 -m celery -A athena.celery flower --uid www-data --gid www-data --basic-auth=athena:7QaTEz4@ &
#      echo "•--» Celery Worker  Startup ... "
#      python3 -m celery -A athena.celery worker --uid www-data --gid www-data  -O fair -l $BRANE_LOG_LEVEL
#
#  elif [ $BRANE_APP_MODE == 'bkg_beat' ]; then
#      echo "•--» Background Beat  Node Startup ... "
#      echo "AQMP Server is: "
#      echo $RABBITMQ_HOST
#      echo "•--» Celery Flower Startup ... "
#      python3 -m celery -A athena.celery flower --uid www-data --gid www-data --basic-auth=athena:7QaTEz4@ &
#      echo "•--» Celery BEAT  Startup ... "
##      python3 -m celery -A athena.celery flower --uid www-data --gid www-data &
#      python3 -m celery -A athena.celery beat -s /tmp/celerybeat-schedule.db --uid www-data --gid www-data -l $BRANE_LOG_LEVEL &
#      python3 -m celery -A athena.celery worker  --uid www-data --gid www-data  -O fair -l $BRANE_LOG_LEVEL
#
#elif [ $BRANE_APP_MODE == "flower" ]; then
#      echo "•--» Background Beat  Node Startup ... "
#      echo "•--» Celery Flower Startup ... "
#      echo "AQMP Server is: "
#      echo $RABBITMQ_HOST
#      python3 -m celery -A athena.celery flower --uid www-data --gid www-data
else
  echo "•--» no BRANE_APP_MODE specified. "
fi
