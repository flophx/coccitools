# Coccitools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with Coccitools.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import sys, os, glob
import re

#
def metrics(params, config):

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--c-files', dest='c_files'
                        , help='C file(s) to check'
                        , nargs='+')
    parser.add_argument('-P', '--project', dest='metricProject',
                        help='Display metrics of a  project', nargs='*')
    parser.add_argument('--verbose', dest= 'verbose_mode', type=int, nargs=1)

    #
    args = parser.parse_args(params)

    #
    verbose = 0
    if args.verbose_mode is not None:
        verbose = args.verbose_mode[0]

    # ---------
    if args.c_files is not None:
        #
        if len(args.c_files) > 1:
            for c_file in args.c_files:
                display_metrics(c_file, metrics_file(c_file), 1)
        else:
            c_file=args.c_files[0]
            print  metrics_file(c_file)
            display_metrics(c_file, metrics_file(c_file), 1)

    elif args.metricProject is not None:

        project = build_project(config, args.metricProject)
        display_metrics(project, metrics_project(project, verbose), 1)
    else:
        print 'no file to apply metrics'

#
def metrics_file(c_file):
    #
    fd = open(c_file, 'r')
    n = 0
    n_blanklines = 0
    #
    for line in fd:
        if not line.strip():
            n_blanklines +=1
        n += 1

    return n, n_blanklines, len(comments_file(c_file))


def comments_file(c_file):
    #
    data = open(c_file, 'r').read()
    regexp = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'',
        re.VERBOSE|re.DOTALL | re.MULTILINE
    )
    comments = [m.group(0) for m in regexp.finditer(data) if m.group(0)]
    return comments

def display_metrics (c_file, results, verbose_mode):

    filename=os.path.basename(c_file)
    n_loc=results[0]
    n_bl=results[1]
    n_com=results[2]
    per_bl= percent(n_bl, n_loc)
    per_com= percent(n_com, n_loc)

    #
    if verbose_mode >=1 :
        print "%s : %s LOC with %s BL(%.1f%%) and %s comments(%.1f%%)" % (filename, n_loc, n_bl, per_bl, n_com, per_com)

def build_project(config, project):
    # Check if it is an existing project
    project_tree_path = config.get('Projects', 'project_path')
    if len(project) == 0:
        return config.get('Projects', 'default_project')
    else:
        #
         if os.path.isdir(project_tree_path + project[0]):
             return project_tree_path + project[0]
         #
         else:
             print "project %s does not exits" % project[0]
             sys.exit(2)


def metrics_project(project, verbose_mode):

    total_loc = 0
    total_bl = 0
    total_com = 0
    p_files = listDirectory(project)

    #
    for p_file in p_files:
        if os.path.splitext(p_file)[1] == '.c':
            result = metrics_file(p_file)
            display_metrics(p_file, result, verbose_mode)
            total_loc += result[0]
            total_bl += result[1]
            total_com += result[2]

    return total_loc, total_bl, total_com

###
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

