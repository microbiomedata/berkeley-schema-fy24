MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:
.SECONDARY:

RUN = poetry run
# get values from about.yaml file
# replaced sh with bash esp for linux
SCHEMA_NAME = $(shell bash ./utils/get-value.sh name)
DOCDIR = docs
SOURCE_SCHEMA_PATH = $(shell bash ./utils/get-value.sh source_schema_path)
SOURCE_SCHEMA_DIR = $(dir $(SOURCE_SCHEMA_PATH))
SRC = src
DEST = project
PYMODEL = $(SCHEMA_NAME)
EXAMPLEDIR = examples
TEMPLATEDIR = doc-templates

.PHONY: all clean examples-clean install site site-clean site-copy squeaky-clean test test-python test-with-examples


# note: "help" MUST be the first target in the file,
# when the user types "make" they should get help info

help: status
	@echo ""
	@echo "This project requires that dependencies are loaded into a poetry environment with 'poetry install'"
	@echo "Most typical usage: 'make squeaky-clean all test'" # I removed the `enchilada` convenience target
	@echo "Documentation publication is handled by a GitHub merge action"
	@echo "  but users can generate a local documentation site with 'make testdoc'"
	@echo "Please excuse the currently verbose logging mode"
	@echo "make help -- show this help"
	@echo ""

cookiecutter-help: status
	@echo ""
	@echo "make setup -- initial setup (run this first)"
	@echo "make site -- makes site locally"
	@echo "make install -- install dependencies"
	@echo "make test -- runs tests"
	@echo "make lint -- perfom linting"
	@echo "make testdoc -- builds docs and runs local test server"
	@echo "make deploy -- deploys site"
	@echo "make update -- updates linkml version"
	@echo "make cookiecutter-help -- show this help"
	@echo ""

status: check-config
	@echo "Project: $(SCHEMA_NAME)"
	@echo "Source: $(SOURCE_SCHEMA_PATH)"

# generate products and add everything to github
setup: install gen-project gendoc git-init-add

# install any dependencies required for building
install:
	poetry install


# ---
# Project Synchronization
# ---
#
# check we are up to date
check: cruft-check
cruft-check:
	# added cruft to poetry env and added poetry wrapper to cruft invocations
	$(RUN) cruft check
cruft-diff:
	$(RUN) cruft diff

update: update-template update-linkml
update-template:
	$(RUN) cruft update

# todo: consider pinning to template
update-linkml:
	poetry add -D linkml@latest

# EXPERIMENTAL
create-data-harmonizer:
	npm init data-harmonizer $(SOURCE_SCHEMA_PATH)

# Note: `all` is an alias for `site`.
all: site

# TODO: Document this make target.
site: clean site-clean gen-project gendoc nmdc_schema/gold-to-mixs.sssom.tsv accepting-legacy-ids-all

# may change files in nmdc_schema/ or project/. uncommitted changes are not tolerated by mkd-gh-deploy

%.yaml: gen-project

# was deploy: all mkd-gh-deploy
deploy: gendoc mkd-gh-deploy

