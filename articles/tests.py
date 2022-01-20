from django.test import TestCase
from articles.models import Article
from django.utils.text import slugify
# Create your tests here.

class ArticleTestCase(TestCase):
    def setUp(self):
        self.number_of_articles = 5
        for i in range(0, self.number_of_articles):
            Article.objects.create(title='Hello world', content='Something Random')

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.number_of_articles)
    
    def test_slug(self):
        obj = Article.objects.all().order_by('id').first() # grab the first item in the queryset (like qs[0])
        title = obj.title
        slug = obj.slug
        slugified_title = slugify(title)
        self.assertEqual(slug, slugified_title)

    def test_hello_world_slug(self):
        qs = Article.objects.exclude(slug__iexact='hello-world')
        for obj in qs:
            title = obj.title
            slug = obj.slug
            slugified_title = slugify(title)
            self.assertNotEqual(slug, slugified_title)