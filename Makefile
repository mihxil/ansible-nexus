.PHONY: test

test:
	../ansible/hacking/test-module -m ./nexus  -a "nexus=http://nexus.vpro.nl artifactId=nl.vpro.stats:stats-backend:0.2.0 extension=jar"
