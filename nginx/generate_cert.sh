#!/bin/sh

set -e

CERT_DIR=/home/my_cert
mkdir -p $CERT_DIR

# 若已存在则跳过
if [ ! -f "$CERT_DIR/server.crt" ]; then
    echo "Generating self-signed cert..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
      -subj "/CN=localhost" \
      -keyout "$CERT_DIR/server.key" \
      -out "$CERT_DIR/server.crt"
else
    echo "Cert already exists, skipping."
fi
