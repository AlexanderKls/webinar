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
Если не запустится на других версиях и будет желание проверить на этой версии debian, инструкции по установке docker & docker-compose брал с digitalocean:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-debian-10
https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-debian-10

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
## Странности и преднамеренные действия

1. Первое, что бросается в глаза, это результат вывода curl. Проблема в том, что когда я собирал nginx контейнер, я загрузил туда python mysql connector модуль,
при учете того, что он был виден в установленных пакетах(pip list), я не мог его вызвать в скрипте. Следовательно, я не мог правильным методом конектиться к mysql и делать выборку. Реализовал с помощью subprocess модуля и вызова shell команды. Отформатировать строку там проблематично, из за того, что даже явным указанием типа данных как string, он не давал мне корректно форматировать строку, по этой причине мы видим в качестве разделителя '\t'. 

В рамках тестового задания я решил не зацикливаться на этой проблеме.

2. Все контейнеры и приложения, кроме wsgi, запускаются от root. Я знаю, что это плохо и нужно по другому, но для тестового задания решил, что можем обойтись и без этого.

3. Так как само приложение wsgiapp.py выглядит так, словно его писал человек, который вчера прочитал про python(извините, но мне с wsgi было правда сложно), я написал скрипт автоматической генерации пароля или же ручной вставкой, при создании инфраструктуры. Может быть выполнено как при запуске make, так и вручную /opt/webinar-bastion/set_root_password.py. 

## Масштабирование

Так как подобными задачами я никогда не занимался и docker scale не использовал, я решил сделать это так, как я вижу. 

Для изменения количества backend контейнеров требуется изменить значение переменной backend_count:
```
# Real count, its number - 3. Example, 6 - 3 = 3 backends
backend_count: 6
```
Почему 3 - 6? Потому что это число используется для цикла генерации ip адресов. Где:
0 - это подсеть
1 - это мост
2 - это контейнер nginx

Следовательно, первый доступный адрес для контейнера backend - это 3.

## Кастомный контейнер на docker hub

Так как была просьба собрать свой контейнер и разместить его на docker hub, я собрал свой контейнер со стаком LEMW, где W - WSGI для работы python с nginx. 
Ссылка: https://hub.docker.com/r/mackedonsky/webinar

Чтобы понятно было, как собирал и что внутри - в репозитории лежит Dockerfile.

## Makefile

Я никогда не создавал make файлы. Поэтому если там чего критически важного не хватает - извините, я про это не знал. 
