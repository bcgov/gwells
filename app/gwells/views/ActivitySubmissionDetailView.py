from django.views import generic
from ..models import ActivitySubmission

class ActivitySubmissionDetailView(generic.DetailView):
    model = ActivitySubmission
    context_object_name = 'activity_submission'
    template_name = 'gwells/activity_submission_detail.html'

    def get_context_data(self, **kwargs):
        """
        Return the context for the page.
        """
        context = super(ActivitySubmissionDetailView, self).get_context_data(**kwargs)
        return context
