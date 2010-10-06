# Coccitools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with Coccitools.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import sys, os, glob
def metrics(params, config):

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--c-files', dest='c_files'
                        , help='C file(s) to check'
                        , nargs='+')
    parser.add_argument('-P', '--project', dest='metricProject',
                        help='Display metrics of a  project', nargs='*')
    #
    args = parser.parse_args(params)
    if args.c_files is not None:
        loc_file(args.c_files)
    elif args.metricProject is not None:
        loc_project(config, args.metricProject)
    else:
        print 'no file to apply metrics'

def loc_file(c_file):
        fd = open(c_file, 'r')
        n = 0
        n_blanklines = 0
        for line in fd:
            if not line.strip():
                n_blanklines +=1
            n += 1

        #
        percentage =  ( (n_blanklines *1.0) / n) * 100
        filename = os.path.basename(c_file)
        print "Number of loc in %s : %s with %s blank lines (%.1f%%)" % (filename, n, n_blanklines, percentage)

        return n, n_blanklines

def loc_project(config, param_project):

    project=''
    # Check if it is an existing project
    project_tree_path = config.get('Projects', 'project_path')
    if len(param_project) == 0:
        project = config.get('Projects', 'default_project')
    else:
        #
         if os.path.isdir(project_tree_path + project):
             project = project_tree_path + param_project[0]
         #
         else:
             print "project %s does not exits" % param_project[0]
             sys.exit(2)

    #
    total_loc = 0
    total_bl = 0
    p_files = listDirectory(project)
    for p_file in p_files:
        if os.path.splitext(p_file)[1] == '.c':
            result = loc_file(p_file)
            total_loc += result[0]
            total_bl += result[1]

    percentage =  ( (total_bl *1.0) / total_loc) * 100
    print "Number of loc in %s : %s with %s blank lines (%.1f%%)" % (project, total_loc, total_bl, percentage)

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

