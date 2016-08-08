NAME = plugin.audio.radio-t
GIT = git
GIT_VERSION = $(shell $(GIT) describe --always)
VERSION = $(shell cat VERSION)
ZIP_SUFFIX = zip
ZIP_FILE = $(NAME)-$(VERSION).$(ZIP_SUFFIX)

all: clean zip

$(ZIP_FILE):
	git archive --format zip --prefix $(NAME)/ --output $(ZIP_FILE) HEAD
	rm -rf $(NAME)

zip: $(ZIP_FILE)

clean:
	rm -rf $(NAME)
