kubectl get all
kubectl get pods

helm repo update

helm dep build


helm upgrade --install templatechart .
helm uninstall templatechart
kubectl rollout restart deployment templatechart
