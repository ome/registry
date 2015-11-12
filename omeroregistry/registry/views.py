#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
# Copyright (c) 2015 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Aleksandra Tarkowska <A(dot)Tarkowska(at)dundee(dot)ac(dot)uk>.
#
# Version: 1.0
#

''' A view functions is simply a Python function that takes a Web request and
returns a Web response. This response can be the HTML contents of a Web page,
or a redirect, or the 404 and 500 error, or an XML document, or an image...
or anything.'''

import traceback
import logging
import re

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

from models import Hit, Version

from utils import get_agent, get_agent_version, get_client_IP
from utils import get_java_vendor, get_java_version
from utils import get_python_version, get_python_compiler, get_python_build
from utils import get_os_name, get_os_arch, get_os_version

logger = logging.getLogger(__name__)


def hit(request):
    # registry accept request GET or POST
    req = request.GET or request.POST

    # check Agent: HTTP_USER_AGENT
    agent = get_agent(request)
    if not agent:
        return HttpResponseRedirect(settings.UPGRADE_CHECK_URL)

    # create Hit
    hit = Hit(agent=agent)

    # check AgentVersion
    agent_version = req.get('version', None)
    ver = Version.objects.get(pk=1)
    update = ('Please upgrade to %s, see %s for the latest '
              'version.' % (ver, settings.DOWNLOAD_PAGE))
    if agent_version:
        agent_version = get_agent_version(agent_version)
        hit.agentversion = agent_version

        # check if upgrade needed
        try:
            if agent_version is not None:
                try:
                    regex = re.compile(
                        "^.*?[-]?(\\d+[.]\\d+([.]\\d+)?)[-]?.*?$"
                    )

                    agent_cleaned = regex.match(agent_version.version).group(1)
                    agent_split = agent_cleaned.split(".")

                    local_cleaned = regex.match(ver.version).group(1)
                    local_split = local_cleaned.split(".")

                    rv = (agent_split < local_split)
                except:
                    rv = True
                if not rv:
                    update = None
            else:
                update = None
        except:
            logger.debug(traceback.format_exc())

    # check client IP
    hit.ip = get_client_IP(request)

    # check JavaVendor
    java_vendor = req.get('java.vm.vendor', None)
    if java_vendor:
        hit.javavendor = get_java_vendor(java_vendor)

    # check JavaVersion
    java_version = req.get('java.runtime.version', None)
    if java_version:
        hit.javaversion = get_java_version(java_version)

    # check PythonVersion
    python_version = req.get('python.version', None)
    if python_version:
        hit.pythonversion = get_python_version(python_version)

    # check PythonCompiler
    python_compiler = req.get('python.compiler', None)
    if python_compiler:
        hit.pythoncompiler = get_python_compiler(python_compiler)

    # check PythonBuild
    python_build = req.get('python.build', None)
    if python_build:
        hit.pythonbuild = get_python_build(python_build)

    # check OSName
    os_name = req.get('os.name', None)
    if os_name:
        hit.osname = get_os_name(os_name)

    # check OSArch
    os_arch = req.get('os.arch', None)
    if os_arch:
        hit.osarch = get_os_arch(os_arch)

    # check OSVersion
    os_version = req.get('os.version', None)
    if os_version:
        hit.osversion = get_os_version(os_version)

    try:
        hit.save()
        # hit.save(force_insert=True)
    except Exception, x:
        logger.debug(traceback.format_exc())
        HttpResponse(x)

    if update is not None:
        logger.debug("Update %s" % update)
        return HttpResponse(update)
    return HttpResponse()
