ansible-nexus
=============

Storage (Nexus/Artifactory) module for ansible.

 It can be used
like so:

Place 'nexus' in 'library/nexus' next to your ansible script.

A task can look like this 
```
- name: Download rpc-repository to this host
  nexus:
      nexus=http://nexus.vpro.nl/
      artifactId=nl.vpro.stats:stats-backend:{{version}}
      extension=jar
    register: download

- name: get statistics jar
  nexus:
    artifactory=http://artifactory.vpro.nl
    artifactId=nl.vpro.stats:stats-backend:0.3-SNAPSHOT
    extension=jar

- name: Upload rpc-repository
  copy:
    src={{download.dest}}
    dest=/opt/{{file}}
```

Here the action is executed locally, because the remote host may not have access to the storage server.
  