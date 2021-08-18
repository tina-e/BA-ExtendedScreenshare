.PHONY: all packages run

all: packages

packages:
	$(MAKE) -C clip_server
	$(MAKE) -C clipboard_bridge

run:
	cd clip_server && . venv/bin/activate && python3 ./src/main.py & echo $$! > server.pid
	cd clipboard_bridge && . venv/bin/activate && python3 ./src/main.py & echo $$! > bridge.pid
stop:
	SERVERPID=$(shell cat server.pid); \
	rm server.pid; \
	kill $$SERVERPID;
	BRIDGEPID=$(shell cat bridge.pid); \
	rm bridge.pid; \
	kill $$BRIDGEPID;