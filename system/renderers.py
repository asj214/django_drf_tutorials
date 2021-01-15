import json
from rest_framework.renderers import JSONRenderer


class BaseRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    pagination_object_label = 'objects'
    pagination_object_count = 'count'

    def render(self, data, media_type=None, renderer_context=None):

        is_dict = isinstance(data, dict)

        if data is None:
            return None
        elif is_dict and data.get('results', None) is not None:
            return json.dumps({
                self.pagination_object_label: data['results'],
                self.pagination_count_label: data['count']
            })

        # If the view throws an error (such as the user can't be authenticated
        # or something similar), `data` will contain an `errors` key. We want
        # the default JSONRenderer to handle rendering errors, so we need to
        # check for this case.
        elif is_dict and data.get('errors', None) is not None:
            return super(BaseRenderer, self).render(data)
        else:
            return json.dumps({
                self.object_label: data
            })
