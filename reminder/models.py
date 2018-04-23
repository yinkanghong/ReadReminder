from django.db import models

import requests
from bs4 import BeautifulSoup


# 章节
class Chapter(models.Model):
    # 排序
    order = models.CharField(max_length=255,
                             verbose_name=u'第x节')
    # 名称
    name = models.CharField(max_length=255,
                            null=True,
                            blank=True,
                            verbose_name=u'名称')
    # 链接
    href = models.CharField(max_length=255,
                            null=True,
                            blank=True,
                            verbose_name=u'链接')
    # 内容
    content = models.TextField(verbose_name=u'内容')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name=u'创建时间')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name=u'更新时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = '章节'
        ordering = ('-id',)

    def get_content(self):
        # 抓取内容
        response = requests.get(self.href)
        soup = BeautifulSoup(response.text, 'lxml')
        div = soup.find("div", {"id": "chaptercontent"})
        self.content = str(div)
        self.save()

    def __str__(self):
        return '{} {}'.format(self.order, self.name)
