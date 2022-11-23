PACKAGE=pygradethis
VERSION=$(shell grep 'Version' ./DESCRIPTION | cut -d':' -f2 | tr -d ' ')

# The fallback R library to use when there isn't a specific library selected
# You can set this to your system's R library or a project library when using {renv}
R_LIB_PATH_FALLBACK="/Library/Frameworks/R.framework/Versions/4.1-arm64/Resources/library"

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

# NOTE: R_LIB_PATH is an environment variable that points to the path of an R library
# if that is not set, this installs the package in the system R library (R_LIB_PATH_FALLBACK)
.PHONY: install
install: docs build
ifeq ($(local), true)
	R CMD INSTALL -l $(or $(R_LIB_PATH), $(R_LIB_PATH_FALLBACK)) $(PACKAGE)_$(VERSION).tar.gz
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