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

import platform

from django.test import TestCase
from django.core.urlresolvers import reverse

from django.test.client import RequestFactory

from views import hit as views_hit
from models import Agent, Hit, Version


def getOSVersion():
    try:
        if len(platform.mac_ver()[0]) > 0:
            version = "%s;%s" % (platform.platform(),
                                 platform.mac_ver()[0])
        else:
            version = platform.platform()
    except:
        version = platform.platform()
    return version


class RegistryTestCase(TestCase):

    def setUp(self):
        Version.objects.create(version="1.2.3")
        Agent.objects.create(agent_name="OMERO.test",
                             display_name="OMERO.test")
        Agent.objects.create(agent_name="OMERO.insight",
                             display_name="OMERO.insight")
        Agent.objects.create(agent_name="OMERO.web",
                             display_name="OMERO.web")
        self.factory = RequestFactory()

    def test_empty_hit(self):
        count_before = Hit.objects.all().count()

        hit_url = reverse('registry_hit')

        response = self.client.get(hit_url)
        self.assertEqual(response.status_code, 302)

        count_after = Hit.objects.all().count()

        # check if nothing was created
        self.assertEqual(count_before, count_after)

    def test_bad_agent(self):
        count_before = Hit.objects.all().count()

        hit_url = reverse('registry_hit')

        request = self.factory.get(hit_url, HTTP_USER_AGENT='foo')
        response = views_hit(request)
        self.assertEqual(response.status_code, 302)

        count_after = Hit.objects.all().count()

        # check if nothing was created
        self.assertEqual(count_before, count_after)

        # check if nothing was created
        try:
            Hit.objects.get(agent__agent_name='foo')
        except Hit.DoesNotExist:
            pass

    def test_old_version(self):
        count_before = Hit.objects.all().count()

        ver = Version.objects.get(pk=1)
        data = {}
        data["version"] = '0.0.0'

        hit_url = reverse('registry_hit')

        request = self.factory.get(hit_url, data,
                                   HTTP_USER_AGENT='OMERO.test',
                                   HTTP_X_FORWARDED_FOR='1.2.3.4')

        response = views_hit(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            str(('Please upgrade to %s, see '
                 'http://downloads.openmicroscopy.org/latest-stable/omero'
                 ' for the latest version.') % ver.version))

        hit = Hit.objects.get(agentversion__version=data["version"])
        self.assertEqual(hit.agent.agent_name, 'OMERO.test')
        self.assertEqual(hit.ip.ip, '1.2.3.4')

        count_after = Hit.objects.all().count()
        # check if nothing was created
        self.assertEqual(count_before+1, count_after)

    def test_current_version(self):
        count_before = Hit.objects.all().count()

        ver = Version.objects.get(pk=1)
        data = {}
        data["version"] = ver.version

        hit_url = reverse('registry_hit')

        request = self.factory.get(hit_url, data,
                                   HTTP_USER_AGENT='OMERO.test',
                                   HTTP_X_FORWARDED_FOR='1.2.3.4')

        response = views_hit(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '')

        hit = Hit.objects.get(agentversion__version=data["version"])
        self.assertEqual(hit.agent.agent_name, 'OMERO.test')
        self.assertEqual(hit.ip.ip, '1.2.3.4')

        count_after = Hit.objects.all().count()
        # check if nothing was created
        self.assertEqual(count_before+1, count_after)

    def test_java_client(self):
        count_before = Hit.objects.all().count()

        ver = Version.objects.get(pk=1)
        data = {}
        data["version"] = ver.version
        data["os.name"] = platform.system()
        data["os.arch"] = platform.machine()
        data["os.version"] = getOSVersion()
        data["java.vm.vendor"] = "Java vendor"
        data["java.runtime.version"] = "Java version"

        hit_url = reverse('registry_hit')

        request = self.factory.get(hit_url, data,
                                   HTTP_USER_AGENT='OMERO.insight',
                                   HTTP_X_FORWARDED_FOR='1.2.3.4')

        response = views_hit(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '')

        hit = Hit.objects.get(agentversion__version=data["version"])
        self.assertEqual(hit.ip.ip, '1.2.3.4')

        self.assertEqual(hit.agent.agent_name, 'OMERO.insight')
        self.assertEqual(hit.osname.name, data["os.name"])
        self.assertEqual(hit.osarch.name, data["os.arch"])
        self.assertEqual(hit.osversion.version, data["os.version"])
        self.assertEqual(hit.javavendor.name, data["java.vm.vendor"])
        self.assertEqual(hit.javaversion.version,
                         data["java.runtime.version"])

        self.assertEqual(hit.pythonversion, None)
        self.assertEqual(hit.pythoncompiler, None)
        self.assertEqual(hit.pythonbuild, None)

        count_after = Hit.objects.all().count()
        # check if nothing was created
        self.assertEqual(count_before+1, count_after)

    def test_python_client(self):
        count_before = Hit.objects.all().count()

        ver = Version.objects.get(pk=1)
        data = {}
        data["version"] = ver.version
        data["os.name"] = platform.system()
        data["os.arch"] = platform.machine()
        data["os.version"] = getOSVersion()
        data["python.version"] = platform.python_version()
        data["python.compiler"] = platform.python_compiler()
        data["python.build"] = platform.python_build()

        hit_url = reverse('registry_hit')

        request = self.factory.get(hit_url, data,
                                   HTTP_USER_AGENT='OMERO.web',
                                   HTTP_X_FORWARDED_FOR='1.2.3.4')

        response = views_hit(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '')

        hit = Hit.objects.get(agentversion__version=data["version"])
        self.assertEqual(hit.ip.ip, '1.2.3.4')

        self.assertEqual(hit.agent.agent_name, 'OMERO.web')
        self.assertEqual(hit.osname.name, data["os.name"])
        self.assertEqual(hit.osarch.name, data["os.arch"])
        self.assertEqual(hit.osversion.version, data["os.version"])
        self.assertEqual(hit.pythonversion.version, data["python.version"])
        self.assertEqual(hit.pythoncompiler.name, data["python.compiler"])
        self.assertEqual(hit.pythonbuild.name, data["python.build"][1])

        self.assertEqual(hit.javavendor, None)
        self.assertEqual(hit.javaversion, None)

        count_after = Hit.objects.all().count()
        # check if nothing was created
        self.assertEqual(count_before+1, count_after)

    def test_HTTP_X_FORWARDED_FOR(self):
        count_before = Hit.objects.all().count()

        ver = Version.objects.get(pk=1)
        data = {}
        data["version"] = ver.version

        hit_url = reverse('registry_hit')

        # HTTP_X_FORWARDED_FOR coma separated list
        request = self.factory.get(hit_url, data,
                                   HTTP_USER_AGENT='OMERO.test',
                                   HTTP_X_FORWARDED_FOR=(
                                       '1.2.3.4,10.20.30.40,11.22.33.44'
                                   ))

        response = views_hit(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '')

        hit = Hit.objects.get(agentversion__version=data["version"])
        self.assertEqual(hit.agent.agent_name, 'OMERO.test')
        self.assertEqual(hit.ip.ip, '11.22.33.44')

        count_after = Hit.objects.all().count()
        # check if nothing was created
        self.assertEqual(count_before+1, count_after)

    def test_no_ip(self):
        count_before = Hit.objects.all().count()

        ver = Version.objects.get(pk=1)
        data = {}
        data["version"] = ver.version

        hit_url = reverse('registry_hit')

        # REMOTE_ADDR empty
        request = self.factory.get(hit_url, data,
                                   HTTP_USER_AGENT='OMERO.test',
                                   HTTP_X_FORWARDED_FOR=None,
                                   REMOTE_ADDR=None)

        response = views_hit(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '')

        hit = Hit.objects.get(agentversion__version=data["version"])
        self.assertEqual(hit.agent.agent_name, 'OMERO.test')
        self.assertEqual(hit.ip, None)

        count_after = Hit.objects.all().count()
        # check if nothing was created
        self.assertEqual(count_before+1, count_after)
