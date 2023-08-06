""" Unit tests for UserMetada components
"""
from unittest import TestCase
from unittest.mock import Mock, patch

from core_main_app.commons.exceptions import ApiError
from core_user_registration_app.components.user_metadata.api import upsert


class TestUpsert(TestCase):
    """Tests api upsert function"""

    def setUp(self) -> None:
        """setUp"""
        self.data = Mock()

    def test_xml_content_none_raise_api_error(self):
        """test_xml_content_none_raise_api_error"""
        self.data.xml_content = None

        with self.assertRaises(ApiError):
            upsert(self.data, None)

    @patch(
        "core_user_registration_app.components.user_metadata.api.check_xml_file_is_valid"
    )
    def test_xml_content_present_saves_data(
        self, mock_check_xml_file_is_valid
    ):
        """test_xml_content_present_saves_data"""
        mock_check_xml_file_is_valid.return_value = None
        self.data.xml_content = "mock_xml_content"

        upsert(self.data, None)
        self.assertTrue(self.data.convert_and_save.called)
