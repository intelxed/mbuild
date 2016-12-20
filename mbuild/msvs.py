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

# TESTING MATRIX
# ('e' is for express)
#
#       32   32/64 64
#  6    ok    ?    N/A
#  7    ok    ok   N/A
#  8    ?     ok   ok
#  8e   ?     ?    ?
#  9    ?     ok   ok
#  9e   ok    ?    ?
# 10    ?     ?    ?
#

"""Environment setup for Microsoft Visual Studio.  Set INCLUDE,
LIBPATH, LIB, PATH, VCINSTALLDIR, VS80COMNTOOLS, VSINSTALLDIR, etc.
"""

import os
import sys
import platform
from .base import *
from .util import *
from .env import *

########################################################################
def set_env(v,s):
    """Add v=s to the shell environment"""
    if v in os.environ:
        orig = os.environ[v]
    else:
        orig = ''
        
    # We have had issues on windows were we attempt to make the
    # environment too long. This catches the error and prints a nice
    # error msg.
    try:
        os.environ[v]=s
    except Exception as e:
        sys.stderr.write( str(e) + '\n')
        sys.stderr.write("Env Variable [%s]\n" % (v))
        sys.stderr.write("Original was [%s]\n" % (orig))
        sys.stderr.write("New value was [%s]\n" % (s))
        sys.exit(1)
        
def set_env_list(v,slist):
    set_env(v,";".join(slist))

def add_to_front(v,s):
    """Add v=s+old_v to the shell environment"""
    set_env(v,s + ';' + os.environ[v])

def add_to_front_list(v,s):
    add_to_front(v,';'.join(s))

def add_env(v,s):
    """Add v=v;old_vs to the shell environment. Inserts at front"""
    v.insert(0,s)
########################################################################

def _find_dir_list(lst):
    for dir in lst:
        if os.path.exists(dir):
            return dir
    return None


def _set_msvs_dev6(env, x64_host, x64_target):   # VC 98
    vc_prefixes = [ "C:/VC98",
                    "C:/Program Files (x86)/Microsoft Visual Studio",
                    "C:/Program Files/Microsoft Visual Studio" ]

    msdev_prefixes = [
        "C:/Program Files/Microsoft Visual Studio/Common" ]
    vc_prefix = _find_dir_list(vc_prefixes)
    msdev_prefix = _find_dir_list(msdev_prefixes)
    if not vc_prefix:
        die("Could not find VC98")
    if not msdev_prefix:
        die("Could not find VC98 MSDEV")

    i = []
    add_env(i, vc_prefix + "/VC98/ATL/INCLUDE")
    add_env(i, vc_prefix + "/VC98/INCLUDE")
    add_env(i, vc_prefix + "/VC98/MFC/INCUDE")
    set_env_list("INCLUDE",i)

    lib = []
    add_env(lib, vc_prefix + "/VC98/LIB")
    add_env(lib, vc_prefix + "/VC98/MFC/LIB")
    set_env_list("LIB",lib)

    path=[]
    add_env(path, msdev_prefix + "/msdev98/Bin")
    add_env(path,    vc_prefix + "/VC98/Bin")
    add_env(path, msdev_prefix + "/TOOLS/WINNT")
    add_env(path, msdev_prefix + "/TOOLS")
    add_to_front_list('PATH', path)

    set_env("MSDevDir", msdev_prefix + "/msdev98")
    set_env("MSVCDir",     vc_prefix + "/VC98")

    return    vc_prefix + "/VC98"

def _set_msvs_dev7(env, x64_host, x64_target): # .NET 2003

    prefixes = [ "c:/Program Files/Microsoft Visual Studio .NET 2003",
                 "c:/Program Files (x86)/Microsoft Visual Studio .NET 2003"]
    prefix = _find_dir_list(prefixes)
    if not prefix:
        die("Could not find MSVS7 .NET 2003")

    inc = []
    add_env(inc, prefix + '/VC7/ATLMFC/INCLUDE')
    add_env(inc, prefix + '/VC7/include')
    add_env(inc, prefix + '/VC7/PlatformSDK/include/prerelease')
    add_env(inc, prefix + '/VC7/PlatformSDK/include')
    add_env(inc, prefix + '/SDK/v1.1/include')
    add_env(inc, prefix + '/SDK/v1.1/include/')
    set_env_list("INCLUDE",inc)

    lib = []
    add_env(lib, prefix + '/VC7/ATLMFC/LIB')
    add_env(lib, prefix + '/VC7/LIB')
    add_env(lib, prefix + '/VC7/PlatformSDK/lib/prerelease')
    add_env(lib, prefix + '/VC7/PlatformSDK/lib')
    add_env(lib, prefix + '/SDK/v1.1/lib')
    add_env(lib, prefix + '/SDK/v1.1/Lib/')
    set_env_list("LIB",lib)
    
    path = []
    add_env(path, prefix + "/Common7/IDE")
    add_env(path, prefix + "/VC7/bin")
    add_env(path, prefix + "/Common7/Tools")
    add_env(path, prefix + "/Common7/Tools/bin/prerelease")
    add_env(path, prefix + "/Common7/Tools/bin")
    add_env(path, prefix + "/SDK/v1.1/bin")
    add_to_front_list('PATH', path)
   
    set_env("VCINSTALLDIR",  prefix)
    set_env("VC71COMNTOOLS", prefix + "/Common7/Tools/")
    set_env("VSINSTALLDIR",  prefix + '/Common7/IDE')
    set_env("MSVCDir",  prefix + '/VC7')
    set_env("FrameworkVersion","v1.1.4322")
    set_env("FrameworkSDKDir", prefix + "/SDK/v1.1")
    set_env("FrameworkDir", "C:/WINDOWS/Microsoft.NET/Framework")
    # DevEnvDir has a trailing slash
    set_env("DevEnvDir",  prefix + "/Common7/IDE/")

    return    prefix + "/VC7"
