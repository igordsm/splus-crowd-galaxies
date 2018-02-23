from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    completed_tutorial = models.BooleanField('Fez tutorial', default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
    instance.profile.save()

class FITSRawImage(models.Model):
    fits_image = models.FileField('FITS image', upload_to='fits_images/')

class GalaxyImage(models.Model):
    original_fits_image = models.ForeignKey(FITSRawImage, null=True, blank=True)
    image = models.ImageField('Galaxy image', upload_to='galaxies/')
    description = models.TextField('Descrição')
    tutorial_image = models.BooleanField('Usar no tutorial', default=False)
    id_splus = models.BigIntegerField('ID splus')
    field_number = models.IntegerField('Campo', default=0)
    is_consensus = models.BooleanField('Consenso', default=False)

    coord_ra = models.CharField('RA', max_length=14, default='')
    coord_dec = models.CharField('DEC', max_length=14, default='')

    def __str__(self):
        return 'ID splus: %d, campo: %d'%(self.id_splus, self.field_number)

    @property
    def consensus_type(self):
        types = GalaxyClassification.objects.filter(image=self)
        counts = [types.filter(galaxy_type=t[0]).count() for t in GALAXY_TYPES]
        consensus_type = max(enumerate(counts))[1]
        return consensus_type
    
    @property
    def get_consensus_type_display(self):
        return GALAXY_TYPES[self.consensus_type][1]


GALAXY_TYPES = (
    (0, 'Espiral'),
    (10, 'Elíptica'),
    (20, 'Irregular'),
    (30, 'Outra')
)

class GalaxyClassification(models.Model):
    image = models.ForeignKey(GalaxyImage)
    user = models.ForeignKey(User)
    galaxy_type = models.IntegerField('Galaxy type', choices=GALAXY_TYPES)

    def __str__(self):
        return 'Classificação de %s por %s'%(self.image, self.user)

@receiver(post_save, sender=GalaxyClassification)
def galaxy_image_consensus(sender, **kwargs):

    image = kwargs['instance'].image
    image_classifications = GalaxyClassification.objects.filter(image=image)
    num = image_classifications.count()

    if num >= 10:
        # require at least 10 classifications to reach consensus
        probs = [
            image_classifications.filter(galaxy_type=t[0]).count() / num
            for t in GALAXY_TYPES
        ]
        print(probs, num)
        max_prob = max(probs)
        if max_prob >= 0.9:
            image.is_consensus = True
            image.save()
