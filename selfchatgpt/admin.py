# from django.contrib import admin
# from django.urls import path
# from django.shortcuts import render, redirect
# import pandas as pd
# from .models import Document
# from .forms import CsvUploadForm
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.schema import Document as LangchainDocument
# import pandas as pd
# import numpy as np
# import os
# import sqlite3
# from datetime import datetime

# import openai

# from langchain.chat_models import ChatOpenAI
# from langchain.schema import HumanMessage, SystemMessage, Document
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.chains import RetrievalQA, ConversationalRetrievalChain
# from langchain.memory import ConversationBufferMemory

# from django.contrib import admin
# from django.urls import path
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# import pandas as pd
# from .models import Document
# from .forms import CsvUploadForm
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.schema import Document as LangchainDocument

# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ('page_content', 'category')
#     change_list_template = "admin/document_change_list.html"

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('upload-csv/', self.upload_csv, name='upload_csv'),
#             path('view-documents/', self.view_documents, name='view_documents'),
#         ]
#         return custom_urls + urls

#     def upload_csv(self, request):
#         if request.method == "POST":
#             csv_file = request.FILES["csv_file"]
#             if not csv_file.name.endswith('.csv'):
#                 self.message_user(request, "This is not a CSV file")
#                 return redirect("..")

#             df = pd.read_csv(csv_file)

#             embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
#             database = Chroma(persist_directory="./db_new", embedding_function=embeddings)
#             documents = [LangchainDocument(page_content=df['QA'][i], metadata={'category': df['구분'][i]}) for i in range(len(df))]
#             # database.add_documents(documents)
#             for doc in documents :
#                 results = database.similarity_search_with_score(doc, k=3)
#                 print(results)
#             for i in range(len(df)):
#                 Document.objects.create(
#                     page_content=df['QA'][i],
#                     category=df['구분'][i],
#                     vector=b''  # 벡터 데이터는 Chroma DB에 저장
#                 )

#             self.message_user(request, "Your csv file has been uploaded and processed")
#             return redirect("..")
#         form = CsvUploadForm()
#         payload = {"form": form}
#         return render(
#             request, "admin/csv_form.html", payload
#         )

#     def view_documents(self, request):
#         documents = Document.objects.all()
#         payload = {"documents": documents}
#         return render(
#             request, "admin/view_documents.html", payload
#         )

# admin.site.register(Document, DocumentAdmin)

# from django.contrib import admin
# from django.urls import path
# from django.shortcuts import render, redirect
# import pandas as pd
# from .models import Document
# from .forms import CsvUploadForm
# from langchain_openai import OpenAIEmbeddings  # 수정된 부분
# from langchain.vectorstores import Chroma
# from langchain.schema import Document as LangchainDocument
# import numpy as np

# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ('page_content', 'category')
#     change_list_template = "admin/document_change_list.html"

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('upload-csv/', self.upload_csv, name='upload_csv'),
#             path('view-documents/', self.view_documents, name='view_documents'),
#         ]
#         return custom_urls + urls

#     def upload_csv(self, request):
#         if request.method == "POST":
#             csv_file = request.FILES["csv_file"]
#             if not csv_file.name.endswith('.csv'):
#                 self.message_user(request, "This is not a CSV file")
#                 return redirect("..")

#             df = pd.read_csv(csv_file)

#             embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
#             database = Chroma(persist_directory="./db_new", embedding_function=embeddings)
#             new_documents = [LangchainDocument(page_content=df['QA'][i], metadata={'category': df['구분'][i]}) for i in range(len(df))]
#             new_vectors = [embeddings.embed_documents([doc.page_content])[0] for doc in new_documents]

#             unique_new_documents = []
#             for doc, vec in zip(new_documents, new_vectors):
#                 vec = np.array(vec)  # list를 numpy 배열로 변환
#                 query_embedding = vec.tolist()  # numpy 배열을 list로 변환
#                 try:
#                     results = database.similarity_search_with_score(doc, k=1)
#                     if not results or results[0][1] < 0.95:  # 유사도 임계값 0.95
#                         unique_new_documents.append(doc)
#                         Document.objects.create(
#                             page_content=doc.page_content,
#                             category=doc.metadata['category'],
#                             vector=vec.tobytes()
#                         )
#                 except Exception as e:  # 일반 예외 처리
#                     self.message_user(request, f"Error during similarity search: {e}")
#                     return redirect("..")

#             if unique_new_documents:
#                 database.add_documents(unique_new_documents)