def _set_msvs_dev8(env, x64_host, x64_target, regv=None): # VS 2005
    if regv:
        prefix = regv
    else:
        prefixes = ["c:/Program Files (x86)/Microsoft Visual Studio 8",
                    "c:/Program Files/Microsoft Visual Studio 8"]
    prefix = _find_dir_list(prefixes)
    if not os.path.exists(prefix):
        die("Could not find MSVC8 (2005)")

    set_env('VCINSTALLDIR',  prefix + '/VC')
    set_env('VS80COMNTOOLS', prefix + "/Common7/Tools")
    set_env('VSINSTALLDIR',  prefix)

    i =[] 
    add_env(i, prefix + "/VC/ATLMFC/INCLUDE")
    add_env(i, prefix + "/VC/INCLUDE")
    add_env(i, prefix + "/VC/PlatformSDK/include")
    add_env(i, prefix + "/SDK/v2.0/include")
    set_env_list('INCLUDE', i)

    set_env('FrameworkDir','C:/WINDOWS/Microsoft.NET/Framework')
    set_env('FrameworkVersion', 'v2.0.50727')
    set_env('FrameworkSDKDir', prefix  +'/SDK/v2.0')

    # DevEnvDir has a trailing slash
    set_env("DevEnvDir", prefix  +'/Common7/IDE/')

    lp = []
    path=[]
    lib=[]
    if x64_host and x64_target:
        add_env(lp, prefix + '/VC/ATLMFC/LIB/amd64')
        
        add_env(lib, prefix  + "/VC/ATLMFC/LIB/amd64")
        add_env(lib, prefix  + "/VC/LIB/amd64")
        add_env(lib, prefix  + "/VC/PlatformSDK/lib/amd64")
        add_env(lib, prefix  + "/SDK/v2.0/LIBAMD64")

        add_env(path, prefix + "/VC/bin/amd64")                    
        add_env(path, prefix + "/VC/PlatformSDK/bin/win64/amd64")  
        add_env(path, prefix + "/VC/PlatformSDK/bin")              
        add_env(path, prefix + "/VC/VCPackages")                   
        add_env(path, prefix + "/Common7/IDE")                     
        add_env(path, prefix + "/Common7/Tools")                   
        add_env(path, prefix + "/Common7/Tools/bin")               
        add_env(path, prefix + "/SDK/v2.0/bin")                    
        add_env(path, prefix + "C:/WINDOWS/Microsoft.NET/Framework64/v2.0.50727")

    elif not x64_target:

        add_env(path, prefix + '/Common7/IDE')
        add_env(path, prefix + '/VC/BIN')
        add_env(path, prefix + '/Common7/Tools')
        add_env(path, prefix + '/Common7/Tools/bin')
        add_env(path, prefix + '/VC/PlatformSDK/bin')
        add_env(path, prefix + '/SDK/v2.0/bin')
        add_env(path, prefix + '/VC/VCPackages')
        add_env(path, 'C:/WINDOWS/Microsoft.NET/Framework/v2.0.50727')

        add_env(lib, prefix +  '/VC/ATLMFC/LIB')
        add_env(lib, prefix +  '/VC/LIB')
        add_env(lib, prefix +  '/VC/PlatformSDK/lib')
        add_env(lib, prefix +  '/SDK/v2.0/lib')

        add_env(lp, prefix + '/VC/ATLMFC/LIB')
        add_env(lp, 'C:/WINDOWS/Microsoft.NET/Framework/v2.0.50727')

    add_to_front_list('PATH', path)
    set_env_list('LIB',lib)
    set_env_list('LIBPATH', lp)

    return    prefix + "/VC"

