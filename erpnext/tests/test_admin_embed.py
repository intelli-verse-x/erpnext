import unittest

from werkzeug.wrappers import Response

from erpnext.utilities.admin_embed import (
	_FRAME_ANCESTORS_DIRECTIVE,
	allow_admin_hub_iframe,
)


class TestAdminEmbed(unittest.TestCase):
	def test_strips_x_frame_options_and_sets_csp(self):
		response = Response("ok")
		response.headers["X-Frame-Options"] = "SAMEORIGIN"

		allow_admin_hub_iframe(response)

		self.assertNotIn("X-Frame-Options", response.headers)
		self.assertIn("frame-ancestors", response.headers["Content-Security-Policy"])
		self.assertIn("https://admin.intelli-verse-x.ai", response.headers["Content-Security-Policy"])
		self.assertIn("http://localhost:3000", response.headers["Content-Security-Policy"])

	def test_replaces_existing_frame_ancestors(self):
		response = Response("ok")
		response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'"

		allow_admin_hub_iframe(response)

		csp = response.headers["Content-Security-Policy"]
		self.assertIn("default-src 'self'", csp)
		self.assertIn(_FRAME_ANCESTORS_DIRECTIVE, csp)
		self.assertNotIn("frame-ancestors 'none'", csp)

	def test_strips_lowercase_x_frame_options(self):
		response = Response("ok")
		response.headers["x-frame-options"] = "DENY"

		allow_admin_hub_iframe(response)

		self.assertFalse(any(k.lower() == "x-frame-options" for k in response.headers.keys()))


if __name__ == "__main__":
	unittest.main()
