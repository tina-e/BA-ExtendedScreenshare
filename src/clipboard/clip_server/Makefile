.PHONY: all packages clean run

all: packages

packages:
	python3 -m venv venv; . venv/bin/activate; pip3 install -r requirements.txt

run:
	. venv/bin/activate; python3 ./src/main.py $(ARGS)

clean:
	rm -rf venv
test:
	. venv/bin/activate; python3 ./src/main.py $(ARGS) & echo $$! > testserver.pid
	sleep 5;
	. venv/bin/activate; python3 -m pytest;
	# TPID=$(shell cat testserver.pid);
	# rm testserver.pid; \
	# kill $$TPID;