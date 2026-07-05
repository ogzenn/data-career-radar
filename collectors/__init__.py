# Makes collectors a package. Each collector module exposes a fetch_*_jobs() function
# that returns a list of job dicts in this shared format:
#
# {
#     "id": str (unique, prefixed by source e.g. "remoteok_12345"),
#     "title": str,
#     "company": str,
#     "url": str,
#     "description": str,
#     "tags": str,
#     "location": str,
#     "source": str,
#     "posted_at": datetime | None,
# }
