
<h1>Intro to MySQL</h1>
<hr/>
<p>This module introduces SQL injection through <code>MySQL</code>, and it is crucial to learn more about <code>MySQL</code> and SQL to understand how SQL injections work and utilize them properly. Therefore, this section will cover some of MySQL/SQL's basics and syntax and examples used within MySQL/MariaDB databases.</p>
<hr/>
<h2>Structured Query Language (SQL)</h2>
<p>SQL syntax can differ from one RDBMS to another. However, they are all required to follow the <a href="https://en.wikipedia.org/wiki/ISO/IEC_9075">ISO standard</a> for Structured Query Language. We will be following the MySQL/MariaDB syntax for the examples shown. SQL can be used to perform the following actions:</p>
<ul>
<li>Retrieve data</li>
<li>Update data</li>
<li>Delete data</li>
<li>Create new tables and databases</li>
<li>Add / remove users</li>
<li>Assign permissions to these users</li>
</ul>
<hr/>
<h2>Command Line</h2>
<p>The <code>mysql</code> utility is used to authenticate to and interact with a MySQL/MariaDB database. The <code>-u</code> flag is used to supply the username and the <code>-p</code> flag for the password. The <code>-p</code> flag should be passed empty, so we are prompted to enter the password and do not pass it directly on the command line since it could be stored in cleartext in the bash_history file.</p>
<pre><code class="language-shell-session">[!bash!]$ mysql -u root -p

Enter password: &lt;password&gt;
...SNIP...

mysql&gt; 
</code></pre>
<p>Again, it is also possible to use the password directly in the command, though this should be avoided, as it could lead to the password being kept in logs and terminal history:</p>
<pre><code class="language-shell-session">[!bash!]$ mysql -u root -p&lt;password&gt;

...SNIP...

mysql&gt; 
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: There shouldn't be any spaces between '-p' and the password.</p>
</div>
</div>
<p>The examples above log us in as the superuser, i.e.,"<code>root</code>" with the password "<code>password</code>," to have privileges to execute all commands. Other DBMS users would have certain privileges to which statements they can execute. We can view which privileges we have using the <a href="https://dev.mysql.com/doc/refman/8.0/en/show-grants.html">SHOW GRANTS</a> command which we will be discussing later.</p>
<p>When we do not specify a host, it will default to the <code>localhost</code> server. We can specify a remote host and port using the <code>-h</code> and <code>-P</code> flags.</p>
<pre><code class="language-shell-session">[!bash!]$ mysql -u root -h docker.hackthebox.eu -P 3306 -p 

Enter password: 
...SNIP...

mysql&gt; 
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: The default MySQL/MariaDB port is (3306), but it can be configured to another port. It is specified using an uppercase `P`, unlike the lowercase `p` used for passwords.</p>
</div>
</div>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: To follow along with the examples, try to use the 'mysql' tool on your PwnBox to log in to the DBMS found in the question at the end of the section, using its IP and port. Use 'root' for the username and 'password' for the password.</p>
</div>
</div>
<hr/>
<h2>Creating a database</h2>
<p>Once we log in to the database using the <code>mysql</code> utility, we can start using SQL queries to interact with the DBMS. For example, a new database can be created within the MySQL DBMS using the <a href="https://dev.mysql.com/doc/refman/5.7/en/create-database.html">CREATE DATABASE</a> statement.</p>
<pre><code class="language-shell-session">mysql&gt; CREATE DATABASE users;

Query OK, 1 row affected (0.02 sec)
</code></pre>
<p>MySQL expects command-line queries to be terminated with a semi-colon. The example above created a new database named <code>users</code>. We can view the list of databases with <a href="https://dev.mysql.com/doc/refman/8.0/en/show-databases.html">SHOW DATABASES</a>, and we can switch to the <code>users</code> database with the <code>USE</code> statement:</p>
<pre><code class="language-shell-session">mysql&gt; SHOW DATABASES;

+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| users              |
+--------------------+

mysql&gt; USE users;

Database changed
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">SQL statements aren't case sensitive, which means 'USE users;' and 'use users;' refer to the same command. However, the database name is case sensitive, so we cannot do 'USE USERS;' instead of 'USE users;'. So, it is a good practice to specify statements in uppercase to avoid confusion.</p>
</div>
</div>
<hr/>
<h2>Tables</h2>
<p>DBMS stores data in the form of tables. A table is made up of horizontal rows and vertical columns. The intersection of a row and a column is called a cell. Every table is created with a fixed set of columns, where each column is of a particular data type.</p>
<p>A data type defines what kind of value is to be held by a column. Common examples are <code>numbers</code>, <code>strings</code>, <code>date</code>, <code>time</code>, and <code>binary data</code>. There could be data types specific to DBMS as well. A complete list of data types in MySQL can be found <a href="https://dev.mysql.com/doc/refman/8.0/en/data-types.html">here</a>. For example, let us create a table named <code>logins</code> to store user data, using the <a href="https://dev.mysql.com/doc/refman/8.0/en/creating-tables.html">CREATE TABLE</a> SQL query:</p>
<pre><code class="language-sql">CREATE TABLE logins (
    id INT,
    username VARCHAR(100),
    password VARCHAR(100),
    date_of_joining DATETIME
    );
