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

    def _create_blog(self, title="test"):
        blog_dict = {}
        blog_dict.update(title=title, description="testdesc")
        encoded = encoded_image_args(blog_dict, "base/dummy/image.jpeg")
        resp = self.client.post("/blogs/", encoded, content_type=MULTIPART_CONTENT)
        return resp

    def create_blog(self):
        resp = self._create_blog()
        self.blog_id = resp.json().get("id")
        self.blog_name = resp.json().get("title")
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
        new_title = "test2"
        resp = self.client.patch(f"/blogs/{self.blog_id}/", {"title": new_title})
        self.blog_name = new_title
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.client.logout()
        resp = self.client.get(f"/blogs/{self.blog_id}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.delete(f"/blogs/{self.blog_id}/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_have_two_blog(self):
        self.client.login()
        self._create_blog()
        resp = self._create_blog("doubled")
        print(f"{resp.json()=}")
        self.assertEqual(resp.status_code, 400)


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
        print(resp.json())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual("changed", resp.json().get("title"))
        resp = self.client.get(f"/categories/{cat_id}/")

        print(resp.json())


class AuthorizeTest(TestTemplate):
    def test_authorize(self):
        self.client.fake()
        resp = self.client.get("/blogs/")
        print(resp)
