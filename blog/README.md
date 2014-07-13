blog - based on zinnia
=====

Install
1. install zinnia
$ git clone git://github.com/Fantomas42/django-blog-zinnia.git
$ cd django-blog-zinnia
$ grep django_comments -r *|awk -F: '{print $1}'|while read f; do sed -i 's/django_comments/django.contrib.comments/g' $;f done
$ python setup.py install

2. create database
mysql -uroot
create database blog;
grant all privileges on blog.* to blogu@localhost identified by blogp;
flush privileges;

3. syncdb
python manage.py syncdb


4. run
python manage.py runserver 0.0.0.0:80
