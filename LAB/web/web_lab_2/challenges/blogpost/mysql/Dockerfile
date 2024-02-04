# start from the official MySQL image
FROM mysql:8.0

# add the init.sql script to the docker-entrypoint-initdb.d directory
# this script will be run automatically during container startup
COPY init.sql /docker-entrypoint-initdb.d/

