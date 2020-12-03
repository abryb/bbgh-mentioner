#### Running on production
It runs single container with cron jobs defined in [crontab](crontab)
```shell script
docker-compose up --build -d
```

#### Usage manually 
```shell script
# build docker container
docker-compose build
# run mentioner help
docker-compose run --rm app
docker-compose run --rm app mentioner --help
# run same command as running in cron job
docker-compose run --rm app mentioner run
# download players
docker-compose run --rm app mentioner download_players
# create all mentions
docker-compose run --rm app mentioner create_mentions
# state info
docker-compose run --rm app mentioner state_info
# clear state
docker-compose run --rm app mentioner clear_state
```

#### Interactive usage
```shell script
docker-compose run --rm app python
```

```python
import mentioner
app = mentioner.create_app()
app.download_players()
app.create_mentions()
```


#### Development

If using PyCharm follow https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#tw