#             self.message_user(request, "Your csv file has been uploaded and processed")
#             return redirect("..")
#         form = CsvUploadForm()
#         payload = {"form": form}
#         return render(
#             request, "admin/csv_form.html", payload
#         )

#     def view_documents(self, request):
#         documents = Document.objects.all()
#         payload = {"documents": documents}
#         return render(
#             request, "admin/view_documents.html", payload
#         )

# admin.site.register(Document, DocumentAdmin)
# from django.contrib import admin
# from django.urls import path
# from django.shortcuts import render, redirect
# import pandas as pd
# import numpy as np
# from .models import Document
# from .forms import CsvUploadForm
# from .utils import cosine_similarity
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.schema import Document as LangchainDocument

# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ('page_content', 'category')
#     change_list_template = "admin/document_change_list.html"

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('upload-csv/', self.upload_csv, name='upload_csv'),
#             path('view-documents/', self.view_documents, name='view_documents'),
#         ]
#         return custom_urls + urls

#     def upload_csv(self, request):
#         if request.method == "POST":
#             csv_file = request.FILES["csv_file"]
#             if not csv_file.name.endswith('.csv'):
#                 self.message_user(request, "This is not a CSV file")
#                 return redirect("..")

#             # 인코딩을 지정하여 CSV 파일을 읽습니다.
#             try:
#                 df = pd.read_csv(csv_file, encoding='utf-8')
#             except UnicodeDecodeError:
#                 try:
#                     df = pd.read_csv(csv_file, encoding='ISO-8859-1')
#                 except UnicodeDecodeError:
#                     df = pd.read_csv(csv_file, encoding='CP949')

#             embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
#             database = Chroma(persist_directory="./db_new", embedding_function=embeddings)
#             new_documents = [LangchainDocument(page_content=df['QA'][i], metadata={'category': df['구분'][i]}) for i in range(len(df))]
#             new_vectors = [embeddings.embed_documents([doc.page_content])[0] for doc in new_documents]

#             existing_documents = Document.objects.all()
#             existing_vectors = [np.frombuffer(doc.vector, dtype=np.float32) for doc in existing_documents]

#             unique_new_documents = []
#             for doc, vec in zip(new_documents, new_vectors):
#                 vec = np.array(vec)  # list를 numpy 배열로 변환
#                 for existing_vec in existing_vectors : 
#                     print(cosine_similarity(vec, existing_vec))
#                 if all(existing_vec.size > 0 and cosine_similarity(vec, existing_vec) < 0.95 for existing_vec in existing_vectors):  # 유사도 임계값 0.95
#                     # print(cosine_similarity(vec, existing_vec) < 0.95)
#                     unique_new_documents.append(doc)
#                     Document.objects.create(
#                         page_content=doc.page_content,
#                         category=doc.metadata['category'],
#                         vector=vec.tobytes()
#                     )

#             if unique_new_documents:
#                 database.add_documents(unique_new_documents)

#             self.message_user(request, "Your csv file has been uploaded and processed")
#             return redirect("..")
#         form = CsvUploadForm()
#         payload = {"form": form}
#         return render(
#             request, "admin/csv_form.html", payload
#         )

#     def view_documents(self, request):
#         documents = Document.objects.all()
#         payload = {"documents": documents}
#         return render(
#             request, "admin/view_documents.html", payload
#         )

# admin.site.register(Document, DocumentAdmin)


# from django.contrib import admin
# from django.urls import path
# from django.shortcuts import render, redirect
# import pandas as pd
# import numpy as np
# from .models import Document
# from .forms import CsvUploadForm
# from langchain_openai import OpenAIEmbeddings  # 수정된 부분
# from langchain.vectorstores import Chroma
# from langchain.schema import Document as LangchainDocument

# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ('page_content', 'category')
#     change_list_template = "admin/document_change_list.html"

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('upload-csv/', self.upload_csv, name='upload_csv'),
#             path('view-documents/', self.view_documents, name='view_documents'),
#         ]
#         return custom_urls + urls

#     def upload_csv(self, request):
#         if request.method == "POST":
#             csv_file = request.FILES["csv_file"]
#             if not csv_file.name.endswith('.csv'):
#                 self.message_user(request, "This is not a CSV file")
#                 return redirect("..")

#             # 인코딩을 지정하여 CSV 파일을 읽습니다.
#             try:
#                 df = pd.read_csv(csv_file, encoding='utf-8')
#             except UnicodeDecodeError:
#                 try:
#                     df = pd.read_csv(csv_file, encoding='ISO-8859-1')
#                 except UnicodeDecodeError:
#                     df = pd.read_csv(csv_file, encoding='CP949')

