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

import sys, os, glob
import argparse

## Function called by the cocci module
# @param params command line options/args of "cocci show"
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
def show(params, config):

    # Options and Arguements
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', '--project', dest='showProject',
                        help='Display existing projects', nargs='*')
    parser.add_argument('-C', '--cocci', dest='showCocci',
                        help='Display existing cocci patch directories', nargs='*')
    # parser.add_argument('-F', '--files', dest='isDisplayFiles',
    #                     help='Display all files', action='store_true')
    # parser.add_argument('-R', '--recursive', dest='isDisplayFiles',
    #                     help='Display directory trees', action='store_true')

    # Parse program arguments
    args = parser.parse_args(params)

    # Actions according to (options/args)
    #
    if args.showCocci is not None:
        cocci_path = config.get('Cocci', 'cocci_path')
        displayDirectory(cocci_path, args.showCocci, config)
    #
    elif args.showProject is not None:
        project_path = config.get('Projects', 'project_path')
        displayDirectory(project_path, args.showProject, config)
    else:
        print "No option specified. End of programm."
        sys.exit(2)

## Internal function which displays the files inside the required directory. The display is "[i] directory". In case of display of the project tree, the displays is "[i] directory *" for the default project.
# @param path path of cocci tree or project tree
# @param list_directory list of directories to delete
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
def displayDirectory(path, list_projects, config):

    #
    default_project = os.path.basename(config.get('Projects', 'default_project')).split("/")[0]

    #
    if len(list_projects) == 0:
        all_projects = os.listdir(path)
        all_projects.sort()
        index = 0
        for project in all_projects:
            index = index +1
            if project == default_project:
                print "[%d] %s *" % (index,project)
            else:
                print "[%d] %s" % (index,project)
    #
    else:
        for project in list_projects:
            path_project = path + project + "/"

        #
        if not os.path.isdir(path_project):
            print "%s is not an existing in %s" % (project, path)
            #
        else:
            print "================> %s" % project
            for _file in listDirectory(path_project):
                print _file.split(path_project)[1]

## Internal function which extracts all files from a directory tree
# @param path path of the source directory
# @return list of files
def listDirectory(path):
    fichier=[]
    l = glob.glob(path + "/*")

    #
    for i in l:
        if os.path.isdir(i):
            fichier.extend(listDirectory(i))
        else:
            fichier.append(i)
    #
    return fichier
