from django.contrib import admin
from .models import (
    Person,
    Organization,
    ContactInfo,
    ActivityCode,
    SubactivityCode,
    QualificationCode,
    RegistriesApplication,
    ClassificationAppliedFor,
    RegistriesStatusCode,
    RegistriesRemovalReason,
    Register,
    ApplicationStatusCode,
    RegistriesApplicationStatus
)
from gwells.models.ProvinceStateCode import ProvinceStateCode

# Register your models here.

admin.site.register(Person)
admin.site.register(Organization)
admin.site.register(Register)
admin.site.register(RegistriesApplication)
admin.site.register(ClassificationAppliedFor)
admin.site.register(RegistriesApplicationStatus)
admin.site.register(ContactInfo)
admin.site.register(ActivityCode)
admin.site.register(SubactivityCode)
admin.site.register(QualificationCode)
admin.site.register(RegistriesStatusCode)
admin.site.register(RegistriesRemovalReason)
admin.site.register(ApplicationStatusCode)
admin.site.register(ProvinceStateCode)
