FROM php:7.4-apache
COPY src/ /var/www/html/
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN chown -R www-data:www-data /var/www/html/uploads
RUN chmod -R 755 /var/www/html/uploads
RUN docker-php-ext-install exif
ENTRYPOINT ["entrypoint.sh"]

