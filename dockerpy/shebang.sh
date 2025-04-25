#!/bin/bash

set -e


echo "Starting Xvfb..."
Xvfb :99 -screen 0 1280x1024x24 -nolisten tcp -ac &



sleep 3  # give it a moment to start


echo 'starting cron'
crond -f -l 8 & # runs crond in background; 


tail -f /var/log/cron.log # read the tail with follow mode - this mode prevents the container from shutting down; 
