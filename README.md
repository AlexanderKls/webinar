# Webinar - тестовое задание

Привет. 

Автоматизированная развертка была протестирована на свежеустановленной виртуалке. 

Версии ОС и утилит:
```
Debian 10.9.0-amd64
uname -a
Linux mak 4.19.0-23-amd64 #1 SMP Debian 4.19.269-1 (2022-12-20) x86_64 GNU/Linux

make --version
GNU Make 4.2.1

docker --version
Docker version 20.10.22, build 3a2c30b

docker-compose --version
docker-compose version 1.25.3, build d4d1b42b

ansible --version
ansible 2.7.7

python3 --version
Python 3.7.3
```

Проверка работоспособности делается отправкой запроса на 127.0.0.1:80/api
```
root@mak:/opt/webinar-bastion# curl localhost:80/api
Anastasiya\tQwe\t1d7abd0365f1
Oleg\tCde\t35936b4b218c
Oleg\tQwe\t30973dbac359
root@mak:/opt/webinar-bastion# curl localhost:80/api
Andrew\tAsd\t1d7abd0365f1
Anastasiya\tXsw\t35936b4b218c
Anastasiya\tEwq\t30973dbac359
root@mak:/opt/webinar-bastion# curl localhost:80/api
Vladimir\tQwe\t1d7abd0365f1
Evgeniy\tQwe\t35936b4b218c
Stanislav\tCxz\t30973dbac359
```

## Как проверить?

Клонируем:
```
git clone https://github.com/AlexanderKls/webinar.git /opt/webinar-bastion/ && cd /opt/webinar-bastion/
```

Запускаем:
```
make
```
Проверяем:
```
curl localhost:80/api
```
