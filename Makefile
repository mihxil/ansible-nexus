.PHONY: test

test:
	#~/github/ansible/ansible/hacking/test-module -m ./nexus  -a "nexus=http://nexus.vpro.nl artifactId=nl.vpro.stats:stats-backend:0.3-SNAPSHOT extension=jar"
	~/github/ansible/ansible/hacking/test-module -m ./nexus  -a "nexus=http://nexus.vpro.nl artifactId=nl.vpro.stats:stats-backend:0.2.0 extension=jar"