</code></pre>
<p>As we can see, the <code>CREATE TABLE</code> query first specifies the table name, and then (within parentheses) we specify each column by its name and its data type, all being comma separated. After the name and type, we can specify specific properties, as will be discussed later.</p>
<pre><code class="language-shell-session">mysql&gt; CREATE TABLE logins (
    -&gt;     id INT,
    -&gt;     username VARCHAR(100),
    -&gt;     password VARCHAR(100),
    -&gt;     date_of_joining DATETIME
    -&gt;     );
Query OK, 0 rows affected (0.03 sec)
</code></pre>
<p>The SQL queries above create a table named <code>logins</code> with four columns. The first column, <code>id</code> is an integer. The following two columns, <code>username</code> and <code>password</code> are set to strings of 100 characters each. Any input longer than this will result in an error. The <code>date_of_joining</code> column of type <code>DATETIME</code> stores the date when an entry was added.</p>
<pre><code class="language-shell-session">mysql&gt; SHOW TABLES;

+-----------------+
| Tables_in_users |
+-----------------+
| logins          |
+-----------------+
1 row in set (0.00 sec)
</code></pre>
<p>A list of tables in the current database can be obtained using the <code>SHOW TABLES</code> statement. In addition, the <a href="https://dev.mysql.com/doc/refman/8.0/en/describe.html">DESCRIBE</a> keyword is used to list the table structure with its fields and data types.</p>
<pre><code class="language-shell-session">mysql&gt; DESCRIBE logins;

+-----------------+--------------+
| Field           | Type         |
+-----------------+--------------+
| id              | int          |
| username        | varchar(100) |
| password        | varchar(100) |
| date_of_joining | date         |
+-----------------+--------------+
4 rows in set (0.00 sec)
</code></pre>
<h4>Table Properties</h4>
<p>Within the <code>CREATE TABLE</code> query, there are many <a href="https://dev.mysql.com/doc/refman/8.0/en/create-table.html">properties</a> that can be set for the table and each column. For example, we can set the <code>id</code> column to auto-increment using the <code>AUTO_INCREMENT</code> keyword, which automatically increments the id by one every time a new item is added to the table:</p>
<pre><code class="language-sql">    id INT NOT NULL AUTO_INCREMENT,
</code></pre>
<p>The <code>NOT NULL</code> constraint ensures that a particular column is never left empty 'i.e., required field.' We can also use the <code>UNIQUE</code> constraint to ensures that the inserted item are always unique. For example, if we use it with the <code>username</code> column, we can ensure that no two users will have the same username:</p>
<pre><code class="language-sql">    username VARCHAR(100) UNIQUE NOT NULL,
</code></pre>
<p>Another important keyword is the <code>DEFAULT</code> keyword, which is used to specify the default value. For example, within the <code>date_of_joining</code> column, we can set the default value to <a href="https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_now">Now()</a>, which in MySQL returns the current date and time:</p>
<pre><code class="language-sql">    date_of_joining DATETIME DEFAULT NOW(),
</code></pre>
<p>Finally, one of the most important properties is <code>PRIMARY KEY</code>, which we can use to uniquely identify each record in the table, referring to all data of a record within a table for relational databases, as previously discussed in the previous section. We can make the <code>id</code> column the <code>PRIMARY KEY</code> for this table:</p>
<pre><code class="language-sql">    PRIMARY KEY (id)
</code></pre>
<p>The final <code>CREATE TABLE</code> query will be as follows:</p>
<pre><code class="language-sql">CREATE TABLE logins (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    date_of_joining DATETIME DEFAULT NOW(),
    PRIMARY KEY (id)
    );
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: Allow 10-15 seconds for the servers in the questions to start, to allow enough time for Apache/MySQL to initiate and run.</p>
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
<p class="mb-0 font-size-12"><i class="fad fa-chart-network text-success mr-2 font-size-medium"></i>
                                Authenticate
                                to <span class="target-protocol-ip target-protocol-ip-460 text-dark"></span> with user "<span class="text-success">root</span>" and
                                password "<span class="text-danger">password</span>" </p>
<label class="module-question" for="460"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> Connect to the database using the MySQL client from the command line. Use the 'show databases;' command to list databases in the DBMS. What is the name of the first database?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="employees"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="460" disabled="true" id="btnAnswer460">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint460" data-toggle="modal" id="hintBtn460"><i class="fad fa-life-ring mr-2"></i> Hint
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
