"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
# Don't split all the model classes into seperate files (see The Zen of Python: "Flat is better than nested.")
# If you are going to do it, adhere to the standards:
# See: https://docs.djangoproject.com/en/2.0/topics/db/models/#organizing-models-in-a-package
# See: https://www.python.org/dev/peps/pep-0008/#package-and-module-names
import uuid

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from .common import AuditModel, ProvinceStateCode, CodeTableModel, BasicCodeTableModel
from .screen import ScreenIntakeMethodCode, ScreenMaterialCode, ScreenOpeningCode, ScreenBottomCode,\
    ScreenTypeCode, ScreenAssemblyTypeCode
from .survey import Survey, OnlineSurvey


class Profile(models.Model):
    """
    Extended User Profile
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    profile_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'profile'


class Border(models.Model):
    se_a_c_flg = models.CharField(max_length=254)
    obejctid = models.FloatField()
    shape = models.FloatField()
    length_m = models.FloatField()
    oic_number = models.CharField(max_length=7)
    area_sqm = models.FloatField()
    upt_date = models.CharField(max_length=20)
    upt_type = models.CharField(max_length=50)
    chng_org = models.CharField(max_length=30)
    aa_parent = models.CharField(max_length=100)
    aa_type = models.CharField(max_length=50)
    aa_id = models.BigIntegerField()
    aa_name = models.CharField(max_length=100)
    abrvn = models.CharField(max_length=40)
    bdy_type = models.CharField(max_length=20)
    oic_year = models.CharField(max_length=4)
    afctd_area = models.CharField(max_length=120)
    geom = models.MultiPolygonField(srid=4269)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