def _set_msvs_dev9(env, x64_host, x64_target, regv=None): # VS 2008
    if regv:
        prefix = regv
    else:
        prefixes = ['C:/Program Files (x86)/Microsoft Visual Studio 9.0',
                    'C:/Program Files/Microsoft Visual Studio 9.0']
    prefix = _find_dir_list(prefixes)

    set_env('VSINSTALLDIR', prefix)
    set_env('VS90COMNTOOLS', prefix + '/Common7/Tools')
    set_env('VCINSTALLDIR', prefix  +'/VC')
    set_env('FrameworkDir', 'C:/WINDOWS/Microsoft.NET/Framework')
    set_env('Framework35Version','v3.5')
    set_env('FrameworkVersion','v2.0.50727')
    set_env('FrameworkSDKDir', prefix  +'/SDK/v3.5')
    set_env('WindowsSdkDir','C:/Program Files/Microsoft SDKs/Windows/v6.0A')

    # DevEnvDir has a trailing slash
    set_env('DevEnvDir', prefix  + '/Common7/IDE/')
    inc = []
    add_env(inc,  prefix + 'VC/ATLMFC/INCLUDE')
    add_env(inc,  prefix + '/VC/INCLUDE')
    add_env(inc,  'C:/Program Files/Microsoft SDKs/Windows/v6.0A/include')
    set_env_list('INCLUDE',inc)

    path = []
    lib = []
    libpath = []

    if x64_target: # FIXME! 64b!!!!
        add_env(path, prefix + '/Common7/IDE')
        add_env(path, prefix + '/VC/BIN')
        add_env(path, prefix + '/Common7/Tools')
        add_env(path, prefix + '/VC/VCPackages')
        add_env(path, 'C:/Program Files/Microsoft SDKs/Windows/v6.0A/bin')
        add_env(path, 'C:/WINDOWS/Microsoft.NET/Framework/v3.5')
        add_env(path, 'C:/WINDOWS/Microsoft.NET/Framework/v2.0.50727')

        add_env(lib,  prefix +'/VC/ATLMFC/LIB/amdt64')
        add_env(lib,  prefix +'/VC/LIB/amd64')
        add_env(lib,  'C:/Program Files/Microsoft SDKs/Windows/v6.0A/lib/x64')

        add_env(libpath, 'C:/WINDOWS/Microsoft.NET/Framework64/v2.0.50727')
        add_env(libpath, 'C:/WINDOWS/Microsoft.NET/Framework64/v3.5')
        add_env(libpath, 'C:/WINDOWS/Microsoft.NET/Framework64/v2.0.50727')
        add_env(libpath, 'C:/WINDOWS/Microsoft.NET/Framework64/v2.0.50727')
        add_env(libpath, prefix + '/VC/ATLMFC/LIB/amd64')
        add_env(libpath, prefix + '/VC/LIB/amd64')
    else:
        add_env(path, prefix + '/Common7/IDE')
        add_env(path, prefix + '/VC/BIN')
        add_env(path, prefix + '/Common7/Tools')
        add_env(path, prefix + '/VC/VCPackages')
        add_env(path, 'C:/Program Files/Microsoft SDKs/Windows/v6.0A/bin')
        add_env(path, 'C:/WINDOWS/Microsoft.NET/Framework/v3.5')
        add_env(path, 'C:/WINDOWS/Microsoft.NET/Framework/v2.0.50727')

        add_env(lib,  prefix +'/VC/LIB')
        add_env(lib,  prefix +'/VC/ATLMFC/LIB')
        add_env(lib,  'C:/Program Files/Microsoft SDKs/Windows/v6.0A/lib')

        add_env(libpath, 'C:/WINDOWS/Microsoft.NET/Framework/v3.5')
        add_env(libpath, 'C:/WINDOWS/Microsoft.NET/Framework/v2.0.50727')
        add_env(libpath, prefix + '/VC/ATLMFC/LIB')
        add_env(libpath, prefix + '/VC/LIB')

    set_env_list('LIBPATH',libpath)
    set_env_list('LIB',lib)
    add_to_front_list('PATH',path)

    return    prefix + "/VC"


def _set_msvs_dev10(env, x64_host, x64_target, regv=None): # VS 2010
    if regv:
        prefix = regv
    else:
        prefix = 'C:/Program Files (x86)/Microsoft Visual Studio 10.0'

    path = []
    lib = []
    libpath = []

    inc  = []
    add_env(inc, prefix + '/VC/INCLUDE')
    add_env(inc, prefix + '/VC/ATLMFC/INCLUDE')
    add_env(inc, 'c:/Program Files (x86)/Microsoft SDKs/Windows/v7.0A/include')
    set_env_list('INCLUDE',inc)

    set_env('Framework35Version','v3.5')
    set_env('FrameworkVersion',   'v4.0.20728')
    set_env('FrameworkVersion32', 'v4.0.20728')

    set_env('VCINSTALLDIR', prefix + '/VC')
    set_env('VS100COMNTOOLS', prefix + '/Common7/Tools')
    set_env('VSINSTALLDIR' , prefix)
    set_env('WindowsSdkDir', 'c:/Program Files (x86)/Microsoft SDKs/Windows/v7.0A')

    # DevEnvDir has a trailing slash
    set_env('DevEnvDir', prefix  + '/Common7/IDE/')

    if x64_target:
        set_env('FrameworkDir','c:/WINDOWS/Microsoft.NET/Framework64')
        set_env('FrameworkDIR64','c:/WINDOWS/Microsoft.NET/Framework64')
        set_env('FrameworkVersion64', 'v4.0.20728')

        set_env('Platform','X64')
        add_env(lib, prefix  + '/VC/LIB/amd64')
        add_env(lib, prefix  + '/VC/ATLMFC/LIB/amd64')
        add_env(lib, 'c:/Program Files (x86)/Microsoft SDKs/Windows/v7.0A/lib/x64')
        
        add_env(libpath, 'c:/WINDOWS/Microsoft.NET/Framework64/v4.0.20728')
        add_env(libpath, 'c:/WINDOWS/Microsoft.NET/Framework64/v3.5')
        add_env(libpath, prefix + '/VC/LIB/amd64')
        add_env(libpath, prefix + '/VC/ATLMFC/LIB/amd64')

        add_env(path,  prefix + '/VC/BIN/amd64')
        add_env(path,  'c:/WINDOWS/Microsoft.NET/Framework64/v4.0.20728')
        add_env(path,  'C:/WINDOWS/Microsoft.NET/Framework64/v3.5')
        add_env(path,  prefix + '/VC/VCPackages')
        add_env(path,  prefix + '/Common7/IDE')
        add_env(path,  prefix + '/Common7/Tools')
        add_env(path,  'C:/Program Files (x86)/HTML Help Workshop')
        add_env(path,  'C:/Program Files (x86)/Microsoft SDKs/Windows/v7.0A/' +
                'bin/NETFX 4.0 Tools/x64')
        add_env(path,  'C:/Program Files (x86)/Microsoft SDKs/Windows/v7.0A/bin/x64')
        add_env(path,  'C:/Program Files (x86)/Microsoft SDKs/Windows/v7.0A/bin')
    else:
        set_env('FrameworkDir', 'c:/WINDOWS/Microsoft.NET/Framework')
        set_env('FrameworkDIR32', 'c:/WINDOWS/Microsoft.NET/Framework')
        
        add_env(lib,  prefix  + '/VC/LIB')
        add_env(lib,  prefix  + '/VC/ATLMFC/LIB')
        add_env(lib,  'c:/Program Files (x86)/Microsoft SDKs/Windows/v7.0A/lib')
        
        add_env(libpath,  'c:/WINDOWS/Microsoft.NET/Framework/v4.0.20728')
        add_env(libpath,  'c:/WINDOWS/Microsoft.NET/Framework/v3.5')
        add_env(libpath,  prefix  + '/VC/LIB')
        add_env(libpath,  prefix  + '/VC/ATLMFC/LIB')
        
        add_env(path,  prefix + '/Common7/IDE/')
        add_env(path,  prefix + '/VC/BIN')
        add_env(path,  prefix +'/Common7/Tools')
        add_env(path,  'C:/WINDOWS/Microsoft.NET/Framework/v4.0.20728')
        add_env(path,  'C:/WINDOWS/Microsoft.NET/Framework/v3.5')
        add_env(path,  prefix + '/VC/VCPackages')
        add_env(path,  'C:/Program Files (x86)/HTML Help Workshop')
        add_env(path,  prefix + '/Team Tools/Performance Tools')
        add_env(path,  'C;/Program Files (x86)/Microsoft SDKs/Windows/v7.0A/' +
                'bin/NETFX 4.0 Tools')
        add_env(path,  'C:/Program Files (x86)/Microsoft SDKs/Windows/v7.0A/bin')

    set_env_list('LIBPATH',libpath)
    set_env_list('LIB',lib)
    add_to_front_list('PATH',path)

    return    prefix + "/VC"


