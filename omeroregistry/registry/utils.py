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

import logging
import traceback

from models import IP, Agent, AgentVersion
from models import OSName, OSArch, OSVersion
from models import JavaVendor, JavaVersion
from models import PythonVersion, PythonCompiler, PythonBuild

logger = logging.getLogger(__name__)


def get_client_IP(request):
    ip = None
    try:
        real_ip = None
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
            logger.debug("request.META['HTTP_X_FORWARDED_FOR']: %s" % real_ip)
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.
            if real_ip:
                real_ip = real_ip.split(",")[-1].strip()
        except KeyError:
            real_ip = request.META.get('REMOTE_ADDR')
            logger.debug("request.META['REMOTE_ADDR']: %s" % real_ip)

        if real_ip:
            try:
                ip = IP.objects.get(ip=real_ip)
            except IP.DoesNotExist:
                ip = IP.objects.create(ip=real_ip)
        else:
            logger.error("No IP ???")
    except Exception:
        logger.debug(traceback.format_exc())
    return ip


def get_agent(request):
    agent = None
    try:
        user_agent = request.META.get('HTTP_USER_AGENT', None)
        logger.debug("HTTP_USER_AGENT '%s'" % user_agent)
        if user_agent and user_agent.startswith("OMERO."):
            try:
                agent = Agent.objects.get(agent_name=user_agent)
                logger.debug("Agent '%s'" % agent)
            except Agent.DoesNotExist:
                logger.debug("Agent '%s' does not exist" % agent)
            except:
                logger.error(traceback.format_exc())
        else:
            logger.debug("'%s' is not OMERO agent" % user_agent)
    except:
        logger.error(traceback.format_exc())
    return agent


def get_agent_version(agent_version):
    try:
        av = AgentVersion.objects.get(version=agent_version)
    except AgentVersion.DoesNotExist:
        av = AgentVersion.objects.create(version=agent_version)
    logger.debug("Agent version %s" % av)
    return av


def get_java_vendor(java_vendor):
    try:
        jv = JavaVendor.objects.get(name=java_vendor)
    except JavaVendor.DoesNotExist:
        jv = JavaVendor.objects.create(name=java_vendor)
    logger.debug("Java vendor %s" % jv)
    return jv


def get_java_version(java_version):
    try:
        jv = JavaVersion.objects.get(version=java_version)
    except JavaVersion.DoesNotExist:
        jv = JavaVersion.objects.create(version=java_version)
    logger.debug("Java version %s" % jv)
    return jv


def get_python_version(python_version):
    try:
        pv = PythonVersion.objects.get(version=python_version)
    except PythonVersion.DoesNotExist:
        pv = PythonVersion.objects.create(version=python_version)
    logger.debug("Python version %s" % pv)
    return pv


def get_python_compiler(python_compiler):
    try:
        pc = PythonCompiler.objects.get(name=python_compiler)
    except PythonCompiler.DoesNotExist:
        pc = PythonCompiler.objects.create(name=python_compiler)
    logger.debug("Python compiler %s" % pc)
    return pc


def get_python_build(python_build):
    try:
        pb = PythonBuild.objects.get(name=python_build)
    except PythonBuild.DoesNotExist:
        pb = PythonBuild.objects.create(name=python_build)
    logger.debug("Python build %s" % pb)
    return pb


def get_os_name(os_name):
    try:
        osn = OSName.objects.get(name=os_name)
    except OSName.DoesNotExist:
        osn = OSName.objects.create(name=os_name)
    logger.debug("OS name %s" % osn)
    return osn


def get_os_arch(os_arch):
    try:
        osa = OSArch.objects.get(name=os_arch)
    except OSArch.DoesNotExist:
        osa = OSArch.objects.create(name=os_arch)
    logger.debug("OS arch %s" % osa)
    return osa


def get_os_version(os_version):
    try:
        osv = OSVersion.objects.get(version=os_version)
    except OSVersion.DoesNotExist:
        osv = OSVersion.objects.create(version=os_version)
    logger.debug("OS version %s" % os_version)
    return osv
