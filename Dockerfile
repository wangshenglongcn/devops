FROM gcc:13

WORKDIR /app
COPY . .

RUN g++ hello.cc -o app

CMD ["./app"]
