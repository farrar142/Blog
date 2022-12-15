from common_module.test import TestCase
from common_module.models import Image
from rest_framework import status
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY


def encoded_image_args(args: dict, image: str):
    with open(image, "rb") as image_file:
        _args = args.copy()
        _args.update(image=image_file)
        encoded = encode_multipart(
            BOUNDARY,
            _args,
        )
        return encoded


class TestBlog(TestCase):
    def create_blog(self):
        blog_dict = {}
        blog_dict.update(title="test", description="testdesc")
        encoded = encoded_image_args(blog_dict, "base/dummy/image.jpeg")
        return self.client.post("/blogs/", encoded, content_type=MULTIPART_CONTENT)

    def tearDown(self):
        return super().tearDown()

    def test_crud(self):
        self.client.login()
        resp = self.create_blog()
        # self.assertGreaterEqual(Image.objects.count(), 1)
        # print(resp.json())
        # self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # blog_dict = {}
        # blog_dict.update(title="test", description="testdesc")
        # resp = self.client.post("/blogs/", blog_dict)
        # self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # resp = self.client.post(
        #     "/admin/voice_profiles/", encoded, content_type=MULTIPART_CONTENT
        # )
