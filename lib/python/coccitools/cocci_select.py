#!/usr/bin/env python

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

import sys, os, argparse

## Function called by the cocci module
# @param params command line options/args of "cocci select"
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
def select(params, config):

    # Options and Arguements
    parser = argparse.ArgumentParser()
    parser.add_argument('--default-project',  dest='default_project', help='Select the default Project', nargs=1)

    # Parse program arguments
    args = parser.parse_args(params)

    #
    if args.default_project is not None :
        setDefaultProject(args.default_project[0], config)
    #
    else :
        print "No option specified. End of programm."
        sys.exit(2)

## Internal function corresponding to the option '--default-project'
# @param defaultProject specifies the new default project, if it exists.
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
def setDefaultProject(defaultProject, config):

    project_path = config.get('Projects', 'project_path')

    #
    if not os.path.isdir( project_path + defaultProject ):
        print "Unable to select %s : non-existent project"
    #
    else :
        print "Select %s as default project" % defaultProject
        config.remove_option('Projects', 'default_project')
        config.set('Projects', 'default_project', project_path + defaultProject )
         # Writing our configuration file to 'example.cfg'
        with open(config.get('Environment', 'installation_path') + "coccitools.conf", 'wb') as configfile:
            config.write(configfile)
