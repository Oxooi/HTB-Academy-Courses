
<h1>Database Enumeration</h1>
<hr/>
<p>In the previous sections, we learned about different SQL queries in <code>MySQL</code> and SQL injections and how to use them. This section will put all of that to use and gather data from the database using SQL queries within SQL injections.</p>
<hr/>
<h2>MySQL Fingerprinting</h2>
<p>Before enumerating the database, we usually need to identify the type of DBMS we are dealing with. This is because each DBMS has different queries, and knowing what it is will help us know what queries to use.</p>
<p>As an initial guess, if the webserver we see in HTTP responses is <code>Apache</code> or <code>Nginx</code>, it is a good guess that the webserver is running on Linux, so the DBMS is likely <code>MySQL</code>.  The same also applies to Microsoft DBMS if the webserver is <code>IIS</code>, so it is likely to be <code>MSSQL</code>. However, this is a far-fetched guess, as many other databases can be used on either operating system or web server.  So, there are different queries we can test to fingerprint the type of database we are dealing with.</p>
<p>As we cover <code>MySQL</code> in this module, let us fingerprint <code>MySQL</code> databases.  The following queries and their output will tell us that we are dealing with <code>MySQL</code>:</p>
<table>
<thead>
<tr>
<th>Payload</th>
<th>When to Use</th>
<th>Expected Output</th>
<th>Wrong Output</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>SELECT @@version</code></td>
<td>When we have full query output</td>
<td>MySQL Version 'i.e. <code>10.3.22-MariaDB-1ubuntu1</code>'</td>
<td>In MSSQL it returns MSSQL version. Error with other DBMS.</td>
</tr>
<tr>
<td><code>SELECT POW(1,1)</code></td>
<td>When we only have numeric output</td>
<td><code>1</code></td>
<td>Error with other DBMS</td>
</tr>
<tr>
<td><code>SELECT SLEEP(5)</code></td>
<td>Blind/No Output</td>
<td>Delays page response for 5 seconds and returns <code>0</code>.</td>
<td>Will not delay response with other DBMS</td>
</tr>
</tbody>
</table>
<p>As we saw in the example from the previous section, when we tried <code>@@version</code>, it gave us:</p>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entry includes 10.3.22-MariaDB-1ubuntu1, 3, and 4" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION select 1,@@version,3,4-- -" src="/storage/modules/33/db_version_1.jpg"/>
<p>The output <code>10.3.22-MariaDB-1ubuntu1</code> means that we are dealing with a <code>MariaDB</code> DBMS similar to MySQL. Since we have direct query output, we will not have to test the other payloads. Instead, we can test them and see what we get.</p>
<hr/>
<h2>INFORMATION_SCHEMA Database</h2>
<p>To pull data from tables using <code>UNION SELECT</code>, we need to properly form our <code>SELECT</code> queries. To do so, we need the following information:</p>
<ul>
<li>List of databases</li>
<li>List of tables within each database</li>
<li>List of columns within each table</li>
</ul>
<p>With the above information, we can form our <code>SELECT</code> statement to dump data from any column in any table within any database inside the DBMS. This is where we can utilize the <code>INFORMATION_SCHEMA</code> Database.</p>
<p>The <a href="https://dev.mysql.com/doc/refman/8.0/en/information-schema-introduction.html">INFORMATION_SCHEMA</a> database contains metadata about the databases and tables present on the server. This database plays a crucial role while exploiting SQL injection vulnerabilities. As this is a different database, we cannot call its tables directly with a <code>SELECT</code> statement. If we only specify a table's name for a <code>SELECT</code> statement, it will look for tables within the same database.</p>
<p>So, to reference a table present in another DB, we can use the dot ‘<code>.</code>’ operator. For example, to <code>SELECT</code> a table <code>users</code> present in a database named <code>my_database</code>, we can use:</p>
<pre><code class="language-sql">SELECT * FROM my_database.users;
</code></pre>
<p>Similarly, we can look at tables present in the <code>INFORMATION_SCHEMA</code> Database.</p>
<hr/>
<h2>SCHEMATA</h2>
<p>To start our enumeration, we should find what databases are available on the DBMS. The table <a href="https://dev.mysql.com/doc/refman/8.0/en/information-schema-schemata-table.html">SCHEMATA</a> in the <code>INFORMATION_SCHEMA</code> database contains information about all databases on the server. It is used to obtain database names so we can then query them. The <code>SCHEMA_NAME</code> column contains all the database names currently present.</p>
<p>Let us first test this on a local database to see how the query is used:</p>
<pre><code class="language-shell-session">mysql&gt; SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;

