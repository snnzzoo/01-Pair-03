from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

"""
리뷰 제목 (30자 이하)
리뷰 내용
영화 이름
영화 평점
리뷰 작성시간
리뷰 수정시간
"""

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    movie_name = models.CharField(max_length=50)
    grade = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # image = models.ImageField(upload_to='images/', blank=True)
    image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(400, 300)],
                                format='JPEG',
                                options={'quality': 100})
    

