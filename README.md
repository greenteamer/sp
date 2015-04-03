## sp


# полезные ссылки:
http://rche.ru/818_cms-dlya-sajta-sovmestnyx-pokupok.html - расписаны основные функции сайта сп



# mysql:
CREATE DATABASE `sp` CHARACTER SET utf8 COLLATE utf8_general_ci;

    
# для модуля
если возникает ошибка: decoder jpeg not available, то:

///install libjpeg-dev with apt
`sudo apt-get install libjpeg-dev`

///reinstall pillow
`pip install -I pillow`


# после создания базы
python ../manage.py syncdb
python ../manage.py syncdb --all
python ../manage.py migrate pybb --fake
python ../manage.py schemamigration core --initial
python ../manage.py schemamigration pristroy --initial
python ../manage.py schemamigration cart --initial
python ../manage.py schemamigration accounts --initial
python ../manage.py migrate core 0001 --fake
python ../manage.py migrate pristroy 0001 --fake
python ../manage.py migrate cart 0001 --fake
python ../manage.py migrate accounts 0001 --fake
python ../manage.py loaddata __initial_data.json



