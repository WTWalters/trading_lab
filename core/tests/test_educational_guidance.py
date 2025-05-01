# core/tests/test_educational_guidance.py
import unittest
from unittest.mock import patch, MagicMock, PropertyMock
import os
# Assuming google.generativeai might not be installed in all test environments
# We handle potential ImportError during mocking setup if needed
try:
    import google.generativeai as genai
    GENAI_INSTALLED = True
except ImportError:
    GENAI_INSTALLED = False
    genai = None # Define genai as None if not installed

from core.educational_guidance import (
    initialize_gemini_client,
    get_educational_context,
    EDUCATIONAL_PROMPTS
)

# Only run tests requiring genai if it's installed
# You might need to adjust decorators based on your test runner if not using unittest skipIf
# For pytest, you might use @pytest.mark.skipif(not GENAI_INSTALLED, reason="google.generativeai not installed")

@unittest.skipUnless(GENAI_INSTALLED, "google.generativeai not installed")
class TestEducationalGuidance(unittest.TestCase):
    """
    Test cases for the educational_guidance module.
    """

    def test_prompts_exist(self):
        """Test that all expected topic prompts exist."""
        expected_topics = [
            'volume_confirmation', 'atr_stop', 'chandelier_exit',
            'consolidation', 'rr_ratio', 'position_sizing', 'default'
        ]
        for topic in expected_topics:
            self.assertIn(topic, EDUCATIONAL_PROMPTS)
            self.assertTrue(EDUCATIONAL_PROMPTS[topic].strip())

    # --- Tests for initialize_gemini_client ---

    @patch('core.educational_guidance.GEMINI_API_KEY', 'fake_key')
    @patch('core.educational_guidance.genai')
    def test_initialize_gemini_client_success(self, mock_genai):
        """Test successful client initialization."""
        # No need for patch.dict on os.environ anymore
        client = initialize_gemini_client()
        self.assertEqual(client, mock_genai)
        mock_genai.configure.assert_called_once_with(api_key="fake_key") # Now this should match

    @patch.dict(os.environ, {}, clear=True) # No API Key
    def test_initialize_gemini_client_missing_key(self):
        """Test client initialization with missing API key."""
        # Temporarily remove the key if it exists from a previous test's patch
        if 'GEMINI_API_KEY' in os.environ:
             del os.environ['GEMINI_API_KEY']
        # Need to also ensure the module-level constant is reset if accessed directly
        with patch('core.educational_guidance.GEMINI_API_KEY', None):
              client = initialize_gemini_client()
              self.assertIsNone(client)

    @patch('core.educational_guidance.GEMINI_API_KEY', 'fake_key')
    @patch('core.educational_guidance.genai')
    def test_initialize_gemini_client_configure_error(self, mock_genai):
        """Test client initialization with a configuration error."""
        # No need for patch.dict on os.environ anymore
        mock_genai.configure.side_effect = Exception("Config Error")
        client = initialize_gemini_client()
        self.assertIsNone(client)
        mock_genai.configure.assert_called_once_with(api_key="fake_key") # Now this should match


    # Note: Testing ImportError reliably might require more complex mocking
    # or environment manipulation, skipping direct test for now.

    # --- Tests for get_educational_context ---

    @patch('core.educational_guidance.initialize_gemini_client')
    def test_get_educational_context_client_initialization_failed(self, mock_init):
        """Test handling when client initialization fails."""
        mock_init.return_value = None
        result = get_educational_context('volume_confirmation')
        self.assertIn("Could not initialize", result)
        mock_init.assert_called_once() # Ensure init was attempted

    @patch('core.educational_guidance.initialize_gemini_client')
    def test_get_educational_context_successful_with_text(self, mock_init):
        """Test successful generation via response.text attribute."""
        # --- Mock Setup ---
        mock_response = MagicMock()
        # Configure .text attribute
        type(mock_response).text = PropertyMock(return_value="Response via text")
        # Ensure .parts does not exist or causes issues if accessed
        del mock_response.parts
        # Ensure no blocking
        mock_response.prompt_feedback = None

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response

        mock_genai_instance = MagicMock()
        mock_genai_instance.GenerativeModel.return_value = mock_model

        mock_init.return_value = mock_genai_instance
        # --- End Mock Setup ---

        result = get_educational_context('volume_confirmation')

        self.assertEqual("Response via text", result)
        mock_model.generate_content.assert_called_once()
        call_args = mock_model.generate_content.call_args[0][0]
        self.assertIn('volume confirmation', call_args.lower())

    @patch('core.educational_guidance.initialize_gemini_client')
    def test_get_educational_context_successful_with_parts(self, mock_init):
        """Test successful generation via response.parts attribute."""
        # --- Mock Setup ---
        mock_part = MagicMock()
        type(mock_part).text = PropertyMock(return_value="Response via parts")

        mock_response = MagicMock()
        # Ensure .text does not exist or causes issues if accessed
        # We can simulate this by making hasattr(mock_response, 'text') return False
        # or simply not setting it and relying on the hasattr check in the code.
        # Let's specifically delete it if it exists from MagicMock default
        if hasattr(mock_response, 'text'):
            delattr(mock_response, 'text')
        # Configure .parts attribute
        type(mock_response).parts = PropertyMock(return_value=[mock_part])
        # Ensure no blocking
        mock_response.prompt_feedback = None

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response

        mock_genai_instance = MagicMock()
        mock_genai_instance.GenerativeModel.return_value = mock_model

        mock_init.return_value = mock_genai_instance
        # --- End Mock Setup ---

        result = get_educational_context('rr_ratio')

        self.assertEqual("Response via parts", result)
        mock_model.generate_content.assert_called_once()
        call_args = mock_model.generate_content.call_args[0][0]
        self.assertIn('risk:reward ratio', call_args.lower())


    @patch('core.educational_guidance.initialize_gemini_client')
    def test_get_educational_context_unknown_response_format(self, mock_init):
        """Test handling when response format has neither .text nor .parts."""
        # --- Mock Setup ---
        mock_response = MagicMock()
        # Ensure neither .text nor .parts exist
        if hasattr(mock_response, 'text'):
            delattr(mock_response, 'text')
        if hasattr(mock_response, 'parts'):
             delattr(mock_response, 'parts')
        # Ensure no blocking
        mock_response.prompt_feedback = None

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response

        mock_genai_instance = MagicMock()
        mock_genai_instance.GenerativeModel.return_value = mock_model

        mock_init.return_value = mock_genai_instance
        # --- End Mock Setup ---

        result = get_educational_context('consolidation')
        # --- UPDATE THIS ASSERTION ---
        # self.assertIn("Unknown response format", result)
        self.assertIn("issue with the educational content format", result)
        # -----------------------------
        mock_model.generate_content.assert_called_once()


    @patch('core.educational_guidance.initialize_gemini_client')
    def test_get_educational_context_content_blocked(self, mock_init):
        """Test handling when content is blocked by safety filters."""
        # --- Mock Setup ---
        mock_feedback = MagicMock()
        type(mock_feedback).block_reason = PropertyMock(return_value="SAFETY")

        mock_response = MagicMock()
        # Ensure text/parts don't matter here, focus on feedback
        type(mock_response).prompt_feedback = PropertyMock(return_value=mock_feedback)

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response

        mock_genai_instance = MagicMock()
        mock_genai_instance.GenerativeModel.return_value = mock_model

        mock_init.return_value = mock_genai_instance
        # --- End Mock Setup ---

        result = get_educational_context('atr_stop')

        self.assertIn("content restrictions", result)
        mock_model.generate_content.assert_called_once()

    @patch('core.educational_guidance.initialize_gemini_client')
    def test_get_educational_context_api_error(self, mock_init):
        """Test handling when API call raises an exception."""
        # --- Mock Setup ---
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")

        mock_genai_instance = MagicMock()
        mock_genai_instance.GenerativeModel.return_value = mock_model

        mock_init.return_value = mock_genai_instance
        # --- End Mock Setup ---

        result = get_educational_context('position_sizing')

        self.assertIn("there was an error", result)
        self.assertIn("API Error", result)
        mock_model.generate_content.assert_called_once()

    @patch('core.educational_guidance.initialize_gemini_client')
    def test_get_educational_context_unknown_topic_uses_default(self, mock_init):
        """Test that an unknown topic uses the default prompt."""
        # --- Mock Setup ---
        mock_response = MagicMock()
        type(mock_response).text = PropertyMock(return_value="Default response")
        mock_response.prompt_feedback = None

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response

        mock_genai_instance = MagicMock()
        mock_genai_instance.GenerativeModel.return_value = mock_model

        mock_init.return_value = mock_genai_instance
        # --- End Mock Setup ---

        result = get_educational_context('some_unknown_topic_key')

        self.assertEqual("Default response", result)
        # Verify the *default* prompt was used
        mock_model.generate_content.assert_called_once_with(EDUCATIONAL_PROMPTS['default'])

    @patch('core.educational_guidance.initialize_gemini_client')
    def test_get_educational_context_no_topic_uses_default(self, mock_init):
        """Test that providing None or empty string for topic uses the default prompt."""
         # --- Mock Setup ---
        mock_response = MagicMock()
        type(mock_response).text = PropertyMock(return_value="Default response again")
        mock_response.prompt_feedback = None

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response

        mock_genai_instance = MagicMock()
        mock_genai_instance.GenerativeModel.return_value = mock_model

        mock_init.return_value = mock_genai_instance
        # --- End Mock Setup ---

        # Test with None topic
        result_none = get_educational_context(None)
        self.assertEqual("Default response again", result_none)
        mock_model.generate_content.assert_called_with(EDUCATIONAL_PROMPTS['default'])

        # Reset mock call count for next assertion
        mock_model.generate_content.reset_mock()

        # Test with empty string topic
        result_empty = get_educational_context("")
        self.assertEqual("Default response again", result_empty)
        mock_model.generate_content.assert_called_with(EDUCATIONAL_PROMPTS['default'])


# Conditional execution for running directly
if __name__ == '__main__':
    # Ensure genai is mocked or installed before running
    if GENAI_INSTALLED:
         unittest.main()
    else:
         print("Skipping tests: google.generativeai not installed.")
