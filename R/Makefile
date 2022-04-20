PACKAGE=pygradethis

############
# Building #
############

all: test
.PHONY: all clean
.PHONY: build

build: clean
	R CMD build .

.PHONY: install
install: install
	R CMD INSTALL --no-multiarch --with-keep.source R .

###########
# Testing #
###########

.PHONY: check test

test: check

############
# Clean up #
############

.PHONY: clean

clean:
	rm -f $(PACKAGE)_*.tar.gz
	rm -rf $(PACKAGE).Rcheck