# Instrucciones

> Levantar  K8S en ambiente local MAC


Herramientes necesarias

```
docker --version
kubectl version
kind --version
cloud-provider-kind version # Binario
```

Abri el Editor  `zed .` posterior a eso explorar el proyecto. Continuar con la creacion de la imagen

Levantar cluster

```shell
kind create cluster --config kind-config.yaml
```

Simula el balanceador de carga

```shell
sudo cloud-provider-kind
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

```
kubectl get nodes
kubectl get pods
kubectl get svc python-app-service
```


## Version 2

Crear imagen

> docker build -t mi-app-python-k8s:v2 .

Cargar Imagen
> kind load docker-image mi-app-python-k8s:v2

Aplicar cambio sobre la raiz /  cambiar le version del despliegue
> kubectl apply -f k8s-despliegue.yaml



## killercoda

Clonar el repo
> git clone https://github.com/favillon/poli-contenedores-k8s.git


Crear imagen
```
docker build -t mi-app-python-k8s:v1 ./src/
```

Guardar imagen
```
docker save mi-app-python-k8s:v1 > mi-app.tar
```

Importar imagen
```
ctr -n=k8s.io images import mi-app.tar
```


Montar la imagen en el cluster

```
kubectl apply -f k8s-despliegue-killercoda.yaml
```

Consultar nodos y pods

```
kubectl get nodes
kubectl get pods
```

Terminar  pods

```
kubectl delete -f k8s-despliegue.yaml
kind delete cluster
```