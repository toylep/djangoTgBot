DC = docker-compose
EXEC = $(DC) exec django python

up:
	@$(DC) up --detach --wait

up-debug:
	@$(DC) up

down:
	@$(DC) down

logs:
	@$(DC) logs --tail=0 --follow

migrate:
	@$(EXEC) manage.py migrate

migrations:
	@$(EXEC) manage.py makemigrations

bash:
	@$(DC) exec django bash
