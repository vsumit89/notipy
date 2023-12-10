build:
	docker compose build
build-and-run:
	docker compose up --build
stop:
	docker compose stop
clean:
	docker compose down
run:
	docker compose up