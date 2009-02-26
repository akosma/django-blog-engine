from django.db import models, connection
from django.newforms import form_for_model
from datetime import datetime

class Tag(models.Model):
    text = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ["text"]

    class Admin:
        pass
        
    def get_link(self):
        return '<a href="/tag/%(tag)s">%(tag)s</a>' % { "tag": self.text }        



class PostManager(models.Manager):
    def get_by_date_and_slug(self, date, slug):
        query = "SELECT id, slug, title, body, date FROM engine_post WHERE date(date) = %s AND slug = %s"
        cursor = connection.cursor()
        cursor.execute(query, [date, slug])
        row = cursor.fetchone()
        if row is None:
            raise Post.DoesNotExist
        result = self.model(id=row[0], slug=row[1], title=row[2], body=row[3], date=row[4])
        return result



class Post(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique_for_date="date")
    body = models.TextField()
    date = models.DateTimeField()
    tags = models.ManyToManyField(Tag)
    objects = PostManager()
    
    def __unicode__(self):
        return self.title
        
    class Meta:
        ordering = ["-date"]
    
    class Admin:
        pass
        
    def get_summary(self):
        return self.body[:400] + " [...]"

    def get_tags(self):
        # http://www.skymind.com/~ocrow/python_string/
        return ', '.join([tag.get_link() for tag in self.tags.all()])

    def get_nice_url(self):
        return '/'.join([str(self.date.year).zfill(4), 
                             str(self.date.month).zfill(2), 
                             str(self.date.day).zfill(2), 
                             self.slug])

    def get_absolute_url(self):
        return "http://localhost:8000/" + self.get_nice_url()


class Comment(models.Model):
    author = models.CharField(max_length=30)
    email = models.EmailField()
    website = models.URLField(blank=True, verify_exists=False)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return '%s (%s)' % (self.author, self.email)

    class Meta:
        ordering = ["-date"]

    class Admin:
        pass
        
    def get_header(self):
        if self.website == "":
            return "%(author)s on %(date)s" % { "author": self.author, 
                                              "date": self.date }

        else:
            return '<a href="%(website)s">%(author)s</a> on %(date)s' % { "website": self.website, 
                                                                       "author": self.author, 
                                                                       "date": self.date }



CommentForm = form_for_model(Comment)
