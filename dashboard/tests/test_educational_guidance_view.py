#tests/test_educational_guidance_view.py
"""
Tests for the educational guidance view.
"""

from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class TestEducationalGuidanceView(TestCase):
    """
    Test cases for the educational_guidance_view.
    """

    @patch('dashboard.views.get_educational_context')
    def test_educational_guidance_view_get(self, mock_get_context):
        """Test the educational_guidance_view normal GET request."""
        # Set up mock to return a test response
        mock_get_context.return_value = "This is a test educational response."

        # Make a GET request to the view
        response = self.client.get(reverse('dashboard:education_query'), {'topic': 'consolidation'})

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the mock was called with the right topic
        mock_get_context.assert_called_once_with('consolidation')

        # Check that the template is used
        self.assertTemplateUsed(response, 'dashboard/educational_guidance.html')

        # Check that the context contains the explanation and topic
        self.assertEqual(response.context['explanation'], "This is a test educational response.")
        self.assertEqual(response.context['topic'], 'consolidation')

    @patch('dashboard.views.get_educational_context')
    def test_educational_guidance_view_ajax(self, mock_get_context):
        """Test the educational_guidance_view AJAX request."""
        # Set up mock to return a test response
        mock_get_context.return_value = "This is a test educational response."

        # Make an AJAX request to the view
        response = self.client.get(
            reverse('dashboard:education_query'),
            {'topic': 'atr_stop'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the mock was called with the right topic
        mock_get_context.assert_called_once_with('atr_stop')

        # Check that the response is JSON
        self.assertEqual(response['Content-Type'], 'application/json')

        # Check that the JSON response contains the expected data
        self.assertJSONEqual(response.content, {
            'explanation': "This is a test educational response.",
            'topic': 'atr_stop'
        })

    @patch('dashboard.views.get_educational_context')
    def test_educational_guidance_view_default_topic(self, mock_get_context):
        """Test the educational_guidance_view with default topic."""
        # Set up mock to return a test response
        mock_get_context.return_value = "This is the default explanation."

        # Make a GET request to the view without specifying a topic
        response = self.client.get(reverse('dashboard:education_query'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the mock was called with the default topic
        mock_get_context.assert_called_once_with('default')
