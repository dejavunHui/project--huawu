from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser

# Create your models here.

class Admain(AbstractBaseUser):
    '''管理员用户'''
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    USERNAME_FIELD = 'username'
    is_active = models.BooleanField(
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )


    class Meta:
        db_table = 'app_admain'
        verbose_name = '管理员'
        verbose_name_plural = verbose_name
