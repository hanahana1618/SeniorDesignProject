#setup a web server in a pi

sudo apt-get update && sudo apt-get upgrade
sudo apt-get install apache2 php5 libapache2-mod-php5

#after apache is done installing, make sure to restart the service
sudo service apache2 restart

#install the MySQL + MariaDB programs
sudo apt-get install default-mysql-server
location of install: /var/lib/mysql

#LAMP server implementation
https://www.raspberrypistarterkits.com/how-to/install-wordpress-on-raspberry-pi/

#allow user registration to the wordpress site
https://www.wpbeginner.com/beginners-guide/how-to-allow-user-registration-on-your-wordpress-site/

#raspberrypi 2 main unit
username: pi
password: ~1234%^

#database data same as MySQL credentials
database name: wordpress
username: root
password: p@$$G0!@#
database host: localhost
table prefix: wp_

#Wordpress settings
Site Title: PDS Website
Username: root
Password: 7#Pm*oZP2*jll@3~
Your Email: peterdefense@gmail.com


#to connect wordpress to the outside world you need FTP
install fileZill in the development computer to make sure
the connection is good: sudo apt install filezilla

install ftp in the target device to be able to interact
with the ftp: sudo apt install proftpd
after installation make sure to follow the steps here: https://howtoraspberrypi.com/setup-ftp-server-raspberry-pi/

run a nmap sn scan to make sure the target device has ftp setup
correctly: nmap sn 192.168.1.1
if port 22 is open then the ftp server is working correctly

#TODO
uninstall Filezilla in endpoint unit
uninstall apache, mysql and wordpress and php5 from endpoint
