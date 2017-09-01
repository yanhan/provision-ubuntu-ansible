#!/usr/bin/env python
# vim: set fileencoding=utf-8

DOCUMENTATION = """
---
module: check_if_need_to_apt_get_update
short_description: Checks if an `apt-get update` should be performed
description:
    - Performs `apt-get update` when the Singapore Ubuntu mirror has been
      replaced or when the last successful `apt-get update` was performed >=
      `cache_time_valid` seconds ago
author: "Pang Yan Han (@yanhan_pang)"
notes: []
requirements:
    - Ubuntu Linux
options:
    cache_valid_time:
        description:
            - If at least `cache_valid_time` seconds has passed between the time
              of invocation of this Ansible module and the previous
              `apt-get update`, then the `need_to_update` field of the return
              value will be set to `True`. The time of the previous
              `apt-get update` is obtained from the last modify time of the
              `/var/cache/apt/pkgcache.bin` file, as suggested by
              http://askubuntu.com/a/410259
        required: False
        default: 0

    nr_line_with_sg_mirror_in_apt_sources:
        description:
            - Number of lines in /etc/apt/sources.list where the
              http://sg.archive.ubuntu.com mirror is used. If this is greater
              than 0, then the `need_to_update` field of the return value will
              bet set to `True`.
        required: False
        default: 0
"""

import datetime
import os
import subprocess
import tempfile

def main():
    module = AnsibleModule(
        argument_spec=dict(
            cache_valid_time                       = dict(required=False, type="int", default=0),
            nr_lines_with_sg_mirror_in_apt_sources = dict(required=False, type="int", default=0),
        )
    )
    params = module.params
    need_to_update = False
    if params["nr_lines_with_sg_mirror_in_apt_sources"] > 0:
        # If the mirrors have just been replaced, we must do an `apt-get update`
        need_to_update = True
    else:
        # No mirrors have been replaced, so we check to see if the last
        # time an `apt-get update` was done was at least `cache_valid_time`
        # seconds ago.
        # We will obtain the time where the previous successful `apt-get update`
        # was done using the following command:
        #
        #    stat /var/cache/apt/pkgcache.bin
        #
        # which will output something like the following:
        #
        #       File: ‘/var/cache/apt/pkgcache.bin’
        #       Size: 44475190        Blocks: 86848      IO Block: 4096   regular file
        #     Device: fc01h/64513d    Inode: 24117775    Links: 1
        #     Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
        #     Access: 2015-12-25 10:20:28.797758347 +0800
        #     Modify: 2015-12-25 10:20:28.657757888 +0800
        #     Change: 2015-12-25 10:20:28.657757888 +0800
        #     Birth: -
        #
        # The value of the `Modify` field is what we're interested in.
        #
        # Because how Ansible handles stdout and stderr is an unknown to us, to
        # properly capture the standard output of the process we will be
        # spawning, we will need to direct it to a file. `delete=False` is
        # specified here to avoid automatically deleting the file when we close
        # it. So we'll remove it manually later.
        process_stdout_tempfile = tempfile.NamedTemporaryFile(delete=False)
        stat_cmd_list = ["stat", "/var/cache/apt/pkgcache.bin",]
        p = subprocess.Popen(stat_cmd_list, stdout=process_stdout_tempfile)
        p.communicate()
        process_stdout_tempfile.close()
        # Read the contents of stdout
        p_stdout = ""
        with open(process_stdout_tempfile.name, "r") as f:
            p_stdout = f.read()
        os.remove(process_stdout_tempfile.name)
        # split the output of into individual lines and get the 0th indexed item
        modify_str = "Modify: "
        lines_of_interest = list(
            filter(lambda l: l.startswith(modify_str), p_stdout.split("\n"))
        )
        if not lines_of_interest:
            module.fail_json(
                msg="Error: Output of `{}` does not contain any line starting with `Modify: `. See the value of the `stdout` field for the standard output of that command. You'll probably have to reprogram this.".format(
                    " ".join(stat_cmd_list),
                ),
                stdout=p_stdout,
            )
        # Take the first line, strip off the `modify_str`
        line_of_interest = lines_of_interest[0][len(modify_str):]
        # The datetime string is going to be in this format:
        #
        #     2015-12-25 10:20:28.657757888 +0800
        #
        # We are only interested in this part:
        #
        #     2015-12-25 10:20:28
        #
        # which comes before the period.
        dot_idx = line_of_interest.index(".")
        datetime_string = line_of_interest[:dot_idx]
        datetime_last_apt_get_update = datetime.datetime.strptime(
            datetime_string, "%Y-%m-%d %H:%M:%S"
        )
        datetime_now = datetime.datetime.now()
        if datetime_now - datetime_last_apt_get_update > \
                datetime.timedelta(seconds=int(params["cache_valid_time"])):
            need_to_update = True

    module.exit_json(
        changed=False,
        need_to_update=need_to_update,
    )

from ansible.module_utils.basic import *
if __name__ == "__main__":
    main()
