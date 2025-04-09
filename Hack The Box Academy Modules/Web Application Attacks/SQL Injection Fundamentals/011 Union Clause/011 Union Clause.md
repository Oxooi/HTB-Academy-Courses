
<h1>Union Clause</h1>
<hr/>
<p>So far, we have only been manipulating the original query to subvert the web application logic and bypass authentication, using the <code>OR</code> operator and comments. However, another type of SQL injection is injecting entire SQL queries executed along with the original query. This section will demonstrate this by using the MySQL <code>Union</code> clause to do <code>SQL Union Injection</code>.</p>
<hr/>
<h2>Union</h2>
<p>Before we start learning about Union Injection, we should first learn more about the SQL Union clause. The <a href="https://dev.mysql.com/doc/refman/8.0/en/union.html">Union</a> clause is used to combine results from multiple <code>SELECT</code> statements. This means that through a <code>UNION</code> injection, we will be able to <code>SELECT</code> and dump data from all across the DBMS, from multiple tables and databases. Let us try using the <code>UNION</code> operator in a sample database. First, let us see the content of the <code>ports</code> table:</p>
<pre><code class="language-shell-session">mysql&gt; SELECT * FROM ports;

+----------+-----------+
| code     | city      |
+----------+-----------+
| CN SHA   | Shanghai  |
| SG SIN   | Singapore |
| ZZ-21    | Shenzhen  |
+----------+-----------+
3 rows in set (0.00 sec)
</code></pre>
<p>Next, let us see the output of the <code>ships</code> tables:</p>
<pre><code class="language-shell-session">mysql&gt; SELECT * FROM ships;

+----------+-----------+
| Ship     | city      |
+----------+-----------+
| Morrison | New York  |
+----------+-----------+
1 rows in set (0.00 sec)
</code></pre>
<p>Now, let us try to use <code>UNION</code> to combine both results:</p>
<pre><code class="language-shell-session">mysql&gt; SELECT * FROM ports UNION SELECT * FROM ships;

+----------+-----------+
| code     | city      |
+----------+-----------+
| CN SHA   | Shanghai  |
| SG SIN   | Singapore |
| Morrison | New York  |
| ZZ-21    | Shenzhen  |
+----------+-----------+
4 rows in set (0.00 sec)
</code></pre>
<p>As we can see, <code>UNION</code> combined the output of both <code>SELECT</code> statements into one, so entries from the <code>ports</code> table and the <code>ships</code> table were combined into a single output with four rows. As we can see, some of the rows belong to the <code>ports</code> table while others belong to the <code>ships</code> table.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: The data types of the selected columns on all positions should be the same.</p>
</div>
</div>
<hr/>
<h2>Even Columns</h2>
<p>A <code>UNION</code> statement can only operate on <code>SELECT</code> statements with an equal number of columns. For example, if we attempt to <code>UNION</code> two queries that have results with a different number of columns, we get the following error:</p>
<pre><code class="language-shell-session">mysql&gt; SELECT city FROM ports UNION SELECT * FROM ships;

ERROR 1222 (21000): The used SELECT statements have a different number of columns
</code></pre>
<p>The above query results in an error, as the first <code>SELECT</code> returns one column and the second <code>SELECT</code> returns two. Once we have two queries that return the same number of columns, we can use the <code>UNION</code> operator to extract data from other tables and databases.</p>
<p>For example, if the query is:</p>
<pre><code class="language-sql">SELECT * FROM products WHERE product_id = 'user_input'
</code></pre>
<p>We can inject a <code>UNION</code> query into the input, such that rows from another table are returned:</p>
<pre><code class="language-sql">SELECT * from products where product_id = '1' UNION SELECT username, password from passwords-- '
</code></pre>
<p>The above query would return <code>username</code> and <code>password</code> entries from the <code>passwords</code> table, assuming the <code>products</code> table has two columns.</p>
<hr/>
<h2>Un-even Columns</h2>
<p>We will find out that the original query will usually not have the same number of columns as the SQL query we want to execute, so we will have to work around that. For example, suppose we only had one column. In that case, we want to <code>SELECT</code>, we can put junk data for the remaining required columns so that the total number of columns we are <code>UNION</code>ing with remains the same as the original query.</p>
<p>For example, we can use any string as our junk data, and the query will return the string as its output for that column.  If we <code>UNION</code> with the string <code>"junk"</code>, the <code>SELECT</code> query would be <code>SELECT "junk" from passwords</code>, which will always return <code>junk</code>. We can also use numbers. For example, the query <code>SELECT 1 from passwords</code> will always return <code>1</code> as the output.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: When filling other columns with junk data, we must ensure that the data type matches the columns data type, otherwise the query will return an error. For the sake of simplicity, we will use numbers as our junk data, which will also become handy for tracking our payloads positions, as we will discuss later.</p>
</div>
</div>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: For advanced SQL injection, we may want to simply use 'NULL' to fill other columns, as 'NULL' fits all data types.</p>
</div>
</div>
<p>The <code>products</code> table has two columns in the above example, so we have to <code>UNION</code> with two columns.  If we only wanted to get one column 'e.g. <code>username</code>', we have to do <code>username, 2</code>, such that we have the same number of columns:</p>
<pre><code class="language-sql">SELECT * from products where product_id = '1' UNION SELECT username, 2 from passwords
</code></pre>
<p>If we had more columns in the table of the original query, we have to add more numbers to create the remaining required columns. For example, if the original query used <code>SELECT</code> on a table with four columns, our <code>UNION</code> injection would be:</p>
<pre><code class="language-sql">UNION SELECT username, 2, 3, 4 from passwords-- '
</code></pre>
<p>This query would return:</p>
<pre><code class="language-shell-session">mysql&gt; SELECT * from products where product_id UNION SELECT username, 2, 3, 4 from passwords-- '

+-----------+-----------+-----------+-----------+
| product_1 | product_2 | product_3 | product_4 |
+-----------+-----------+-----------+-----------+
|   admin   |    2      |    3      |    4      |
+-----------+-----------+-----------+-----------+
</code></pre>
<p>As we can see, our wanted output of the '<code>UNION SELECT username from passwords</code>' query is found at the first column of the second row, while the numbers filled the remaining columns.</p>
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
                                to <span class="target-protocol-ip target-protocol-ip-467 text-dark"></span> with user "<span class="text-success">root</span>" and
                                password "<span class="text-danger">password</span>" </p>
<label class="module-question" for="467"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Connect to the above MySQL server with the 'mysql' tool, and find the number of records returned when doing a 'Union' of all records in the 'employees' table and all records in the 'departments' table.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer467" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-467">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="467" id="btnAnswer467">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint467" data-toggle="modal" id="hintBtn467"><i class="fad fa-life-ring mr-2"></i> Hint
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
