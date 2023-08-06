#!/bin/python

import unicodedata
import re
from prettytable import PrettyTable

# import BAC0

from .bacpoint import BACPoint


class ObjectVariableMounter(object):
    def __init__(self, parent):
        self._parent=parent

    def strip(self, text):
        try:
            text = str(text, 'utf-8')
        except:
            pass

        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
        return str(text)

    def normalize(self, text):
        try:
            text = self.strip(text)
            text = re.sub('[ ]+\'', '_', text)
            text = re.sub('[^0-9a-zA-Z_-]', '', text)
            return text
        finally:
            return text

    def mount(self, obj):
        try:
            tag=self.normalize(obj.name)
            if tag and not hasattr(self._parent, tag):
                setattr(self._parent, tag, obj)
        except:
            pass


class BACPoints(object):
    def __init__(self, points=None ):
        self._points=[]
        self._pointByName={}
        self._indexByName={}
        self.add(points)

    def add(self, points):
        if points is None:
            return

        if isinstance(points, BACPoints):
            points=[point for point in points._points]
        else:
            if type(points) != list:
                points=[points]

        for point in points:
            assert(isinstance(point, BACPoint))
            if self.getByName(point.name):
                continue

            index=len(self._points)
            point._index=index
            self._points.append(point)
            self._pointByName[point.name]=point
            self._indexByName[point.name]=index

    def __iadd__(self, point):
        self.add(point)
        return self

    @property
    def points(self, keys=None):
        return self._points

    def pointsMatching(self, keys=None):
        if self._points:
            return [p for p in self._points if p.match(keys)]

    def match(self, keys):
        return [p for p in self.points if p.match(keys)]

    def type(self, objectType):
        return [p for p in self.points if p.type==objectType]

    def analogInput(self, address):
        for p in self._points:
            if p.type=='analogInput' and p.address==address:
                return p

    def analogOutput(self, address):
        for p in self._points:
            if p.type=='analogOutput' and p.address==address:
                return p

    def binaryInput(self, address):
        for p in self._points:
            if p.type=='binaryInput' and p.address==address:
                return p

    def binaryOutput(self, address):
        for p in self._points:
            if p.type=='binaryOutput' and p.address==address:
                return p

    def analogValue(self, address):
        for p in self._points:
            if p.type=='analogValue' and p.address==address:
                return p

    def binaryValue(self, address):
        for p in self._points:
            if p.type=='binaryValue' and p.address==address:
                return p

    def multiStateValue(self, address):
        for p in self._points:
            if p.type=='multiStateValue' and p.address==address:
                return p

    def __repr__(self):
        return '<%s(%d points)>' % (self.__class__.__name__, len(self.points))

    def count(self):
        return len(self._points)

    def __len__(self):
        return self.count()

    def __iter__(self):
        return iter(self._points)

    def getByName(self, name):
        try:
            return self._pointByName[name]
        except:
            pass

    def getByIndex(self, index):
        try:
            return self._points[int(index)]
        except:
            pass

    def __getitem__(self, index):
        item=self.getByIndex(index) or self.getByName(index)
        if not item:
            try:
                item=self.match(index)[0]
            except:
                pass
        return item

    def index(self, name):
        try:
            return self._indexByName[name]
        except:
            pass

    def dump(self, keys=None):
        if type(keys) is list:
            points=keys
        else:
            points=self.pointsMatching(keys)
        if points:
            t=PrettyTable()
            t.field_names=['#', 'name', 'description', 'type', 'address', 'value', 'label', 'unit', 'COV', 'OoS']
            t.align['name']='l'
            t.align['description']='l'
            t.align['type']='l'
            t.align['address']='r'
            t.align['value']='r'
            t.align['label']='l'
            t.align['unit']='l'
            t.align['prio']='l'
            for p in points:
                unit=p.unit
                if p.digUnitStr():
                    unit=p.digUnitStr()
                t.add_row([self.index(p.name),
                           p.name,
                           p.description,   # generate traffic the first time
                           p.type, p.address,
                           p.value,
                           p.label, # FIXME: traffic
                           unit,
                           p.isCOV(), p.isOutOfService()])
            print(t)

    def refresh(self, keys=None):
        points=self.match(keys)
        if self._points:
            for p in points:
                p.refresh()

    def cov(self, ttl=300):
        if self._points:
            for p in self._points:
                p.cov(ttl)

    def covCancel(self):
        if self._points:
            for p in self._points:
                p.covCancel()

    def poll(self, delay=15):
        """Register a polling task for each point. Better do it directly on the device (and not on each device's points)"""
        for point in self._points:
            point.pollStop()
            point.poll(delay)

    def pollStop(self):
        """Unregister polling task on each point"""
        for point in self._points:
            point.pollStop()

    def mountPointNamesAsVariables(self):
        """Create object variables mapped to each corresponding point's name"""
        mounter=ObjectVariableMounter(self)
        for point in self.points:
            mounter.mount(point)

    def relinquishAll(self):
        """Reset priority array of each writable objects"""
        for point in self.points:
            if point.isWritable():
                point.relinquishAll()


class BACBag(BACPoints):
    def __init__(self, device, points=None):
        # assert(isinstance(BACDevice, device))
        self._device=device
        super().__init__(points=points)

    def __repr__(self):
        return '<%s[%s](%d points)>' % (self.__class__.__name__, self.device.name,
            len(self._points))

    @property
    def device(self):
        return self._device


if __name__ == "__main__":
    pass
