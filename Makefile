APP = restapi-flask
test:
	@bandit -c bandit.toml -r .
	@black .
	@flake8 . --exclude .venv
	@pytest -v --disable-warnings
compose:
	@docker compose up -d
	@docker compose down

heroku:
	@heroku container:login
	@heroku container:push -a $(APP) web
	@heroku container:release -a $(APP) web