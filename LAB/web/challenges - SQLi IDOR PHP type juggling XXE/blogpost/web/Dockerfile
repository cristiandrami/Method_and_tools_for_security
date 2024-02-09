FROM php:7.4-apache
RUN docker-php-ext-install pdo_mysql
RUN apt update && apt install vim -y
COPY src/ /var/www/html/
#RUN chown www-data:www-data /var/www/html/posts.json  && chmod 644 /var/www/html/posts.json
EXPOSE 80

