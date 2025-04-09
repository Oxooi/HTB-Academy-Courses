
<h1>MySQL</h1>
<hr/>
<p><code>MySQL</code> is an open-source SQL relational database management system developed and supported by Oracle. A database is simply a structured collection of data organized for easy use and retrieval. The database system can quickly process large amounts of data with high performance. Within the database, data storage is done in a manner to take up as little space as possible. The database is controlled using the <a href="https://www.w3schools.com/sql/sql_intro.asp">SQL database language</a>. MySQL works according to the <code>client-server principle</code> and consists of a MySQL server and one or more MySQL clients. The MySQL server is the actual database management system. It takes care of data storage and distribution. The data is stored in tables with different columns, rows, and data types. These databases are often stored in a single file with the file extension <code>.sql</code>, for example, like <code>wordpress.sql</code>.</p>
<h4>MySQL Clients</h4>
<p>The MySQL clients can retrieve and edit the data using structured queries to the database engine. Inserting, deleting, modifying, and retrieving data, is done using the SQL database language. Therefore, MySQL is suitable for managing many different databases to which clients can send multiple queries simultaneously. Depending on the use of the database, access is possible via an internal network or the public Internet.</p>
<p>One of the best examples of database usage is the CMS WordPress. WordPress stores all created posts, usernames, and passwords in their own database, which is only accessible from the localhost. However, as explained in more detail in the module <a href="https://academy.hackthebox.com/course/preview/introduction-to-web-applications">Introduction to Web Applications</a>, there are database structures that are distributed across multiple servers also.</p>
<h4>MySQL Databases</h4>
<p>MySQL is ideally suited for applications such as <code>dynamic websites</code>, where efficient syntax and high response speed are essential. It is often combined with a Linux OS, PHP, and an Apache web server and is also known in this combination as <a href="https://en.wikipedia.org/wiki/LAMP_(software_bundle)">LAMP</a> (Linux, Apache, MySQL, PHP), or when using Nginx, as <a href="https://lemp.io/">LEMP</a>. In a web hosting with MySQL database, this serves as a central instance in which content required by PHP scripts is stored. Among these are:</p>
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
<td>Headers</td>
<td>Texts</td>
<td>Meta tags</td>
<td>Forms</td>
</tr>
<tr>
<td>Customers</td>
<td>Usernames</td>
<td>Administrators</td>
<td>Moderators</td>
</tr>
<tr>
<td>Email addresses</td>
<td>User information</td>
<td>Permissions</td>
<td>Passwords</td>
</tr>
<tr>
<td>External/Internal links</td>
<td>Links to Files</td>
<td>Specific contents</td>
<td>Values</td>
</tr>
</tbody>
</table>
<p>Sensitive data such as passwords can be stored in their plain-text form by MySQL; however, they are generally encrypted beforehand by the PHP scripts using secure methods such as <a href="https://en.citizendium.org/wiki/One-way_encryption">One-Way-Encryption</a>.</p>
<h4>MySQL Commands</h4>
<p>A MySQL database translates the commands internally into executable code and performs the requested actions. The web application informs the user if an error occurs during processing, which various <code>SQL injections</code> can provoke. Often, these error descriptions contain important information and confirm, among other things, that the web application interacts with the database in a different way than the developers intended.</p>
<p>The web application sends the generated information back to the client if the data is processed correctly. This information can be the data extracts from a table or records needed for further processing with logins, search functions, etc. SQL commands can display, modify, add or delete rows in tables. In addition, SQL can also change the structure of tables, create or delete relationships and indexes, and manage users.</p>
<p><code>MariaDB</code>, which is often connected with MySQL, is a fork of the original MySQL code. This is because the chief developer of MySQL left the company <code>MySQL AB</code> after it was acquired by <code>Oracle</code> and developed another open-source SQL database management system based on the source code of MySQL and called it MariaDB.</p>
<hr/>
<h2>Default Configuration</h2>
<p>The management of SQL databases and their configurations is a vast topic. It is so large that entire professions, such as <code>database administrator</code>, deal with almost nothing but databases. These structures become very large quickly, and their planning can become complicated. Among other things, DB management is a core competency for <code>software developers</code> but also <code>information security analysts</code>. To cover this area completely would go beyond the scope of this module. Therefore, we recommend setting up a MySQL/MariaDB instance to experiment with the various configurations to understand the available functionality and configuration options better. Let us have a look at the default configuration of MySQL.</p>
<h4>Default Configuration</h4>
<pre><code class="language-shell-session">[!bash!]$ sudo apt install mysql-server -y
[!bash!]$ cat /etc/mysql/mysql.conf.d/mysqld.cnf | grep -v "#" | sed -r '/^\s*$/d'

