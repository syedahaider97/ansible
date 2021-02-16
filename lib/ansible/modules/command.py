#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>, and others
# Copyright: (c) 2016, Toshio Kuratomi <tkuratomi@ansible.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: command
short_description: Execute commands on targets
version_added: historical
description:
     - The C(command) module takes the command name followed by a list of space-delimited arguments.
     - The given command will be executed on all selected nodes.
     - The command(s) will not be
       processed through the shell, so variables like C($HOSTNAME) and operations
       like C("*"), C("<"), C(">"), C("|"), C(";") and C("&") will not work.
       Use the M(ansible.builtin.shell) module if you need these features.
     - To create C(command) tasks that are easier to read than the ones using space-delimited
       arguments, pass parameters using the C(args) L(task keyword,../reference_appendices/playbooks_keywords.html#task)
       or use C(cmd) parameter.
     - Either a free form command or C(cmd) parameter is required, see the examples.
     - For Windows targets, use the M(ansible.windows.win_command) module instead.
options:
  free_form:
    description:
      - The command module takes a free form string as a command to run.
      - There is no actual parameter named 'free form'.
  cmd:
    type: str
    description:
      - The command to run.
  argv:
    type: list
    elements: str
    description:
      - Passes the command as a list rather than a string.
      - Use C(argv) to avoid quoting values that would otherwise be interpreted incorrectly (for example "user name").
      - Only the string (free form) or the list (argv) form can be provided, not both.  One or the other must be provided.
    version_added: "2.6"
  creates:
    type: path
    description:
      - A filename or (since 2.0) glob pattern. If a matching file already exists, this step B(will not) be run.
  removes:
    type: path
    description:
      - A filename or (since 2.0) glob pattern. If a matching file exists, this step B(will) be run.
    version_added: "0.8"
  chdir:
    type: path
    description:
      - Change into this directory before running the command.
    version_added: "0.6"
  warn:
    description:
      - (deprecated) Enable or disable task warnings.
      - This feature is deprecated and will be removed in 2.14.
      - As of version 2.11, this option is now disabled by default.
    type: bool
    default: no
    version_added: "1.8"
  stdin:
    description:
      - Set the stdin of the command directly to the specified value.
    type: str
    version_added: "2.4"
  stdin_add_newline:
    type: bool
    default: yes
    description:
      - If set to C(yes), append a newline to stdin data.
    version_added: "2.8"
  strip_empty_ends:
    description:
      - Strip empty lines from the end of stdout/stderr in result.
    version_added: "2.8"
    type: bool
    default: yes
notes:
    -  If you want to run a command through the shell (say you are using C(<), C(>), C(|), and so on),
       you actually want the M(ansible.builtin.shell) module instead.
       Parsing shell metacharacters can lead to unexpected commands being executed if quoting is not done correctly so it is more secure to
       use the C(command) module when possible.
    -  C(creates), C(removes), and C(chdir) can be specified after the command.
       For instance, if you only want to run a command if a certain file does not exist, use this.
    -  Check mode is supported when passing C(creates) or C(removes). If running in check mode and either of these are specified, the module will
       check for the existence of the file and report the correct changed status. If these are not supplied, the task will be skipped.
    -  The C(executable) parameter is removed since version 2.4. If you have a need for this parameter, use the M(ansible.builtin.shell) module instead.
    -  For Windows targets, use the M(ansible.windows.win_command) module instead.
    -  For rebooting systems, use the M(ansible.builtin.reboot) or M(ansible.windows.win_reboot) module.
seealso:
- module: ansible.builtin.raw
- module: ansible.builtin.script
- module: ansible.builtin.shell
- module: ansible.windows.win_command
author:
    - Ansible Core Team
    - Michael DeHaan
'''

EXAMPLES = r'''
- name: Return motd to registered var
  command: cat /etc/motd
  register: mymotd

# free-form (string) arguments, all arguments on one line
- name: Run command if /path/to/database does not exist (without 'args')
  command: /usr/bin/make_database.sh db_user db_name creates=/path/to/database

# free-form (string) arguments, some arguments on separate lines with the 'args' keyword
# 'args' is a task keyword, passed at the same level as the module
- name: Run command if /path/to/database does not exist (with 'args' keyword)
  command: /usr/bin/make_database.sh db_user db_name
  args:
    creates: /path/to/database

# 'cmd' is module parameter
- name: Run command if /path/to/database does not exist (with 'cmd' parameter)
  command:
    cmd: /usr/bin/make_database.sh db_user db_name
    creates: /path/to/database

- name: Change the working directory to somedir/ and run the command as db_owner if /path/to/database does not exist
  command: /usr/bin/make_database.sh db_user db_name
  become: yes
  become_user: db_owner
  args:
    chdir: somedir/
    creates: /path/to/database

# argv (list) arguments, each argument on a separate line, 'args' keyword not necessary
# 'argv' is a parameter, indented one level from the module
- name: Use 'argv' to send a command as a list - leave 'command' empty
  command:
    argv:
      - /usr/bin/make_database.sh
      - Username with whitespace
      - dbname with whitespace
    creates: /path/to/database

- name: Safely use templated variable to run command. Always use the quote filter to avoid injection issues
  command: cat {{ myfile|quote }}
  register: myoutput
'''

RETURN = r'''
msg:
  description: changed
  returned: always
  type: bool
  sample: True
start:
  description: The command execution start time.
  returned: always
  type: str
  sample: '2017-09-29 22:03:48.083128'
end:
  description: The command execution end time.
  returned: always
  type: str
  sample: '2017-09-29 22:03:48.084657'
delta:
  description: The command execution delta time.
  returned: always
  type: str
  sample: '0:00:00.001529'
stdout:
  description: The command standard output.
  returned: always
  type: str
  sample: 'Clustering node rabbit@slave1 with rabbit@master …'
stderr:
  description: The command standard error.
  returned: always
  type: str
  sample: 'ls cannot access foo: No such file or directory'
cmd:
  description: The command executed by the task.
  returned: always
  type: list
  sample:
  - echo
  - hello
rc:
  description: The command return code (0 means success).
  returned: always
  type: int
  sample: 0
stdout_lines:
  description: The command standard output split in lines.
  returned: always
  type: list
  sample: [u'Clustering node rabbit@slave1 with rabbit@master …']
stderr_lines:
  description: The command standard error split in lines.
  returned: always
  type: list
  sample: [u'ls cannot access foo: No such file or directory', u'ls …']
'''

import datetime
import glob
import os
import shlex

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native, to_bytes, to_text
from ansible.module_utils.common.collections import is_iterable


def check_command(module, commandline):
    arguments = {'chown': 'owner', 'chmod': 'mode', 'chgrp': 'group',
                 'ln': 'state=link', 'mkdir': 'state=directory',
                 'rmdir': 'state=absent', 'rm': 'state=absent', 'touch': 'state=touch'}
    commands = {'curl': 'get_url or uri', 'wget': 'get_url or uri',
                'svn': 'subversion', 'service': 'service',
                'mount': 'mount', 'rpm': 'yum, dnf or zypper', 'yum': 'yum', 'apt-get': 'apt',
                'tar': 'unarchive', 'unzip': 'unarchive', 'sed': 'replace, lineinfile or template',
                'dnf': 'dnf', 'zypper': 'zypper'}
    become = ['sudo', 'su', 'pbrun', 'pfexec', 'runas', 'pmrun', 'machinectl']
    if isinstance(commandline, list):
        command = commandline[0]
    else:
        command = commandline.split()[0]
    command = os.path.basename(command)

    disable_suffix = "If you need to use command because {mod} is insufficient you can add" \
                     " 'warn: false' to this command task or set 'command_warnings=False' in" \
                     " ansible.cfg to get rid of this message."
    substitutions = {'mod': None, 'cmd': command}

    if command in arguments:
        msg = "Consider using the {mod} module with {subcmd} rather than running '{cmd}'.  " + disable_suffix
        substitutions['mod'] = 'file'
        substitutions['subcmd'] = arguments[command]
        module.warn(msg.format(**substitutions))

    if command in commands:
        msg = "Consider using the {mod} module rather than running '{cmd}'.  " + disable_suffix
        substitutions['mod'] = commands[command]
        module.warn(msg.format(**substitutions))

    if command in become:
        module.warn("Consider using 'become', 'become_method', and 'become_user' rather than running %s" % (command,))


def main():

    # the command module is the one ansible module that does not take key=value args
    # hence don't copy this one if you are looking to build others!
    module = AnsibleModule(
        argument_spec=dict(
            _raw_params=dict(),
            _uses_shell=dict(type='bool', default=False),
            argv=dict(type='list', elements='str'),
            chdir=dict(type='path'),
            executable=dict(),
            creates=dict(type='path'),
            removes=dict(type='path'),
            # The default for this really comes from the action plugin
            warn=dict(type='bool', default=False, removed_in_version='2.14', removed_from_collection='ansible.builtin'),
            stdin=dict(required=False),
            stdin_add_newline=dict(type='bool', default=True),
            strip_empty_ends=dict(type='bool', default=True),
        ),
        supports_check_mode=True,
    )
    shell = module.params['_uses_shell']
    chdir = module.params['chdir']
    executable = module.params['executable']
    args = module.params['_raw_params']
    argv = module.params['argv']
    creates = module.params['creates']
    removes = module.params['removes']
    warn = module.params['warn']
    stdin = module.params['stdin']
    stdin_add_newline = module.params['stdin_add_newline']
    strip = module.params['strip_empty_ends']

    if not shell and executable:
        module.warn("As of Ansible 2.4, the parameter 'executable' is no longer supported with the 'command' module. Not using '%s'." % executable)
        executable = None

    if (not args or args.strip() == '') and not argv:
        module.fail_json(rc=256, msg="no command given")

    if args and argv:
        module.fail_json(rc=256, msg="only command or argv can be given, not both")

    if not shell and args:
        args = shlex.split(args)

    args = args or argv

    # All args must be strings
    if is_iterable(args, include_strings=False):
        args = [to_native(arg, errors='surrogate_or_strict', nonstring='simplerepr') for arg in args]

    if chdir:
        try:
            chdir = to_bytes(os.path.abspath(chdir), errors='surrogate_or_strict')
        except ValueError as e:
            module.fail_json(msg='Unable to use supplied chdir: %s' % to_text(e))

        try:
            os.chdir(chdir)
        except (IOError, OSError) as e:
            module.fail_json(msg='Unable to change directory before execution: %s' % to_text(e))

    if creates:
        # do not run the command if the line contains creates=filename
        # and the filename already exists.  This allows idempotence
        # of command executions.
        if glob.glob(creates):
            module.exit_json(
                cmd=args,
                stdout="skipped, since %s exists" % creates,
                changed=False,
                rc=0
            )

    if removes:
        # do not run the command if the line contains removes=filename
        # and the filename does not exist.  This allows idempotence
        # of command executions.
        if not glob.glob(removes):
            module.exit_json(
                cmd=args,
                stdout="skipped, since %s does not exist" % removes,
                changed=False,
                rc=0
            )

    if warn:
        check_command(module, args)

    startd = datetime.datetime.now()

    if not module.check_mode:
        rc, out, err = module.run_command(args, executable=executable, use_unsafe_shell=shell, encoding=None, data=stdin, binary_data=(not stdin_add_newline))
    elif creates or removes:
        rc = 0
        out = err = b'Command would have run if not in check mode'
    else:
        module.exit_json(msg="skipped, running in check mode", skipped=True)

    endd = datetime.datetime.now()
    delta = endd - startd

    if strip:
        out = out.rstrip(b"\r\n")
        err = err.rstrip(b"\r\n")

    result = dict(
        cmd=args,
        stdout=out,
        stderr=err,
        rc=rc,
        start=str(startd),
        end=str(endd),
        delta=str(delta),
        changed=True,
    )

    if rc != 0:
        module.fail_json(msg='non-zero return code', **result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
