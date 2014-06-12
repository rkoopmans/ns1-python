#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from nsone.rest.zones import Zones
from nsone.records import Record


class ZoneException(Exception):
    pass


class Zone(object):

    def __init__(self, config, zone):
        self._rest = Zones(config)
        self.config = config
        self.zone = zone
        self.data = None

    def load(self, callback=None):
        if self.data:
            raise ZoneException('zone already loaded')

        def success(result):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self
        return self._rest.retrieve(self.zone, callback=success)

    def delete(self, callback=None):
        def success(result):
            if callback:
                return callback(result)
        return self._rest.delete(self.zone, callback=callback)

    def create(self, refresh=None, retry=None, expiry=None, nx_ttl=None,
               callback=None):
        if self.data:
            raise ZoneException('zone already loaded')

        def success(result):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self
        return self._rest.create(self.zone, refresh, retry,
                                 expiry, nx_ttl, callback=success)

    def add_AAAA(self, domain, answers, callback=None):
        record = Record(self, domain, 'AAAA')
        return record.create(answers, callback=callback)

    def add_A(self, domain, answers, callback=None):
        record = Record(self, domain, 'A')
        return record.create(answers, callback=callback)

    def add_CNAME(self, domain, answers, callback=None):
        record = Record(self, domain, 'CNAME')
        return record.create(answers, callback=callback)

    def add_ALIAS(self, domain, answers, callback=None):
        record = Record(self, domain, 'ALIAS')
        return record.create(answers, callback=callback)