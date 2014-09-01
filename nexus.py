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


import datetime
import sys
import json
import os
import shlex
import urllib


def main():
    args_file = sys.argv[1]
    args_data = file(args_file).read()
    arguments = shlex.split(args_data)

    extension = "war"
    for arg in arguments:
        if "=" in arg:
            (key, value) = arg.split("=")
            if key == "artifactId":
                artifactId = value
            if key == "nexus":
                nexus = value
            if key == "extension":
                extension = value



    public = nexus + "/content/groups/public/"
    split = artifactId.split(":");
    groupId    = split[0]
    artifactId = split[1]
    version    = split[2]
    if len(split) >= 4:
        classifier = "&c=" + split[3]
    else:
        classifier = ""


    if  "$classifier" == "":
        postfix = ""
    else:
        postfix = "-" + classifier

    artifactFileName = artifactId + "-" + version + postfix + extension
    if "SNAPSHOT" in version:
        repo = "snapshots"
    else:
        repo = "releases"

    artifactDownload = nexus + "/service/local/artifact/maven/redirect?r=" + repo + "&g=" + groupId + "&a=" + artifactId + "&v=" + version + "&e=" + extension + classifier
    dest = artifactId + "-" + version + "." + extension
    get(artifactDownload, dest)

    print json.dumps({
        "artifactId" : artifactId,
        "nexus": nexus,
        "artifactDownload": artifactDownload,
        "dest": dest
    })


def get(url, dest):
    #print "retrieving " + url
    respon = urllib.urlretrieve(url,  dest)



main()
