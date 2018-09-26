
PWD := $(shell pwd)
PACKAGE = os-config
SERVER := lookout-micro

default: rpm

push: rpm
	scp rpm/RPMS/noarch/*$(PACKAGE)*.rpm $(SERVER):
	ssh $(SERVER) 'sudo yum update -y *$(PACKAGE)*.rpm'
	ssh $(SERVER) 'rm -f *$(PACKAGE)*.rpm'

update: rpm
	sudo yum --enablerepo=epel update -y rpm/RPMS/noarch/$(PACKAGE)-*.noarch.rpm

repo: rpm
	rm -rf repo
	mkdir -p repo/Packages
	cp rpm/RPMS/*/*.rpm repo/Packages
	createrepo --quiet --unique-md-filenames repo

rpm: build
	rm -rf rpm
	mkdir -p rpm/BUILD rpm/RPMS rpm/BUILDROOT
	rpmbuild --quiet -bb --define="_topdir $(PWD)/rpm" $(PACKAGE).spec

build:
	@echo Nothing to build yet

clean:
	$(RM) -rf $(CLEANS)
	$(RM) -rf rpm exports repo

distclean: clean

