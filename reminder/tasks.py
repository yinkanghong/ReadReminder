from celery import task

from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

import requests
from bs4 import BeautifulSoup

from .models import *


@task
def check_update():
    response = requests.get('https://m.qu.la/book/3137/')
    soup = BeautifulSoup(response.text, 'lxml')
    div = soup.find("div", {"id": "chapterlist"})

    new_chapter = False
    email_errors = []
    for p in div.find_all('p'):
        a = p.find('a', href=True)
        # 记录数据
        a_data = a.getText().split(' ')
        chapter, is_create = Chapter.objects.get_or_create(order=a_data[0])

        if is_create:
            new_chapter = True
            try:
                chapter.name = a_data[1]
            except IndexError:
                chapter.name = ''
            chapter.href = 'https://m.qu.la{}'.format(a['href'])
            chapter.save()
            chapter.get_content()
            try:
                # 新章节邮件提醒
                # TODO 直接发送Html邮件 会被邮箱识别为垃圾邮件
                send_mail(chapter.__str__(),
                          'http://{}{}'.format(settings.DOMAIN, reverse('chapter_detail', args=[str(chapter.id)])),
                          settings.DEFAULT_FROM_EMAIL, ['614457662@qq.com'])
            except Exception as e:
                email_errors.append(str(e))
    if new_chapter:
        if len(email_errors) == 0:
            return '检测完成 有新章节 发送成功'
        else:
            return '检测完成 有新章节 发送错误：{}'.format(' '.join(email_errors))
    else:
        return '检测完成 暂无新章节'
