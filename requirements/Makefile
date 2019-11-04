# https://jamescooke.info/a-successful-pip-tools-workflow-for-managing-python-package-requirements.html

objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)

.PHONY: all
all: $(outputs)

%.txt: %.in
	pip-compile -v --output-file $@ $<

test.txt: base.txt
production.txt: base.txt
ci.txt: test.txt
local.txt: test.txt

.PHONY: check
check:
	@which pip-compile > /dev/null

.PHONY: clean
clean: check
	- rm *.txt
