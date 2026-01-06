import re


ROUTE_PATTERN = re.compile(r'["\']([A-Za-z0-9_/]+)["\']')


def extract_routes_and_flows(files):
    routes = set()
    flows = []

    for path, content in files:
        for match in ROUTE_PATTERN.findall(content):
            if "/" in match or match.islower():
                routes.add(match)

        if "navigate(" in content:
            flows.append((path, content))

    return sorted(routes), flows
