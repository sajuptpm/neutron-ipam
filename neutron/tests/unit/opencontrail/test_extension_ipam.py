# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Big Switch Networks, Inc.
# All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

# @author: Sumit Naiksatam, sumitnaiksatam@gmail.com, Big Switch Networks, Inc.

import copy

import mock
from webob import exc

from neutron.plugins.opencontrail.extensions import ipam
from neutron.openstack.common import uuidutils
from neutron.tests.unit import test_api_v2
from neutron.tests.unit import test_api_v2_extension


_uuid = uuidutils.generate_uuid
_get_path = test_api_v2._get_path


class IpamExtensionTestCase(test_api_v2_extension.ExtensionTestCase):
    fmt = 'json'

    def setUp(self):
        super(IpamExtensionTestCase, self).setUp()
        plural_mappings = {'ipam': 'ipams'}
        self._setUpExtension(
            'neutron.plugins.opencontrail.extensions.ipam.IpamPluginBase',
            None, ipam.RESOURCE_ATTRIBUTE_MAP,
            ipam.Ipam, 'neutron', plural_mappings=plural_mappings)

    def test_create_ipam(self):
        ipam_id = _uuid()
        data = {'ipam': {'name': 'ipam1',
                             'mgmt': {},
                             'tenant_id': _uuid()}}
        return_value = copy.copy(data['ipam'])
        return_value.update({'id': ipam_id})

        instance = self.plugin.return_value
        instance.create_ipam.return_value = return_value
        res = self.api.post(_get_path('ipams', fmt=self.fmt),
                            self.serialize(data),
                            content_type='application/%s' % self.fmt)
        instance.create_ipam.assert_called_with(mock.ANY,
                                                    ipam=data)
        self.assertEqual(res.status_int, exc.HTTPCreated.code)
        res = self.deserialize(res)
        self.assertIn('ipam', res)
        self.assertEqual(res['ipam'], return_value)

    def test_ipam_list(self):
        ipam_id = _uuid()
        return_value = [{'tenant_id': _uuid(),
                         'id': ipam_id}]

        instance = self.plugin.return_value
        instance.get_ipams.return_value = return_value

        res = self.api.get(_get_path('ipams', fmt=self.fmt))

        instance.get_ipams.assert_called_with(mock.ANY,
                                              fields=mock.ANY,
                                              filters=mock.ANY)
        self.assertEqual(res.status_int, exc.HTTPOk.code)

    def test_ipam_get(self):
        ipam_id = _uuid()
        return_value = {'tenant_id': _uuid(),
                        'id': ipam_id}

        instance = self.plugin.return_value
        instance.get_ipam.return_value = return_value

        res = self.api.get(_get_path('ipams',
                                     id=ipam_id, fmt=self.fmt))

        instance.get_ipam.assert_called_with(mock.ANY,
                                             ipam_id,
                                             fields=mock.ANY)
        self.assertEqual(res.status_int, exc.HTTPOk.code)
        res = self.deserialize(res)
        self.assertIn('ipam', res)
        self.assertEqual(res['ipam'], return_value)

    def test_ipam_update(self):
        ipam_id = _uuid()
        update_data = {'ipam': {'mgmt': ''}}
        return_value = {'tenant_id': _uuid(),
                        'id': ipam_id}

        instance = self.plugin.return_value
        instance.update_ipam.return_value = return_value

        res = self.api.put(_get_path('ipams', id=ipam_id,
                                     fmt=self.fmt),
                           self.serialize(update_data))

        instance.update_ipam.assert_called_with(mock.ANY, ipam_id,
                                                ipam=update_data)
        self.assertEqual(res.status_int, exc.HTTPOk.code)
        res = self.deserialize(res)
        self.assertIn('ipam', res)
        self.assertEqual(res['ipam'], return_value)

    def test_ipam_delete(self):
        ipam_id = _uuid()
        res = self.api.delete(_get_path('ipams', id=ipam_id,
                                     fmt=self.fmt))
        delete_entity = getattr(self.plugin.return_value, "delete_" + 'ipam')
        delete_entity.assert_called_with(mock.ANY, ipam_id)
        self.assertEqual(res.status_int, exc.HTTPNoContent.code)
