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

## Function called by the cocci module
# @param params command line options/args of "cocci create"
# @param config object ConfigParser which contains all features of configuration file "coccitools.conf"
def create(params, config):

    #
    parser = argparse.ArgumentParser()
    parser.add_argument('-L', '--use-symlink', dest='use_symlink'
                        , help='generate a symbolic link instead of importing files from the directory'
                        ,  action='store_true')
    parser.add_argument('-c', dest='cocci_files'
                        , help='list of semantic patchs for generate project rules (only for -R/--rules option)'
                        , nargs='*')
    parser.add_argument('-p', dest='project'
                        , help='existing project (only for -R/--rules option)'
                        , nargs=1)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-P', '--project', dest='newProject'
                       , help='create new project'
                       , nargs=2)
    group.add_argument('-C', '--cocci', dest='newCocci'
                       , help='create new cocci patchs directory'
                       , nargs=2)
    group.add_argument('-R', '--rules', dest='newRules'
                      , help='create a set of rules for an existing project'
                      , nargs=1)
    #
    args = parser.parse_args(params)

    if args.newCocci is not None:
        cocci_path = config.get('Cocci', 'cocci_path')
        newCocci(args.newCocci[0], args.newCocci[1], args.use_symlink, cocci_path )
    #
    elif args.newProject is not None:
        newProject(args.newProject[0], args.newProject[1], args.use_symlink, config)
    #
    elif args.newRules is not None:
        newRules(args.newRules[0], args.cocci_files, args.project, config)
    else:
        print "No option specified. End of programm."
        sys.exit(2)

## Internal function which extracts all cocci files from a directory tree
# @param path path of the source directory
# @return list of cocci files
def listdirectory(path):
    fichier=[]
    l = glob.glob(path + "/*")

    #
    for i in l:
        if os.path.isdir(i):

            fichier.extend(listdirectory(i))
        else:
            ext = os.path.splitext(i)[1]
            if ext == '.cocci':
                fichier.append(i)
    #
    return fichier

## Internal function which cheks if the source directory exists. If not, the program ends
# @param dir : the source directory
def checkSource(dir):
     if( not os.path.isdir(dir) ):
        print "%s is not a directory" % dir
        sys.exit(2)

## Internal funciton which create a cocci directory in the cocci tree and imports the cocci files
# @param destination the name of the new cocci directory
# @param source the source directory which contains cocci files
# @param isImportFiles boolean which specifies the use of symlinks on directories
# @param isImportDirectories  which specifies the use of symlinks on files
# @param path the path of the cocci tree
def newCocci(destination, source, use_symlink, path):

    checkSource(source)
    # Check if the directory contains cocci file
    cocci_files = listdirectory(source)
    if len(cocci_files) == 0:
        print "No cocci file found, abort"
        sys.exit(2)
    else:
        print "Cocci files found, continue"

    # Check if the destination directory exists
    dest_dir = path + destination
    if( os.path.isdir(dest_dir) ):
        print "impossible to create %s : project already exists" % destination
        sys.exit(2)
    else:
        print "Create %s cocci directory" % destination
        os.makedirs(dest_dir)

        #
        if not use_symlink:

            # Create cocci files or symbolic link
            for cocci_file in cocci_files:
                # print "Cocci file : %s" % cocci_file
                cocci_path =  os.path.abspath(cocci_file).split(source)[1]
                # print "Cocci path : %s" % cocci_path
                cocci_filename = os.path.basename(cocci_file)
                # print "Cocci filename : %s" % cocci_filename
                relative_cocci_dir = cocci_path.split(cocci_filename)[0]
                # print "Cocci relative directory : %s" % relative_cocci_dir
                relative_destination_dir = dest_dir + "/" + relative_cocci_dir
                # print "Cocci relative destination dir : %s" % relative_destination_dir

                if (not os.path.isdir(relative_destination_dir) ):
                    os.makedirs(relative_destination_dir)

                    shutil.copyfile(cocci_file, relative_destination_dir + cocci_filename )
        else:
            os.symlink(source, dest_dir + "/link_cocci")

## Internal funciton which create a project directory in the cocci tree and imports the C files
# @param destination the name of the new cocci directory
# @param source the source directory which contains cocci files
# @param isImportFiles boolean which specifies the use of symlinks on directories
# @param config object config which contains the project path
def newProject(destination, source, use_symlink, config):

    checkSource(source)

    # Check if the destination directory exists
    dest_dir = config.get('Projects', 'project_path') + destination + "/src/"
    if( os.path.isdir(dest_dir) ):
        print "impossible to create %s : project already exists" % destination
        sys.exit(2)

    print "Create %s project" % destination
    # Create a directory with source file or symbolic link
    if  not use_symlink:
        shutil.copytree(source, dest_dir)
    else:
        os.makedirs(dest_dir)
        os.symlink(source, dest_dir + "link_project")

    # Update Config File
    config.remove_option('Projects', 'default_project')
    config.set('Projects', 'default_project', config.get('Projects', 'project_path') + destination)

     # Writing our configuration file to 'example.cfg'
    with open(config.get('Environment', 'installation_path') + "coccitools.conf", 'wb') as configfile:
        config.write(configfile)

def newRules(name, cocci_files, project, config):

    cocci_tree_path = config.get('Cocci', 'cocci_path')
    #check project
    if project is None:
        project = config.get('Projects', 'default_project')
    #
    else:
        project_tree_path = config.get('Projects', 'project_path')
        #
        if os.path.isdir(project_tree_path + project[0]):
            project = project_tree_path + project[0]
        else:
            print "project %s does not exist" %project[0]

    #check rule file
    if os.path.isfile(project + '/' + name + '.txt'):
        print 'Cannot create %s.txt rules file: file exists.' % name
    else:
        f = open (project + '/' + name + '.txt', 'wb')
        if cocci_files is None:
            whole_cocci = listdirectory(cocci_tree_path)
            #
            for cocci_file in whole_cocci:
                f.write(cocci_file.split(cocci_tree_path)[1] + '\n')
        #
        else:
            for cocci_file in cocci_files:
                f.write(cocci_file + '\n')

        f.close()

def usage():
    return '   create     Import C projects or cocci files directory and create file rules'
