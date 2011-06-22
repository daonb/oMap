import re

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import *
from django.contrib.auth.models import User, AnonymousUser
from django import template
#from knesset.mks.server_urls import mock_pingback_server
from django.utils import simplejson as json

from models import Layer, Point

just_id = lambda x: x.id

class ViewsTest(TestCase):

    def setUp(self):
        self.jacob = User.objects.create_user('jacob', 'jacob@jacob.org',
                                              'JKM')
        self.layer = Layer.objects.create(name='layer 1', owner=self.jacob)
        self.p1 = Point.objects.create(user = self.jacob, layer = self.layer, 
                        point = fromstr('POINT(31,31)', srid=4326), 
                        subject = 'p1', description= 'This is p1')
        self.p2 = Point.objects.create(user = self.jacob, layer = self.layer,
                        point = fromstr('POINT(32,32)', srid=4326), 
                        subject = 'p2', description= 'This is p2', views_count=4)
        
    def testMainView(self):
        res = self.client.get(reverse('map-home'))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'site/index.html')
        self.assertEqual(map(just_id, res.context['points']), 
                         [ self.p1.id, self.p2.id, ])
        self.assertEqual(map(just_id, res.context['most_recent']), 
                         [ self.p2.id, self.p1.id, ])
        self.assertEqual(map(just_id, res.context['hot_topics']), 
                         [ self.p2.id, self.p1.id])

    def tearDown(self):
        self.p1.delete()
        self.p2.delete()
        self.layer.delete()
        self.jacob.delete()
        
