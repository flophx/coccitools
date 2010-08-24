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
import shutil
import subprocess

## Function called by the cocci module. Check a project directory or a set of C files with coccinelle and a set of cocci patch files
# @param params command line options/args of "cocci create"
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
def check(params, config):

    #
    parser = argparse.ArgumentParser()
    parser.add_argument('-sp', '--cocci-files', dest='cocci_files'
                        , help='cocci file(s) to apply on chosen project '
                        ,  nargs='+')
    parser.add_mutually_exclusive_group()
    parser.add_argument('-p', '--project', dest='project'
                        , help='project to check. If no precision, default project'
                        ,  nargs=1)
    parser.add_argument('-f', '--c-files', dest='c_files'
                        , help='C file(s) to check'
                        , nargs='+')
    #
    args = parser.parse_args(params)


    if args.cocci_files is not None:
        #
        if args.project is not None:
            applyCocciOnProject(args.cocci_files, config, args.project[0])
        elif args.c_files is not None:
            applyCocciOnFiles(args.cocci_files, config, args.c_files)
        else:
              applyCocciOnProject(args.cocci_files, config)
    else:
        print 'no cocci-files'

## Internal function that checks an existing project with a set of cocci files
# @param cocci_files list of cocci patchs files to apply
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
# @param project existing project to check. By default, the project=default project
def applyCocciOnProject(cocci_files, config, project=''):

    cocci_tree_path = config.get('Cocci', 'cocci_path')
    project_tree_path = config.get('Projects', 'project_path')
    #
    if project == '':
        project = config.get('Projects', 'default_project')
    else:
        #
        if os.path.isdir(project_tree_path + project):
            project = project_tree_path + project
        #
        else:
            print "project %s does not exits" % project
            sys.exit(2)
    #
    for cocci_file in cocci_files:
        #
        if os.path.splitext(cocci_file)[1] == '.cocci':
            #
            if os.path.isfile(cocci_tree_path + cocci_file):
                command_line = "spatch -sp_file " + cocci_tree_path + cocci_file + " -dir " + project
                subprocess.call(command_line, shell=True)
            #
            else:
                 print "%s is not an existing cocci file" % cocci_file

        #
        else:
            print "%s is not a cocci file" % cocci_file

## Internal function that checks an existing project with a set of cocci files
# @param cocci_files list of cocci patchs files to apply
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
# @param c_files existing c_files in one or more projects
def applyCocciOnFiles(cocci_files, config, c_files):

    cocci_tree_path = config.get('Cocci', 'cocci_path')
    project_tree_path = config.get('Projects', 'project_path')

    # check c_files
    list_files = ''
    for c_file in c_files:
        #
        if os.path.splitext(c_file)[1] == '.c':
            #
             if os.path.isfile(project_tree_path + c_file):
                 list_files = list_files + ' ' + project_tree_path + c_file
             #
             else:
                 print "%s is not an existing c file" % c_file

        #
        else:
            print "%s is not a c file" % c_file

    if not list_files == '':
    #
        for cocci_file in cocci_files:
            #
            if os.path.splitext(cocci_file)[1] == '.cocci':
                #
                if os.path.isfile(cocci_tree_path + cocci_file):
                    command_line = "spatch -sp_file " + cocci_tree_path + cocci_file + ' ' + list_files
                    print command_line
                    subprocess.call(command_line, shell=True)
                #
                else:
                    print "%s is not an existing cocci file" % cocci_file
            #
            else:
                print "%s is not a cocci file" % cocci_file
    #
    else:
        print "No existing C file. End of program"
        sys.exit(2)