def _set_msvs_dev11(env, x64_host, x64_target, regv=None): # msvs2012
    progfi = 'C:/Program Files (x86)'
    if regv:
        prefix = regv
    else:
        prefix = progfi + '/Microsoft Visual Studio 11.0'

    sdkdir = progfi + '/Microsoft SDKs/Windows/v8.0'
    sdk8   = progfi + '/Microsoft SDKs/Windows/v8.0A'
    sdk7   = progfi + '/Microsoft SDKs/Windows/v7.0A'
    winkit = progfi + '/Windows Kits/8.0'

    path = []
    lib = []
    libpath = []

    inc  = []
    add_env(inc, prefix + '/VC/INCLUDE')
    add_env(inc, prefix + '/VC/ATLMFC/INCLUDE')
    add_env(inc, winkit + '/include')
    add_env(inc, winkit + '/include/um')
    add_env(inc, winkit + '/include/shared')
    add_env(inc, winkit + '/include/winrt')
    set_env_list('INCLUDE',inc)

    set_env('Framework35Version','v3.5')
    set_env('FrameworkVersion',   'v4.0.30319')
    set_env('FrameworkVersion32', 'v4.0.30319')

    set_env('VCINSTALLDIR', prefix + '/VC/')
    set_env('VS110COMNTOOLS', prefix + '/Common7/Tools')
    set_env('VSINSTALLDIR' , prefix)
    set_env('WindowsSdkDir', winkit)


    if x64_target:
        set_env('FrameworkDir','c:/WINDOWS/Microsoft.NET/Framework64')
        set_env('FrameworkDIR64','c:/WINDOWS/Microsoft.NET/Framework64')
        set_env('FrameworkVersion64', 'v4.0.30319')

        set_env('Platform','X64')

        add_env(lib, prefix  + '/VC/LIB/amd64')
        add_env(lib, prefix  + '/VC/ATLMFC/LIB/amd64')
        add_env(lib, winkit + '/lib/win8/um/x64')


        add_env(libpath, 'c:/WINDOWS/Microsoft.NET/Framework64/v4.0.30319')
        add_env(libpath, 'c:/WINDOWS/Microsoft.NET/Framework64/v3.5')
        add_env(libpath, prefix + '/VC/LIB/amd64')
        add_env(libpath, prefix + '/VC/ATLMFC/LIB/amd64')
        add_env(libpath, winkit + '/References/CommonConfiguration/Neutral')
        add_env(libpath, sdkdir + 'ExtensionSDKs/Microsoft.VCLibs/11.0/' + 
                'References/CommonConfiguration/neutral')

        add_env(path,  prefix + '/VC/BIN/amd64')
        add_env(path,  'c:/WINDOWS/Microsoft.NET/Framework64/v4.0.30319')
        add_env(path,  'C:/WINDOWS/Microsoft.NET/Framework64/v3.5')

        add_env(path, prefix + '/Common7/IDE/CommonExtensions/Microsoft/TestWindow')
        add_env(path, prefix + '/VC/VCPackages')
        add_env(path, prefix + '/Common7/IDE')
        add_env(path, prefix + '/Common7/Tools')
        add_env(path, 'C:/Program Files (x86)/HTML Help Workshop')
        add_env(path, prefix + '/Team Tools/Performance Tools/x64')
        add_env(path, prefix + '/Team Tools/Performance Tools')
        add_env(path, winkit  + '/8.0/bin/x64')
        add_env(path, sdk8 + '/bin/NETFX 4.0 Tools/x64')
        add_env(path, sdk7 + '/Bin/x64')
        add_env(path, sdk8 + '/bin/NETFX 4.0 Tools')
        add_env(path, sdk7 + '/Bin')
        add_env(path, winkit + '/Windows Performance Toolkit')
        add_env(path, 'C:/Program Files/Microsoft SQL Server/110/Tools/Binn')

    else:
        set_env('FrameworkDir', 'c:/WINDOWS/Microsoft.NET/Framework')
        set_env('FrameworkDIR32', 'c:/WINDOWS/Microsoft.NET/Framework')

        add_env(lib,  prefix + '/VC/LIB')
        add_env(lib,  prefix + '/VC/ATLMFC/LIB')
        add_env(lib,  winkit + '/lib/win8/um/x86')

        
        add_env(libpath,  'c:/WINDOWS/Microsoft.NET/Framework/v4.0.30319')
        add_env(libpath,  'c:/WINDOWS/Microsoft.NET/Framework/v3.5')
        add_env(libpath,  prefix  + '/VC/LIB')
        add_env(libpath,  prefix  + '/VC/ATLMFC/LIB')
        add_env(libpath,  winkit  + '/References/CommonConfiguration/Neutral')
        add_env(libpath,  sdkdir  + '/ExtensionSDKs/Microsoft.VCLibs/11.0/' +
                'References/CommonConfiguration/neutral')


        add_env(path, prefix + '/Common7/IDE/CommonExtensions/Microsoft/TestWindow')
        add_env(path, 'C:/Program Files (x86)/Microsoft SDKs/F#/3.0/Framework/v4.0')
        add_env(path, prefix + '/Common7/IDE')
        add_env(path, prefix + '/VC/BIN')
        add_env(path, prefix + '/Common7/Tools')
        add_env(path, 'C:/Windows/Microsoft.NET/Framework/v4.0.30319')
        add_env(path, 'C:/Windows/Microsoft.NET/Framework/v3.5')
        add_env(path, prefix + '/VC/VCPackages')
        add_env(path, 'C:/Program Files (x86)/HTML Help Workshop')
        add_env(path, prefix + '/Team Tools/Performance Tools')
        add_env(path, winkit + '/bin/x86')
        add_env(path, sdk8 + '/bin/NETFX 4.0 Tools')
        add_env(path, sdk7 + '/Bin')
        add_env(path, winkit + '/Windows Performance Toolkit')
        add_env(path, 'C:/Program Files/Microsoft SQL Server/110/Tools/Binn')



    set_env_list('LIBPATH',libpath)
    set_env_list('LIB',lib)
    add_to_front_list('PATH',path)

    return    prefix + "/VC"