[client]
port		= 3306
socket		= /var/run/mysqld/mysqld.sock

[mysqld_safe]
pid-file	= /var/run/mysqld/mysqld.pid
socket		= /var/run/mysqld/mysqld.sock
nice		= 0

[mysqld]
skip-host-cache
skip-name-resolve
user		= mysql
pid-file	= /var/run/mysqld/mysqld.pid
socket		= /var/run/mysqld/mysqld.sock
port		= 3306
basedir		= /usr
datadir		= /var/lib/mysql
tmpdir		= /tmp
lc-messages-dir	= /usr/share/mysql
explicit_defaults_for_timestamp

symbolic-links=0

!includedir /etc/mysql/conf.d/
</code></pre>
<hr/>
<h2>Dangerous Settings</h2>
<p>Many things can be misconfigured with MySQL. We can look in more detail at the <a href="https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html">MySQL reference</a> to determine which options can be made in the server configuration. The main options that are security-relevant are:</p>
<table>
<thead>
<tr>
<th><strong>Settings</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>user</code></td>
<td>Sets which user the MySQL service will run as.</td>
</tr>
<tr>
<td><code>password</code></td>
<td>Sets the password for the MySQL user.</td>
</tr>
<tr>
<td><code>admin_address</code></td>
<td>The IP address on which to listen for TCP/IP connections on the administrative network interface.</td>
</tr>
<tr>
<td><code>debug</code></td>
<td>This variable indicates the current debugging settings</td>
</tr>
<tr>
<td><code>sql_warnings</code></td>
<td>This variable controls whether single-row INSERT statements produce an information string if warnings occur.</td>
</tr>
<tr>
<td><code>secure_file_priv</code></td>
<td>This variable is used to limit the effect of data import and export operations.</td>
</tr>
</tbody>
</table>
<p>The settings <code>user</code>, <code>password</code>, and <code>admin_address</code> are security-relevant because the entries are made in plain text. Often, the rights for the configuration file of the MySQL server are not assigned correctly. If we get another way to read files or even a shell, we can see the file and the username and password for the MySQL server. Suppose there are no other security measures to prevent unauthorized access. In that case, the entire database and all the existing customers' information, email addresses, passwords, and personal data can be viewed and even edited.</p>
<p>The <code>debug</code> and <code>sql_warnings</code> settings provide verbose information output in case of errors, which are essential for the administrator but should not be seen by others. This information often contains sensitive content, which could be detected by trial and error to identify further attack possibilities. These error messages are often displayed directly on web applications. Accordingly, the SQL injections could be manipulated even to have the MySQL server execute system commands. This is discussed and shown in the module <a href="https://academy.hackthebox.com/course/preview/sql-injection-fundamentals">SQL Injection Fundamentals</a> and <a href="https://academy.hackthebox.com/course/preview/sqlmap-essentials">SQLMap Essentials</a>.</p>
<hr/>
<h2>Footprinting the Service</h2>
<p>There are many reasons why a MySQL server could be accessed from an external network. Nevertheless, it is far from being one of the best practices, and we can always find databases that we can reach. Often, these settings were only meant to be temporary but were forgotten by the administrators. This server setup could also be used as a workaround due to a technical problem. Usually, the MySQL server runs on <code>TCP port 3306</code>, and we can scan this port with <code>Nmap</code> to get more detailed information.</p>
<h4>Scanning MySQL Server</h4>
<pre><code class="language-shell-session">[!bash!]$ sudo nmap 10.129.14.128 -sV -sC -p3306 --script mysql*

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-21 00:53 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00021s latency).

