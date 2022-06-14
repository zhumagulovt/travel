from django.contrib import admin

from .models import *


class TourImageAdmin(admin.StackedInline):
    model = TourImage
    max_num = 7


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'company', 'start_date', 'end_date']
    list_display_links = ['id', 'name']
    inlines = [TourImageAdmin]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'tour', 'user', 'rating']


admin.site.register(Saved)
admin.site.register(Comment)
admin.site.register(UserTourViewed)