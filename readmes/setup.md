## Setup(Docker)

- コンテナは以下の 3 つ。`docker-compose.yml`に詳細
  - postgres_db
  - back-api(`backend`に Dockerfile)
- [ここのセットアップ手順](https://hodalog.com/tutorial-django-rest-framework-and-react/#index-toc-8)を参考に作成

### Local で動かし，ダミーデータを入れるには (ローカルで動かす場合まずここを参照してください)

- (データを消す場合は) `docker-compose down` して `docker volume rm recipe_hub_back_django_data_volume`
- `docker-compose build`
- local_settings.py (https://gist.github.com/asSqr/89503d2187d00a518c27dcf077915e94) を ./backend/app 下に配置 (これは git に上げないでください)
- `docker-compose up -d`
- `docker-compose exec backend python ./manage.py makemigrations`
- `docker-compose exec backend python ./manage.py migrate`
- できなければ以下 2 つをさらに
- `docker-compose exec backend python ./manage.py makemigrations recipe_hub`
- `docker-compose exec backend python ./manage.py migrate recipe_hub`
- (まれに db と back-api コンテナの起動順が壊れて DB が読み込めないエラーになることがありますが，その際は `docker-compose down` をいったんしてまた立ち上げ直してください)
- VSCode で設定を共有しているので，VSCode で開発を行い，念のため VSCode を再起動してください．
- `pip install autopep8` `pip install flake8` してください
- 他に，VSCode 起動時にインストールすべきプラグインやパッケージがあると言われたら「はい」を選択してください．