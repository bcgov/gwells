from django.views import generic

from ..models import *

from ..settings import *

from ..minioClient import MinioClient

class WellDetailView(generic.DetailView):
    model = Well
    context_object_name = 'well'
    template_name = 'gwells/well_detail.html'

    def get_context_data(self, **kwargs):
        """
        Return the context for the well details page.
        """

        context = super(WellDetailView, self).get_context_data(**kwargs)
        surveys = Survey.objects.order_by('create_date')
        context['surveys'] = surveys
        context['page'] = 'w'

        if ENABLE_ADDITIONAL_DOCUMENTS:
            #Generic error Handling for now
            try:

                minio_client = MinioClient()

                context['host'] = minio_client.host;
                context['documents'] = [];

                documents = minio_client.get_documents(context['well'].well_tag_number)

                for doc in documents :
                    document = {}
                    document['bucket_name'] = doc.bucket_name
                    object_name = doc.object_name;
                    document['object_name'] = object_name.replace(' ', '+')
                    document['display_name'] = object_name[ object_name.find('/')+1 : object_name.find('/') + 1 + len(object_name)]
                    context['documents'].append(document)
                    context['documents'] = sorted(context['documents'], key=lambda k: k['display_name'])
            except Exception as exception:
                context['file_client_error'] = 'Error retrieving documents.'
                print("Document access exception: " + str(exception))
        return context
