running the container:
```
docker pull ryantanaka/iris:http-proxy
docker container run -d -e PYTHONUNBUFFERED=1 -p 8000:8000 ryantanaka/iris:http-proxy 
```
