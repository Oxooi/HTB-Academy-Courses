
<h1>SQL Statements</h1>
<hr/>
<p>Now that we understand how to use the <code>mysql</code> utility and create databases and tables, let us look at some of the essential SQL statements and their uses.</p>
<hr/>
<h2>INSERT Statement</h2>
<p>The <a href="https://dev.mysql.com/doc/refman/8.0/en/insert.html">INSERT</a> statement is used to add new records to a given table. The statement following the below syntax:</p>
<pre><code class="language-sql">INSERT INTO table_name VALUES (column1_value, column2_value, column3_value, ...);
</code></pre>
<p>The syntax above requires the user to fill in values for all the columns present in the table.</p>
<pre><code class="language-shell-session">mysql&gt; INSERT INTO logins VALUES(1, 'admin', 'p@ssw0rd', '2020-07-02');

Query OK, 1 row affected (0.00 sec)
</code></pre>
<p>The example above shows how to add a new login to the logins table, with appropriate values for each column. However, we can skip filling columns with default values, such as <code>id</code> and <code>date_of_joining</code>. This can be done by specifying the column names to insert values into a table selectively:</p>
<pre><code class="language-sql">INSERT INTO table_name(column2, column3, ...) VALUES (column2_value, column3_value, ...);
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: skipping columns with the 'NOT NULL' constraint will result in an error, as it is a required value.</p>
</div>
</div>
<p>We can do the same to insert values into the <code>logins</code> table:</p>
<pre><code class="language-shell-session">mysql&gt; INSERT INTO logins(username, password) VALUES('administrator', 'adm1n_p@ss');

Query OK, 1 row affected (0.00 sec)
</code></pre>
<p>We inserted a username-password pair in the example above while skipping the <code>id</code> and <code>date_of_joining</code> columns.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: The examples insert cleartext passwords into the table, for demonstration only. This is a bad practice, as passwords should always be hashed/encrypted before storage.</p>
</div>
</div>
<p>We can also insert multiple records at once by separating them with a comma:</p>
<pre><code class="language-shell-session">mysql&gt; INSERT INTO logins(username, password) VALUES ('john', 'john123!'), ('tom', 'tom123!');

Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0
</code></pre>
<p>The query above inserted two new records at once.</p>
<hr/>
<h2>SELECT Statement</h2>
<p>Now that we have inserted data into tables let us see how to retrieve data with the <a href="https://dev.mysql.com/doc/refman/8.0/en/select.html">SELECT</a> statement. This statement can also be used for many other purposes, which we will come across later. The general syntax to view the entire table is as follows:</p>
<pre><code class="language-sql">SELECT * FROM table_name;
</code></pre>
<p>The asterisk symbol (*) acts as a wildcard and selects all the columns. The <code>FROM</code> keyword is used to denote the table to select from. It is possible to view data present in specific columns as well:</p>
<pre><code class="language-sql">SELECT column1, column2 FROM table_name;
</code></pre>
<p>The query above will select data present in column1 and column2 only.</p>
<pre><code class="language-shell-session">mysql&gt; SELECT * FROM logins;

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  1 | admin         | p@ssw0rd   | 2020-07-02 00:00:00 |
|  2 | administrator | adm1n_p@ss | 2020-07-02 11:30:50 |
|  3 | john          | john123!   | 2020-07-02 11:47:16 |
|  4 | tom           | tom123!    | 2020-07-02 11:47:16 |
+----+---------------+------------+---------------------+
4 rows in set (0.00 sec)


mysql&gt; SELECT username,password FROM logins;

+---------------+------------+
| username      | password   |
+---------------+------------+
| admin         | p@ssw0rd   |
| administrator | adm1n_p@ss |
| john          | john123!   |
| tom           | tom123!    |
+---------------+------------+
4 rows in set (0.00 sec)
</code></pre>
<p>The first query in the example above looks at all records present in the logins table. We can see the four records which were entered before. The second query selects just the username and password columns while skipping the other two.</p>
<hr/>
<h2>DROP Statement</h2>
<p>We can use <a href="https://dev.mysql.com/doc/refman/8.0/en/drop-table.html">DROP</a> to remove tables and databases from the server.</p>
<pre><code class="language-shell-session">mysql&gt; DROP TABLE logins;

