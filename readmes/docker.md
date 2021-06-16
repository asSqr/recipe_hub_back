### build

```
docker-compose build
```

### 起動

```
docker-compose up -d
```

### backend コマンド実行

```
docker-compose exec backend {打ちたいコマンド}
```

`打ちたいコマンド`を`/bin/bash`にすると、コンテナ内シェルにアクセス可能

### frontend コマンド実行

```
docker-compose exec frontend {打ちたいコマンド}
```