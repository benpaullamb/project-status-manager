import json
import os
from pathlib import Path
import re

class ProjectManager:

  def load_config(self):
    with open('projects.config.json') as file:
      config = json.load(file)
      print(config)
  
  def load_readmes(self):
    project_names = os.listdir('../')
    projects = []

    for project in project_names:
      readme = Path('../%s/README.md' % project)
      if readme.is_file():
        with readme.open() as file:

          status = self.get_status(file)
          if status is not None:
            projects.append({
              'name': project,
              'status': status
            })

    with open('projects.config.json', 'w') as file:
      json.dump(projects, file)
  
  def get_status(self, file):
    try:
      for line in file:
        if line.startswith('![status:'):
          match = re.search('!\[status:\s*(.+)\]\(https:\/\/img\.shields\.io\/badge\/status-(.+)-(.+)\)', line, re.I)
          if match:
            status = match.group(1)
            return status
    except UnicodeDecodeError:
      return None

if __name__ == '__main__':
  project_manager = ProjectManager()
  project_manager.load_readmes()