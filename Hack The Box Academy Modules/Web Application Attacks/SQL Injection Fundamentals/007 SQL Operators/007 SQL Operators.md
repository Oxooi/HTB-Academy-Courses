
<h1>SQL Operators</h1>
<hr/>
<p>Sometimes, expressions with a single condition are not enough to satisfy the user's requirement. For that, SQL supports <a href="https://dev.mysql.com/doc/refman/8.0/en/logical-operators.html">Logical Operators</a> to use multiple conditions at once. The most common logical operators are <code>AND</code>, <code>OR</code>, and <code>NOT</code>.</p>
<hr/>
<h2>AND Operator</h2>
<p>The <code>AND</code> operator takes in two conditions and returns <code>true</code> or <code>false</code> based on their evaluation:</p>
<pre><code class="language-sql">condition1 AND condition2
</code></pre>
<p>The result of the <code>AND</code> operation is <code>true</code> if and only if both <code>condition1</code> and <code>condition2</code> evaluate to <code>true</code>:</p>
<pre><code class="language-shell-session">mysql&gt; SELECT 1 = 1 AND 'test' = 'test';

+---------------------------+
| 1 = 1 AND 'test' = 'test' |
+---------------------------+
|                         1 |
+---------------------------+
1 row in set (0.00 sec)

mysql&gt; SELECT 1 = 1 AND 'test' = 'abc';

+--------------------------+
| 1 = 1 AND 'test' = 'abc' |
+--------------------------+
|                        0 |
+--------------------------+
1 row in set (0.00 sec)
</code></pre>
<p>In MySQL terms, any <code>non-zero</code> value is considered <code>true</code>, and it usually returns the value <code>1</code> to signify <code>true</code>. <code>0</code> is considered <code>false</code>. As we can see in the example above, the first query returned <code>true</code> as both expressions were evaluated as <code>true</code>. However, the second query returned <code>false</code> as the second condition <code>'test' = 'abc'</code> is <code>false</code>.</p>
<hr/>
<h2>OR Operator</h2>
<p>The <code>OR</code> operator takes in two expressions as well, and returns <code>true</code> when at least one of them evaluates to <code>true</code>:</p>
<pre><code class="language-shell-session">mysql&gt; SELECT 1 = 1 OR 'test' = 'abc';

+-------------------------+
| 1 = 1 OR 'test' = 'abc' |
+-------------------------+
|                       1 |
+-------------------------+
1 row in set (0.00 sec)

mysql&gt; SELECT 1 = 2 OR 'test' = 'abc';

+-------------------------+
| 1 = 2 OR 'test' = 'abc' |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set (0.00 sec)
</code></pre>
<p>The queries above demonstrate how the <code>OR</code> operator works. The first query evaluated to <code>true</code> as the condition <code>1 = 1</code> is <code>true</code>. The second query has two <code>false</code> conditions, resulting in <code>false</code> output.</p>
<hr/>
<h2>NOT Operator</h2>
<p>The <code>NOT</code> operator simply toggles a <code>boolean</code> value 'i.e. <code>true</code> is converted to <code>false</code> and vice versa':</p>
<pre><code class="language-shell-session">mysql&gt; SELECT NOT 1 = 1;

+-----------+
| NOT 1 = 1 |
+-----------+
|         0 |
+-----------+
1 row in set (0.00 sec)

mysql&gt; SELECT NOT 1 = 2;

+-----------+
| NOT 1 = 2 |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)
</code></pre>
<p>As seen in the examples above, the first query resulted in <code>false</code> because it is the inverse of the evaluation of <code>1 = 1</code>, which is <code>true</code>, so its inverse is <code>false</code>. On the other hand, the second query returned <code>true</code>, as the inverse of <code>1 = 2</code> 'which is <code>false</code>' is <code>true</code>.</p>
<hr/>
<h2>Symbol Operators</h2>
<p>The <code>AND</code>, <code>OR</code> and <code>NOT</code> operators can also be represented as <code>&amp;&amp;</code>, <code>||</code> and <code>!</code>, respectively. The below are the same previous examples, by using the symbol operators:</p>
<pre><code class="language-shell-session">mysql&gt; SELECT 1 = 1 &amp;&amp; 'test' = 'abc';

+-------------------------+
| 1 = 1 &amp;&amp; 'test' = 'abc' |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set, 1 warning (0.00 sec)

mysql&gt; SELECT 1 = 1 || 'test' = 'abc';