def _set_msvs_dev12(env, x64_host, x64_target, regv=None): # msvs2013
    progfi = 'C:/Program Files (x86)'
    if regv:
        prefix = regv
    else:
        prefix = progfi + '/Microsoft Visual Studio 12.0'

    sdk81a = progfi + '/Microsoft SDKs/Windows/v8.1A'
    sdk81  = progfi + '/Microsoft SDKs/Windows/v8.1'
    winkit = progfi + '/Windows Kits/8.1'


    path = []
    lib = []
    libpath = []

    inc  = []
    add_env(inc, prefix + '/VC/INCLUDE')
    add_env(inc, prefix + '/VC/ATLMFC/INCLUDE')
    add_env(inc, winkit + '/include') # not used in msvs12
    add_env(inc, winkit + '/include/um')
    add_env(inc, winkit + '/include/shared')
    add_env(inc, winkit + '/include/winrt')
    set_env_list('INCLUDE',inc)

    set_env('Framework40Version','v4.0')
    set_env('FrameworkVersion',   'v4.0.30319')
    set_env('ExtensionSdkDir', 
                   sdk81  + '/ExtensionSDKs')

    set_env('VCINSTALLDIR', prefix + '/VC/')
    set_env('VS120COMNTOOLS', prefix + '/Common7/Tools')
    set_env('VSINSTALLDIR' , prefix)
    set_env('WindowsSdkDir', winkit)
    set_env('VisualStudioVersion','12.0')

    set_env('WindowsSDK_ExecutablePath_x86',
            sdk81a + '/bin/NETFX 4.5.1 Tools/')

    if x64_target:
        set_env('WindowsSDK_ExecutablePath_x64',
                sdk81a +'/bin/NETFX 4.5.1 Tools/x64/')

        set_env('FrameworkDir','c:/WINDOWS/Microsoft.NET/Framework64')
        set_env('FrameworkDIR64','c:/WINDOWS/Microsoft.NET/Framework64')
        set_env('FrameworkVersion64', 'v4.0.30319')

        set_env('Platform','X64')

        add_env(lib, prefix  + '/VC/LIB/amd64')
        add_env(lib, prefix  + '/VC/ATLMFC/LIB/amd64')
        add_env(lib, winkit + '/lib/winv6.3/um/x64')

        add_env(libpath, 'c:/WINDOWS/Microsoft.NET/Framework64/v4.0.30319')
        add_env(libpath, prefix + '/VC/LIB/amd64')
        add_env(libpath, prefix + '/VC/ATLMFC/LIB/amd64')
        add_env(libpath, winkit + '/References/CommonConfiguration/Neutral')
        add_env(libpath, sdk81 + '/ExtensionSDKs/Microsoft.VCLibs/12.0/' + 
                'References/CommonConfiguration/neutral')

        add_env(path, prefix + '/Common7/IDE/CommonExtensions/Microsoft/TestWindow')
        add_env(path,  prefix + '/VC/BIN/amd64')
        add_env(path,  'c:/WINDOWS/Microsoft.NET/Framework64/v4.0.30319')

        add_env(path, prefix + '/VC/VCPackages')
        add_env(path, prefix + '/Common7/IDE')
        add_env(path, prefix + '/Common7/Tools')
        add_env(path, 'C:/Program Files (x86)/HTML Help Workshop')
        add_env(path, prefix + '/Team Tools/Performance Tools/x64')
        add_env(path, prefix + '/Team Tools/Performance Tools')
        add_env(path, winkit  + '/8.1/bin/x64')
        add_env(path, winkit  + '/8.1/bin/x86')
        add_env(path, sdk81a + '/bin/NETFX 4.5.1 Tools/x64')
        add_env(path, winkit + '/Windows Performance Toolkit')


    else:
        set_env('FrameworkDir', 'c:/WINDOWS/Microsoft.NET/Framework')
        set_env('FrameworkDIR32', 'c:/WINDOWS/Microsoft.NET/Framework')
        set_env('FrameworkVersion32','v4.0.30319')

        add_env(lib,  prefix + '/VC/LIB')
        add_env(lib,  prefix + '/VC/ATLMFC/LIB')
        add_env(lib,  winkit + '/lib/winv6.3/um/x86')
        
        add_env(libpath,  'c:/WINDOWS/Microsoft.NET/Framework/v4.0.30319')
        add_env(libpath,  prefix  + '/VC/LIB')
        add_env(libpath,  prefix  + '/VC/ATLMFC/LIB')
        add_env(libpath,  winkit  + '/References/CommonConfiguration/Neutral')
        add_env(libpath,  sdk81  + '/ExtensionSDKs/Microsoft.VCLibs/12.0/' + 
                'References/CommonConfiguration/neutral')


        add_env(path, prefix + '/Common7/IDE/CommonExtensions/Microsoft/TestWindow')
        add_env(path, progfi + '/Microsoft SDKs/F#/3.1/Framework/v4.0')
        add_env(path, progfi  + '/MSBuild/12.0/bin')
        add_env(path, prefix + '/Common7/IDE')
        add_env(path, prefix + '/VC/BIN')
        add_env(path, prefix + '/Common7/Tools')
        add_env(path, 'C:/Windows/Microsoft.NET/Framework/v4.0.30319')
        add_env(path, prefix + '/VC/VCPackages')
        add_env(path, progfi + '/HTML Help Workshop')
        add_env(path, prefix + '/Team Tools/Performance Tools')
        add_env(path, winkit + '/bin/x86')
        add_env(path, sdk81a + '/bin/NETFX 4.5.1 Tools')
        add_env(path, winkit + '/Windows Performance Toolkit')


    set_env_list('LIBPATH',libpath)
    set_env_list('LIB',lib)
    add_to_front_list('PATH',path)

    return    prefix + "/VC"