# --include prefixmap \
# mv project/prefixmap/nmdc.yaml project/prefixmap/nmdc.json
# that was accounting for the fact that the autogenerated file has a JSON format
# but is given a .yaml extension
# also, it doesn't appear to do the (default) merge over all imports
gen-project: $(PYMODEL) # depends on src/schema/mixs.yaml # can be nuked with mixs-yaml-clean
	# keep these in sync between PROJECT_FOLDERS and the includes/excludes for gen-project and test-schema
	$(RUN) gen-project \
		--exclude excel \
		--exclude graphql \
		--exclude jsonld \
		--exclude markdown \
		--exclude proto \
		--exclude shacl \
		--exclude shex \
		--exclude sqlddl \
		--include jsonldcontext \
		--include jsonschema \
		--include owl \
		--include python \
		--include rdf \
		-d $(DEST) $(SOURCE_SCHEMA_PATH) && mv $(DEST)/*.py $(PYMODEL)
		cp project/jsonschema/nmdc.schema.json  $(PYMODEL)

# TODO: Document these make targets.
test: examples-clean site accepting-legacy-ids-all test-python migration-doctests examples/output
only-test: examples-clean accepting-legacy-ids-all test-python migration-doctests examples/output

test-schema:
	# keep these in sync between PROJECT_FOLDERS and the includes/excludes for gen-project and test-schema
	$(RUN) gen-project \
		--exclude excel \
		--exclude graphql \
		--exclude jsonld \
		--exclude markdown \
		--exclude proto \
		--exclude shacl \
		--exclude shex \
		--exclude sqlddl \
		--include jsonldcontext \
		--include jsonschema \
		--include owl \
		--include python \
		--include rdf \
		-d tmp $(SOURCE_SCHEMA_PATH)

test-python:
	$(RUN) python -m unittest discover

lint:
	$(RUN) linkml-lint $(SOURCE_SCHEMA_PATH) > local/lint.log

check-config:
	@(grep my-datamodel about.yaml > /dev/null && printf "\n**Project not configured**:\n\n - Remember to edit 'about.yaml'\n\n" || exit 0)

# Test documentation locally
serve: mkd-serve

# Python datamodel
$(PYMODEL):
	mkdir -p $@

$(DOCDIR):
	mkdir -p $@

gendoc: $(DOCDIR)
	# added copying of images and renaming of TEMP.md
	cp $(SRC)/docs/*md $(DOCDIR) ; \
	cp -r $(SRC)/docs/images $(DOCDIR) ; \
	$(RUN) gen-doc -d $(DOCDIR) --template-directory $(SRC)/$(TEMPLATEDIR) $(SOURCE_SCHEMA_PATH)
	mkdir -p $(DOCDIR)/javascripts
	$(RUN) cp $(SRC)/scripts/*.js $(DOCDIR)/javascripts/

testdoc: gendoc serve

MKDOCS = $(RUN) mkdocs
mkd-%:
	$(MKDOCS) $*

# keep these in sync between PROJECT_FOLDERS and the includes/excludes for gen-project and test-schema
PROJECT_FOLDERS = jsonldcontext jsonschema owl python rdf
git-init-add: git-init git-add git-commit git-status
git-init:
	git init
git-add: .cruft.json
	git add \
		*.md \
		.cruft.json \
		.github \
		.gitignore \
		CODE_OF_CONDUCT.md \
		CONTRIBUTING.md \
		LICENSE \
		MAINTAINERS.md \
		Makefile \
		README.md \
		RELEASE_NOTES_v7.7.2_to_v7.7.7.md \
		about.yaml \
		assets \
		images \
		mkdocs.yml \
		nmdc_schema \
		notebooks \
		poetry.lock \
		project.Makefile \
		project/ \
		pyproject.toml \
		src/ \
		tests \
		utils
	git add $(patsubst %, project/%, $(PROJECT_FOLDERS))

git-commit:
	git commit -m 'Initial commit' -a

git-status:
	git status

# only necessary if setting up via cookiecutter
.cruft.json:
	echo "creating a stub for .cruft.json. IMPORTANT: setup via cruft not cookiecutter recommended!" ; \
	touch $@

clean:
	rm -rf $(DEST)
	rm -rf tmp
	rm -rf docs/*.md
	rm -rf docs/*.html

include project.Makefile

# custom
site-clean: clean
	rm -rf nmdc_schema/*.json
	rm -rf nmdc_schema/*.tsv
	rm -rf nmdc_schema/*.yaml

squeaky-clean: clean accepting-legacy-ids-clean examples-clean rdf-clean shuttle-clean site-clean # does not include mixs-yaml-clean
	mkdir project

project/nmdc_schema_merged.yaml:
	$(RUN) gen-linkml \
		--format yaml \
		--no-materialize-attributes \
		--no-materialize-patterns \
		--output $@ $(SOURCE_SCHEMA_PATH)
#	mkdir -p project/prefixmap
#	$(RUN) gen-prefix-map \
#		--output project/prefixmap/nmdc.json \
#	  	--mergeimports $@

project/nmdc_materialized_patterns.yaml:
	$(RUN) gen-linkml \
		--format yaml \
		--materialize-patterns \
		--no-materialize-attributes \
		--output $@ $(SOURCE_SCHEMA_PATH)

project/nmdc_materialized_patterns.schema.json: project/nmdc_materialized_patterns.yaml
	$(RUN) gen-json-schema \
		--closed \
		--top-class Database $< > $@

nmdc_schema/gold-to-mixs.sssom.tsv: sssom/gold-to-mixs.sssom.tsv nmdc_schema/nmdc_materialized_patterns.schema.json \
nmdc_schema/nmdc_materialized_patterns.yaml nmdc_schema/nmdc_schema_merged.yaml
	# just can't seem to tell pyproject.toml to bundle artifacts like these
	#   so reverting to copying into the module
	cp $< $@

nmdc_schema/nmdc_materialized_patterns.schema.json: project/nmdc_materialized_patterns.schema.json
	cp $< $@

nmdc_schema/nmdc_materialized_patterns.yaml: project/nmdc_materialized_patterns.yaml
	cp $< $@

nmdc_schema/nmdc_schema_merged.yaml: project/nmdc_schema_merged.yaml
	cp $< $@