#             embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
#             database = Chroma(persist_directory="./db_new", embedding_function=embeddings)
#             new_documents = [LangchainDocument(page_content=df['QA'][i], metadata={'category': df['구분'][i]}) for i in range(len(df))]
#             new_vectors = [embeddings.embed_documents([doc.page_content])[0] for doc in new_documents]

#             unique_new_documents = []
#             for doc, vec in zip(new_documents, new_vectors):
#                 try:
#                     # similarity_search_with_score는 텍스트 쿼리를 기대하므로, 텍스트 쿼리를 함께 전달합니다.
#                     results = database.similarity_search_with_score(doc.page_content, k=1)
#                     print(results)
#                     if not results or results[0][1] < 0.8:  # 유사도 임계값 0.95
#                         unique_new_documents.append(doc)
#                         Document.objects.create(
#                             page_content=doc.page_content,
#                             category=doc.metadata['category'],
#                             vector=np.array(vec).tobytes()
#                         )
#                 except Exception as e:  # 일반 예외 처리
#                     self.message_user(request, f"Error during similarity search: {e}")
#                     return redirect("..")

#             if unique_new_documents:
#                 database.add_documents(unique_new_documents)

#             self.message_user(request, "Your csv file has been uploaded and processed")
#             return redirect("..")
#         form = CsvUploadForm()
#         payload = {"form": form}
#         return render(
#             request, "admin/csv_form.html", payload
#         )

#     def view_documents(self, request):
#         documents = Document.objects.all()
#         payload = {"documents": documents}
#         return render(
#             request, "admin/view_documents.html", payload
#         )

# admin.site.register(Document, DocumentAdmin)
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
import pandas as pd
import numpy as np
from .models import Document, Chatlog
from .forms import CsvUploadForm
from langchain_openai import OpenAIEmbeddings  # 수정된 부분
from langchain.vectorstores import Chroma
from langchain.schema import Document as LangchainDocument
@admin.register(Chatlog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'question', 'answer', 'ip')  # Admin 페이지에 표시할 필드
    search_fields = ('id', 'date', 'question', 'answer', 'ip')  # 검색 기능에 사용할 필드
    date_hierarchy = 'date'  # 날짜 계층 필터 추가
    list_filter = ('date',)  # 필터 기능에 사용할 필드

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('page_content', 'category')
    change_list_template = "admin/document_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv, name='upload_csv'),
            path('view-documents/', self.view_documents, name='view_documents'),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                self.message_user(request, "This is not a CSV file")
                return redirect("..")

            # 인코딩을 지정하여 CSV 파일을 읽습니다.
            try:
                df = pd.read_csv(csv_file, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    df = pd.read_csv(csv_file, encoding='ISO-8859-1')
                except UnicodeDecodeError:
                    df = pd.read_csv(csv_file, encoding='CP949')

            embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
            database = Chroma(persist_directory="./db_new", embedding_function=embeddings)
            new_documents = [LangchainDocument(page_content=df['QA'][i], metadata={'category': df['구분'][i]}) for i in range(len(df))]
            new_vectors = [embeddings.embed_documents([doc.page_content])[0] for doc in new_documents]

            unique_new_documents = []
            for doc, vec in zip(new_documents, new_vectors):
                try:
                    # similarity_search_with_score는 텍스트 쿼리를 기대하므로, 텍스트 쿼리를 함께 전달합니다.
                    results = database.similarity_search_with_score(doc.page_content, k=1)
                    print(results, doc.page_content)
                    if not results or results[0][1] > 0.05:  # 유사도 임계값 0.95
                        unique_new_documents.append(doc)
                        Document.objects.create(
                            page_content=doc.page_content,
                            category=doc.metadata['category'],
                            vector=np.array(vec).tobytes()
                        )
                except Exception as e:  # 일반 예외 처리
                    self.message_user(request, f"Error during similarity search: {e}")
                    return redirect("..")

            if unique_new_documents:
                database.add_documents(unique_new_documents)

            self.message_user(request, "Your csv file has been uploaded and processed")
            return redirect("..")
        form = CsvUploadForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )

    def view_documents(self, request):
        documents = Document.objects.all()
        payload = {"documents": documents}
        return render(
            request, "admin/view_documents.html", payload
        )

admin.site.register(Document, DocumentAdmin)
