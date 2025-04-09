
<h1>Subverting Query Logic</h1>
<hr/>
<p>Now that we have a basic idea about how SQL statements work let us get started with SQL injection.  Before we start executing entire SQL queries, we will first learn to modify the original query by injecting the <code>OR</code> operator and using SQL comments to subvert the original query's logic. A basic example of this is bypassing web authentication, which we will demonstrate in this section.</p>
<hr/>
<h2>Authentication Bypass</h2>
<p>Consider the following administrator login page.</p>
<p><img alt="Admin panel login form with fields for Username and Password, and a Login button" src="https://academy.hackthebox.com/storage/modules/33/admin_panel.png"/></p>
<p>We can log in with the administrator credentials <code>admin / p@ssw0rd</code>.</p>
<p><img alt="Admin panel displaying an SQL query execution: SELECT * FROM logins WHERE username='admin' AND password='p@ssw0rd'; followed by a message: Login successful as user: admin" src="https://academy.hackthebox.com/storage/modules/33/admin_creds.png"/></p>
<p>The page also displays the SQL query being executed to understand better how we will subvert the query logic.  Our goal is to log in as the admin user without using the existing password. As we can see, the current SQL query being executed is:</p>
<pre><code class="language-sql">SELECT * FROM logins WHERE username='admin' AND password = 'p@ssw0rd';
</code></pre>
<p>The page takes in the credentials, then uses the <code>AND</code> operator to select records matching the given username and password. If the <code>MySQL</code> database returns matched records, the credentials are valid, so the <code>PHP</code> code would evaluate the login attempt condition as <code>true</code>. If the condition evaluates to <code>true</code>, the admin record is returned, and our login is validated. Let us see what happens when we enter incorrect credentials.</p>
<p><img alt="Admin panel showing an SQL query execution: SELECT * FROM logins WHERE username='admin' AND password='admin'; with a message: Login failed! Below is a login form with fields for Username and Password, and a Login button" src="https://academy.hackthebox.com/storage/modules/33/admin_incorrect.png"/></p>
<p>As expected, the login failed due to the wrong password leading to a <code>false</code> result from the <code>AND</code> operation.</p>
<hr/>
<h2>SQLi Discovery</h2>
<p>Before we start subverting the web application's logic and attempting to bypass the authentication, we first have to test whether the login form is vulnerable to SQL injection. To do that, we will try to add one of the below payloads after our username and see if it causes any errors or changes how the page behaves:</p>
<table>
<thead>
<tr>
<th>Payload</th>
<th>URL Encoded</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>'</code></td>
<td><code>%27</code></td>
</tr>
<tr>
<td><code>"</code></td>
<td><code>%22</code></td>
</tr>
<tr>
<td><code>#</code></td>
<td><code>%23</code></td>
</tr>
<tr>
<td><code>;</code></td>
<td><code>%3B</code></td>
</tr>
<tr>
<td><code>)</code></td>
<td><code>%29</code></td>
</tr>
</tbody>
</table>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: In some cases, we may have to use the URL encoded version of the payload. An example of this is when we put our payload directly in the URL 'i.e. HTTP GET request'.</p>
</div>
</div>
<p>So, let us start by injecting a single quote:</p>
<p><img alt="Admin panel showing an SQL query execution: SELECT * FROM logins WHERE username='' AND password='something'; with an error message: You have an error in your SQL syntax; check the manual for the right syntax near 'something' at line 1&quot;" src="https://academy.hackthebox.com/storage/modules/33/quote_error.png"/></p>
<p>We see that a SQL error was thrown instead of the <code>Login Failed</code> message. The page threw an error because the resulting query was:</p>
<pre><code class="language-sql">SELECT * FROM logins WHERE username=''' AND password = 'something';
</code></pre>
<p>As discussed in the previous section, the quote we entered resulted in an odd number of quotes, causing a syntax error.  One option would be to comment out the rest of the query and write the remainder of the query as part of our injection to form a working query. Another option is to use an even number of quotes within our injected query, such that the final query would still work.</p>
<hr/>
<h2>OR Injection</h2>
<p>We would need the query always to return <code>true</code>, regardless of the username and password entered, to bypass the authentication. To do this, we can abuse the <code>OR</code> operator in our SQL injection.</p>
<p>As previously discussed, the MySQL documentation for <a href="https://dev.mysql.com/doc/refman/8.0/en/operator-precedence.html">operation precedence</a> states that the <code>AND</code> operator would be evaluated before the <code>OR</code> operator.  This means that if there is at least one <code>TRUE</code> condition in the entire query along with an <code>OR</code> operator, the entire query will evaluate to <code>TRUE</code> since the <code>OR</code> operator returns <code>TRUE</code> if one of its operands is <code>TRUE</code>.</p>
<p>An example of a condition that will always return <code>true</code> is <code>'1'='1'</code>. However, to keep the SQL query working and keep an even number of quotes, instead of using ('1'='1'), we will remove the last quote and use ('1'='1), so the remaining single quote from the original query would be in its place.</p>
<p>So, if we inject the below condition and have an <code>OR</code> operator between it and the original condition, it should always return <code>true</code>:</p>
<pre><code class="language-sql">admin' or '1'='1
</code></pre>
<p>The final query should be as follow:</p>
<pre><code class="language-sql">SELECT * FROM logins WHERE username='admin' or '1'='1' AND password = 'something';
</code></pre>
<p>This means the following:</p>
<ul>
<li>If username is <code>admin</code><br/>
<code>OR</code>
</li>
<li>If <code>1=1</code> return <code>true</code> 'which always returns <code>true</code>'<br/>
<code>AND</code>
</li>
<li>If password is <code>something</code>
</li>
</ul>
<p><img alt="SQL query logic diagram: SELECT * FROM logins WHERE username='admin' OR '1'='1' AND password='something'. Logic flow shows OR condition as True, making the entire statement True despite the False password condition" src="https://academy.hackthebox.com/storage/modules/33/or_inject_diagram.png"/></p>
<p>The <code>AND</code> operator will be evaluated first, and it will return <code>false</code>. Then, the <code>OR</code> operator would be evalutated, and if either of the statements is <code>true</code>, it would return <code>true</code>. Since <code>1=1</code> always returns <code>true</code>, this query will return <code>true</code>, and it will grant us access.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: The payload we used above is one of many auth bypass payloads we can use to subvert the authentication logic. You can find a comprehensive list of SQLi auth bypass payloads in <a href="https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection#authentication-bypass">PayloadAllTheThings</a>, each of which works on a certain type of SQL queries.</p>
</div>
</div>
<hr/>
<h2>Auth Bypass with OR operator</h2>
<p>Let us try this as the username and see the response.
<img alt="Admin panel showing an SQL query execution: SELECT * FROM logins WHERE username='admin' OR '1'='1' AND password='something'; with a message: Login successful as user: admin" src="https://academy.hackthebox.com/storage/modules/33/inject_success.png"/></p>
<p>We were able to log in successfully as admin. However, what if we did not know a valid username?  Let us try the same request with a different username this time.</p>
<p><img alt="Admin panel showing an SQL query execution: SELECT * FROM logins WHERE username='notAdmin' OR '1'='1' AND password='something'; with a message: Login failed!" src="https://academy.hackthebox.com/storage/modules/33/notadmin_fail.png"/></p>
<p>The login failed because <code>notAdmin</code> does not exist in the table and resulted in a false query overall.</p>
<p><img alt="SQL query logic diagram: SELECT * FROM logins WHERE username='notAdmin' OR '1'='1' AND password='something'. Logic flow shows OR condition as False, making the entire statement False" src="https://academy.hackthebox.com/storage/modules/33/notadmin_diagram_1.png"/></p>
<p>To successfully log in once again, we will need an overall <code>true</code> query.  This can be achieved by injecting an <code>OR</code> condition into the password field, so it will always return <code>true</code>. Let us try <code>something' or '1'='1</code> as the password.</p>
<p><img alt="Admin panel showing an SQL query execution: SELECT * FROM logins WHERE username='notAdmin' OR '1'='1' AND password='something' OR '1'='1'; with a message: Login successful as user: admin" src="https://academy.hackthebox.com/storage/modules/33/password_or_injection.png"/></p>
<p>The additional <code>OR</code> condition resulted in a <code>true</code> query overall, as the <code>WHERE</code> clause returns everything in the table, and the user present in the first row is logged in. In this case, as both conditions will return <code>true</code>, we do not have to provide a test username and password and can directly start with the <code>'</code> injection and log in with just <code>' or '1' = '1</code>.</p>
<p><img alt="Admin panel showing an SQL query execution: SELECT * FROM logins WHERE username='' OR '1'='1' AND password='something' OR '1'='1'; with a message: Login successful as user: admin" src="https://academy.hackthebox.com/storage/modules/33/basic_auth_bypass.png"/></p>
<p>This works since the query evaluate to <code>true</code> irrespective of the username or password.</p>
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
<img alt="sparkles-icon-decoration" class="ml-2 w-auto sparkles-icon" height="20" src="/images/sparkles-solid.svg"/>
</div>
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
<label class="module-question" for="464"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Try to log in as the user 'tom'. What is the flag value shown after you successfully log in?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer464" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-464">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="464" id="btnAnswer464">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint464" data-toggle="modal" id="hintBtn464"><i class="fad fa-life-ring mr-2"></i> Hint
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
