import json
from pathlib import Path
import re
import subprocess

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
    print('Config initialised.')
  
  def update_projects(self):
    print('=================')
    print('Updating projects')
    print('-----------------')
    config = self.get_config()

    for project_name, status in config.items():
      readme = Path('../%s/README.md' % (project_name))

      old_status = self.get_readme_status(readme)

      if old_status == status:
        print(f'[SKIPPED] {project_name}: {old_status} => {status}')
        continue
      
      print(f'{project_name}: {old_status} => {status}')
      self.set_readme_status(readme, status)
    
    print('Done.')

  def get_all_readme_paths(self):
    project_folder = Path('../')
    readmes = project_folder.glob('*/README.md')
    return list(readmes)

  def get_readme_status(self, readme):
    try:
      readme_text = readme.read_text()

      match = re.search(self.status_regex, readme_text, re.I)
      if match:
        return match.group(1).strip()
      else:
        return None

    except UnicodeDecodeError:
      print(f'Decoding error for {readme.parent}')
      return None

  def set_readme_status(self, readme, status):
    if status not in self.statuses:
      return print(f'"{status}" is not a valid status')

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
      json.dump(config, file, indent=2)
  
  def commit_to_github(self):
    print('====================')
    print('Committing to GitHub')
    print('--------------------')

    project_folder = Path(__file__).joinpath('../../').resolve()

    for project in project_folder.iterdir():
      if project.name == 'project-status-manager':
        continue

      git_status = subprocess.run(['git', 'status'], cwd=project, capture_output=True, text=True)
      is_mods = re.search('modified:\s*README.md', git_status.stdout)

      if not is_mods:
        continue
      
      print(f'\n{project.name.upper()} HAS CHANGED:')
      print('--------------------------------------')
      print(git_status.stdout)

      should_commit_input = input('Commit & push? (y/n)')
      
      if 'y' in should_commit_input.lower():
        subprocess.run(['git', 'add', 'README.md'], cwd=project)
        subprocess.run(['git', 'commit', '-m', '"chore: updated project status"'], cwd=project)
        subprocess.run(['git', 'push'], cwd=project)
    
    print('Done.')


if __name__ == '__main__':
  project_manager = ProjectManager()
  # project_manager.init_config()
  project_manager.update_projects()
  project_manager.commit_to_github()