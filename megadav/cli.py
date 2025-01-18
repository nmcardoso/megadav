import os
from argparse import ArgumentParser
from pathlib import Path
from subprocess import run


def start_handler(args):
  usr = os.environ.get('MEGA_USER')
  pwd = os.environ.get('MEGA_PASS')
  if usr and pwd:
    run(['mega-login', usr, pwd])
    run(['mega-webdav', '/'])



def url_handler(args):
  run(['mega-webdav'])



def logout_handler(args):
  run(['mega-logout'])



def credentials_handler(args):
  print('MEGA_USER:', os.environ.get('MEGA_USER', 'not found'))
  print('MEGA_PASS:', os.environ.get('MEGA_PASS', 'not found'))
  
  
  
  
def install_handler(args):
  entry = """
[Desktop Entry]
Type=Application
Exec="megadav start"
Hidden=true
NoDisplay=true
X-GNOME-Autostart-enabled=true
Name=MegaDAV startup
  """.strip()
  dest = Path.home() / '.config' / 'autostart' / 'megadav.desktop'
  dest.parent.mkdir(parents=True, exist_ok=True)
  dest.write_text(entry)
  run(['chmod', 'a+x', str(dest.absolute())])


def entrypoint():
  parser = ArgumentParser(prog='MegaDAV', description='MEGA.nz DAV daemon')
  subparser = parser.add_subparsers(dest='subprog')
  start = subparser.add_parser('start', description='Start DAV server')
  
  url = subparser.add_parser('url', description='Show DAV url')
  
  logout = subparser.add_parser('logout', description='Logout Mega account')
  
  credentials = subparser.add_parser('credentials', description='Mega account credentials')
  
  install = subparser.add_parser('install', description='Install MegaDAV daemon')
  
  args = parser.parse_args()
  
  cmd_handlers = {
    'start': start_handler,
    'url': url_handler,
    'logout': logout_handler,
    'credentials': credentials_handler,
    'install': install_handler,
  }
  
  handler = cmd_handlers.get(args.subprog)
  
  if handler:
    handler(args)
  else:
    parser.print_help()
    

if __name__ == "__main__":
  entrypoint()