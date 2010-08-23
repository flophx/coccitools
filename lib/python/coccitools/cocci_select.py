#!/usr/bin/env python
import sys, os, argparse

# ============================
# init
# ============================
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

# ============================
# Set Default Project
# ============================
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
