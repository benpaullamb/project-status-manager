import json
import os
from pathlib import Path
import re

class ProjectManager:
  config_file = './projects.config.json'

  statuses = {
    'in-progress': 'green',
    'on-hold': 'blue',
    'plan-to-finish': 'yellow',
    'dropped': 'inactive',
    'completed': 'success'
  }

  status_regex = r'!\[status:(.+)\]\(https:\/\/img\.shields\.io\/badge\/status-(.+)-(.+)\)'

  def init_config(self):
    config = {}
    
    readmes = project_manager.get_all_readme_paths()
    for readme in readmes:
      status = project_manager.get_readme_status(readme)
      if status is not None:
        config[readme.parts[1]] = status
    
    project_manager.set_config(config)
  
  # TODO
  def update_projects(self):
    pass 

  def get_all_readme_paths(self):
    project_folder = Path('../')
    readmes = project_folder.glob('*/README.md')
    return list(readmes)

  def get_readme_status(self, readme):
    match = re.search(self.status_regex, readme.read_text(), re.I)
    if match:
      return match.group(1).strip()
    else:
      return None

  def set_readme_status(self, readme, status):
    status_colour = self.statuses[status]
    status_badge = re.sub(r'-', '--', status)
    new_status = '![status: %s](https://img.shields.io/badge/status-%s-%s)' % (status, status_badge, status_colour)

    new_readme = re.sub(self.status_regex, new_status, readme.read_text())
    readme.write_text(new_readme)
  
  def get_config(self):
    with open(self.config_file) as file:
      return json.load(file)

  def set_config(self, config):
    with open(self.config_file, 'w') as file:
      json.dump(config, file)

if __name__ == '__main__':
  project_manager = ProjectManager()
  project_manager.init_config()