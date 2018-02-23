from django.test import TestCase
from unittest.mock import MagicMock
from django.core.files import File
# Create your tests here.

from .models import GalaxyClassification, GalaxyImage
from django.contrib.auth.models import User

class GalaxyClassificationAndImageTest(TestCase):

    def test_reach_consensus_with_10_equal_classifications(self):
        user = User.objects.create_user('test')
        user.save()

        mock_png = MagicMock(spec=File, name='FileMock')
        mock_png.name = 'mock.png'
        image = GalaxyImage(image=mock_png,
                            description='bla',
                            id_splus=10)
        image.save()

        for i in range(11):
            g = GalaxyClassification(image=image, user=user, galaxy_type=0)
            g.save()
        
        image = GalaxyImage.objects.get(id=image.id)
        self.assertTrue(image.is_consensus)

    def test_reach_consensus_with_90_percent(self):
        user = User.objects.create_user('test')
        user.save()

        mock_png = MagicMock(spec=File, name='FileMock')
        mock_png.name = 'mock.png'
        image = GalaxyImage(image=mock_png,
                            description='bla',
                            id_splus=10)
        image.save()

        for i in range(9):
            g = GalaxyClassification(image=image, user=user, galaxy_type=20)
            g.save()
        g = GalaxyClassification(image=image, user=user, galaxy_type=10)
        g.save()
        
        image = GalaxyImage.objects.get(id=image.id)
        self.assertTrue(image.is_consensus)

    def test_does_notreach_consensus_with_less_90_percent(self):
        user = User.objects.create_user('test')
        user.save()

        mock_png = MagicMock(spec=File, name='FileMock')
        mock_png.name = 'mock.png'
        image = GalaxyImage(image=mock_png,
                            description='bla',
                            id_splus=10)
        image.save()

        for i in range(7):
            g = GalaxyClassification(image=image, user=user, galaxy_type=30)
            g.save()
        for i in range(4):
            g = GalaxyClassification(image=image, user=user, galaxy_type=10)
            g.save()
        
        image = GalaxyImage.objects.get(id=image.id)
        self.assertFalse(image.is_consensus)

def test_does_notreach_consensus_with_less_9_classifications(self):
        user = User.objects.create_user('test')
        user.save()

        mock_png = MagicMock(spec=File, name='FileMock')
        mock_png.name = 'mock.png'
        image = GalaxyImage(image=mock_png,
                            description='bla',
                            id_splus=10)
        image.save()

        for i in range(9):
            g = GalaxyClassification(image=image, user=user, galaxy_type=30)
            g.save()
        
        image = GalaxyImage.objects.get(id=image.id)
        self.assertFalse(image.is_consensus)