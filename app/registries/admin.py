from django.contrib import admin
from .models import (
    Person,
    ContactInfo,
    Organization,
    ActivityCode,
    AccreditedCertificateCode,
    CertifyingAuthorityCode,
    SubactivityCode,
    RegistriesApplication,
    RegistriesStatusCode,
    RegistriesRemovalReason,
    Register,
    ApplicationStatusCode,
    WellClassCode,
    Qualification,
    PersonNote,
    OrganizationNote
)

# Register your models here.

admin.site.register(AccreditedCertificateCode)
admin.site.register(CertifyingAuthorityCode)
admin.site.register(ContactInfo)
admin.site.register(Person)
admin.site.register(Organization)
admin.site.register(ActivityCode)
admin.site.register(SubactivityCode)
admin.site.register(RegistriesApplication)
admin.site.register(RegistriesStatusCode)
admin.site.register(RegistriesRemovalReason)
admin.site.register(Register)
admin.site.register(ApplicationStatusCode)
admin.site.register(WellClassCode)
admin.site.register(Qualification)
admin.site.register(PersonNote)
admin.site.register(OrganizationNote)