def _set_msvs_dev14(env, x64_host, x64_target, regv=None): # msvs 2015
    progfi = 'C:/Program Files (x86)'
    if regv:
        prefix = regv
    else:
        prefix = progfi + '/Microsoft Visual Studio 14.0'

    sdk81a = progfi + '/Microsoft SDKs/Windows/v8.1A'
    sdk81  = progfi + '/Microsoft SDKs/Windows/v8.1'
    winkit = progfi + '/Windows Kits/8.1'
    winkit10 = progfi + '/Windows Kits/10'

    # Find the UCRT Version. Could not locate a registry entry with
    # the information. Preview version of msvs2015/dev14 did not set
    # the env var. Poke around in the directory system as a last
    # resort. Could make this configrable
    winkit10version = None
    if 'UCRTVersion' in os.environ:
        winkit10version = os.environ['UCRTVersion']
    if not winkit10version:
        # use glob and find youngest directory
        ctime = 0
        for g in glob(winkit10 + '/include/*'):
            if os.path.exists('{}/ucrt'.format(g)):
                gtime = os.path.getctime(g)
                if gtime > ctime:
                    winkit10version = os.path.basename(g)
                    ctime = gtime
    if not winkit10version:
        die("Did not find winkit 10 version")
    msgb("UCRT Version", winkit10version)
       
    path = []
    lib = []
    libpath = []

    inc  = []
    add_env(inc, prefix + '/VC/INCLUDE')
    add_env(inc, prefix + '/VC/ATLMFC/INCLUDE')
    add_env(inc, winkit + '/include') # not used in msvs12
    
    add_env(inc, winkit10 + '/include/{}/ucrt'.format(winkit10version)) 
    add_env(inc, winkit + '/include/shared')
    add_env(inc, winkit + '/include/um')
    add_env(inc, winkit + '/include/winrt')
    set_env_list('INCLUDE',inc)

    set_env('Framework40Version','v4.0')
    set_env('FrameworkVersion',   'v4.0.30319')
    set_env('ExtensionSdkDir', 
                   sdk81  + '/ExtensionSDKs')

    set_env('VCINSTALLDIR', prefix + '/VC/')
    set_env('VS140COMNTOOLS', prefix + '/Common7/Tools')
    set_env('VSINSTALLDIR' , prefix)
    set_env('WindowsSdkDir', winkit)
    set_env('VisualStudioVersion','14.0')

    set_env('WindowsSDK_ExecutablePath_x86',
            sdk81a + '/bin/NETFX 4.5.1 Tools/')

    if x64_target:
        set_env('WindowsSDK_ExecutablePath_x64',
                sdk81a +'/bin/NETFX 4.5.1 Tools/x64/')

        set_env('FrameworkDir','c:/WINDOWS/Microsoft.NET/Framework64')
        set_env('FrameworkDIR64','c:/WINDOWS/Microsoft.NET/Framework64')
        set_env('FrameworkVersion64', 'v4.0.30319')

        set_env('Platform','X64')

        add_env(lib, prefix  + '/VC/LIB/amd64')
        add_env(lib, prefix  + '/VC/ATLMFC/LIB/amd64')
        add_env(lib,  winkit10 + '/lib/{}/ucrt/x64'.format(winkit10version))
        add_env(lib, winkit + '/lib/winv6.3/um/x64')

        add_env(libpath, 'c:/WINDOWS/Microsoft.NET/Framework64/v4.0.30319')
        add_env(libpath, prefix + '/VC/LIB/amd64')
        add_env(libpath, prefix + '/VC/ATLMFC/LIB/amd64')
        add_env(libpath, winkit + '/References/CommonConfiguration/Neutral')
        add_env(libpath, sdk81 + '/ExtensionSDKs/Microsoft.VCLibs/14.0/' + 
                'References/CommonConfiguration/neutral')

        add_env(path, prefix + '/Common7/IDE/CommonExtensions/Microsoft/TestWindow')
        add_env(path,  prefix + '/VC/BIN/amd64')
        add_env(path,  'c:/WINDOWS/Microsoft.NET/Framework64/v4.0.30319')

        add_env(path, prefix + '/VC/VCPackages')
        add_env(path, prefix + '/Common7/IDE')
        add_env(path, prefix + '/Common7/Tools')
        add_env(path, 'C:/Program Files (x86)/HTML Help Workshop')
        add_env(path, prefix + '/Team Tools/Performance Tools/x64')
        add_env(path, prefix + '/Team Tools/Performance Tools')
        add_env(path, winkit  + '/8.1/bin/x64')
        add_env(path, winkit  + '/8.1/bin/x86')
        add_env(path, sdk81a + '/bin/NETFX 4.5.1 Tools/x64')
        add_env(path, winkit + '/Windows Performance Toolkit')


    else:
        set_env('FrameworkDir', 'c:/WINDOWS/Microsoft.NET/Framework')
        set_env('FrameworkDIR32', 'c:/WINDOWS/Microsoft.NET/Framework')
        set_env('FrameworkVersion32','v4.0.30319')

        add_env(lib,  prefix + '/VC/LIB')
        add_env(lib,  prefix + '/VC/ATLMFC/LIB')
        add_env(lib,  winkit10 + '/lib/{}/ucrt/x86'.format(winkit10version))
        add_env(lib,  winkit + '/lib/winv6.3/um/x86')
        
        add_env(libpath,  'c:/WINDOWS/Microsoft.NET/Framework/v4.0.30319')
        add_env(libpath,  prefix  + '/VC/LIB')
        add_env(libpath,  prefix  + '/VC/ATLMFC/LIB')
        add_env(libpath,  winkit  + '/References/CommonConfiguration/Neutral')
        add_env(libpath,  sdk81  + '/ExtensionSDKs/Microsoft.VCLibs/14.0/' + 
                'References/CommonConfiguration/neutral')


        add_env(path, prefix + '/Common7/IDE/CommonExtensions/Microsoft/TestWindow')
        add_env(path, progfi + '/Microsoft SDKs/F#/3.1/Framework/v4.0')
        add_env(path, progfi  + '/MSBuild/14.0/bin')
        add_env(path, prefix + '/Common7/IDE')
        add_env(path, prefix + '/VC/BIN')
        add_env(path, prefix + '/Common7/Tools')
        add_env(path, 'C:/Windows/Microsoft.NET/Framework/v4.0.30319')
        add_env(path, prefix + '/VC/VCPackages')
        add_env(path, progfi + '/HTML Help Workshop')
        add_env(path, prefix + '/Team Tools/Performance Tools')
        add_env(path, winkit + '/bin/x86')
        add_env(path, sdk81a + '/bin/NETFX 4.5.1 Tools')
        add_env(path, winkit + '/Windows Performance Toolkit')


    set_env_list('LIBPATH',libpath)
    set_env_list('LIB',lib)
    add_to_front_list('PATH',path)

    return    prefix + "/VC"


