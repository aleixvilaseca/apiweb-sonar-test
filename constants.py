# Applications to exclude
APPLICATIONS_TO_EXCLUDE = [
    "0192-Incasol.OBI",
    "0192-jenkins-autoservei-library",
    "0192-jenkins-delegated-deployment-library",
    "0192-jenkins-oficines-externes-library",
    "0192-jenkins-oqual-library",
    "0192-jenkins-utils-library",
    "0192-prova-maven-library",
    "0192-prova-node-library",
    "0192-repository-artifactory-cleaner",
    "0192-SIC-jenkins-pipeline-library",
    "0192-test-intcan-2354",
    "cpd4-jenkins-shared-library",
    "cpd3-nex-jenkins-shared-library",
    "cpd3-mc-jenkins-shared-library",
    "cpd2-jenkins-shared-library",
    "cpd1-jenkins-shared-library",
    "null-null",
    "cat.gencat.ctti.sic:RemedyWSClient"
]

# URLs to get the list of metrics from SonarQube
GET_NCLOC_URL = "https://codi.qualitat.solucions.gencat.cat/api/measures/component?component=%s&metricKeys=ncloc&ps=100"
GET_MAINTAINABILITY_URL = "https://codi.qualitat.solucions.gencat.cat/api/measures/component?component=%s&metricKeys=sqale_debt_ratio&ps=100"
GET_RELIABILITY_URL = "https://codi.qualitat.solucions.gencat.cat/api/measures/component?component=%s&metricKeys=reliability_remediation_effort&ps=100"
GET_SECURITY_EFFORT_URL = "https://codi.qualitat.solucions.gencat.cat/api/measures/search?ps=100&projectKeys=%s&metricKeys=security_remediation_effort"
GET_DUPLICATED_LINES_URL = "https://codi.qualitat.solucions.gencat.cat/api/measures/search?projectKeys=%s&metricKeys=duplicated_lines_density&ps=100"
GET_SECURITY_RATING_URL = "https://codi.qualitat.solucions.gencat.cat/api/measures/component?component=%s&metricKeys=security_rating&ps=100"
GET_VULNERABILITIES_URL = "https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=%s&types=VULNERABILITY&ps=100"
GET_SECURITY_BLOCKER_URL = "https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=%s&types=VULNERABILITY&severities=BLOCKER&ps=100"
GET_SECURITY_CRITICAL_URL = "https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=%s&types=VULNERABILITY&severities=CRITICAL&ps=100"
GET_BLOCKER_URL = "https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=%s&types=CODE_SMELL,BUG&severities=BLOCKER&ps=100"
GET_CRITICAL_URL = "https://codi.qualitat.solucions.gencat.cat/api/issues/search?componentKeys=%s&types=CODE_SMELL,BUG&severities=CRITICAL&ps=100"