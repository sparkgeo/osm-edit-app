
fetch-remotes:
	docker compose up fetch-osm fetch-iD

start:
	docker compose up web db editor -d

clean:
	docker compose up clean-osm clean-iD

run-all:
	make fetch-remotes
	make start
	make clean