<%
import groovy.json.JsonSlurper	

def summaryFile = new File(build.workspace.toString() + "/testreport/allure-report/widgets/summary.json")
//def message = "summaryFile: ${summaryFile}"
//out.println message

def total = "N/A"
def passed = "N/A"
def failed = "N/A"
def skipped = "N/A"

if (summaryFile.exists()) {
    //out.println "summary file exists"
    def json = new JsonSlurper().parse(summaryFile)
    total = json.statistic.total
    passed = json.statistic.passed
    failed = json.statistic.failed
    skipped = json.statistic.skipped
    //out.println "total:    ${total}"
    //out.println "passed:   ${passed}"
    //out.println "failed:   ${failed}"
    //out.println "skipped:  ${skipped}"
}
//else {out.println "summary file doesn't exist!"}
%>

<html>
<body style="font-family: Arial;">

<h2>Build #${build.number} - Test Summary</h2>

<p>
<b>Job:</b> ${project.name} <br/>
<b>Status:</b> ${build.result} <br/>
<b>Build URL:</b> <a href="${rooturl}${build.url}">${rooturl}${build.url}</a>
</p>

<h3>Test Summary</h3>

<table border="1" cellpadding="6" cellspacing="0">
<tr>
    <th>Total</th>
    <th style="color:green;">Passed</th>
    <th style="color:red;">Failed</th>
    <th>Skipped</th>
</tr>
<tr>
    <td>${total}</td>
    <td>${passed}</td>
    <td>${failed}</td>
    <td>${skipped}</td>
</tr>
</table>

<h3>Allure Report</h3>
<p>
<a href="${rooturl}${build.url}allure" 
   style="background:#28a745;color:white;padding:10px 15px;text-decoration:none;">
   View Allure Report
</a>
</p>

</body>
</html>
