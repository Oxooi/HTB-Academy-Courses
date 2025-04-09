
<h1>Burp Scanner</h1>
<hr/>
<p>An essential feature of web proxy tools is their web scanners. Burp Suite comes with <code>Burp Scanner</code>, a powerful scanner for various types of web vulnerabilities, using a <code>Crawler</code> for building the website structure, and <code>Scanner</code> for passive and active scanning.</p>
<p>Burp Scanner is a Pro-Only feature, and it is not available in the free Community version of Burp Suite. However, given the wide scope that Burp Scanner covers and the advanced features it includes, it makes it an enterprise-level tool, and as such, it is expected to be a paid feature.</p>
<hr/>
<h2>Target Scope</h2>
<p>To start a scan in Burp Suite, we have the following options:</p>
<ol>
<li>Start scan on a specific request from Proxy History</li>
<li>Start a new scan on a set of targets</li>
<li>Start a scan on items in-scope</li>
</ol>
<p>To start a scan on a specific request from Proxy History, we can right-click on it once we locate it in the history, and then select <code>Scan</code> to be able to configure the scan before we run it, or select <code>Passive/Active Scan</code> to quickly start a scan with the default configurations:</p>
<p><img alt="Scan Request" src="https://academy.hackthebox.com/storage/modules/110/burp_scan_request.jpg"/></p>
<p>We may also click on the <code>New Scan</code> button on the <code>Dashboard</code> tab, which would open the <code>New Scan</code> configuration window to configure a scan on a set of custom targets. Instead of creating a custom scan from scratch, let's see how we can utilize the scope to properly define what's included/excluded from our scans using the <code>Target Scope</code>. The <code>Target Scope</code> can be utilized with all Burp features to define a custom set of targets that will be processed. Burp also allows us to limit Burp to in-scope items to save resources by ignoring any out-of-scope URLs.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: We will be scanning the web application from the exercise found at the end of the next section. If you obtain a license to use Burp Pro, you may spawn the target at the end of the next section and follow along here.</p>
</div>
</div>
<p>If we go to (<code>Target&gt;Site map</code>), it will show a listing of all directories and files burp has detected in various requests that went through its proxy:</p>
<p><img alt="Site Map" src="https://academy.hackthebox.com/storage/modules/110/burp_site_map_before.jpg"/></p>
<p>To add an item to our scope, we can right-click on it and select <code>Add to scope</code>:</p>
<p><img alt="Add to Scope" src="https://academy.hackthebox.com/storage/modules/110/burp_add_to_scope.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: When you add the first item to your scope, Burp will give you the option to restrict its features to in-scope items only, and ignore any out-of-scope items.</p>
</div>
</div>
<p>We may also need to exclude a few items from scope if scanning them may be dangerous or may end our session 'like a logout function'. To exclude an item from our scope, we can right-click on any in-scope item and select <code>Remove from scope</code>. Finally, we can go to (<code>Target&gt;Scope</code>) to view the details of our scope. Here, we may also add/remove other items and use advanced scope control to specify regex patterns to be included/excluded.</p>
<p><img alt="Target Scope" src="https://academy.hackthebox.com/storage/modules/110/burp_target_scope.jpg"/></p>
<hr/>
<h2>Crawler</h2>
<p>Once we have our scope ready, we can go to the <code>Dashboard</code> tab and click on <code>New Scan</code> to configure our scan, which would be automatically populated with our in-scope items:</p>
<p><img alt="New Scan" src="https://academy.hackthebox.com/storage/modules/110/burp_new_scan.jpg"/></p>
<p>We see that Burp gives us two scanning options: <code>Crawl and Audit</code> and <code>Crawl</code>. A Web Crawler navigates a website by accessing any links found in its pages, accessing any forms, and examining any requests it makes to build a comprehensive map of the website. In the end, Burp Scanner presents us with a map of the target, showing all publicly accessible data in a single place. If we select <code>Crawl and Audit</code>, Burp will run its scanner after its Crawler (as we will see later).</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: A Crawl scan only follows and maps links found in the page we specified, and any pages found on it. It does not perform a fuzzing scan to identify pages that are never referenced, like what dirbuster or ffuf would do. This can be done with Burp Intruder or Content Discovery, and then added to scope, if needed.</p>
</div>
</div>
<p>Let us select <code>Crawl</code> as a start and go to the <code>Scan configuration</code> tab to configure our scan. From here, we may choose to click on <code>New</code> to build a custom configuration, which would allow us to set the configurations like the crawling speed or limit, whether Burp will attempt to log in to any login forms, and a few other configurations. For the sake of simplicity, we will click on the <code>Select from library</code> button, which gives us a few preset configurations we can pick from (or custom configurations we previously defined):</p>
<p><img alt="Crawl Config" src="https://academy.hackthebox.com/storage/modules/110/burp_crawl_config.jpg"/></p>
<p>We will select the <code>Crawl strategy - fastest</code> option and continue to the <code>Application login</code> tab. In this tab, we can add a set of credentials for Burp to attempt in any Login forms/fields it can find. We may also record a set of steps by performing a manual login in the pre-configured browser, such that Burp knows what steps to follow to gain a login session. This can be essential if we were running our scan using an authenticated user, which would allow us to cover parts of the web application that Burp may otherwise not have access to. As we do not have any credentials, we'll leave it empty.</p>
<p>With that, we can click on the <code>Ok</code> button to start our Crawl scan. Once our scan starts, we can see its progress in the <code>Dashboard</code> tab under <code>Tasks</code>:</p>
<p><img alt="Crawl Config" src="https://academy.hackthebox.com/storage/modules/110/burp_crawl_progress.jpg"/></p>
<p>We may also click on the <code>View details</code> button on the tasks to see more details about the running scan or click on the gear icon to customize our scan configurations further. Finally, once our scan is complete, we'll see <code>Crawl Finished</code> in the task info, and then we can go back to (<code>Target&gt;Site map</code>) to view the updated site map:</p>
<p><img alt="Site Map" src="https://academy.hackthebox.com/storage/modules/110/burp_site_map_after.jpg"/></p>
<hr/>
<h2>Passive Scanner</h2>
<p>Now that the site map is fully built, we may select to scan this target for potential vulnerabilities. When we choose the <code>Crawl and Audit</code> option in the <code>New Scan</code> dialog, Burp will perform two types of scans: A <code>Passive Vulnerability Scan</code> and an <code>Active Vulnerability Scan</code>.</p>
<p>Unlike an Active Scan, a Passive Scan does not send any new requests but analyzes the source of pages already visited in the target/scope and then tries to identify <code>potential</code> vulnerabilities. This is very useful for a quick analysis of a specific target, like missing HTML tags or potential DOM-based XSS vulnerabilities. However, without sending any requests to test and verify these vulnerabilities, a Passive Scan can only suggest a list of potential vulnerabilities. Still, Burp Passive Scanner does provide a level of <code>Confidence</code> for each identified vulnerability, which is also helpful for prioritizing potential vulnerabilities.</p>
<p>Let's start by trying to perform a Passive Scan only. To do so, we can once again select the target in (<code>Target&gt;Site map</code>) or a request in Burp Proxy History, then right-click on it and select <code>Do passive scan</code> or <code>Passively scan this target</code>. The Passive Scan will start running, and its task can be seen in the <code>Dashboard</code> tab as well. Once the scan finishes, we can click on <code>View Details</code> to review identified vulnerabilities and then select the <code>Issue activity</code> tab:</p>
<p><img alt="Passive Scan" src="https://academy.hackthebox.com/storage/modules/110/burp_passive_scan.jpg"/></p>
<p>Alternately, we can view all identified issues in the <code>Issue activity</code> pane on the <code>Dashboard</code> tab. As we can see, it shows the list of potential vulnerabilities, their severity, and their confidence. Usually, we want to look for vulnerabilities with <code>High</code> severity and <code>Certain</code> confidence. However, we should include all levels of severity and confidence for very sensitive web applications, with a special focus on <code>High</code> severity and <code>Confident/Firm</code> confidence.</p>
<hr/>
<h2>Active Scanner</h2>
<p>We finally reach the most powerful part of Burp Scanner, which is its Active Vulnerability Scanner. An active scan runs a more comprehensive scan than a Passive Scan, as follows:</p>
<ol>
<li>
<p>It starts by running a Crawl and a web fuzzer (like dirbuster/ffuf) to identify all possible pages</p>
</li>
<li>
<p>It runs a Passive Scan on all identified pages</p>
</li>
<li>
<p>It checks each of the identified vulnerabilities from the Passive Scan and sends requests to verify them</p>
</li>
<li>
<p>It performs a JavaScript analysis to identify further potential vulnerabilities</p>
</li>
<li>
<p>It fuzzes various identified insertion points and parameters to look for common vulnerabilities like XSS, Command Injection, SQL Injection, and other common web vulnerabilities</p>
</li>
</ol>
<p>The Burp Active scanner is considered one of the best tools in that field and is frequently updated to scan for newly identified web vulnerabilities by the Burp research team.</p>
<p>We can start an Active Scan similarly to how we began a Passive Scan by selecting the <code>Do active scan</code> from the right-click menu on a request in Burp Proxy History. Alternatively, we can run a scan on our scope with the <code>New Scan</code> button in the <code>Dashboard</code> tab, which would allow us to configure our active scan. This time, we will select the <code>Crawl and Audit</code> option, which would perform all of the above points and everything we have discussed so far.</p>
<p>We may also set the Crawl configurations (as we discussed earlier) and the Audit configurations. The Audit configurations enable us to select what type of vulnerabilities we want to scan (defaults to all), where the scanner would attempt inserting its payloads, in addition to many other useful configurations. Once again, we can select a configuration preset with the <code>Select from library</code> button. For our test, as we are interested in <code>High</code> vulnerabilities that may allow us to gain control over the backend server, we will select the <code>Audit checks - critical issues only</code> option. Finally, we may add login details, as we previously saw with the Crawl configurations.</p>
<p>Once we select our configurations, we can click on the <code>Ok</code> button to start the scan, and the active scan task should be added in the <code>Tasks</code> pane in the <code>Dashboard</code> tab:</p>
<p><img alt="Active Scan" src="https://academy.hackthebox.com/storage/modules/110/burp_active_scan.jpg"/></p>
<p>The scan will run all of the steps mentioned above, which is why it will take significantly longer to finish than our earlier scans depending on the configurations we selected. As the scan is running, we can view the various requests it is making by clicking on the <code>View details</code> button and selecting the <code>Logger</code> tab, or by going to the <code>Logger</code> tab in Burp, which shows all requests that went through or were made by Burp:</p>
<p><img alt="Logger" src="https://academy.hackthebox.com/storage/modules/110/burp_logger.jpg"/></p>
<p>Once the scan is done, we can look at the <code>Issue activity</code> pane in the <code>Dashboard</code> tab to view and filter all of the issues identified so far. From the filter above the results, let's select <code>High</code> and <code>Certain</code> and see our filtered results:</p>
<p><img alt="High Vulnerabilities" src="https://academy.hackthebox.com/storage/modules/110/burp_high_vulnerabilities.jpg"/></p>
<p>We see that Burp identified an <code>OS command injection</code> vulnerability, which is ranked with a <code>High</code> severity and <code>Firm</code> confidence. As Burp is firmly confident that this severe vulnerability exists, we can read about it by clicking on it and reading the advisory shown and view the sent request and received response, to be able to know whether the vulnerability can be exploited or how it poses a threat on the webserver:</p>
<p><img alt="Vulnerably Details" src="https://academy.hackthebox.com/storage/modules/110/burp_vuln_details.jpg"/></p>
<hr/>
<h2>Reporting</h2>
<p>Finally, once all of our scans are completed, and all potential issues have been identified, we can go to (<code>Target&gt;Site map</code>), right-click on our target, and select (<code>Issue&gt;Report issues for this host</code>). We will get prompted to select the export type for the report and what information we would like to include in the report. Once we export the report, we can open it in any web browser to view its details:</p>
<p><img alt="Scan Report" src="https://academy.hackthebox.com/storage/modules/110/burp_scan_report.jpg"/></p>
<p>As we can see, Burp's report is very organized and can be customized to only include select issues by severity/confidence. It also shows proof-of-concept details of how to exploit the vulnerability and information on how to remediate it. These reports may be used as supplementary data for the detailed reports that we prepare for our clients or the web application developers when performing a web penetration test or can be stored for our future reference. We should never merely export a report from any penetration tool and submit it to a client as the final deliverable. Instead, the reports and data generated by tools can be helpful as appendix data for clients who may need the raw scan data for remediation efforts or to import into a tracking dashboard.</p>
