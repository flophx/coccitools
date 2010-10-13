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
import utils

## Function called by the cocci module. Check a project directory or a set of C files with coccinelle and a set of cocci patch files
# @param params command line options/args of "cocci create"
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
def check(params, config):

    #
    parser = argparse.ArgumentParser()

    gp_cocci = parser.add_mutually_exclusive_group()
    gp_cocci.add_argument('-sp', '--cocci-files', dest='cocci_files',
                        help='cocci file(s) to apply on chosen project ',
                        nargs='+')
    gp_cocci.add_argument('-r', '--rules-file', dest='rules_file',
                        help='apply rules file',
                        nargs=1)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--project', dest='project',
                        help='project to check. If no precision, default project',
                        const='', default='', nargs='?')
    group.add_argument('-f', '--c-files', dest='c_files',
                        help='C file(s) to check',
                        nargs='+')

    args = parser.parse_args(params)

    if args.cocci_files is not None:

        if args.c_files is not None:
            applyCocciOnFiles(args.cocci_files, config, args.c_files)

        #
        elif args.project is not None:
            applyCocciOnProject(args.cocci_files, config, args.project)

        else:
            applyCocciOnProject(args.cocci_files, config)

    elif args.rules_file is not None:
        if args.project is not None:
            applyRulesOnProject(args.rules_file[0], config, args.project)
    else:
        print 'no cocci-files'
        sys.exit(2)

## Internal function that checks an existing project with a set of cocci files
# @param cocci_files list of cocci patchs files to apply
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
# @param project existing project to check. By default, the project=default project
def applyCocciOnProject(cocci_files, config, project):

    cocci_tree_path = config.get('Cocci', 'cocci_path')
    project_tree_path = config.get('Projects', 'project_path')

    _project = utils.checkProject(project_tree_path, project)

    for cocci_file in cocci_files:

        cocci_abspath = utils.checkCocciFile(cocci_tree_path, cocci_file)
        if cocci_abspath is not None:
             command_line = "spatch -sp_file " + cocci_abspath + " -dir " + _project
             subprocess.call(command_line, shell=True)
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
        c_abspath = utils.checkCFile(project_tree_path, c_file)

        if c_abspath is not None:
            list_files = list_files + ' ' + project_tree_path + c_file
        else:
            print "%s is not an existing c file, escape" % c_file

    if not list_files == '':
    #
        for cocci_file in cocci_files:
            cocci_abspath = utils.checkCocciFile(cocci_tree_path, cocci_file)

            if cocci_abspath is not None:
                command_line = "spatch -sp_file " + cocci_abspath + ' ' + list_files
                subprocess.call(command_line, shell=True)
            else:
                print "%s is not an existing cocci file" % cocci_file
    #
    else:
        print "No existing C file. End of program"
        sys.exit(2)

## Internal function that checks an existing project with a set of cocci files
# @param cocci_files list of cocci patchs files to apply
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
# @param c_files existing c_files in one or more projects
def applyRulesOnProject(rules_file, config, project):

    cocci_tree_path = config.get('Cocci', 'cocci_path')
    project_tree_path = config.get('Projects', 'project_path')

    # Check Project
    _project = utils.checkProject(config, project)

    # Check Rules File
    rules_abspath = utils.checkRulesFile(_project, rules_file)

    if rules_abspath is None:
        print "Rules File %s does not exist. Aborting" % rules_file
        sys.exit(2)

    # Create list of cocci_files from rules_files
    cocci_files = []
    fd = open(rules_abspath, 'r')
    for line in fd:
        if not line.startswith('#'):
            cocci_files.append(line.strip())

    # Command line
    for cocci_file in cocci_files:
        cocci_abspath = utils.checkCocciFile(cocci_tree_path, cocci_file)
        print cocci_abspath
        if cocci_abspath is not None:
            command_line = "spatch -sp_file " + cocci_abspath + " -dir " + _project
            subprocess.call(command_line, shell=True)
        else:
            print "%s is not a cocci file" % cocci_file

def usage():
    return '   check      Apply rules or cocci files to a project or C files'
