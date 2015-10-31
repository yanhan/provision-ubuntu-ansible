#!/usr/bin/env python

# This program adds the supplied folders (via the --folder flag(s)) to the PATH
# environment variable inside the `/etc/environment` file.
# No error checking is done on the supplied folders.
#
#
# Example
#
# Adds the `/usr/local/go/bin` and `/home/vagrant/bin` folders to the PATH
# environment variable in the `/etc/environment` file:
#
#     update-etc-environment-path --folder /usr/local/go/bin --folder /home/vagrant/bin

import argparse
import re

ETC_ENVIRONMENT = "/etc/environment"
PATH_STRING_TEMPLATE = "PATH=\"{folders}\""

parser = argparse.ArgumentParser(
  description="Adds a folder to the PATH environment variable in " +
    "/etc/environment"
)
parser.add_argument("--folder", action="append", required=True,
  dest="folders",
  help=re.sub(r"""\s+""", " ",
    """Folder to add to the PATH environment variable. Multiple folders can
    be supplied, one for each --folder option"""
  )
)

def _remove_duplicate_folders(folder_list):
  """Removes duplicate folders from a list of folders and maintains the
  original order of the list

  Args:
    folder_list(list of str): List of folders

  Returns:
    list of str: List of folders with duplicates removed
  """
  new_folders_set = set()
  new_folders_list = []
  for folder in folder_list:
    if folder not in new_folders_set:
      new_folders_set.add(folder)
      new_folders_list.append(folder)
  return new_folders_list

def _add_folders_to_path(path_line, folders_to_add_list):
  """Ensures that the given list of folders are inside the given line (for
  the PATH environment variable).

  Args:
    path_line(str): line in /etc/environment for the PATH environment variable
    folder_to_add_list(list of str): list of strings, where each string is a
      folder that must be present in the PATH environment variable. This list is
      assumed to be free of duplicate folders.

  Returns:
    (bool, str): The boolean value indicates if the line for the PATH
      environment variable has been modified; true means modified, false means
      not modified. The string value is the new line for the PATH environment
      variable, with all the folders in the `folders_to_add_list`
  """
  PATH_STRING_TEMPLATE = "PATH=\"{folders}\""

  # strip off surrounding quotes
  match_obj = re.match(r"""^PATH=['"]*(.*)$""", path_line)
  existing_folders_line = None
  if match_obj is None:
    return (True, PATH_STRING_TEMPLATE.format(
      folders=":".join(folders_to_add_list)
    ),)
  else:
    # strip trailing quotes.
    # We cannot just add a ['"]* to the above regex due to how greedy matching
    # works. It's possible to use non-greedy pattern matching but we do not do
    # that here.
    existing_folders_line = re.sub(r"""['"]*$""", "", match_obj.group(1))

  # obtain existing folders
  existing_folders_list = [
    folder for folder in existing_folders_line.split(":")
      if folder.strip() != ""
  ]
  existing_folders_set = set(existing_folders_list)
  path_line_modified = False
  for folder in folders_to_add_list:
    if folder not in existing_folders_set:
      path_line_modified = True
      existing_folders_list.append(folder)
      existing_folders_set.add(folder)
  return (path_line_modified, PATH_STRING_TEMPLATE.format(
    folders=":".join(existing_folders_list)
  ),)

def main():
  args = parser.parse_args()
  etc_env_lines_list = None
  with open(ETC_ENVIRONMENT, "r") as f:
    etc_env_lines_list = f.read().split("\n")
    if etc_env_lines_list[-1] == "":
      del etc_env_lines_list[-1]

  path_line_idx = None
  path_line = None
  for (idx, line) in enumerate(etc_env_lines_list):
    if line.startswith("PATH="):
      path_line_idx = idx
      path_line = line
      break

  folders_to_add_list = _remove_duplicate_folders(args.folders)

  if path_line_idx is None:
    etc_env_lines_list.append(
      PATH_STRING_TEMPLATE.format(folders=":".join(folders_to_add_list))
    )
  else:
    (_, new_path_line) = _add_folders_to_path(path_line, folders_to_add_list)
    etc_env_lines_list[path_line_idx] = new_path_line

  with open(ETC_ENVIRONMENT, "w") as f:
    for line in etc_env_lines_list:
      f.write("{}\n".format(line))

if __name__ == "__main__":
  main()