PORT     STATE SERVICE     VERSION
3306/tcp open  nagios-nsca Nagios NSCA
| mysql-brute: 
|   Accounts: 
|     root:&lt;empty&gt; - Valid credentials
|_  Statistics: Performed 45010 guesses in 5 seconds, average tps: 9002.0
|_mysql-databases: ERROR: Script execution failed (use -d to debug)
|_mysql-dump-hashes: ERROR: Script execution failed (use -d to debug)
| mysql-empty-password: 
|_  root account has empty password
| mysql-enum: 
|   Valid usernames: 
|     root:&lt;empty&gt; - Valid credentials
|     netadmin:&lt;empty&gt; - Valid credentials
|     guest:&lt;empty&gt; - Valid credentials
|     user:&lt;empty&gt; - Valid credentials
|     web:&lt;empty&gt; - Valid credentials
|     sysadmin:&lt;empty&gt; - Valid credentials
|     administrator:&lt;empty&gt; - Valid credentials
|     webadmin:&lt;empty&gt; - Valid credentials
|     admin:&lt;empty&gt; - Valid credentials
|     test:&lt;empty&gt; - Valid credentials
|_  Statistics: Performed 10 guesses in 1 seconds, average tps: 10.0
| mysql-info: 
|   Protocol: 10
|   Version: 8.0.26-0ubuntu0.20.04.1
|   Thread ID: 13
|   Capabilities flags: 65535
|   Some Capabilities: SupportsLoadDataLocal, SupportsTransactions, Speaks41ProtocolOld, LongPassword, DontAllowDatabaseTableColumn, Support41Auth, IgnoreSigpipes, SwitchToSSLAfterHandshake, FoundRows, InteractiveClient, Speaks41ProtocolNew, ConnectWithDatabase, IgnoreSpaceBeforeParenthesis, LongColumnFlag, SupportsCompression, ODBCClient, SupportsMultipleStatments, SupportsAuthPlugins, SupportsMultipleResults
|   Status: Autocommit
|   Salt: YTSgMfqvx\x0F\x7F\x16\&amp;\x1EAeK&gt;0
|_  Auth Plugin Name: caching_sha2_password
|_mysql-users: ERROR: Script execution failed (use -d to debug)
|_mysql-variables: ERROR: Script execution failed (use -d to debug)
|_mysql-vuln-cve2012-2122: ERROR: Script execution failed (use -d to debug)
MAC Address: 00:00:00:00:00:00 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.21 seconds
</code></pre>
<p>As with all our scans, we must be careful with the results and manually confirm the information obtained because some of the information might turn out to be a false-positive. This scan above is an excellent example of this, as we know for a fact that the target MySQL server does not use an empty password for the user <code>root</code>, but a fixed password. We can test this with the following command:</p>
<h4>Interaction with the MySQL Server</h4>
<pre><code class="language-shell-session">[!bash!]$ mysql -u root -h 10.129.14.132

ERROR 1045 (28000): Access denied for user 'root'@'10.129.14.1' (using password: NO)
</code></pre>
<p>For example, if we use a password that we have guessed or found through our research, we will be able to log in to the MySQL server and execute some commands.</p>
<pre><code class="language-shell-session">[!bash!]$ mysql -u root -pP4SSw0rd -h 10.129.14.128

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 150165
Server version: 8.0.27-0ubuntu0.20.04.1 (Ubuntu)                                                         
Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.                                     
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.                           
      
MySQL [(none)]&gt; show databases;                                                                          
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.006 sec)


MySQL [(none)]&gt; select version();
+-------------------------+
| version()               |
+-------------------------+
| 8.0.27-0ubuntu0.20.04.1 |
+-------------------------+
1 row in set (0.001 sec)


