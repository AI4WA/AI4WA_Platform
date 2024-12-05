from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from crime.models import Crime


class CrimeModelTests(TestCase):
    def setUp(self):
        self.crime = Crime.objects.create(
            name="Test Crime",
            description="Test Description",
            count=10
        )

    def test_crime_creation(self):
        """Test crime instance creation"""
        self.assertEqual(self.crime.name, "Test Crime")
        self.assertEqual(self.crime.description, "Test Description")
        self.assertEqual(self.crime.count, 10)
        self.assertIsNotNone(self.crime.created_at)
        self.assertIsNotNone(self.crime.updated_at)

    def test_crime_str_representation(self):
        """Test string representation of crime"""
        self.assertEqual(str(self.crime), "Test Crime")

    def test_crime_auto_timestamps(self):
        """Test auto-updating of timestamps"""
        old_updated_at = self.crime.updated_at
        self.crime.name = "Updated Crime"
        self.crime.save()
        self.crime.refresh_from_db()
        self.assertGreater(self.crime.updated_at, old_updated_at)

    def test_negative_count_allowed(self):
        """Test that negative count is allowed"""
        self.crime.count = -1
        self.crime.save()
        self.assertEqual(self.crime.count, -1)

    def test_blank_count_allowed(self):
        """Test that blank count is allowed"""
        self.crime.count = None
        self.crime.save()
        self.assertIsNone(self.crime.count)

    def test_name_max_length_model_level(self):
        """Test that model validation catches name field max length"""
        long_name = 'x' * 256
        crime = Crime(
            name=long_name,
            description="Test Description"
        )

        # Using full_clean() to trigger model-level validation
        with self.assertRaises(ValidationError):
            crime.full_clean()
