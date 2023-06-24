env:
	cp .env.sample .env

prepare:
	pip install -r requirements.txt

update_requirements:
	pip freeze > requirements.txt

init:
	make env
	make prepare

test_report:
	coverage run --source='.' manage.py test
	coverage report
	coverage html
