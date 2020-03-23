.PHONY: all help translate test clean update compass collect rebuild

MODULE := recipes_rest

SETTINGS={{ project_name }}.settings
TEST_SETTINGS={{ project_name }}.test_settings

TAG := $(shell git describe --tags --always --dirty)
IMAGE := $(REGISTRY)/$(MODULE)

BLUE='\033[0;34m'
NC='\033[0m' #

# target: all - Default target. Does nothing.
all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: Runs django server
run:
	@echo "Running django app"
	@python manage.py runserver

build:
	@echo "\n${BLUE}Building Development image with labels:\n"
	@echo "name: $(MODULE)"
	@echo "version: $(TAG)${NC}\n"
	@sed                                 \
	    -e 's|{NAME}|$(MODULE)|g'        \
	    -e 's|{VERSION}|$(TAG)|g'        \
	    dev.Dockerfile | docker build -t $(IMAGE):$(TAG) -f- .

# Example: make shell CMD="-c 'date > datefile'"
shell: build-dev
	@echo "\n${BLUE}Launching a shell in the containerized build environment...${NC}\n"
		@docker run                                                 \
			-ti                                                     \
			--rm                                                    \
			--entrypoint /bin/bash                                  \
			-u $$(id -u):$$(id -g)                                  \
			$(IMAGE):$(TAG)										    \
			$(CMD)

.PHONY: clean image-clean build-prod push test

docker-clean:
	@docker system prune -f --filter "label=name=$(MODULE)"

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: translate - calls the "makemessages" django command
translate:
	cd {{ project_name }} && django-admin.py makemessages --settings=$(SETTINGS) -i "site-static/*" -a --no-location

# target: test - calls the "test" django command
test:
	django-admin.py test --settings=$(TEST_SETTINGS)

# target: clean - remove all ".pyc" files
clean:
	django-admin.py clean_pyc --settings=$(SETTINGS)
	rm -rf .pytest_cache .coverage .pytest_cache coverage.xml

# target: update - install (and update) pip requirements
update:
	pip install -U -r requirements.txt

# target: compass - compass compile all scss files
compass:
	cd {{ project_name }}/compass && compass compile

# target: collect - calls the "collectstatic" django command
collect:
	django-admin.py collectstatic --settings=$(SETTINGS) --noinput

# target: rebuild - clean, update, compass, collect, then rebuild all data
rebuild: clean update compass collect
	django-admin.py reset_db --settings=$(SETTINGS) --router=default --noinput
	django-admin.py syncdb --settings=$(SETTINGS) --noinput
	django-admin.py migrate --settings=$(SETTINGS)
	#django-admin.py loaddata --settings=$(SETTINGS) <your fixtures here>