import os
import subprocess

from setuptools import setup

output = subprocess.check_output("dpkg-query -W --showformat='${Status}' sense-hat".split(' '))
package_installed = 'install ok installed' in output.decode()
reboot_required = False
if not package_installed:
    print('Updating package list')
    subprocess.call(['apt-get', 'update'])
    print('Installing sense-hat package')
    reboot_required = subprocess.call(['apt-get', 'install', '-y', 'sense-hat']) == 0
  
classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: Home Automation',
               'Topic :: System :: Hardware',
               'Topic :: System :: Monitoring']

try:
    os.makedirs('/etc/myDevices/plugins/cayenne-plugin-sensehat/data')
except FileExistsError:
    pass

setup(name             = 'sensehat',
      version          = '0.1.0',
      author           = 'myDevices',
      author_email     = 'N/A',
      description      = 'myDevices Cayenne Sense HAT plugin',
      keywords         = 'myDevices IoT Cayenne Sense HAT plugin',
      url              = 'https://www.mydevices.com/',
      classifiers      = classifiers,
      packages         = ['sensehat'],
      data_files       = [('/etc/myDevices/plugins/cayenne-plugin-sensehat/data', ['data/image.png']),
                            ('/lib/systemd/system', ['data/sensehat.service'])]
      )

subprocess.call(['systemctl', 'daemon-reload'])
subprocess.call(['systemctl', 'start', 'sensehat.service'])

if reboot_required:
    answer = input('\nSense HAT requires a reboot to finish the install. Reboot now? [Y/n]: ').lower()
    if answer not in ('n', 'no'):
        os.system('reboot')
