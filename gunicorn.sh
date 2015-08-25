#!/bin/bash

NAME="simpleenergy_dev"
APPDIR=/home/simpleenergy/app
SOCKFILE=$APPDIR/pid/gunicorn.sock
VENV=$APPDIR/venv
USER=simpleenergy
GROUP=webapps
NUM_WORKERS=3

echo "Starting $NAME as `whoami`"

export APP_SETTINGS="config.DevelopmentConfig"

# Activate the virtual environment
cd $APPDIR
if [ ! -d "$VENV" ]; then
  virtualenv venv
  pip install -r requirements.txt
fi
source $VENV/bin/activate
export PYTHONPATH=$APPDIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec $VENV/bin/gunicorn app:app \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=unix:$SOCKFILE