def _try_to_figure_out_msvs_version(env):
    prefixes = [ 
        (14,'C:/Program Files (x86)/Microsoft Visual Studio 14.0'),
        (14,'C:/Program Files/Microsoft Visual Studio 14.0'),
        
        (12,'C:/Program Files (x86)/Microsoft Visual Studio 12.0'),
        (12,'C:/Program Files/Microsoft Visual Studio 12.0'),

        (11,'C:/Program Files (x86)/Microsoft Visual Studio 11.0'),
        (11,'C:/Program Files/Microsoft Visual Studio 11.0'),
        
        (10,'C:/Program Files (x86)/Microsoft Visual Studio 10.0'),
        (10,'C:/Program Files/Microsoft Visual Studio 10.0'),
        
        (9,'C:/Program Files (x86)/Microsoft Visual Studio 9.0'),
        (9,'C:/Program Files/Microsoft Visual Studio 9.0'),
        
        (8, "c:/Program Files (x86)/Microsoft Visual Studio 8"),
        (8,"c:/Program Files/Microsoft Visual Studio 8"),
        
        (7, "c:/Program Files/Microsoft Visual Studio .NET 2003"),
        (7,"c:/Program Files (x86)/Microsoft Visual Studio .NET 2003")

    ]
    for v,dir in prefixes:
        #print dir
        if os.path.exists(dir):
            #print 'FOUND', dir
            return str(v)
    return '' # we don't know

