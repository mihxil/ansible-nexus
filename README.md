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

# Download validation and md5 checks

Currently only the timestamp of the file is used to validate whether to run the download task. This should be changed to leverage the md5 checking built into Nexus.

This can be grabbed by making a HEAD request to the nexus for http://blar.com/service/local/repositories/<repository>/content/<groupid>/<artifact>/<version>/<artifact>-<version>.<type>.md5


