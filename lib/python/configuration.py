#!/usr/bin/python

# This file is part of Coccitools.

# Copyright (C) 2010  Florian MANY

# Coccitools is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Coccitools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with Coccitools.  If not, see <http://www.gnu.org/licenses/>.


import os, ConfigParser


## Function called by the cocci module if the file "coccitools.conf" does not exist.
#This function generates a "coccitools.conf" file that contains the features of the installation, the path of the cocci tree and  the path of the project tree.
# @param path installation path of coccitools
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

