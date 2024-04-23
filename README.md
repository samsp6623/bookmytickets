# bookmytickets
A Django app to book tickets for show

# Setup for Testing
```
# start django and db service
docker compose up

# allows fresh restart of the database every time
docker compose down -volume

# to keep container reload to any changes in project directory
docker compose watch backend
```
