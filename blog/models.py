from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
        .filter(status='published')

class Post(models.Model):
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )

    title = models.CharField(max_length=250) #This field is CharField, which translates into a VARCHAR column in the SQL database.

    '''
    This is a field intended to be used in URLs. A slug is a short label
    that contains only letters, numbers, underscores, or hyphens. You will use
    the slug field to build beautiful, SEO-friendly URLs for your blog posts.
    You have added the unique_for_date parameter to this field so that you
    can build URLs for posts using their publish date and slug. Django will
    prevent multiple posts from having the same slug for a given date.
    '''
    slug = models.SlugField(max_length=250, unique_for_date='publish')

    author = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='blog_posts')

    '''
        author: This field defines a many-to-one relationship, meaning that each
    post is written by a user, and a user can write any number of posts. For this
    field, Django will create a foreign key in the database using the primary
    key of the related model. In this case, you are relying on the User model of
    the Django authentication system. The on_delete parameter specifies the
    behavior to adopt when the referenced object is deleted. This is not specific
    to Django; it is an SQL standard. Using CASCADE, you specify that when
    the referenced user is deleted, the database will also delete all related blog
    posts.

    '''
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,

    choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail',
            args=[self.publish.year,
                self.publish.month,
                self.publish.day, self.slug])

    '''
    The Meta class inside the model contains metadata. You tell Django to sort results
    by the publish field in descending order by default when you query the database.
    '''
    class Meta:
        ordering = ('-publish',)
        def __str__(self):
            return self.title

        '''
        The __str__() method is the default human-readable representation of the object.
        Django will use it in many places, such as the administration site.
        '''
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    '''
    The related_name attribute allows you to name the attribute that you use for
    the relationship from the related object back to this one. After defining this, you
    can retrieve the post of a comment object using comment.post and retrieve all
    comments of a post using post.comments.all(). If you don't define the related_
    name attribute, Django will use the name of the model in lowercase, followed by _
    set (that is, comment_set) to name the relationship of the related object to the object
    of the model, where this relationship has been defined.
    You can learn more about many-to-one relationships at https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_one/.
    '''
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
        def __str__(self):
            return f'Comment by {self.name} on {self.post}'
