from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django_countries.fields import CountryField
from django.utils import timezone
from django.shortcuts import reverse
from .manager import UserManager
from questions.models import Question, Answer
from functools import reduce
from django.db.models import Q


       
GENDER_CHOICE = (
    ('male','Male'),
    ('female','Female'),
    ('others','Others')
) 
class User(AbstractBaseUser):
    email       =   models.EmailField(verbose_name="email", max_length=100, unique=True)
    username    =   models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    gender      =   models.CharField(max_length=10, choices=GENDER_CHOICE)
    bio         =   models.TextField(max_length=2000, blank=True, null=True)
    profile_pic =   models.ImageField(default='default/profile.jpeg',
                        upload_to="users/%Y/%m/%d", blank=True, null=True)
    mobile      =   models.CharField(max_length=15, null=True, blank=True)
    country     =   CountryField()
    points      =   models.IntegerField(default=0, null=True)
    is_admin    =   models.BooleanField(default=False)
    is_active   =   models.BooleanField(default=True) 
    is_staff    =   models.BooleanField(default=False)
    is_superuser =  models.BooleanField(default=False)
    date_joined =   models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login  =   models.DateTimeField(verbose_name="last login", auto_now=True)
    upvoted_questions = models.ManyToManyField(Question, related_name="upvoted_users")
    downvoted_questions = models.ManyToManyField(Question, related_name="downvoted_users")
    upvoted_answers = models.ManyToManyField(Answer, related_name="upvoted_users")
    downvoted_answers = models.ManyToManyField(Answer, related_name="downvoted_users")
    points = models.IntegerField(default=0)
    is_shadow_banned = models.BooleanField(default=False)

    def update_points(self):
        answers = self.answer_set.filter(~Q(points = 0))
        points = map(lambda a: a.points, answers)
        user_points = reduce(lambda x, y: x + y, points, 0)
        self.points = user_points
        self.save()

    ''' setting the email as the required login field,
    but we can also user username if we so wish '''
    USERNAME_FIELD = 'email'

    objects =  UserManager()


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    



class Following(models.Model):
    user_from = models.ForeignKey('User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)
        


User.add_to_class('following', models.ManyToManyField('self', through=Following, related_name='followers', symmetrical=False))