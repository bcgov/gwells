from django.contrib import admin
from reversion.admin import VersionAdmin
from registries.models import (
    Person,
    ContactInfo,
    Organization,
    ActivityCode,
    AccreditedCertificateCode,
    CertifyingAuthorityCode,
    SubactivityCode,
    RegistriesApplication,
    RegistriesRemovalReason,
    Register,
    ApplicationStatusCode,
    WellClassCode,
    Qualification,
    PersonNote,
    OrganizationNote
)

# Register your models here.


class OrganizationModelAdmin(VersionAdmin):
    pass


class PersonModelAdmin(VersionAdmin):
    pass


class RegisterModelAdmin(VersionAdmin):
    pass


class RegistriesApplicationModelAdmin(VersionAdmin):
    pass


admin.site.register(AccreditedCertificateCode)
admin.site.register(CertifyingAuthorityCode)
admin.site.register(ContactInfo)
admin.site.register(Person, PersonModelAdmin)
admin.site.register(Organization, OrganizationModelAdmin)
admin.site.register(ActivityCode)
admin.site.register(SubactivityCode)
admin.site.register(RegistriesApplication, RegistriesApplicationModelAdmin)
admin.site.register(RegistriesRemovalReason)
admin.site.register(Register, RegisterModelAdmin)
admin.site.register(ApplicationStatusCode)
admin.site.register(WellClassCode)
admin.site.register(Qualification)
admin.site.register(PersonNote)
admin.site.register(OrganizationNote)
