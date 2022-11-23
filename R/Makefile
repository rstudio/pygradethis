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

##############
# Installing #
##############

# R_LIB_PATH is the path of your project's R library
# if that is not set, install the package in the system R library
# e.g. /Library/Frameworks/R.framework/Versions/4.1-arm64/Resources/library
.PHONY: install
install: docs build
ifdef R_LIB_PATH
	R CMD INSTALL -l $(R_LIB_PATH) $(PACKAGE)_$(VERSION).tar.gz
else
	R CMD INSTALL $(PACKAGE)_$(VERSION).tar.gz
endif

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