#!/usr/bin/python

import os, ConfigParser

# ============================
# init
# ============================
def initConfig(path):

    # When adding sections or items, add them in the reverse order of
    # how you want them to be displayed in the actual file.
    # In addition, please note that using RawConfigParser's and the raw
    # mode of ConfigParser's respective set functions, you can assign
    # non-string values to keys internally, but will receive an error
    # when attempting to write to a file or when you get it in non-raw
    # mode. SafeConfigParser does not allow such assignments to take place.
    config = ConfigParser.RawConfigParser()

    #
    config.add_section('Environment')
    config.set('Environment', 'lib_python_path', path + "lib/python/")
    config.set('Environment', 'libexec_python_path', path +"libexec/python/" )
    config.set('Environment', 'installation_path', path)

    #
    config.add_section('Projects')
    config.set('Projects', 'default_project', '')
    config.set('Projects', 'project_path', path + "projects/")

    #
    config.add_section('Cocci')
    config.set('Cocci', 'cocci_path', path + "cocci/")

    # Writing our configuration file to 'example.cfg'
    with open(path + "coccitools.conf", 'wb') as configfile:
        config.write(configfile)

