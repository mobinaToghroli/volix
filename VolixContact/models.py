from django.db import models

# Create your models here.


class ContactUs(models.Model):
    fullname = models.CharField(max_length=150 , verbose_name='نام و نام خانوادگی')
    email = models.EmailField(verbose_name='ایمیل')
    message = models.TextField(verbose_name='متن پیام')
    time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False , verbose_name='خوانده شده/نشده')


    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'


    def __str__(self):
        return self.fullname


