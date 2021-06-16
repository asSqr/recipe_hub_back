### DB の initialize

- docker 内アクセス

```
docker-compose exec db psql -U postgres
```

- 初期化の自動実行

./db/init.sql がコンテナ起動時に一度だけ実行され，DB が初期化されます．また，起動したら以下のコマンドを順に実行して migrate してください．

```
docker-compose exec backend python ./manage.py makemigrations
docker-compose exec backend python ./manage.py migrate
```

DB が初期化されていないときは，

```
docker volume rm recipe_hub_back_django_data_volume
```

をして，エラーメッセージの中のハッシュ値を使って

```
docker container rm {ハッシュ値}
```

とした後にもう一度

```
docker volume rm recipe_hub_back_django_data_volume
```

とするとボリュームを初期化でき，再度コンテナを起動すると DB 初期化が走ります．

これらをしても "does not exist" 等のエラーが出る場合は，以下を試してみてください．(recipe_hub が migrate されておらず DB に反映されていない可能性があります)

```
docker-compose exec backend python ./manage.py makemigrations recipe_hub
docker-compose exec backend python ./manage.py migrate
```

### DB の dump

DB にダミーデータを入れる場合は 2 番目の restore をしてください．

以下を実行してバックアップを取ります．

```
docker-compose exec db pg_dump --no-acl --no-owner -h localhost -U postgres recipehub > ./db/dump.sql
```

以下でバックアップを restore します．

```
docker cp db/dump.sql postgres_db:/tmp
docker-compose exec db psql -U postgres -f /tmp/dump.sql
```

### DB 全削除

```
docker-compose down
docker volume rm recipe_hub_back_django_data_volume
docker-compose exec backend python ./manage.py makemigrations recipe_hub
docker-compose exec backend python ./manage.py migrate recipe_hub
```

### local_settings.py

local で動かす場合は /backend/app/ 以下に local_settings.py (https://gist.github.com/asSqr/89503d2187d00a518c27dcf077915e94) を入れてください．**これは git に push しないでください．**