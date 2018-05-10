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
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Profile(models.Model):
    """
    Extended User Profile

    SMGOV_USERDISPLAYNAME: The display name of the user that can be displayed on web pages
    SMGOV_USEREMAIL: The email address of the user in local-part@domain format
    SMGOV_USERIDENTIFIER: A character string that uniquely identifies the user.   This is 
    typically a 32 character string consisting of hexadecimal characters but may be tailored 
    to the requirements of the relying party.

    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")

    profile_guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    smgov_useridentifier = models.UUIDField(blank=True, null=True)
    smgov_useremail = models.EmailField(unique=True, blank=True, null=True)
    smgov_userdisplayname = models.CharField(
        max_length=100, blank=True, null=True)
    realm = models.CharField(max_length=10, default="Django")
    name = models.CharField(max_length=100, blank=True, null=True)

    is_gwells_admin = models.BooleanField(default=False)

    class Meta:
        db_table = 'profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
