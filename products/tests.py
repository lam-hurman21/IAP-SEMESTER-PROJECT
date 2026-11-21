from io import StringIO

from django.conf import settings
from django.contrib.auth import SESSION_KEY, get_user_model
from django.contrib.auth.models import Permission
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import Client, TestCase
from django.urls import reverse

from .forms import ProductForm, RegistrationForm
from .models import Category, Product


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Paper goods')
        cls.product = Product.objects.create(
            name='A5 Notebook', category=cls.category, description='Lecture notes.',
        )
        cls.hidden = Product.objects.create(
            name='Hidden product', category=cls.category,
            description='Not yet published.', is_active=False,
        )

    def test_public_catalog_uses_database_and_hides_inactive_products(self):
        response = self.client.get(reverse('products:index'))
        self.assertTemplateUsed(response, 'products/index.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, self.product.name)
        self.assertNotContains(response, self.hidden.name)

    def test_empty_catalog(self):
        Product.objects.all().delete()
        self.assertContains(self.client.get(reverse('products:index')),
                            'No products are available yet.')

    def test_about_and_navigation(self):
        for name in ('products:index', 'products:about'):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200)
            for destination in ('products:index', 'products:about',
                                'products:login', 'products:register'):
                self.assertContains(response, f'href="{reverse(destination)}"')
        self.assertTemplateUsed(self.client.get(reverse('products:about')), 'about.html')

    def test_category_cannot_be_deleted_with_products(self):
        with self.assertRaises(ProtectedError):
            self.category.delete()

    def test_category_name_is_unique(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Category.objects.create(name=self.category.name)

    def test_deleting_creator_preserves_product(self):
        creator = get_user_model().objects.create_user('creator')
        self.product.created_by = creator
        self.product.save()
        creator.delete()
        self.product.refresh_from_db()
        self.assertIsNone(self.product.created_by)

    def test_seed_command_is_repeatable_and_preserves_edits(self):
        for _ in range(2):
            call_command('seed_catalog', stdout=StringIO())
        self.assertEqual(Product.objects.count(), 4)
        self.product.refresh_from_db()
        self.assertEqual(self.product.description, 'Lecture notes.')


class AuthenticationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = 'Campus!Study-Strong92'
        cls.user = get_user_model().objects.create_user(
            username='student', email='student@example.com', password=cls.password,
        )

    def test_registration_hashes_password_and_starts_browser_session(self):
        response = self.client.post(reverse('products:register'), {
            'username': 'newstudent', 'email': 'new@example.com',
            'password1': self.password, 'password2': self.password,
            'is_staff': 'on', 'is_superuser': 'on',
        })
        self.assertRedirects(response, reverse('products:index'))
        user = get_user_model().objects.get(username='newstudent')
        self.assertTrue(user.check_password(self.password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(int(self.client.session[SESSION_KEY]), user.pk)
        self.assertTrue(self.client.session.get_expire_at_browser_close())

    def test_registration_rejects_invalid_input(self):
        cases = [{'username': 'student'}, {'email': 'invalid'},
                 {'password1': '123', 'password2': '123'}, {'password2': 'different'}]
        for invalid in cases:
            with self.subTest(invalid=invalid):
                data = {'username': 'newstudent', 'email': 'new@example.com',
                        'password1': self.password, 'password2': self.password}
                data.update(invalid)
                self.assertFalse(RegistrationForm(data).is_valid())

    def test_login_default_and_remember_me_expiry(self):
        for remember in (False, True):
            with self.subTest(remember=remember):
                client = Client()
                data = {'username': 'student', 'password': self.password}
                if remember:
                    data['remember_me'] = 'on'
                response = client.post(reverse('products:login'), data)
                self.assertRedirects(response, reverse('products:account'))
                self.assertEqual(client.session.get_expire_at_browser_close(), not remember)
                if remember:
                    self.assertEqual(client.session.get_expiry_age(), settings.SESSION_COOKIE_AGE)
                self.assertContains(client.get(reverse('products:account')), 'student@example.com')

    def test_invalid_or_inactive_user_cannot_login(self):
        for inactive in (False, True):
            self.user.is_active = not inactive
            self.user.save()
            response = self.client.post(reverse('products:login'), {
                'username': 'student', 'password': self.password if inactive else 'wrong',
            })
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
            self.assertNotIn(SESSION_KEY, self.client.session)

    def test_login_redirect_validation(self):
        for destination, expected in [
            (reverse('products:about'), reverse('products:about')),
            ('https://example.com/', reverse('products:account')),
        ]:
            client = Client()
            response = client.post(reverse('products:login'), {
                'username': 'student', 'password': self.password, 'next': destination,
            })
            self.assertRedirects(response, expected)

    def test_profile_requires_login(self):
        url = reverse('products:account')
        self.assertRedirects(self.client.get(url), f'{reverse("products:login")}?next={url}')

    def test_logout_requires_post_and_clears_session(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('products:logout')).status_code, 405)
        response = self.client.post(reverse('products:logout'))
        self.assertRedirects(response, reverse('products:index'))
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_authentication_posts_require_csrf(self):
        client = Client(enforce_csrf_checks=True)
        for name in ('products:login', 'products:register', 'products:logout'):
            self.assertEqual(client.post(reverse(name), {}).status_code, 403)


class ProductManagementTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Study space')
        cls.member = get_user_model().objects.create_user('member')
        cls.staff = get_user_model().objects.create_user('staff', is_staff=True)
        cls.manager = get_user_model().objects.create_user('manager', is_staff=True)
        cls.manager.user_permissions.set(Permission.objects.filter(
            content_type__app_label='products',
            codename__in=['add_product', 'change_product', 'view_product'],
        ))
        cls.product = Product.objects.create(
            name='Desk Lamp', category=cls.category, description='Light.',
            created_by=cls.manager, is_active=False,
        )

    def product_data(self, **overrides):
        data = {'name': 'New Lamp', 'category': self.category.pk,
                'description': 'A useful desk lamp.', 'is_active': 'on'}
        data.update(overrides)
        return data

    def test_anonymous_and_unprivileged_access(self):
        urls = [reverse('products:product_create'),
                reverse('products:product_edit', args=[self.product.pk])]
        for url in urls:
            for method in ('get', 'post'):
                self.assertEqual(getattr(self.client, method)(url).status_code, 302)
                for user in (self.member, self.staff):
                    client = Client()
                    client.force_login(user)
                    self.assertEqual(getattr(client, method)(url).status_code, 403)

    def test_manager_create_and_edit_preserves_creator(self):
        self.client.force_login(self.manager)
        response = self.client.post(reverse('products:product_create'),
                                    self.product_data(created_by=self.member.pk))
        self.assertRedirects(response, reverse('products:index'))
        product = Product.objects.get(name='New Lamp')
        self.assertEqual(product.created_by, self.manager)
        self.staff.user_permissions.add(Permission.objects.get(codename='change_product'))
        self.client.force_login(self.staff)
        response = self.client.post(reverse('products:product_edit', args=[product.pk]),
                                    self.product_data(name='Updated Lamp'))
        self.assertRedirects(response, reverse('products:index'))
        product.refresh_from_db()
        self.assertEqual(product.name, 'Updated Lamp')
        self.assertEqual(product.created_by, self.manager)

    def test_invalid_product_is_not_saved(self):
        for invalid in ({'name': ''}, {'description': ''}, {'category': 9999}):
            self.assertFalse(ProductForm(self.product_data(**invalid)).is_valid())
        self.client.force_login(self.manager)
        response = self.client.post(reverse('products:product_create'), self.product_data(name=''))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Product.objects.count(), 1)

    def test_management_pages_and_missing_product(self):
        self.client.force_login(self.manager)
        for url in (reverse('products:product_create'),
                    reverse('products:product_edit', args=[self.product.pk])):
            self.assertTemplateUsed(self.client.get(url), 'products/product_form.html')
        self.assertEqual(self.client.get(reverse('products:product_edit', args=[9999])).status_code, 404)

    def test_hidden_products_require_staff_and_view_permission(self):
        for user, visible in ((self.member, False), (self.staff, False), (self.manager, True)):
            self.client.force_login(user)
            response = self.client.get(reverse('products:index'))
            self.assertEqual(self.product in response.context['products'], visible)


class AdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser(
            'administrator', 'admin@example.com', 'Campus!Admin92',
        )
        cls.member = get_user_model().objects.create_user('member')
        cls.category = Category.objects.create(name='Accessories')

    def test_admin_requires_staff(self):
        self.assertEqual(self.client.get(reverse('admin:index')).status_code, 302)
        self.client.force_login(self.member)
        self.assertEqual(self.client.get(reverse('admin:index')).status_code, 302)

    def test_admin_models_and_creator_assignment(self):
        self.client.force_login(self.admin)
        for name in ('admin:index', 'admin:products_category_changelist',
                     'admin:products_product_changelist'):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        response = self.client.post(reverse('admin:products_product_add'), {
            'name': 'Admin product', 'category': self.category.pk,
            'description': 'Created in admin.', 'is_active': 'on', '_save': 'Save',
        })
        self.assertRedirects(response, reverse('admin:products_product_changelist'))
        self.assertEqual(Product.objects.get(name='Admin product').created_by, self.admin)
