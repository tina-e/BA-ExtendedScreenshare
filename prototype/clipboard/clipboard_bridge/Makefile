.PHONY: all packages clean run

all: packages

packages:
	python3 -m venv venv; . venv/bin/activate; pip3 install -r ./requirements.txt

clean:
	rm -rf venv

run:
	. venv/bin/activate;cd src; python3 main.py $(ARGS)
