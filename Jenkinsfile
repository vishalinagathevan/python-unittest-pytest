import groovy.json.JsonSlurper

properties([
    durabilityHint('PERFORMANCE_OPTIMIZED'),
    disableResume(),
    [$class: 'BuildDiscarderProperty', strategy: [$class: 'LogRotator',  daysToKeepStr: '90', numToKeepStr: '50']],
    parameters([
        string(
            defaultValue: 'https://github.com/vishalinagathevan/python-unittest-pytest/pull/2',
            name: 'prUrl',
            trim: true,
            description: 'Provide github pull request url: (Example: https://github.com/vishalinagathevan/python-unittest-pytest/pull/2).'
        )
    ])
])

String agent = getEnvValue('PR_MERGE_SLAVE_AGENT_LABEL', '')

node(agent) {

    String prUrl = params.prUrl
    String prApiUrl = getPRApiUrl(prUrl)
    def prInfo
    stage('Fetch PR') {
        prInfo = getPRInfo(prApiUrl)
        echo "prInfo = ${prInfo}"
    }
    def mergeResp = [:]
    stage('Merge PR') {
        if(canMerge(prInfo)) {
            echo "PR is mergeable. Merging.."
            mergeResp = mergePR(prApiUrl)
            echo "mergeResp = ${mergeResp}"
        }else {
            echo "prApiUrl"
            echo "prUrl"
            echo "check"
            echo "PR is not mergeable"
            
        }
    }

    if(mergeResp.containsKey('merged') && mergeResp.merged) {
        stage('Build') {
            // Build your application
            echo 'your-build-command'
        }

        stage('Test') {
            // Run tests
            echo 'your-test-command'
        }

        stage('Package') {
            // Package your application
            echo 'your-package-command'
        }

        stage('Deploy') {
            // Deploy your application to a target environment
            echo 'your-deploy-command'
        }
    }
    
}

/**
* Gets the PR Info for the given PR url.
*/
private def getPRInfo(String prApiUrl) {
    def prInfo = [:]
    def pr = getRequest(prApiUrl)
    prInfo['source'] = pr.head.ref
    prInfo['target'] = pr.base.ref
    prInfo['state'] = pr.state
    prInfo['merged'] = pr.merged
    prInfo['mergeable'] = pr.mergeable
    prInfo['mergeable_state'] = pr.mergeable_state
    prInfo['approvalCount'] = getApprovalCount("${prApiUrl}/reviews")
    prInfo['statusChecksSucceeded'] = statusCheckSuccessful(pr.statuses_url)
    return prInfo
}

/**
* Gets PR API Url
*/
private String getPRApiUrl(String prUrl) {
    String org = getOrg(prUrl)
    String repo = getRepo(prUrl)
    String prId = getPRNumber(prUrl)
    return "https://api.github.com/repos/${org}/${repo}/pulls/${prId}"
}

/**
* Gets PR Approval count
*/
private int getApprovalCount(String prReviewsUrl) {
    def reviews = getRequest(prReviewsUrl)
    def approvedReviews = reviews.findAll { it.state == "APPROVED" }
    return approvedReviews.size()
}

/**
* Checks PR status check successful as per the given status desc
*/
private boolean statusCheckSuccessful(String prStatusesUrl) {
    def statuses = getRequest(prStatusesUrl)
    String statusLables = getEnvValue('PR_MERGE_STATUS_LABELS', '')
    def statusLableList = statusLables.split(',')
    boolean allSucceeded = true
    for (label in statusLableList) {
        def status = statuses.find { it.context == label}
        if(status != null && status.state != 'success') {
            allSucceeded = false
            break
        }
    }
    return allSucceeded
}

/**
* Invokes the get request 
*/
private def getRequest(String requestUrl) {
    def response = httpRequest authentication: 'GITHUB_USER_PASS', httpMode: 'GET',
            validResponseCodes: '200',
            url: requestUrl
    def responseJson = new JsonSlurper().parseText(response.content)
    return responseJson
}

/**
* Invokes the post request 
*/
private def putRequest(requestUrl, requestBody) {
    def response = httpRequest authentication: 'GITHUB_USER_PASS',
            acceptType: 'APPLICATION_JSON', 
            contentType: 'APPLICATION_JSON',
            httpMode: 'PUT',
            requestBody: requestBody,
            validResponseCodes: '200,201,204',
            url: requestUrl
    def responseJson = new JsonSlurper().parseText(response.content)
    return responseJson
}

/**
* Gets PR number from github pr url 
*/
private String getPRNumber(String prUrl) {
    return prUrl.tokenize('/').last()
}

/**
* Gets the org name property from github pr url 
*/
private String getOrg(String prUrl) {
    String urlPart = prUrl.replace("https://github.com/", '')
    return urlPart.tokenize('/').first()
}

/**
* Gets the repo name property from github pr url 
*/
private String getRepo(String prUrl) {
    String urlPart = prUrl.replace("https://github.com/", '')
    return urlPart.tokenize('/')[1]
}

/**
* Check given PR can be merged
*/
private boolean canMerge(prInfo) {
    int approvalcount = Integer.parseInt(getEnvValue('PR_MERGE_APPROVAL_COUNT', '2'))
    return (prInfo.approvalCount == approvalcount
        && prInfo.statusChecksSucceeded
        && prInfo.state == 'open'
        && prInfo.mergeable
        && !prInfo.merged
        && prInfo.mergeable_state == 'clean')
}


/**
* Gets the PR Info for the given PR url.
*/
private def mergePR(String prApiUrl) {
    String mergeReqUrl = "${prApiUrl}/merge"
    String mergeBody = getMergeBody()
    return putRequest(mergeReqUrl, mergeBody)
}

/**
* Gets the PR merge body json.
*/
private String getMergeBody() {
    String mergeTitle = 'PR merged by PR Utility (Jenkins)'
    String mergeDesc = 'PR merged by PR Utility (Jenkins) with required checks'
    return "{\"commit_title\":\"${mergeTitle}\",\"commit_message\":\"${mergeDesc}\"}"
}

/**
* Gets the env variable value
*/
private String getEnvValue(String envKey, String defaultValue='') {
	String envValue = defaultValue
	def envMap = env.getEnvironment()
	envMap.each{ key, value ->
		if (key == envKey) {
			envValue = !isEmpty(value) ? value : defaultValue
			return envValue
		}
	}
	return envValue
}

/**
* Is given string empty
*/
private boolean isEmpty(String input) {
    return !input?.trim()
}