+-------------------------+
| 1 = 1 || 'test' = 'abc' |
+-------------------------+
|                       1 |
+-------------------------+
1 row in set, 1 warning (0.00 sec)

mysql&gt; SELECT 1 != 1;

+--------+
| 1 != 1 |
+--------+
|      0 |
+--------+
1 row in set (0.00 sec)
</code></pre>
<hr/>
<h2>Operators in queries</h2>
<p>Let us look at how these operators can be used in queries. The following query lists all records where the <code>username</code> is NOT <code>john</code>:</p>
<pre><code class="language-shell-session">mysql&gt; SELECT * FROM logins WHERE username != 'john';

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  1 | admin         | p@ssw0rd   | 2020-07-02 00:00:00 |
|  2 | administrator | adm1n_p@ss | 2020-07-02 11:30:50 |
|  4 | tom           | tom123!    | 2020-07-02 11:47:16 |
+----+---------------+------------+---------------------+
3 rows in set (0.00 sec)
</code></pre>
<p>The next query selects users who have their <code>id</code> greater than <code>1</code> AND <code>username</code> NOT equal to <code>john</code>:</p>
<pre><code class="language-shell-session">mysql&gt; SELECT * FROM logins WHERE username != 'john' AND id &gt; 1;

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  2 | administrator | adm1n_p@ss | 2020-07-02 11:30:50 |
|  4 | tom           | tom123!    | 2020-07-02 11:47:16 |
+----+---------------+------------+---------------------+
2 rows in set (0.00 sec)
</code></pre>
<hr/>
<h2>Multiple Operator Precedence</h2>
<p>SQL supports various other operations such as addition, division as well as bitwise operations. Thus, a query could have multiple expressions with multiple operations at once. The order of these operations is decided through operator precedence.</p>
<p>Here is a list of common operations and their precedence, as seen in the <a href="https://mariadb.com/kb/en/operator-precedence/">MariaDB Documentation</a>:</p>
<ul>
<li>Division (<code>/</code>), Multiplication (<code>*</code>), and Modulus (<code>%</code>)</li>
<li>Addition (<code>+</code>) and subtraction (<code>-</code>)</li>
<li>Comparison (<code>=</code>, <code>&gt;</code>, <code>&lt;</code>, <code>&lt;=</code>, <code>&gt;=</code>, <code>!=</code>, <code>LIKE</code>)</li>
<li>NOT (<code>!</code>)</li>
<li>AND (<code>&amp;&amp;</code>)</li>
<li>OR (<code>||</code>)</li>
</ul>
<p>Operations at the top are evaluated before the ones at the bottom of the list. Let us look at an example:</p>
<pre><code class="language-sql">SELECT * FROM logins WHERE username != 'tom' AND id &gt; 3 - 2;
</code></pre>
<p>The query has four operations: <code>!=</code>, <code>AND</code>, <code>&gt;</code>, and <code>-</code>. From the operator precedence, we know that subtraction comes first, so it will first evaluate <code>3 - 2</code> to <code>1</code>:</p>
<pre><code class="language-sql">SELECT * FROM logins WHERE username != 'tom' AND id &gt; 1;
</code></pre>
<p>Next, we have two comparison operations, <code>&gt;</code> and <code>!=</code>. Both of these are of the same precedence and will be evaluated together.  So, it will return all records where username is not <code>tom</code>, and  all records where the <code>id</code> is greater than 1, and then apply <code>AND</code> to return all records with both of these conditions:</p>
<pre><code class="language-shell-session">mysql&gt; select * from logins where username != 'tom' AND id &gt; 3 - 2;

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  2 | administrator | adm1n_p@ss | 2020-07-03 12:03:53 |
|  3 | john          | john123!   | 2020-07-03 12:03:57 |
+----+---------------+------------+---------------------+
2 rows in set (0.00 sec)
</code></pre>
<p>We will see a few other scenarios of operator precedence in the upcoming sections.</p>
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
                                to <span class="target-protocol-ip target-protocol-ip-31 text-dark"></span> with user "<span class="text-success">root</span>" and
                                password "<span class="text-danger">password</span>" </p>
<label class="module-question" for="31"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> In the 'titles' table, what is the number of records WHERE the employee number is greater than 10000 OR their title does NOT contain 'engineer'?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="654"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="31" disabled="true" id="btnAnswer31">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint31" data-toggle="modal" id="hintBtn31"><i class="fad fa-life-ring mr-2"></i> Hint
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
