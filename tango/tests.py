from django.test import TestCase
from tango.models import Category
from django.core.urlresolvers import reverse


class CategoryMethodTest(TestCase):

    def test_ensure_views_are_positive(self):
        cat = Category(name='test',views=-1,likes=0)
        cat.save()
        self.assertEqual((cat.views>=0),True)

    def test_slug_line_creation(self):
        cat = cat('Random Category String')
        cat.save()
        self.assertEqual(cat.slug,'random-category-string')


class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])