def _read_registry(root,key,value):
    import winreg
    try:
        hkey = winreg.OpenKey(root, key)
    except:
        return None
    try:
        (val, typ) = winreg.QueryValueEx(hkey, value)
    except:
        winreg.CloseKey(hkey)
        return None
    winreg.CloseKey(hkey)
    return val

def find_msvc(env,version):
    import winreg
    vs_ver = str(version) + '.0'
    vs_key = 'SOFTWARE\\Microsoft\\VisualStudio\\' + vs_ver + '\\Setup\\VS'
    vc_key = 'SOFTWARE\\Microsoft\\VisualStudio\\' + vs_ver + '\\Setup\\VC'
    vs_dir = _read_registry(winreg.HKEY_LOCAL_MACHINE, vs_key, 'ProductDir')
    vc_dir = _read_registry(winreg.HKEY_LOCAL_MACHINE, vc_key, 'ProductDir')
    
    # On a 64-bit host, look for a 32-bit installation 

    if (not vs_dir or not vc_dir):
        vs_key = 'SOFTWARE\\Wow6432Node\\Microsoft\\VisualStudio\\' + \
            vs_ver + '\\Setup\\VS'
        vc_key = 'SOFTWARE\\Wow6432Node\\Microsoft\\VisualStudio\\' + \
            vs_ver + '\\Setup\\VC'
        vs_dir = _read_registry(winreg.HKEY_LOCAL_MACHINE, 
                                vs_key, 'ProductDir')
        vc_dir = _read_registry(winreg.HKEY_LOCAL_MACHINE, 
                                vc_key, 'ProductDir')
    return (vs_dir,vc_dir)

def _try_to_figure_out_msvs_version_registry(env):
    versions = [14,12,11,10,9,8,7,6]
    for v in versions:
        (vs_dir,vc_dir) = find_msvc(env,v)
        if vs_dir and vc_dir:
            return (str(v),vs_dir)
    return (None,None)

def set_msvs_env(env):
    x64_target=False
    if  env['host_cpu'] == 'x86-64':
        x64_target=True

    x64_host = False
    if  env['build_cpu'] == 'x86-64':
        x64_host=True

    # "express" compiler is 32b only
    vc = None
    # Verify validity of chosen msvs_version in registry
    if env['msvs_version'] != '' :
        v = int(env['msvs_version'])
        (vs_dir,vc_dir) = find_msvc(env,v)
        if not (vs_dir and vc_dir):
            warn("Could no find specified version of MSVS. Looking around...")
            env['msvs_version'] = '' 
    if env['msvs_version'] == '':
        # The chosen msvs_version was not valid we need to search for it
        env['msvs_version'] = _try_to_figure_out_msvs_version(env)
    # FIXME: could add a knob to just use registry..
    if env['msvs_version'] == '':
        env['msvs_version'], vs_dir = \
            _try_to_figure_out_msvs_version_registry(env)
        if env['msvs_version'] == None:
            die("Did not find MSVS version!")             

    vs_dir = None
    i = int(env['msvs_version'])
    if i == 6: # 32b only
        vc = _set_msvs_dev6(env,x64_host, x64_target)
    elif i == 7: # 32b only
        vc = _set_msvs_dev7(env,x64_host, x64_target)

    elif i == 8: # 32b or 64b
        vc = _set_msvs_dev8(env, x64_host, x64_target, vs_dir)
    elif i == 9: # 32b or 64b
        vc = _set_msvs_dev9(env, x64_host, x64_target, vs_dir)
    elif i == 10: # 32b or 64b
        vc = _set_msvs_dev10(env, x64_host, x64_target, vs_dir)
    elif i == 11: # 32b or 64b
        vc = _set_msvs_dev11(env, x64_host, x64_target, vs_dir)
    elif i == 12: # 32b or 64b
        vc = _set_msvs_dev12(env, x64_host, x64_target, vs_dir)
    # And 12 shall be followed by 14. 13? 13 is Right Out!
    elif i == 14: # 32b or 64b
        vc = _set_msvs_dev14(env, x64_host, x64_target, vs_dir)
    else:
        die("Unhandled MSVS version: " + env['msvs_version'])

    msgb("FOUND MS VERSION",env['msvs_version'])
    return vc
    
