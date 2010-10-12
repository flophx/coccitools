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

import os, sys, glob

## Check if the project exists and return the absolute path of the project.
# @param config the config file of coccitools
# @param project the project to check
# @return the absolute path of the project if it exists else the program will abort.
def checkProject(config, project):

    project_tree_path = config.get('Projects', 'project_path')
    if project == '':
        return config.get('Projects', 'default_project') + '/'
    else:
        #
         if os.path.isdir(project_tree_path + project):
             return project_tree_path + project + '/'
         #
         else:
             print "project %s does not exist" % project
             sys.exit(2)

## Check if the file exists and if the file extension is correct
# @param abspath the absolute path of the file
# @param extension the file extension
# @return true if the test is validated otherwise false
def checkFile(abspath, extension):
    if os.path.isfile(abspath) and os.path.splitext(abspath)[1] == extension:
        return True
    else:
        return False

def checkRulesFile(project_path, rules_file):
    rules_abspath = project_path + rules_file

    if checkFile(rules_abspath, '.txt'):
        return rules_abspath
    else:
        return None

def checkCFile(project_tree_path, c_file):
     c_abspath = project_tree_path + c_file

     if checkFile(c_abspath, '.c'):
         return c_abspath
     else:
         return None

def checkCocciFile(cocci_tree_path, cocci_file):
     cocci_abspath = cocci_tree_path + cocci_file
     if checkFile(cocci_abspath, '.cocci'):
         return cocci_abspath
     else:
         return None



## Return a percentage
# @param num
# @param denum
# @return the result
def percent (num, denum):
   return ((1.0 * num ) / denum ) * 100

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
