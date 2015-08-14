#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, Brian Valerius <b.valerius@gmail.com>
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: tempfile
author: Brian Valerius (@bvalerius)
version_added: "2.0.0"
short_description: Create temporary files.
description:
    - The M(tempfile) module creates a temporary file using Python's tempfile.
notes:
    - The tempfile will not be automatically deleted. You must manually remove it.
options:
    suffix:
        description:
            - If specified, the file name will end with that suffix.
        required: false
        default: ""
    prefix:
        description:
            - If specified, the file name will begin with that preix.
        required: false
        default: "tmp"
    dir:
        description:
            - If specified, the file will be created in that directory.
            - The default comes from setting the TMPDIR, TEMP, or TMP
            - environment variables.
        required: false
        default: null
    text:
        description:
            - If specified, it indicates to open the file in binary mode
            - (the default) or text mode.
        required: false
        default: "no"
'''

EXAMPLES = '''
- tempfile:
  register: result

- tempfile: dir="/tmp/my_app"
  register: result
'''

from tempfile import mkstemp


def main():
    module = AnsibleModule(
        argument_spec = dict(
            suffix    = dict(default=""),
            prefix    = dict(default="tmp"),
            dir       = dict(default=None),
            text      = dict(default=False, choices=BOOLEANS),
        ),
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(changed=True)

    try:
        _, path = mkstemp(suffix=module.params["suffix"],
                          prefix=module.params["prefix"],
                          dir=module.params["dir"],
                          text=module.boolean(module.params["text"]))
    except Exception, e:
        module.fail_json(msg="Error while creating tempfile: %s" % str(e))

    module.exit_json(changed=True, file=path)

# import module snippets
from ansible.module_utils.basic import *

if __name__ == "__main__":
    main()
