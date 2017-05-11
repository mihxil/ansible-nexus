ansible-nexus
=============

Storage (Nexus/Artifactory) module for ansible.

# Installation

Place 'nexus' in 'library/nexus' next to your ansible script.

# Example tasks

## Download latest version using nexus
```
  - name: Download costello
    nexus:
        nexus: https://oss.sonatype.org/
        artifactId: abbot:costello:latest
        extension: jar
        repository: public
```

## Download specific version using nexus
```
  - name: Download costello 1.4.0
    nexus:
        nexus: https://oss.sonatype.org/
        artifactId: abbot:costello:1.4.0
        extension: jar
        repository: public
```
## Download specific version using artifactory and credentials
```
- name: get statistics jar
  nexus:
    artifactory: http://artifactory.vpro.nl
    artifactId: nl.vpro.stats:stats-backend:0.3-SNAPSHOT
    extension: jar
    http_user: wibble
    http_pass: wibble

```
## Downloading localling and uploading to a remote machine

```
- name: Download costello locally
  local_action: >
      nexus nexus=https://oss.sonatype.org/ artifactId=abbot:costello:latest extension=jar repository=public http_user= http_pass=
  register: download

- debug: msg="{{download.dest}}"

- name: Upload costello to /tmp/wibble.war
  copy:
      src: "{{download.dest}}"
      dest: /tmp/wibble.war

```


# Globally setting default parameters

A common requirement when using a proxied Nexus installation is to fix the Nexus url and the credentials used. Ansible doesn't have a mechanism to set default for types like Puppet:-

https://docs.puppet.com/puppet/4.9/lang_defaults.html

http://serverfault.com/questions/702856/is-there-a-salt-equivalent-to-puppets-resource-default-statements

So a workaround is to change this modules default when you download it:-

```
...

def main():

    module = AnsibleModule(
        argument_spec=dict(
            nexus=dict(required=False, default="wibble"),
            artifactory=dict(required=False),
            repository=dict(required=False, default="public"),
            destdir=dict(required=False, default="/tmp/downloaded_artifacts"),
            filename=dict(required=False, default=None),
            artifactId=dict(required=True),
            extension=dict(required=False, default="war"),
            force=dict(required=False, default=False, choices=BOOLEANS, type='bool'),
            http_user=dict(required=False, default="wibble"),
            http_pass=dict(required=False, default="wibble")
...
```

Caveat is that once the basic auth defaults are set you must unset them with blank values to use some public repositories.

# Download / change validation and md5 checks

2 methods of validation are supported for testing whether to download an artifact:-

1. If timestamp of local file is older than last modified date of the remote artifact
2. If md5 of the file is different from the md5 of the remote file (Nexus only)

Md5 takes precidence if it's available as this method is more robust and allows downgrades as well as upgrades

# Chaining actions when an artifact is downloaded

To perform actions only when a new artifact is downloaded use this stanza:-

```
- name: get statistics jar
  nexus:
    artifactory: http://artifactory.vpro.nl
    artifactId: nl.vpro.stats:stats-backend:0.3-SNAPSHOT
    extension: jar
    http_user: wibble
    http_pass: wibble
  register: nexus_download

- name: copy artifact to final location
  copy:
    dest: /tmp/final/blar.jar
    src: "{{ nexus_download.dest }}"
  when: nexus_download.changed
```