MySQL [(none)]&gt; use mysql;
MySQL [mysql]&gt; show tables;
+------------------------------------------------------+
| Tables_in_mysql                                      |
+------------------------------------------------------+
| columns_priv                                         |
| component                                            |
| db                                                   |
| default_roles                                        |
| engine_cost                                          |
| func                                                 |
| general_log                                          |
| global_grants                                        |
| gtid_executed                                        |
| help_category                                        |
| help_keyword                                         |
| help_relation                                        |
| help_topic                                           |
| innodb_index_stats                                   |
| innodb_table_stats                                   |
| password_history                                     |
...SNIP...
| user                                                 |
+------------------------------------------------------+
37 rows in set (0.002 sec)
</code></pre>
<p>If we look at the existing databases, we will see several already exist. The most important databases for the MySQL server are the <code>system schema</code> (<code>sys</code>) and <code>information schema</code> (<code>information_schema</code>). The system schema contains tables, information, and metadata necessary for management. More about this database can be found in the <a href="https://dev.mysql.com/doc/refman/8.0/en/system-schema.html#:~:text=The%20mysql%20schema%20is%20the,used%20for%20other%20operational%20purposes">reference manual</a> of MySQL.</p>
<pre><code class="language-shell-session">mysql&gt; use sys;
mysql&gt; show tables;  

+-----------------------------------------------+
| Tables_in_sys                                 |
+-----------------------------------------------+
| host_summary                                  |
| host_summary_by_file_io                       |
| host_summary_by_file_io_type                  |
| host_summary_by_stages                        |
| host_summary_by_statement_latency             |
| host_summary_by_statement_type                |
| innodb_buffer_stats_by_schema                 |
| innodb_buffer_stats_by_table                  |
| innodb_lock_waits                             |
| io_by_thread_by_latency                       |
...SNIP...
| x$waits_global_by_latency                     |
+-----------------------------------------------+


mysql&gt; select host, unique_users from host_summary;

+-------------+--------------+                   
| host        | unique_users |                   
+-------------+--------------+                   
| 10.129.14.1 |            1 |                   
| localhost   |            2 |                   
+-------------+--------------+                   
2 rows in set (0,01 sec)  
</code></pre>
<p>The <code>information schema</code> is also a database that contains metadata. However, this metadata is mainly retrieved from the <code>system schema</code> database. The reason for the existence of these two is the ANSI/ISO standard that has been established. <code>System schema</code> is a Microsoft system catalog for SQL servers and contains much more information than the <code>information schema</code>.</p>
<p>Some of the commands we should remember and write down for working with MySQL databases are described below in the table.</p>
<table>
<thead>
<tr>
<th><strong>Command</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>mysql -u &lt;user&gt; -p&lt;password&gt; -h &lt;IP address&gt;</code></td>
<td>Connect to the MySQL server. There should <strong>not</strong> be a space between the '-p' flag, and the password.</td>
</tr>
<tr>
<td><code>show databases;</code></td>
<td>Show all databases.</td>
</tr>
<tr>
<td><code>use &lt;database&gt;;</code></td>
<td>Select one of the existing databases.</td>
</tr>
<tr>
<td><code>show tables;</code></td>
<td>Show all available tables in the selected database.</td>
</tr>
<tr>
<td><code>show columns from &lt;table&gt;;</code></td>
<td>Show all columns in the selected table.</td>
</tr>
<tr>
<td><code>select * from &lt;table&gt;;</code></td>
<td>Show everything in the desired table.</td>
</tr>
<tr>
<td><code>select * from &lt;table&gt; where &lt;column&gt; = "&lt;string&gt;";</code></td>
<td>Search for needed <code>string</code> in the desired table.</td>
</tr>
</tbody>
</table>
<p>We must know how to interact with different databases. Therefore, we recommend installing and configuring a MySQL server on one of our VMs for experimentation. There is also a widely covered <a href="https://dev.mysql.com/doc/refman/8.0/en/general-security-issues.html">security issues</a> section in the reference manual that covers best practices for securing MySQL servers. We should use this when setting up our MySQL server to understand better why something might not work.</p>
<div class="my-3 p-3 vpn-switch-card" id="vpn-switch">
<p class="font-size-14 color-white mb-0">VPN Servers</p>
<p class="font-size-13 mb-0">
<i class="fas fa-exclamation-triangle text-warning"></i><span class="color-white ml-1">Warning:</span> Each
                    time you "Switch",
                    your connection keys are regenerated and you must re-download your VPN connection file.
                </p>
