from urllib.parse import urlencode


def get_indeed_search_url(keyword, location, page=1):
    start = (page - 1) * 10
    parameters = {"q": keyword, "l": location, "start": start}
    return "https://pk.indeed.com/jobs?" + urlencode(parameters)
