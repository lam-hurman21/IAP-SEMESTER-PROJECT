from django.test import SimpleTestCase
from django.urls import reverse


class ProductPageTests(SimpleTestCase):
	def test_catalog_renders_app_template(self):
		response = self.client.get(reverse('products:index'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'products/index.html')
		self.assertTemplateUsed(response, 'base.html')
		self.assertContains(response, 'A5 Notebook')
		self.assertContains(response, 'Everyday Backpack')
		self.assertContains(response, 'Desk Lamp')

	def test_about_renders_project_template(self):
		response = self.client.get(reverse('products:about'))

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'about.html')
		self.assertTemplateUsed(response, 'base.html')
		self.assertContains(response, 'About Campus Supply')

	def test_both_pages_have_working_navigation(self):
		page_names = ('products:index', 'products:about')

		for page_name in page_names:
			with self.subTest(page=page_name):
				response = self.client.get(reverse(page_name))
				for destination in page_names:
					self.assertContains(
						response, f'href="{reverse(destination)}"',
					)