+--------------------+
| SCHEMA_NAME        |
+--------------------+
| mysql              |
| information_schema |
| performance_schema |
| ilfreight          |
| dev                |
+--------------------+
6 rows in set (0.01 sec)
</code></pre>
<p>We see the <code>ilfreight</code> and <code>dev</code> databases.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: The first three databases are default MySQL databases and are present on any server, so we usually ignore them during DB enumeration. Sometimes there's a fourth 'sys' DB as well.</p>
</div>
</div>
<p>Now, let's do the same using a <code>UNION</code> SQL injection, with the following payload:</p>
<pre><code class="language-sql">cn' UNION select 1,schema_name,3,4 from INFORMATION_SCHEMA.SCHEMATA-- -
</code></pre>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entries include information_schema, ilfreight, dev, performance_schema, mysql, all with Port City 3 and Port Volume 4" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION select 1,schema_name,3,4 from INFORMATION_SCHEMA.SCHEMATA-- -" src="/storage/modules/33/ports_dbs.png"/>
<p>Once again, we see two databases, <code>ilfreight</code> and <code>dev</code>, apart from the default ones. Let us find out which database the web application is running to retrieve ports data from.  We can find the current database with the <code>SELECT database()</code> query. We can do this similarly to how we found the DBMS version in the previous section:</p>
<pre><code class="language-sql">cn' UNION select 1,database(),2,3-- -
</code></pre>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entry includes ilfreight, 2, and 3" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION select 1,database(),2,3-- -" src="/storage/modules/33/db_name.jpg"/>
<p>We see that the database name is <code>ilfreight</code>. However, the other database (<code>dev</code>) looks interesting. So, let us try to retrieve the tables from it.</p>
<hr/>
<h2>TABLES</h2>
<p>Before we dump data from the <code>dev</code> database, we need to get a list of the tables to query them with a <code>SELECT</code> statement. To find all tables within a database, we can use the <code>TABLES</code> table in the <code>INFORMATION_SCHEMA</code> Database.</p>
<p>The <a href="https://dev.mysql.com/doc/refman/8.0/en/information-schema-tables-table.html">TABLES</a> table contains information about all tables throughout the database. This table contains multiple columns, but we are interested in the <code>TABLE_SCHEMA</code> and <code>TABLE_NAME</code> columns. The <code>TABLE_NAME</code> column stores table names, while the <code>TABLE_SCHEMA</code> column points to the database each table belongs to. This can be done similarly to how we found the database names. For example, we can use the following payload to find the tables within the <code>dev</code> database:</p>
<pre><code class="language-sql">cn' UNION select 1,TABLE_NAME,TABLE_SCHEMA,4 from INFORMATION_SCHEMA.TABLES where table_schema='dev'-- -
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note how we replaced the numbers '2' and '3' with 'TABLE_NAME' and 'TABLE_SCHEMA', to get the output of both columns in the same query.</p>
</div>
</div>
<img alt="Search interface with a text box containing 'cn' UNION select 1,table_n' and a button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entries include credentials, posts, framework, pages, all with Port City dev and Port Volume 4" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION select 1,TABLE_NAME,TABLE_SCHEMA,4 from INFORMATION_SCHEMA.TABLES where table_schema='dev'-- -" src="/storage/modules/33/ports_tables_1.jpg"/>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: we added a (where table_schema='dev') condition to only return tables from the 'dev' database, otherwise we would get all tables in all databases, which can be many.</p>
</div>
</div>
<p>We see four tables in the dev database, namely <code>credentials</code>, <code>framework</code>, <code>pages</code>, and <code>posts</code>. For example, the <code>credentials</code> table could contain sensitive information to look into it.</p>
<hr/>
<h2>COLUMNS</h2>
<p>To dump the data of the <code>credentials</code> table, we first need to find the column names in the table, which can be found in the <code>COLUMNS</code> table in the <code>INFORMATION_SCHEMA</code> database. The <a href="https://dev.mysql.com/doc/refman/8.0/en/information-schema-columns-table.html">COLUMNS</a> table contains information about all columns present in all the databases. This helps us find the column names to query a table for.  The <code>COLUMN_NAME</code>, <code>TABLE_NAME</code>, and <code>TABLE_SCHEMA</code> columns can be used to achieve this. As we did before, let us try this payload to find the column names in the <code>credentials</code> table:</p>
<pre><code class="language-sql">cn' UNION select 1,COLUMN_NAME,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.COLUMNS where table_name='credentials'-- -
</code></pre>
<img alt="Search interface with a text box containing 'cn' UNION select 1,table_n' and a button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entries include username, password, all with Port City credentials and Port Volume dev" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION select 1,COLUMN_NAME,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.COLUMNS where table_name='credentials'-- -" src="/storage/modules/33/ports_columns_1.jpg"/>
<p>The table has two columns named <code>username</code> and <code>password</code>. We can use this information and dump data from the table.</p>
<hr/>
<h2>Data</h2>
<p>Now that we have all the information, we can form our <code>UNION</code> query to dump data of the <code>username</code> and <code>password</code> columns from the <code>credentials</code> table in the <code>dev</code> database. We can place <code>username</code> and <code>password</code> in place of columns 2 and 3:</p>
<pre><code class="language-sql">cn' UNION select 1, username, password, 4 from dev.credentials-- -
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Remember: don't forget to use the dot operator to refer to the 'credentials' in the 'dev' database, as we are running in the 'ilfreight' database, as previously discussed.</p>
</div>
</div>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entries include admin, dev_admin, api_key, with corresponding Port City values as hashes and Port Volume 4" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION select 1, username, password, 4 from dev.credentials-- -" src="/storage/modules/33/ports_credentials_1.png"/>
<p>We were able to get all the entries in the <code>credentials</code> table, which contains sensitive information such as password hashes and an API key.</p>
<!-- 
<div class="card bg-light">
    <div class="card-body">
        <p class="mb-0">Tip: while we are only focusing on dumping data from other tables and databases using a 'SELECT' statement, there are more advanced techniques to execute arbitrary SQL queries with a 'UNION' SQL injection, like using 'CAST()'. For example, we can do "cn'UNION SELECT 1,CAST(current_user AS NCHAR),3,4-- -", which would execute the "current_user" query. Feel free to test this injection, and try to execute other full SQL queries instead of the 'current_user' used in this example.</p>
    </div>
</div> -->
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
<label class="module-question" for="463"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What is the password hash for 'newuser' stored in the 'users' table in the 'ilfreight' database?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer463" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-463">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="463" id="btnAnswer463">
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
