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
from gwells.roles import WELLS_VIEWER_ROLE, WELLS_EDIT_ROLE, WELLS_SUBMISSION_ROLE, WELLS_SUBMISSION_VIEWER_ROLE


class WellsEditOrReadOnly(BasePermission):
    """
    Allows read-only access to all users (including anonymous users) and write access to users with
    edit rights.
    """
    def has_permission(self, request, view):
        has_edit = request.user and request.user.is_authenticated and request.user.groups.filter(
            name=WELLS_EDIT_ROLE).exists()
        result = has_edit or request.method in SAFE_METHODS
        return result


class WellsDocumentViewPermissions(BasePermission):
    """
    Grants permission to view documents to users with the wells viewer role.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and\
            request.user.groups.filter(name=WELLS_VIEWER_ROLE).exists()


class WellsEditPermissions(BasePermission):
    """
    Grants permissions to edit wells to users
    """

    def has_permission(self, request, view):
        """
        Refuse permission if user is not in an edit group.
        If user is in the edit group, then group permissions will dictate (e.g. user is
        in a group that has 'add_well' permission)
        """
        return request.user and request.user.is_authenticated and\
            request.user.groups.filter(name=WELLS_EDIT_ROLE).exists()


class WellsSubmissionPermissions(BasePermission):
    """
    Grants permissions to well submissions to users
    """

    def has_permission(self, request, view):
        """
        Refuse permission if user is not in a submission group.
        If user is in the submission group, then group permissions will dictate (e.g. user is
        in a group that has 'wells_submission' permission)
        """
        return request.user and request.user.is_authenticated and\
            request.user.groups.filter(name=WELLS_SUBMISSION_ROLE).exists()


class WellsSubmissionViewerPermissions(BasePermission):
    """
    Grants permissions to view well submissions to users
    """

    def has_permission(self, request, view):
        """
        Refuse permission if user is not in a submission_viewer group.
        If user is in the submission_viewer group, then group permissions will dictate (e.g. user is
        in a group that has 'wells_submission_viewer' permission)
        """
        return request.user and request.user.is_authenticated and\
            request.user.groups.filter(name=WELLS_SUBMISSION_VIEWER_ROLE).exists()
