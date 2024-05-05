#BEGIN_LEGAL
#
#Copyright (c) 2022 Intel Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  
#END_LEGAL

#
# to build the distribution file:
#    python setup.py sdist  --formats=gztar,zip
#
# to build an installer for windows:
#    python setup.py bdist_wininst
#
# to install the distribution file:
#     python setup.py install

from distutils.core import setup
setup(name='mbuild',
      version='0.2496',
      url='https://github.com/intelxed/mbuild',
      description='mbuild: python based build system',
      author='XED Team',
      author_email='xed.team@intel.com',
      packages=['mbuild']
      )

