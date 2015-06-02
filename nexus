#!/usr/bin/env python

DOCUMENTATION = '''
---
module: nexus
short_description: Download and install an artifact from storage.
    See https://github.com/mihxil/ansible-nexus
author: Michiel Meeuwissen, Marc Bosserhoff, Rostyslav Fridman
options:
    nexus:
        required: true
        description:
            - Base url of the nexus
    artifactory:
        required: true
        description:
            - Base url of the artifactory
    repository:
        required: false
        description:
            - Optional the used repository
            - Defaults to 'public'
    destdir:
        required: false
        description:
            - The destination dir of the downloaded artifacts
            - Defaults to '/tmp/downloaded_artifacts'
    artifactId:
        required:: true
        description:
            - The artifact to download. The format is separated by ':' and
              will be connected like so: groupId:artifactId:version
    extension:
        required: false
        description:
            - The artifact extension (Defaults to 'war')
    force:
        required: false
        description:
            - Forces the download of the artifacts if they are present
              in the target destination
    http_user:
        required: false
        description:
            - If the storage need a basic authentication, the user name
              can be provided here
    http_pass:
        required: false
        description:
            - If the storage need a basic authentication, the password
              can be provided here
'''

EXAMPLES = '''
- name: get statistics jar
  nexus:
    nexus=http://nexus.vpro.nl
    artifactId=nl.vpro.stats:stats-backend:0.3-SNAPSHOT
    extension=jar

- name: get statistics jar
  nexus:
    artifactory=http://artifactory.vpro.nl
    artifactId=nl.vpro.stats:stats-backend:0.3-SNAPSHOT
    extension=jar
'''

import urllib2
import base64
from datetime import datetime
from wsgiref.handlers import format_date_time
import xml.etree.ElementTree as ET
from ansible.module_utils.basic import *


def loadArtifact(url, dest, http_user, http_pass, force):

    result = dict(url=url, http_user=http_user, force=force)

    try:
        headers = {}

        # Support if modified header if not using 'force' flag
        # to always download artifacts
        if os.path.isfile(dest) and not force:
            headers['IF-Modified-Since'] = \
                format_date_time(time.mktime(datetime.fromtimestamp(
                    os.path.getmtime(dest)).timetuple()))

        if http_user and http_pass:
            headers['Authorization'] = "Basic %s" % \
                base64.encodestring('%s:%s' %
                                    (http_user, http_pass)).replace('\n', '')

        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)

        if response.code == 200:
            handle = open(dest, 'wb')
            handle.write(response.read())
            handle.close()

        # Everything went ok, set result set accordingly
        result['failed'] = False
        result['code'] = response.code
        result['msg'] = "OK"
        result['changed'] = True

        return result

    except Exception as e:
        # In case of error, let ansible stop the playbook
        result['failed'] = True
        result['changed'] = False
        result['msg'] = "Unknown error"
        if hasattr(e, "code"):
            result['code'] = e.code
            if hasattr(e, "reason"):
                result['msg'] = e.reason
            else:
                result['msg'] = "The server couldn\'t fulfill the request."

            # In case of 304 the resource is still in place and not updated
            if e.code == 304:
                result['failed'] = False

            return result

        raise e


def get_version(url, version_to_find, http_user, http_pass):
    result = dict(url=url, http_user=http_user)
    if "SNAPSHOT" in version_to_find:
        url = url + "/" + version_to_find

    try:
        headers = {}
        if http_user and http_pass:
            headers['Authorization'] = "Basic %s" % \
                base64.encodestring('%s:%s' %
                                    (http_user, http_pass)).replace('\n', '')

        request = urllib2.Request(url + "/maven-metadata.xml", None, headers)
        response = urllib2.urlopen(request)

        xml = response.read()

        root = ET.fromstring(xml)

        if any(x in version_to_find.lower() for x in ["latest", "release"]):
            for version in root.findall('versioning'):
                return version.find(version_to_find.lower()).text

        if "SNAPSHOT" in version_to_find:
            return root.find(
                'versioning/snapshotVersions/snapshotVersion/value').text

    except Exception as e:
        # In case of error, let ansible stop the playbook
        result['failed'] = True
        result['msg'] = "Unknown error"
        if hasattr(e, "code"):
            result['code'] = e.code
            if hasattr(e, "reason"):
                result['msg'] = e.reason
            else:
                result['msg'] = "The server couldn\'t fulfill the request."

            return result

        raise e


def main():

    module = AnsibleModule(
        argument_spec=dict(
            nexus=dict(required=False),
            artifactory=dict(required=False),
            repository=dict(required=False, default="public"),
            destdir=dict(required=False, default="/tmp/downloaded_artifacts"),
            filename=dict(required=False, default=None),
            artifactId=dict(required=True),
            extension=dict(required=False, default="war"),
            force=dict(required=False, default=False, choices=BOOLEANS),
            http_user=dict(required=False),
            http_pass=dict(required=False)
        ),
        supports_check_mode=False
    )

    nexus = module.params['nexus']
    artifactory = module.params['artifactory']
    repository = module.params['repository']
    destdir = module.params['destdir']
    artifactId = module.params['artifactId']
    filename = module.params['filename']
    extension = module.params['extension']
    force = module.boolean(module.params['force'])
    http_user = module.params['http_user']
    http_pass = module.params['http_pass']

    # Prepare strings and urls before the storage call
    split = artifactId.split(":")
    (groupId, artifactId, version) = split[0:3]

    classifier = split[3] if len(split) >= 4 else ""

    urlAppendClassifier = "&c=" + classifier if classifier else ""
    postfix = "-" + classifier if classifier else ""

    if repository == "":
        repository = "snapshots" if "SNAPSHOT" in version else "releases"

    original_version = version
    group_version = version
    # Retrieve latest artifact API functionality is available only in
    # Artifactory Pro. We will have to use a workaround
    if artifactory and re.search('(release|latest|snapshot)', version.lower()):
        artifact_url = artifactory + "/" + repository + "/" + \
            groupId.replace(".", "/") + "/" + artifactId
        version = get_version(
            artifact_url,
            original_version,
            http_user,
            http_pass
        )

        if "failed" in version:
            module.fail_json(
                artifactId=artifactId,
                url=artifact_url,
                repository=repository,
                msg=version['msg'],
                result=version
            )

        if any(x in original_version.lower() for x in ["latest", "release"]):
            group_version = version

    # Create generic filename if filename is not set
    if filename is None:
        filename = artifactId + "-" + version + postfix + "." + extension

    if nexus:
        url = nexus + "/service/local/artifact/maven/redirect?r=" + \
            repository + "&g=" + groupId + "&a=" + artifactId + "&v=" + \
            version + "&e=" + extension + urlAppendClassifier
        storage = nexus

    if artifactory:
        url = artifactory + "/" + repository + "/" + \
            groupId.replace(".", "/") + "/" + artifactId + "/" + group_version + \
            "/" + filename
        storage = artifactory

    if not os.path.exists(destdir):
        os.mkdir(destdir)

    dest = destdir + "/" + filename

    # Try to load artifact from storage
    result = loadArtifact(url, dest, http_user, http_pass, force)

    if result['failed']:
        module.fail_json(
            artifactId=artifactId,
            storage=storage,
            url=url,
            filename=filename,
            dest=dest,
            repository=repository,
            changed=result['changed'],
            msg=result['msg'],
            result=result
        )

    module.exit_json(
        dest=dest,
        filename=filename,
        artifactId=artifactId,
        changed=result['changed']
    )

main()
