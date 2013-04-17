#!/usr/bin/env bash

# init.d script for roost service on debian

source /etc/roost/roost.conf
DAEMON=/usr/bin/roost
ARGS="$xbee_device"
PIDFILE=/var/roost/roost.pid
USER=www-data

case "$1" in
  start)
    echo "Starting server"
    /sbin/start-stop-daemon --start --pidfile $PIDFILE \
        --user $USER --group $USER \
        -b --make-pidfile \
        --chuid $USER \
        --exec $DAEMON $ARGS
    ;;
  stop)
    echo "Stopping server"
    /sbin/start-stop-daemon --stop --pidfile $PIDFILE --verbose
    ;;
  *)
    echo "Usage: /etc/init.d/carbage-serve {start|stop}"
    exit 1
    ;;
esac

exit 0
