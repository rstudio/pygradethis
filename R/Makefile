PACKAGE=pygradethis
VERSION=$(shell grep 'Version' ./DESCRIPTION | cut -d':' -f2 | tr -d ' ')

############
# Building #
############

all: test
.PHONY: all clean
.PHONY: build

build: clean
	R CMD build .

.PHONY: install
install: build
	R CMD INSTALL $(PACKAGE)_$(VERSION).tar.gz

###########
# Testing #
###########

.PHONY: check test

test: check

############
# Clean up #
############

.PHONY: uninstall
uninstall:
	R CMD REMOVE $(PACKAGE)

.PHONY: clean

clean:
	rm -f $(PACKAGE)_*.tar.gz
	rm -rf $(PACKAGE).Rcheck