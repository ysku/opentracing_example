Opentraing Example
===================

> Opentracing example of asynchronous distributed processes over queue.

```
# build docker image beforehand
$ docker build -t opentracing_example:latest .

# start example
$ docker-compose up
```

```
$ curl -X POST localhost:50001/upload/[you name it]
```

see stdout of docker containers
