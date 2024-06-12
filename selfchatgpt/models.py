from django.db import models

# Create your models here.
# from django.db import models

class Chatlog(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)  # 자동으로 현재 시간을 저장합니다
    question = models.TextField()
    answer = models.TextField()
    ip = models.CharField(max_length=50)

    def __str__(self):
        return f"Question: {self.question[:50]}... Answer: {self.answer[:50]}..."

    
class Document(models.Model) :
    page_content = models.TextField()
    category = models.CharField(max_length=100)
    vector = models.BinaryField(null=True, blank=True)

    def __str__(self) :
        return self.page_content
    

