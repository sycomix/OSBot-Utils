from unittest import TestCase

from osbot_utils.utils.Dev import Dev
from osbot_utils.utils.Files import temp_file, file_not_exists, file_exists, file_contents_as_bytes, file_delete
from osbot_utils.utils.Http import GET, GET_bytes_to_file


# from 'https://via.placeholder.com/1.png?text=sample-png'
from osbot_utils.utils.Png import save_png_bytes_to_file

TEST_PNG_BYTES = (b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
                  b'\x02\x03\x00\x00\x00b{,\x1a\x00\x00\x00\tPLTE\xcc\xcc\xcc\x96\x96\x96\xb1'
                  b'\xb1\xb1sR\xafI\x00\x00\x00\tpHYs\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95'
                  b'+\x0e\x1b\x00\x00\x00\nIDAT\x08\x99ch\x00\x00\x00\x82\x00\x81\xcb\x13\xb2'
                  b'a\x00\x00\x00\x00IEND\xaeB`\x82')


class test_Png(TestCase):

    def setUp(self):
        self.path_temp_png = temp_file('.png')          # temp file path
        #self.url_test_image  = 'https://via.placeholder.com/1.png?text=sample-png'
        #self.path_test_image = '/tmp/osbot_utils_test_png_sample.png'
        #file_delete(self.path_test_image)
        #self.make_sure_test_file_exists()

    def tearDown(self):
        file_delete(self.path_temp_png)                 # delete file is created


    def test_save_png_bytes_to_file(self):
        assert file_not_exists(self.path_temp_png)
        result = save_png_bytes_to_file(bytes=TEST_PNG_BYTES, png_file=self.path_temp_png, log_status=False)
        assert result == self.path_temp_png
        assert file_exists(self.path_temp_png)
