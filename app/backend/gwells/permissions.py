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
from rest_framework.permissions import BasePermission, SAFE_METHODS
from gwells.roles import (
    SURVEYS_EDIT_ROLE,
    BULK_WELL_AQUIFER_CORRELATION_UPLOAD,
    BULK_AQUIFER_DOCUMENTS_UPLOAD,
    BULK_VERTICAL_AQUIFER_EXTENTS_UPLOAD
)



class ReadOnlyPermission(BasePermission):
    """
    Allows read-only access to all users (including anonymous users) and write access to users with
    edit rights.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class SurveysEditOrReadOnly(BasePermission):
    """
    Allows read-only access to all users (including anonymous users) and write access to users with
    edit rights for surveys (SSO role: surveys_edit).
    """

    def has_permission(self, request, view):
        has_edit = request.user and request.user.is_authenticated and request.user.groups.filter(
            name=SURVEYS_EDIT_ROLE).exists()
        result = has_edit or request.method in SAFE_METHODS
        return result


class HasBulkWellAquiferCorrelationUploadRole(BasePermission):
    """
    Grants permission to users with bulk_well_aquifer_correlation_upload
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name=BULK_WELL_AQUIFER_CORRELATION_UPLOAD).exists()
        )


class HasBulkAquiferDocumentsUploadRole(BasePermission):
    """
    Grants permission to users with bulk_aquifer_documents_upload
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name=BULK_AQUIFER_DOCUMENTS_UPLOAD).exists()
        )


class HasBulkVerticalAquiferExtentsUploadRole(BasePermission):
    """
    Grants permission to users with bulk_vertical_aquifer_extents_upload
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name=BULK_VERTICAL_AQUIFER_EXTENTS_UPLOAD).exists()
        )
