#!/usr/bin/python
import os, sys
import argparse
import shutil

# ====================================================
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

# ============================
# Delete directory
# ============================
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

