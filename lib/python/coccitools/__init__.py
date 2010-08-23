#!/usr/bin/env python

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

## @package coccitools
#  Describe the list of available sub-commands for cocci dispatcher.
#
#
# The module 'cocci_create' provides the 'create' sub-command. The 'create' sub-command is made to import C files or Cocci patchs. The original directory tree is keeped.
#
# The module 'cocci_delete' provides the 'delete' sub-command. The 'delete' sub-command deletes a cocci directory in the cocci tree or a project directory in the project tree.
#
# The module 'cocci_select' provides the 'select' sub-command. The 'select' sub-command serves to change values of the config file and save it.
#
# The module 'cocci_show' provides the 'show' sub-command. The 'show 'sub-command serves to show the available projects in the project tree of the cocci patch directories in the  cocci tree.

from cocci_create import create
from cocci_delete import delete
from cocci_select import select
from cocci_show import show
