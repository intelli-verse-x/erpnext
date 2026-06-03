"""Allow IntelliVerse admin hub to embed ERPNext in an iframe."""

ADMIN_EMBED_ORIGINS = (
	"'self'",
	"https://admin.intelli-verse-x.ai",
	"http://localhost:3000",
)


def allow_admin_hub_iframe(response):
	"""Strip X-Frame-Options and allow admin hub via CSP frame-ancestors."""
	if not getattr(response, "headers", None):
		return response

	response.headers.pop("X-Frame-Options", None)

	frame_ancestors = "frame-ancestors " + " ".join(ADMIN_EMBED_ORIGINS)
	existing_csp = response.headers.get("Content-Security-Policy", "")

	if existing_csp and "frame-ancestors" not in existing_csp:
		response.headers["Content-Security-Policy"] = f"{existing_csp.rstrip(';')}; {frame_ancestors}"
	elif not existing_csp:
		response.headers["Content-Security-Policy"] = frame_ancestors

	return response
