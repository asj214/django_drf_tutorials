import json
from rest_framework.renderers import JSONRenderer


class BaseRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'result'
    pagination_object_label = 'results'
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

        elif is_dict and data.get('errors', None) is not None:
            return super(BaseRenderer, self).render(data)
        else:
            return json.dumps({
                self.object_label: data
            })