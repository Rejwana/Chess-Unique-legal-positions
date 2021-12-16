/etc/init.d/mysql start
mysql -uroot -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456ab';FLUSH PRIVILEGES;"
python3 /Py/DB_create.py 
python3 /Py/DB_insert.py $(cat config.txt)

