# art_hub

# running in docker

## Build the image

```
docker build -t flask-image .
```

## Build the container

```
docker run -p 5000:5000 --rm --name flask-container flask-image
```
