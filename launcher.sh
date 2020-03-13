
#!/bin/bash
# Run the backend on background enviroment and run the frontend at the front
# To see the gunicorn process running on background : ps ax|grep gunicorn
# To stop the gunicorn process : kill <reference number of process> 
#                                (one kill for front end + one kill for backend)

set -e

gunicorn -w 4 -b 127.0.0.1:5000 api_front:app &
gunicorn -w 4 -b 127.0.0.1:8000 api_run:app &
