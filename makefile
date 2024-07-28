.DEFAULT_GOAL := configure

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

.envrc: example.envrc
	touch .envrc
	cat example.envrc >> .envrc
	$${EDITOR:-nano} .envrc

.env: .envrc
	cp .envrc .env
	sed -i "s/export //g" .env

systemd/dyndns.service: systemd/dyndns.service.example
	cp systemd/dyndns.service.example systemd/dyndns.service
	sed -i  "s#/path/to/project/root#${current_dir}#g" systemd/dyndns.service

.venv-created: lock.txt
	python -m venv env
	touch .venv-created

.requirements-installed: .venv-created lock.txt
	. env/bin/activate && pip install -r lock.txt
	touch .requirements-installed

.PHONY: configure
configure: .env systemd/dyndns.service .requirements-installed

.PHONY: install
install: configure
	sudo systemctl enable ${current_dir}/systemd/dyndns.service
	sudo systemctl enable --now ${current_dir}/systemd/dyndns.timer

.PHONE: unconfigure
unconfigure:
	rm -f .env .envrc systemd/dyndns.service
	rm -rf env

.PHONY: uninstall
uninstall: unconfigure
	sudo systemctl disable ${current_dir}/systemd/dyndns.timer
