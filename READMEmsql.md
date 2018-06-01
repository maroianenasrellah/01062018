# MySql

sudo apt-get install mysql-server
sudo apt-get install mysql-client

mysql_secure_installation

sudo su
mysql -u root -p
CREATE DATABASE HR;
CREATE DATABASE rpi;

CREATE USER 'HR'@'localhost' IDENTIFIED BY 'pipi';
CREATE USER 'yapo'@'localhost' IDENTIFIED BY 'pipi'

 SET PASSWORD FOR 'root'@'localhost'= PASSWORD('pipi')
 SET PASSWORD FOR 'HR'@'localhost'= PASSWORD('pipi')
 SET PASSWORD FOR 'yapo'@'localhost'= PASSWORD('pipi')
 //correctif
UPDATE mysql.user SET authenfication_string=PASSWORD('pipi') WHERE User='root' AND Host='localhhost';

UPDATE mysql.user SET authentication_string = PASSWORD('pipi') WHERE User='yapo' and Host='localhost';

UPDATE mysql.user SET authentication_string = PASSWORD('pipi') WHERE User='HR' and Host='localhost';

//GRANT
GRANT ALL PRIVILEGES ON rpi.* TO 'yapo'@'%' IDENTIFIED BY 'pipi';flush privileges;
GRANT select  ON rpi.* TO 'yapo'@'%' IDENTIFIED BY 'pipi';
GRANT ALL PRIVILEGES ON rpi.* TO 'yapo'@'localhost' IDENTIFIED BY 'pipi';flush privileges;

sudo apt install mysql-workbench
sudo nano /etc/mysql/my.cnf