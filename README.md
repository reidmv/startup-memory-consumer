# Startup Memory Consumer


## Build command

```
docker buildx build \
  --tag reidmv/startup-memory-consumer:$VERSION \
  --platform linux/amd64,linux/arm64 \
  --builder container \
  --push .
```
