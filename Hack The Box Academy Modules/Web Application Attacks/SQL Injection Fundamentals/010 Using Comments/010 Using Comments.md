
<h1>Using Comments</h1>
<hr/>
<p>In this section we will learn how to use comments to subvert the logic of more advanced SQL queries and end up with a working SQL query to bypass the login authentication process.</p>
<hr/>
<h2>Comments</h2>
<p>Just like any other language, SQL allows the use of comments as well. Comments are used to document queries or ignore a certain part of the query. We can use two types of line comments with MySQL <code>-- </code> and <code>#</code>, in addition to an in-line comment <code>/**/</code> (though this is not usually used in SQL injections). The <code>-- </code> can be used as follows:</p>
<pre><code class="language-shell-session">mysql&gt; SELECT username FROM logins; -- Selects usernames from the logins table 

+---------------+
| username      |
+---------------+
| admin         |
| administrator |
| john          |
| tom           |
+---------------+
4 rows in set (0.00 sec)
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: In SQL, using two dashes only is not enough to start a comment. So, there has to be an empty space after them, so the comment starts with (-- ), with a space at the end. This is sometimes URL encoded as (--+), as spaces in URLs are encoded as (+). To make it clear, we will add another (-) at the end (-- -), to show the use of a space character.</p>
</div>
</div>
<p>The <code>#</code> symbol can be used as well.</p>
<pre><code class="language-shell-session">mysql&gt; SELECT * FROM logins WHERE username = 'admin'; # You can place anything here AND password = 'something'

+----+----------+----------+---------------------+
| id | username | password | date_of_joining     |
+----+----------+----------+---------------------+
|  1 | admin    | p@ssw0rd | 2020-07-02 00:00:00 |
+----+----------+----------+---------------------+
1 row in set (0.00 sec)
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: if you are inputting your payload in the URL within a browser, a (#) symbol is usually considered as a tag, and will not be passed as part of the URL. In order to use (#) as a comment within a browser, we can use '%23', which is an URL encoded (#) symbol.</p>
</div>
</div>
<p>The server will ignore the part of the query with <code>AND password = 'something'</code> during evaluation.</p>
<hr/>
<h2>Auth Bypass with comments</h2>
<p>Let us go back to our previous example and inject <code>admin'-- </code> as our username. The final query will be:</p>
<pre><code class="language-sql">SELECT * FROM logins WHERE username='admin'-- ' AND password = 'something';
</code></pre>
<p>As we can see from the syntax highlighting, the username is now <code>admin</code>, and the remainder of the query is now ignored as a comment. Also, this way, we can ensure that the query does not have any syntax issues.</p>
<p>Let us try using these on the login page, and log in with the username <code>admin'-- </code> and anything as the password:</p>
<p><img alt="Admin panel showing an SQL query execution: SELECT * FROM logins WHERE username='admin'-- ' AND password='a'; with a message: Login successful as user: admin" src="https://academy.hackthebox.com/storage/modules/33/admin_dash.png"/></p>
<p>As we see, we were able to bypass the authentication, as the new modified query checks for the username, with no other conditions.</p>
<hr/>
<h2>Another Example</h2>
<p>SQL supports the usage of parenthesis if the application needs to check for particular conditions before others. Expressions within the parenthesis take precedence over other operators and are evaluated first. Let us look at a scenario like this:</p>
<p><img alt="Admin panel showing an SQL query execution: SELECT * FROM logins WHERE (username='admin' AND id &gt; 1) AND password='437b930db84b8079c2dd804a71936b5f'; with a message: Login failed!" src="https://academy.hackthebox.com/storage/modules/33/paranthesis_fail.png"/></p>
<p>The above query ensures that the user's id is always greater than 1, which will prevent anyone from logging in as admin. Additionally, we also see that the password was hashed before being used in the query. This will prevent us from injecting through the password field because the input is changed to a hash.</p>
<p>Let us try logging in with valid credentials <code>admin / p@ssw0rd</code> to see the response.</p>
<p><img alt="Admin panel showing an SQL query execution: SELECT * FROM logins WHERE (username='admin' AND id &gt; 1) AND password='0f359740bd1cda994f8b55330c86d845'; with a message: Login failed!" src="https://academy.hackthebox.com/storage/modules/33/paranthesis_valid_fail.png"/></p>
<p>As expected, the login failed even though we supplied valid credentials because the admin’s ID equals 1. So let us try logging in with the credentials of another user, such as <code>tom</code>.</p>
<p><img alt="Admin panel showing an SQL query execution: SELECT * FROM logins WHERE (username='tom' AND id &gt; 1) AND password='f86a3c565937e6315864d1a43c48e7'; with a message: Login successful as user: tom&quot;" src="https://academy.hackthebox.com/storage/modules/33/tom_login.png"/></p>
<p>Logging in as the user with an id not equal to 1 was successful. So, how can we log in as the admin? We know from the previous section on comments that we can use them to comment out the rest of the query. So, let us try using <code>admin'-- </code> as the username.</p>
<p><img alt="Admin panel showing an SQL query execution: SELECT * FROM logins WHERE (username='admin'--' AND id &gt; 1) AND password='437b930db84b8079c2dd804a71936b5f'; with an error message: You have an error in your SQL syntax; check the manual for the right syntax near '437b930db84b8079c2dd804a71936b5f' at line 1" src="https://academy.hackthebox.com/storage/modules/33/paranthesis_error.png"/></p>
<p>The login failed due to a syntax error, as a closed one did not balance the open parenthesis. To execute the query successfully, we will have to add a closing parenthesis. Let us try using the username <code>admin')-- </code> to close and comment out the rest.</p>
<p><img alt="Admin panel showing an SQL query execution: SELECT * FROM logins WHERE (username='admin'--' AND id &gt; 1) AND password='437b930db84b8079c2dd804a71936b5f'; with a message: Login successful as user: admin&quot;" src="https://academy.hackthebox.com/storage/modules/33/paranthesis_success.png"/></p>
<p>The query was successful, and we logged in as admin. The final query as a result of our input is:</p>
<pre><code class="language-sql">SELECT * FROM logins where (username='admin')
</code></pre>
<p>The query above is like the one from the previous example and returns the row containing admin.</p>
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
<label class="module-question" for="33"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Login as the user with the id 5 to get the flag.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer33" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-33">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="33" id="btnAnswer33">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint33" data-toggle="modal" id="hintBtn33"><i class="fad fa-life-ring mr-2"></i> Hint
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
