# source: https://github.com/UCD-Full-Stack-Jan-2024/Frameworks/blob/main/Week5/unit10/Unit_10_Walkthrough_Testing.py

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.urls import reverse

# Create your tests here.

class UserFormsTests(TestCase):
    def setUp(self):
        # Set up a user and profile for the tests
        self.user = User.objects.create_user(username='testuser', password='12345')
        Profile.objects.get_or_create(user=self.user, defaults={'image': 'default.jpg'})
        
    
    #12. test_user_register_form method
    def test_user_register_form(self):
        # Test user registration form with valid data
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'django1234',
            'password2': 'django1234'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    
    # this is from chatgpt
    
    def test_register_valid_case(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        # form_data = {
        #     'username': 'newuser',
        #     'email': 'newuser@example.com',
        # }


    # def test_some_view_invalid_case(self):
    #     response = self.client.post(reverse('some_view_name'), {'some_field': 'invalid_data'})
    #     self.assertEqual(response.status_code, 400)  # Or whatever status code is appropriate
    #     self.assertFormError(response, 'form', 'some_field', 'This field is required.')
       
        
    
    # 13. test_user_update_form method

    def test_user_update_form(self):
        # Test user update form with valid data
        form_data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com'
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        
    
    # 14. test_profile_update_with_invalid_image_format method

    def test_profile_update_with_invalid_image_format(self):
        # Test profile update with an invalid image format
        invalid_image_data = b'this is not real image data'
        invalid_image_file = SimpleUploadedFile('new_image.txt', invalid_image_data, content_type='text/plain')
        form = ProfileUpdateForm(files={'image': invalid_image_file}, instance=self.user.profile)
        self.assertFalse(form.is_valid())
        
    
    # 15. test_profile_update_with_oversized_image()

    def test_profile_update_with_oversized_image(self):
        # Test profile update with an oversized image
        oversized_image_data = b'\x00' * 5242880  # 5MB of zeros
        oversized_image_file = SimpleUploadedFile('new_image.jpg', oversized_image_data, content_type='image/jpeg')
        form = ProfileUpdateForm(files={'image': oversized_image_file}, instance=self.user.profile)
        self.assertFalse(form.is_valid())
