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
root@laboratory:/opt/webinar-bastion# curl localhost:80/api
Anastasiya Xsw from 9731df512368

root@laboratory:/opt/webinar-bastion# curl localhost:80/api
Anastasiya Zxc from 35b543be6a05

root@laboratory:/opt/webinar-bastion# curl localhost:80/api
Alexander Zxc from 35b543be6a05

root@laboratory:/opt/webinar-bastion# curl localhost:80/api
Vladimir Qwe from 9731df512368
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

1. Странная реализация соединения с бекенд контейнерами. Проблема в том, что когда я собирал nginx контейнер, я загрузил туда python mysql connector модуль,
при учете того, что он был виден в установленных пакетах(pip list), я не мог его вызвать в скрипте. Следовательно, я не мог правильным методом конектиться к mysql и делать выборку. Реализовал с помощью subprocess модуля и вызова shell команды. Так же позже пришла мысль использовать defaults-group-suffix через my.cnf, но эта версия mysql не поддерживает такую опцию. "Хорошая мысля приходит опосля"

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
Почему 6 - 3? Потому что это число используется для цикла генерации ip адресов. Где:
```
0 - это подсеть
1 - это мост
2 - это контейнер nginx
```

Следовательно, первый доступный адрес для контейнера backend - это 3.

Если нужна полная поддержка кастомных значений для всех контейнеров бекенда, можно добавить словарь backend_mysql: и определять в нем каждый контейнер с каждым значением. Далее циклом генерировать каждый контейнер с помощью jinja2 шаблона, исходя из определенных параметров. Тут я решил не мудрить, сделать шаблонное масштабирование.

## Кастомный контейнер на docker hub

Так как была просьба собрать свой контейнер и разместить его на docker hub, я собрал свой контейнер со стаком LEMW, где W - WSGI для работы python с nginx. 
Ссылка: https://hub.docker.com/r/mackedonsky/webinar

Чтобы понятно было, как собирал и что внутри - в репозитории лежит Dockerfile.

## Makefile

Я никогда не создавал make файлы. Поэтому если там чего критически важного не хватает - извините, я про это не знал. 

## Ошибки которые допустил при выполнении задания:

1. При сборке контейнера nginx, файл конфига supervisord и wsgi не прокинут в локальную директорию, следовательно, им нельзя управлять. Нужно дописать volume в webinar-nginx. 
2. Dockerfile: Только что узнал, что при установке зависимостей, следует чистить мусор в том же слое, в котором и создал. 
Что то вроде такой чистки
```
&& apt autoremove -y && apt clean -y && apt autoclean -y \
&& rm -rf /var/lib/{apt,dpkg,cache,log}/* \
&& rm -rf /tmp/*
```

P.S. Не обращайте внимание на месседжи коммитов. В реальной среде я пишу нормальные сжатые пояснения.
