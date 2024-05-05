#!/usr/bin/env python
# -*- python -*-
#BEGIN_LEGAL
#
#Copyright (c) 2016 Intel Corporation
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

import sys
import find
import mbuild

def setup():
    env = mbuild.env_t()
    env.parse_args()
    mbuild.cmkdir(env['build_dir'])
    if not env.on_windows():
        env['LINK'] = env['CC'] # not g++ for this program
    return env

def work(env):
    #with then env, the dag hash file is put in the build_dir.
    dag = mbuild.dag_t('circular-test',env=env)
    work_queue = mbuild.work_queue_t(env['jobs'])

    env.compile_and_link(dag, ['main.c'], 'main' + env['EXEEXT'])

    okay = work_queue.build(dag=dag)
    if not okay:
        mbuild.die("build failed")
    mbuild.msgb("SUCCESS")


if __name__ == "__main__":
    env = setup()
    work(env)
