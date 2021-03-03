from django.db import connection
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from configs.utils import (
    fetchone,
    fetchall,
)
from configs.redis_connect import r
from apps.serializers import ArticleSerializer


class RedisView(APIView):
    permission_classes = (AllowAny,)

    key = 'user:actions:likes'
    count_key = 'user:actions:likes_cnt'
    hkey = 'user:info'
    hmkey = 'user:info:all'

    def get_keys(self, user_id):
        return {
            'key': '{0}:{1}'.format(self.key, user_id),
            'count_key': '{0}:{1}'.format(self.count_key, user_id),
            'hkey': '{0}:{1}'.format(self.hkey, user_id),
            'hmkey': '{0}:{1}'.format(self.hmkey, user_id),
        }

    def post(self, request):

        user_id = request.data.get('user_id', 1)
        keys = self.get_keys(user_id)
        key = keys.get('key')
        count_key = keys.get('count_key')
        hkey = keys.get('hkey')
        hmkey = keys.get('hmkey')

        # list
        if r.exists(key):
            r.delete(key)

        if not r.exists(count_key):
            r.set(count_key, 0)

        for i in range(10):
            r.lpush(key, i)
            r.incr(count_key)

        # hash
        r.hset(hkey, 'id', 1)
        r.hset(hkey, 'name', 'sjahn')
        r.hset(hkey, 'email', 'sjahn@ktown4u.com')

        # all
        r.hmset(hmkey, {'id': 1, 'name': 'sjahn', 'email': 'sjahn@ktown4u.com'})

        res = {
            key: r.lrange(key, 0, r.llen(key)),
            count_key: r.get(count_key),
            hkey: {
                'part': {
                    'id': r.hget(hkey, 'id'),
                    'name': r.hget(hkey, 'name'),
                    'email': r.hget(hkey, 'email'),
                },
                'all': r.hgetall(hkey)
            },
            hmkey: r.hgetall(hmkey)
        }

        return Response(res)

    def delete(self, request):

        user_id = request.data.get('user_id', 1)
        units = self.get_keys(user_id)

        for key, value in units.items():
            if r.exists(value):
                r.delete(value)

        return Response(status=status.HTTP_204_NO_CONTENT)
