#!/usr/bin/env python

DOCUMENTATION='''
---
module: nexus
short_description: Download and installs an artifact from nexus
author: Michiel Meeuwissen
'''

EXAMPLES='''
- name: get statistics jar
  nexus: nexus=http://nexus.vpro.nl artifactId=nl.vpro.stats:stats-backend:0.3-SNAPSHOT extension=jar
'''


import sys
import json
import os
import shlex
import urllib
import urllib2


def main():
    args_file = sys.argv[1]
    args_data = file(args_file).read()
    arguments = shlex.split(args_data)

    extension = "war"
    repo = ""
    for arg in arguments:
        if "=" in arg:
            (key, value) = arg.split("=")
            if key == "artifactId":
                artifactId = value
            if key == "nexus":
                nexus = value
            if key == "extension":
                extension = value
            if key == "repository":
                repo = value



    public = nexus + "/content/groups/public/"
    split =  artifactId.split(":")
    (groupId, artifactId, version)  = split[0:3]

    if len(split) >= 4:
        classifier = "&c=" + split[3]
    else:
        classifier = ""


    if  "$classifier" == "":
        postfix = ""
    else:
        postfix = "-" + classifier

    artifactFileName = artifactId + "-" + version + postfix + extension
    if repo == "":
        if "SNAPSHOT" in version:
            repo = "snapshots"
        else:
            repo = "releases"

    artifactDownload = nexus + "/service/local/artifact/maven/redirect?r=" + repo + "&g=" + groupId + "&a=" + artifactId + "&v=" + version + "&e=" + extension + classifier
    if not os.path.exists("nexus"):
        os.mkdir("nexus")
    dest = "nexus/" + artifactId + "-" + version + "." + extension
    resp = get(artifactDownload, dest)

    print json.dumps({
        "artifactId" : artifactId,
        "nexus": nexus,
        "artifactDownload": artifactDownload,
        "dest": dest,
        "repository": repo,
        "response":  {"code": resp['code'], "message": resp['msg'] }
    })


def get(url, dest):
    try:
        #print "retrieving " + url
        (filename, headers) = urllib.urlretrieve(url,  dest)
        return {"code": 200, "msg": "OK"}
    except urllib2.URLError, e:
        if not hasattr(e, "code"):
            raise
        return e



main()
