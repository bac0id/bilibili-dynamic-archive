import json
import os
import unittest

from bilibili_dynamic_archive.bilibili_api.dynamic import ProxyDynamic

BASE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

RESOURCES_DIR = os.path.join(PROJECT_ROOT, "resources")
JSON_IMAGE_9 = os.path.join(RESOURCES_DIR, "text_and_9_images.json")
JSON_VIDEO = os.path.join(RESOURCES_DIR, "text_and_video.json")
JSON_FORWARD = os.path.join(
    RESOURCES_DIR, "text_forward_text_and_5_images.json"
)


class TestProxyDynamic(unittest.TestCase):
    """Unit tests for the ProxyDynamic class handling different dynamic types."""

    @classmethod
    def setUpClass(cls):
        """Load all JSON data once before any tests run."""
        cls.json_data = {}
        try:
            with open(JSON_IMAGE_9, "r", encoding="utf-8") as f:
                cls.json_data["image_9"] = json.load(f)
            with open(JSON_VIDEO, "r", encoding="utf-8") as f:
                cls.json_data["video"] = json.load(f)
            with open(JSON_FORWARD, "r", encoding="utf-8") as f:
                cls.json_data["forward"] = json.load(f)
        except FileNotFoundError as e:
            raise unittest.SkipTest(
                f"Skipping tests due to missing test data file: {e}"
            )
        except json.JSONDecodeError as e:
            raise unittest.SkipTest(
                f"Skipping tests due to JSON decoding error: {e}"
            )
        except Exception as e:
            raise unittest.SkipTest(
                f"Skipping tests due to an unexpected error loading data: {e}"
            )

    def test_image_9_dynamic(self):
        """Test ProxyDynamic with a text and 9 images dynamic."""
        json_data = self.json_data["image_9"]
        dynamic = ProxyDynamic(json_data)

        self.assertEqual(dynamic.get_id(), "998107282443075606")
        self.assertEqual(
            dynamic.get_url(), "https://www.bilibili.com/opus/998107282443075606"
        )
        self.assertFalse(dynamic.has_forwarded_dynamic())
        self.assertIsNone(dynamic.get_forwarded_dynamic_json())

        expected_resources = [
            "http://i0.hdslb.com/bfs/new_dyn/25722f29c5b9cbbb38af568858875dd49871569.jpg",
            "http://i0.hdslb.com/bfs/new_dyn/6419134022386cb38da34e46ca3d18909871569.jpg",
            "http://i0.hdslb.com/bfs/new_dyn/8a3951830c75ed970a1cf7838fa69b279871569.jpg",
            "http://i0.hdslb.com/bfs/new_dyn/3313ba39daa219c921425832702616969871569.jpg",
            "http://i0.hdslb.com/bfs/new_dyn/d26649ca4ad06d11bfdafa94c755b69c9871569.jpg",
            "http://i0.hdslb.com/bfs/new_dyn/1920ffa9bd1ac8e392f0a8f62fe53bd19871569.jpg",
            "http://i0.hdslb.com/bfs/new_dyn/54235b092bdc9398127edf3e27f1f7bf9871569.jpg",
            "http://i0.hdslb.com/bfs/new_dyn/902bd38f1ba9041e3c66a735df22ada89871569.jpg",
            "http://i0.hdslb.com/bfs/new_dyn/949072661b64e9c05e044b1d2928f36f9871569.jpg",
        ]
        self.assertListEqual(dynamic.get_resources_urls(), expected_resources)

    def test_video_dynamic(self):
        """Test ProxyDynamic with a text and video dynamic."""
        json_data = self.json_data["video"]
        dynamic = ProxyDynamic(json_data)

        self.assertEqual(dynamic.get_id(), "1053776797431234564")
        self.assertEqual(
            dynamic.get_url(), "https://www.bilibili.com/opus/1053776797431234564"
        )
        self.assertFalse(dynamic.has_forwarded_dynamic())
        self.assertIsNone(dynamic.get_forwarded_dynamic_json())

        expected_resources = [
            "https://www.bilibili.com/video/BV1XSdwYkE4U/",
            "http://i0.hdslb.com/bfs/archive/b9f9e8786d15310023775c68d023b205be974465.jpg",
        ]
        self.assertListEqual(dynamic.get_resources_urls(), expected_resources)

    def test_forwarded_dynamic(self):
        """Test ProxyDynamic with a forwarded dynamic (original is text and 5 images)."""
        json_data = self.json_data["forward"]
        dynamic = ProxyDynamic(json_data)

        self.assertEqual(dynamic.get_id(), "1051490083797991432")
        self.assertEqual(
            dynamic.get_url(), "https://www.bilibili.com/opus/1051490083797991432"
        )
        self.assertTrue(dynamic.has_forwarded_dynamic())

        # Test get_forwarded_dynamic_json
        forwarded_json = dynamic.get_forwarded_dynamic_json()
        self.assertIsNotNone(forwarded_json)
        self.assertEqual(
            forwarded_json.get("id_str"), "1051191695270477848"
        )  # Check a key in the nested JSON

        # Test get_resources_urls - Should return resources from the original dynamic
        expected_resources = [
            "http://i0.hdslb.com/bfs/new_dyn/359c4e0769a2113c161f43462f457ef19871569.jpg",
            "http://i0.hdslb.com/bfs/new_dyn/07fd2f037d1e29d6a1c5bff3137fb08a9871569.jpg",
            "http://i0.hdslb.com/bfs/new_dyn/bcccb66381344cc09abb81332521a1509871569.jpg",
            "http://i0.hdslb.com/bfs/new_dyn/7d3b5b1202fc82632234836c38cbbf499871569.jpg",
            "http://i0.hdslb.com/bfs/new_dyn/0bdc598b9c17c02789047968f4b758469871569.jpg",
        ]
        self.assertListEqual(dynamic.get_resources_urls(), expected_resources)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
