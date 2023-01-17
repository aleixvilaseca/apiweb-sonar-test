# Applications to exclude
APPLICATIONS_TO_EXCLUDE = [
    "list",
]

# URLs to get the list of metrics from SonarQube
GET_NCLOC_URL = "https://localhost:9000/api/measures/component?component=%s&metricKeys=ncloc&ps=100"
GET_MAINTAINABILITY_URL = "https://localhost:9000/api/measures/component?component=%s&metricKeys=sqale_debt_ratio&ps=100"
GET_RELIABILITY_URL = "https://localhost:9000/api/measures/component?component=%s&metricKeys=reliability_rating&ps=100"
GET_SECURITY_EFFORT_URL = "https://localhost:9000/api/measures/search?ps=100&projectKeys=%s&metricKeys=security_remediation_effort"
GET_DUPLICATED_LINES_URL = "https://localhost:9000/api/measures/search?projectKeys=%s&metricKeys=duplicated_lines_density&ps=100"
GET_SECURITY_RATING_URL = "https://localhost:9000/api/measures/component?component=%s&metricKeys=security_rating&ps=100"
GET_VULNERABILITIES_URL = "https://localhost:9000/api/issues/search?componentKeys=%s&types=VULNERABILITY&ps=100"
GET_SECURITY_BLOCKER_URL = "https://localhost:9000/api/issues/search?componentKeys=%s&types=VULNERABILITY&severities=BLOCKER&ps=100"
GET_SECURITY_CRITICAL_URL = "https://localhost:9000/api/issues/search?componentKeys=%s&types=VULNERABILITY&severities=CRITICAL&ps=100"
GET_BLOCKER_URL = "https://localhost:9000/api/issues/search?componentKeys=%s&types=CODE_SMELL,BUG&severities=BLOCKER&ps=100"
GET_CRITICAL_URL = "https://localhost:9000/api/issues/search?componentKeys=%s&types=CODE_SMELL,BUG&severities=CRITICAL&ps=100"
