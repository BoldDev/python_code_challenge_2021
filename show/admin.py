from django.contrib import admin

# Register your models here.
from show.models import Show, Season, Episode


# class SeasonInline(admin.StackedInline):
#     model = Season
#     extra = 0


class EpisodeInline(admin.StackedInline):
    model = Episode
    extra = 0


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    pass
    # inlines = [SeasonInline]


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    inlines = [EpisodeInline]


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    pass
