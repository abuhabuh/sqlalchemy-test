install:
	pip install -r requirements.txt

run-db: install
	docker-compose up &

run-tests:
	python test_query_perf.py
