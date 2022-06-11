from django.contrib import admin

from .models import *


class TourImageAdmin(admin.StackedInline):
    model = TourImage
    max_num = 7


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    inlines = [TourImageAdmin]


admin.site.register(Rating)
admin.site.register(Saved)
admin.site.register(Comment)