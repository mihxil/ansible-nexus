ansible-nexus
=============

Nexus module for ansible. It speaks to the nexus API.

 It can be used
like so:

Place 'nexus' in 'library/nexus' next to your ansible script.

A task can look like this 
```
- name: Download rpc-repository to this host
  local_action: nexus
      nexus=http://nexus.vpro.nl/
      artifactId=nl.vpro.stats:stats-backend:{{version}}
      extension=jar
    register: download

- name: Upload rpc-repository
  copy:
    src={{download.dest}}
    dest=/opt/{{file}}
```

Here the action is executed locally, because the remote host may not have access to the nexus server.
  
  
