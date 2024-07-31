APP = restapi-flask
NAMESPACE=development

test:
	@black .
	@flake8 . --exclude .venv
	# @pytest -v --disable-warnings
	@bandit -c bandit.toml -r .

compose:
	@docker compose up -d
	@docker compose down

heroku:
	@heroku container:login
	@heroku container:push -a $(APP) web
	@heroku container:release -a $(APP) web

kube-dev:
	@kind create cluster --config kubernetes/kind/cluster.yaml
	@kubectl create ns ${NAMESPACE}
	@kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
	@kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s


kube-secrets:
	@kubectl create secret generic ${APP}-secrets --from-env-file=.env -n ${NAMESPACE}

kube-deploy:
	@docker build -t $(APP):latest .
	@kind load docker-image $(APP):latest
	@kubectl create secret generic ${APP}-secrets --from-env-file=.env -n ${NAMESPACE}
	@kubectl apply -f kubernetes/manifests* -n 

teardown-dev:
	@kind delete clusters kind