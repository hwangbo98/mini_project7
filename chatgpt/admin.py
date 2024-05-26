from django.contrib import admin
from .models import ChromaData
from .views import view_all_data
from django.urls import path
# Register your models here.

class ChromaDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    change_list_template = "admin/chroma_data_changelist.html"  #

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('view-all/', self.admin_site.admin_view(view_all_data), name='view-all'),
        ]
        return custom_urls + urls

admin.site.register(ChromaData, ChromaDataAdmin)