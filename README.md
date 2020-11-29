##### Usage

```shell script
# build docker container
docker-compose build
cp .env.dist .env
# change .env file if needed, look at it
# run mentioner help
docker-compose run --rm app
docker-compose run --rm app mentioner --help
# download players
docker-compose run --rm app mentioner download_players
# create all mentions
docker-compose run --rm app mentioner create_mentions
# state info
docker-compose run --rm app mentioner state_info
# clear state
docker-compose run --rm app mentioner clear_state
```

##### Interactive usage
```shell script
docker-compose run --rm app python
```

```python
import mentioner
app = mentioner.create_app()
app.download_players()
app.create_mentions()
```


##### Development

If using PyCharm follow https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#tw

