APP = restapi-flask
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