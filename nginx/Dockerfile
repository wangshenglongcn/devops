FROM nginx:alpine

RUN apk add --no-cache curl openssl

COPY generate_cert.sh /generate_cert.sh
RUN chmod +x /generate_cert.sh

CMD ["/bin/sh", "-c", "/generate_cert.sh && nginx -g 'daemon off;'"]
