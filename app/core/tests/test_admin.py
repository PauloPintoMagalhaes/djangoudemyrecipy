from django.conf import urls
from django.db.models.fields import reverse_related
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='pass123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@this.com', 
            password="12345",
            name="Thisusername"
        )

    def test_users_listed(self):
        """TEst that users are listed on user page"""
        # reverse is used to pass urls paths without much hassle
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)
        
        # assertContains tests that response contains a certain item
        # but also checks that the http response is 200
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        """TEst that the user edit page works"""
        # args here is used as an argument passed along with the url request
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the created user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)