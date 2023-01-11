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


class TestTemplate(TestCase):
    blog_id: int

    def create_blog(self):
        blog_dict = {}
        blog_dict.update(title="test", description="testdesc")
        encoded = encoded_image_args(blog_dict, "base/dummy/image.jpeg")
        resp = self.client.post("/blogs/", encoded, content_type=MULTIPART_CONTENT)
        self.blog_id = resp.json().get("id")
        return resp


class TestBlog(TestTemplate):
    def tearDown(self):
        return super().tearDown()

    def test_post_update(self):
        self.client.login()
        resp = self.create_blog()
        self.assertGreaterEqual(Image.objects.count(), 1)
        print(resp.json())
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        blog_dict = {}
        blog_dict.update(title="test", description="testdesc")
        resp = self.client.post("/blogs/", blog_dict)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.client.patch(f"/blogs/{self.blog_id}/", {"title": "test2"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)


class TestCategory(TestTemplate):
    def test_post_update(self):
        self.client.login()
        self.create_blog()
        resp = self.client.post(
            f"/categories/", {"blog": self.blog_id, "title": "test_category"}
        )
        cat_id = resp.json().get("id")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp = self.client.patch(f"/categories/{cat_id}/", {"title": "changed"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual("changed", resp.json().get("title"))
