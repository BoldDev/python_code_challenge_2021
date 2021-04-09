from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.cache import SimpleCache
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.fields import ForeignKey
from tastypie.resources import ModelResource

from show.models import Episode, Season, Comment


class SeasonResource(ModelResource):
    class Meta:
        queryset = Season.objects.all()
        resource_name = 'episode'
        allowed_methods = ['get']
        filtering = {
            'number': ('exact')
        }
        cache = SimpleCache(cache_name='resources', timeout=10)


class EpisodeResource(ModelResource):
    season = ForeignKey(SeasonResource, 'season')

    class Meta:
        queryset = Episode.objects.all()
        resource_name = 'episode'
        allowed_methods = ['get']
        filtering = {
            'season': ALL_WITH_RELATIONS,
            'id': ALL
        }
        cache = SimpleCache(cache_name='resources', timeout=10)


class CommentResource(ModelResource):
    episode = ForeignKey(EpisodeResource, 'episode')

    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        allowed_methods = ['get', 'post', 'patch', 'delete']
        authentication = Authentication()
        authorization = Authorization()
        filtering = {
            'episode': ('exact')
        }
        cache = SimpleCache(cache_name='resources', timeout=10)
