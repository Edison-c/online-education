# _*_ coding:utf-8 _*_
__author__ = 'edison'
__date__ = '17-12-20 下午2:21'

from django import forms
from captcha.fields import CaptchaField
from users.models import Userprofile



class LoginForm(forms.Form):
    username =forms.CharField(required=True)
    password =forms.CharField(required=True)


class RegisterForm(forms.Form):
    email=forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages= {"invalid":u"验证码错误"})


class ForgetpwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 =forms.CharField(required=True)
    password2 =forms.CharField(required=True)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields=['image']



class UserInfoForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields=['nick_name','gender','birday','address','mobile']



