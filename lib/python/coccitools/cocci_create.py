#!/usr/bin/python

import sys, os, glob
import argparse
import shutil

# ============================
def create(params, config):

    #
    parser = argparse.ArgumentParser()
    parser.add_argument('-G', '--no-import-files', dest='isImportFiles'
                        , help='generate  symbolic link(s) for the specified source '
                        ,  action='store_true')
    parser.add_argument('-L', '--no-import-directories', dest='isImportDirectories'
                        , help='generate a symbolic link for each files (cocci only)'
                        ,  action='store_true')
    parser.add_argument('-P', '--project', dest='newProject', help='create new project', nargs=2)
    parser.add_argument('-C', '--cocci', dest='newCocci', help='create new cocci patchs directory', nargs=2)

    args = parser.parse_args(params)

    if args.newCocci is not None:
        cocci_path = config.get('Cocci', 'cocci_path')
        newCocci(args.newCocci[0], args.newCocci[1], args.isImportFiles, args.isImportDirectories, cocci_path )
    #
    elif args.newProject is not None:
        newProject(args.newProject[0], args.newProject[1], args.isImportFiles, config)
    #
    else:
        print "No option specified. End of programm."
        sys.exit(2)

# ============================
# Check if the source directory exists
# ============================
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

# ============================
# Check if the source directory exists
# ============================
def checkSource(dir):
     if( not os.path.isdir(dir) ):
        print "%s is not a directory" % dir
        sys.exit(2)

# ============================
#
# ============================
def newCocci(destination, source, isImportFiles, isImportDirectories, path):

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
        if not isImportFiles:

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

                #
                if not isImportDirectories:
                    shutil.copyfile(cocci_file, relative_destination_dir + cocci_filename )
                else:
                    os.symlink(cocci_file, relative_destination_dir + "/" + cocci_filename )
        else:
            os.symlink(source, dest_dir + "/link_cocci")


# ============================
#
# ============================
def newProject(destination, source, isImportFiles, config):

    checkSource(source)

    # Check if the destination directory exists
    dest_dir = config.get('Projects', 'project_path') + destination + "/src/"
    if( os.path.isdir(dest_dir) ):
        print "impossible to create %s : project already exists" % destination
        sys.exit(2)

    print "Create %s project" % destination
    # Create a directory with source file or symbolic link
    if ( not isImportFiles ):
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
