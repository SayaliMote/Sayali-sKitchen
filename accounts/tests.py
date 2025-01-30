from django.contrib.auth import get_user_model
from django.test import TestCase

class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='sims',
            email='1sims@gmail.com',
            age='19',
            password='simskitchen@24'
    )
        self.assertEqual(user.username, 'sims')
        self.assertEqual(user.email, '1sims@gmail.com')
        self.assertEqual(user.age, '19')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='simskitchen',
            email='simskitchen@gmail.com',
            password='sims'
        )
        self.assertEqual(admin_user.username, 'simskitchen')
        self.assertEqual(admin_user.email, 'simskitchen@gmail.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)