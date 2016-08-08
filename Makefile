NAME = plugin.audio.radio-t
GIT = git
GIT_VERSION = $(shell $(GIT) describe --always)
VERSION = $(shell cat VERSION)
ZIP_SUFFIX = zip
ZIP_FILE = $(NAME)-$(VERSION).$(ZIP_SUFFIX)

all: clean zip

$(ZIP_FILE):
	cp addon.xml addon.xml.tmp
	sed -r "2s/([0-9]+\.[0-9]+\.[0-9]+)/$(VERSION)/" addon.xml.tmp > addon.xml
	rm addon.xml.tmp
	git archive --format zip --prefix $(NAME)/ --output $(ZIP_FILE) HEAD

zip: $(ZIP_FILE)

clean:
	rm -rf $(NAME)
