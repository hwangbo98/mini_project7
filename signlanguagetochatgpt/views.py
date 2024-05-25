from django.shortcuts import render
from django.utils import timezone
import logging
from django.conf import settings
from django.core.files.storage import default_storage
logger = logging.getLogger('mylogger')
#signlanguage/models.py의 Result 모델을 import한다.
from .models import ChatResult, Result
# Create your views here.

'''
1. 원칙은 ORM을 사용하여 별도 sql 문이 없는 것이다.
2. 하지만, ORM을 사용하면서도 sql문을 사용해야 하는 경우가 있다.
3. 이때는 아래와 같이 사용한다.
 - 물론 이 부분도 view가 sql을 알면 안되서 분리해야 하지만, 짧은 교육상 이곳에 둔다. 
'''
def getChatResult(self, id):
        query = "SELECT * FROM signlanguagetochatgpt_chatresult WHERE id = {0}".format(id)
        logger.info(">>>>>>>> getChatResult SQL : "+query)
        chatResult = self.t_exec(query)

def index(request):
    return render(request, 'languagechat/index.html')

def chat(request):
    if request.method == 'POST' and request.FILES['files']:

        results=[]

     

        context = {
        'question': 'question',
        'result': 'result'
    }

    return render(request, 'languagechat/result.html', context)  