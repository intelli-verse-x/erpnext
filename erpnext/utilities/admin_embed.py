"""Allow IntelliVerse admin hub to embed ERPNext in an iframe."""

import re

# Origins allowed to embed erp.toba-tech.ai in an <iframe>.
ADMIN_EMBED_ORIGINS = (
	"'self'",
	"https://admin.intelli-verse-x.ai",
	"https://admin.toba-tech.ai",
	"http://localhost:3000",
)

_FRAME_ANCESTORS_DIRECTIVE = "frame-ancestors " + " ".join(ADMIN_EMBED_ORIGINS)
_FRAME_ANCESTORS_RE = re.compile(r"frame-ancestors\s+[^;]+", re.IGNORECASE)


def _strip_x_frame_options(headers) -> None:
	"""Remove X-Frame-Options regardless of header casing."""
	for key in list(headers.keys()):
		if key.lower() == "x-frame-options":
			headers.pop(key)


def _merge_content_security_policy(existing_csp: str) -> str:
	"""Set or replace frame-ancestors; keep other CSP directives intact."""
	existing_csp = (existing_csp or "").strip()
	if not existing_csp:
		return _FRAME_ANCESTORS_DIRECTIVE

	if _FRAME_ANCESTORS_RE.search(existing_csp):
		return _FRAME_ANCESTORS_RE.sub(_FRAME_ANCESTORS_DIRECTIVE, existing_csp)

	return f"{existing_csp.rstrip(';')}; {_FRAME_ANCESTORS_DIRECTIVE}"


def allow_admin_hub_iframe(response):
	"""Strip X-Frame-Options and allow admin hub via CSP frame-ancestors."""
	if not getattr(response, "headers", None):
		return response

	_strip_x_frame_options(response.headers)

	existing_csp = response.headers.get("Content-Security-Policy", "")
	response.headers["Content-Security-Policy"] = _merge_content_security_policy(existing_csp)

	return response
