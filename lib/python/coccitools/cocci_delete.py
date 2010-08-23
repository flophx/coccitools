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

import os, sys
import argparse
import shutil

## Function called by the cocci module
# @param params command line options/args of "cocci delete"
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
def delete(params, config):

    # Options and Arguements
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', '--project', dest='delProject', help='delete existing project', nargs='+')
    parser.add_argument('-C', '--cocci', dest='delCocci', help='delete existing  cocci patch directory', nargs='+')

    # Parse program arguments
    args = parser.parse_args(params)

    # Actions according to (options/args)
    #
    if args.delCocci is not None:
        cocci_path = config.get('Cocci', 'cocci_path')
        delDirectory(cocci_path, args.delCocci, config)
    #
    elif args.delProject is not None:
        project_path = config.get('Projects', 'project_path')
        delDirectory(project_path, args.delProject, config)
    #
    else:
        print "No option specified. End of programm."
        sys.exit(2)

## Internal function which deletes the required directory. If a project is deleted, the default project is set to empty if no project is available, or to another project. The config file is updated
# @param path path of cocci tree or project tree
# @param list_directory list of directories to delete
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
def delDirectory(path, list_directory, config):

    #
    for directory in list_directory:
        if not os.path.isdir(path + directory):
            print "%s is not an existing in %s" (directory, path)
        else:
            shutil.rmtree(path + directory)

    # Update Config File
    default_project_path = os.path.dirname(config.get('Projects', 'default_project')) + "/"
    default_project_name = os.path.basename(config.get('Projects', 'default_project'))

    if path == default_project_path:
        #
        if not os.path.isdir(path + default_project_name):
            config.remove_option('Projects', 'default_project')
            list_projects = os.listdir(path)
            #
            if len(list_projects) == 0:
                config.set('Projects', 'default_project', '')
            #
            else:
                config.set('Projects', 'default_project', path + list_projects[0] )
        # Writing our configuration file to 'example.cfg'
        with open(config.get('Environment', 'installation_path') + "coccitools.conf", 'wb') as configfile:
            config.write(configfile)

