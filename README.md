# bookmytickets

A Django app to book tickets for shows like Theater/Movie, Comedy Show, Circus, Sport match
like events to let the spectator book ticket for the their selected show.

# Setup for Testing

```
# start Django and PostgresQL db service
docker compose up

# allows fresh restart of the database every time
docker compose down -volume

# to keep container reload to any changes in project directory while developing
docker compose watch backend
```

# Environment Variables to set in the Web App Server

for Django
ALLOWED_HOST
SECRET_KEY

for postgres database
NAME
USER
HOST
PORT
PASSWORD
