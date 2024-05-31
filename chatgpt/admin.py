from django.contrib import admin
from .models import ChromaData
from .views import view_all_data,delete_selected_view,add_texts_view, add_documents_view, upload_csv_view
from django.urls import path

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Register your models here.

from .models import History

admin.site.register(History)

@admin.register(ChromaData)
class ChromaDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    change_list_template = "admin/chroma_data_changelist.html"
    def changelist_view(self, request, extra_context=None):
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        database = Chroma(persist_directory="./database", embedding_function=embeddings)
        data = database.get()
        combined_data = list(zip(data['ids'], data['documents'], data['metadatas']))
        
        extra_context = extra_context or {}
        extra_context['combined_data'] = combined_data

        return super().changelist_view(request, extra_context=extra_context)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('delete-selected/', self.admin_site.admin_view(delete_selected_view), name='delete-selected'),
            path('add-texts/', self.admin_site.admin_view(add_texts_view), name='add-texts'),
            path('add-documents/', self.admin_site.admin_view(add_documents_view), name='add-documents'),
            path('upload-csv/', self.admin_site.admin_view(upload_csv_view), name='upload-csv'),
        ]
        return custom_urls + urls