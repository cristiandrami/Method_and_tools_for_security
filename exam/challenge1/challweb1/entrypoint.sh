#!/bin/bash

# Generate a random string and then create its MD5 hash for the flag
FLAG="EMS{$(echo $RANDOM | md5sum | head -c 32)}"
export FLAG

# Keep the container running
apache2-foreground

