# Instrucciones

> Levantar  K8S en ambiente local MAC


Tener docker instalado

docker --version
kubectl version
kind --version
cloud-provider-kind version


Levantar cluster

```shell
kind create cluster --config kind-config.yaml
```

Simula el balanceador de carga

```shell
cloud-provider-kind
```


Crear imagen
```
docker build -t mi-app-python-k8s:v1 .
```


Montar la imagen en el cluster

```
kind load docker-image mi-app-python-k8s:v1
```


Monstar el imange del cluster
```
kubectl apply -f k8s-despliegue.yaml
```


kubectl get nodes
kubectl get pods
kubectl get svc python-app-service