<p class="font-size-13 mb-0">
                    All VM instances associated with the old VPN Server will be terminated when switching to
                    a new VPN server. <br/>
                    Existing PwnBox instances will automatically switch to the new VPN server.</p>
<div class="row mb-3">
<div class="col-12 mt-2">
<div class="d-none justify-content-center vpn-loader">
<div class="spinner-border text-success" role="status">
<span class="sr-only">Switching VPN...</span>
</div>
</div>
<select aria-label="vpn server" class="selectpicker custom-form-control vpnSelector badge-select" title="Select VPN Server">
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 6 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt; &lt;span class='recommended'&gt; &lt;img src='/images/sparkles-solid.svg'/&gt;Recommended&lt;/span&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="30" value="17">US Academy 6</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 5 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="31" value="16">US Academy 5</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 4 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="32" value="13">US Academy 4</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 1 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="33" value="4">US Academy 1</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 2 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="33" value="5">US Academy 2</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 5 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt; &lt;span class='recommended'&gt; &lt;img src='/images/sparkles-solid.svg'/&gt;Recommended&lt;/span&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="37" value="12">EU Academy 5</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 3 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="38" value="9">US Academy 3</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 2 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="39" selected="" value="2">EU Academy 2</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 1 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="40" value="1">EU Academy 1</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 3 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="41" value="14">EU Academy 3</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 4 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="43" value="11">EU Academy 4</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 6 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="47" value="15">EU Academy 6</option>
</select>
<p class="font-size-14 color-white mb-0 mt-2">PROTOCOL</p>
<div class="d-flex">
<div class="custom-control custom-radio custom-control-inline">
<input checked="" class="custom-control-input" id="rd_1" name="vpn-protocol" type="radio" value="udp"/>
<label class="custom-control-label green font-size-14" for="rd_1">UDP
                                    1337</label>
</div>
<div class="custom-control custom-radio">
<input class="custom-control-input" id="rd_2" name="vpn-protocol" type="radio" value="tcp"/>
<label class="custom-control-label green font-size-14" for="rd_2">TCP
                                    443</label>
</div>
</div>
<div class="d-flex justify-content-center">
<button class="btn btn-outline-success btn-lg download-vpn-settings mt-3 px-5 font-size-12">
                                DOWNLOAD VPN CONNECTION FILE
                            </button>
</div>
</div>
</div>
</div>
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
                            <button class="extendTargetSystemBtn btn btn-light btn-sm module-button" data-title="Extend Life by 1 hour (up to 6 hours total lifespan)" data-toggle="tooltip">
<i class="fa fa-plus text-success extend-icon"></i>
<div class="extend-loader spinner-border spinner-border-small text-success d-none" role="status">
</div>
</button>
<button class="text-danger btn btn-light btn-sm module-button font-size-16 mb-1" data-target="#terminateVmModal" data-toggle="modal">
                    Terminate <span class="fa-regular fa-x text-danger font-size-13 ml-2"></span>
</button>
</span>
</div>
</p>
</div>
<div class="col-3 text-right float-right">
<button class="btn btn-light bg-color-blue-nav mt-2 w-100 d-flex align-items-center" data-target="#cheatSheetModal" data-toggle="modal">
<div><i class="fad fa-file-alt mr-2"></i></div>
<div class="text-center w-100 ml-1">Cheat Sheet</div>
</button>
<a class="btn btn-light bg-color-blue-nav mt-2 d-flex align-items-center" data-title='Key is already installed in "My Workstation"' data-toggle="tooltip" href="https://academy.hackthebox.com/vpn/key">
<div><i class="fad fa-chart-network mr-2"></i></div>
<div class="text-center w-100">Download VPN Connection File</div>
</a>
</div>
</div>
<div>
<div>
<label class="module-question" for="934"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Enumerate the MySQL server and determine the version in use. (Format: MySQL X.X.XX)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer934" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-934">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="934" id="btnAnswer934">
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
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="935"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> During our penetration test, we found weak credentials "robin:robin". We should try these against the MySQL server. What is the email address of the customer "Otto Lang"?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer935" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-935">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="935" id="btnAnswer935">
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