Query OK, 0 rows affected (0.01 sec)


mysql&gt; SHOW TABLES;

Empty set (0.00 sec)
</code></pre>
<p>As we can see, the table was removed entirely.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">The 'DROP' statement will permanently and completely delete the table with no confirmation, so it should be used with caution.</p>
</div>
</div>
<hr/>
<h2>ALTER Statement</h2>
<p>Finally, We can use <a href="https://dev.mysql.com/doc/refman/8.0/en/alter-table.html">ALTER</a> to change the name of any table and any of its fields or to delete or add a new column to an existing table. The below example adds a new column <code>newColumn</code> to the <code>logins</code> table using <code>ADD</code>:</p>
<pre><code class="language-shell-session">mysql&gt; ALTER TABLE logins ADD newColumn INT;

Query OK, 0 rows affected (0.01 sec)
</code></pre>
<p>To rename a column, we can use <code>RENAME COLUMN</code>:</p>
<pre><code class="language-shell-session">mysql&gt; ALTER TABLE logins RENAME COLUMN newColumn TO newerColumn;

Query OK, 0 rows affected (0.01 sec)
</code></pre>
<p>We can also change a column's datatype with <code>MODIFY</code>:</p>
<pre><code class="language-shell-session">mysql&gt; ALTER TABLE logins MODIFY newerColumn DATE;

Query OK, 0 rows affected (0.01 sec)
</code></pre>
<p>Finally, we can drop a column using <code>DROP</code>:</p>
<pre><code class="language-shell-session">mysql&gt; ALTER TABLE logins DROP newerColumn;

Query OK, 0 rows affected (0.01 sec)
</code></pre>
<p>We can use any of the above statements with any existing table, as long as we have enough privileges to do so.</p>
<hr/>
<h2>UPDATE Statement</h2>
<p>While <code>ALTER</code> is used to change a table's properties, the <a href="https://dev.mysql.com/doc/refman/8.0/en/update.html">UPDATE</a> statement can be used to update specific records within a table, based on certain conditions. Its general syntax is:</p>
<pre><code class="language-sql">UPDATE table_name SET column1=newvalue1, column2=newvalue2, ... WHERE &lt;condition&gt;;
</code></pre>
<p>We specify the table name, each column and its new value, and the condition for updating records. Let us look at an example:</p>
<pre><code class="language-shell-session">mysql&gt; UPDATE logins SET password = 'change_password' WHERE id &gt; 1;

Query OK, 3 rows affected (0.00 sec)
Rows matched: 3  Changed: 3  Warnings: 0


mysql&gt; SELECT * FROM logins;

+----+---------------+-----------------+---------------------+
| id | username      | password        | date_of_joining     |
+----+---------------+-----------------+---------------------+
|  1 | admin         | p@ssw0rd        | 2020-07-02 00:00:00 |
|  2 | administrator | change_password | 2020-07-02 11:30:50 |
|  3 | john          | change_password | 2020-07-02 11:47:16 |
|  4 | tom           | change_password | 2020-07-02 11:47:16 |
+----+---------------+-----------------+---------------------+
4 rows in set (0.00 sec)
</code></pre>
<p>The query above updated all passwords in all records where the id was more significant than 1.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: we have to specify the 'WHERE' clause with UPDATE, in order to specify which records get updated. The 'WHERE' clause will be discussed next.</p>
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
                                to <span class="target-protocol-ip target-protocol-ip-461 text-dark"></span> with user "<span class="text-success">root</span>" and
                                password "<span class="text-danger">password</span>" </p>
<label class="module-question" for="461"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> What is the department number for the 'Development' department?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="d005"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="461" disabled="true" id="btnAnswer461">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint461" data-toggle="modal" id="hintBtn461"><i class="fad fa-life-ring mr-2"></i> Hint
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
