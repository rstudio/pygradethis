PACKAGE=pygradethis
VERSION=$(shell grep 'Version' ./DESCRIPTION | cut -d':' -f2 | tr -d ' ')

############
# Building #
############

all: test
.PHONY: all clean
.PHONY: build

.PHONY: docs
docs:
	R -e "devtools::document(roclets = c('rd', 'collate', 'namespace'))"

build: clean
	R CMD build .

.PHONY: install
install: docs build
	R CMD INSTALL $(PACKAGE)_$(VERSION).tar.gz

###########
# Testing #
###########

.PHONY: test
test:
	R -e "devtools::test()"

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