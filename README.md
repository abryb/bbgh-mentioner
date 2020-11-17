##### Usage

```shell script
docker-compose build
cp .env.dist .env
# change .env file if needed, look at it
# build docker container
docker-compose build
# run mentioner help
docker-compose run --rm app --help
# download players
docker-compose run --rm app mentioner download_players
# create all mentions
docker-compose run --rm app mentioner create_all_mentions
# state info
docker-compose run --rm app mentioner state_info
```

##### Interactive usage
```shell script
docker-compose run --rm app python
```

```python
import mentioner
app = mentioner.create_app()

```


##### Development

If using PyCharm follow https://www.jetbrains.com/help/pycharm/using-docker-compose-as-a-remote-interpreter.html#tw

