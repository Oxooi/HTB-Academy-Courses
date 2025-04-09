
<h1>Log Poisoning</h1>
<p>We have seen in previous sections that if we include any file that contains PHP code, it will get executed, as long as the vulnerable function has the <code>Execute</code> privileges. The attacks we will discuss in this section all rely on the same concept: Writing PHP code in a field we control that gets logged into a log file (i.e. <code>poison</code>/<code>contaminate</code> the log file), and then include that log file to execute the PHP code. For this attack to work, the PHP web application should have read privileges over the logged files, which vary from one server to another.</p>
<p>As was the case in the previous section, any of the following functions with <code>Execute</code> privileges should be vulnerable to these attacks:</p>
<table>
<thead>
<tr>
<th><strong>Function</strong></th>
<th align="center"><strong>Read Content</strong></th>
<th align="center"><strong>Execute</strong></th>
<th align="center"><strong>Remote URL</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>PHP</strong></td>
<td align="center"></td>
<td align="center"></td>
<td align="center"></td>
</tr>
<tr>
<td><code>include()</code>/<code>include_once()</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">✅</td>
</tr>
<tr>
<td><code>require()</code>/<code>require_once()</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">❌</td>
</tr>
<tr>
<td><strong>NodeJS</strong></td>
<td align="center"></td>
<td align="center"></td>
<td align="center"></td>
</tr>
<tr>
<td><code>res.render()</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">❌</td>
</tr>
<tr>
<td><strong>Java</strong></td>
<td align="center"></td>
<td align="center"></td>
<td align="center"></td>
</tr>
<tr>
<td><code>import</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">✅</td>
</tr>
<tr>
<td><strong>.NET</strong></td>
<td align="center"></td>
<td align="center"></td>
<td align="center"></td>
</tr>
<tr>
<td><code>include</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">✅</td>
</tr>
</tbody>
</table>
<hr/>
<h2>PHP Session Poisoning</h2>
<p>Most PHP web applications utilize <code>PHPSESSID</code> cookies, which can hold specific user-related data on the back-end, so the web application can keep track of user details through their cookies. These details are stored in <code>session</code> files on the back-end, and saved in <code>/var/lib/php/sessions/</code> on Linux and in <code>C:\Windows\Temp\</code> on Windows. The name of the file that contains our user's data matches the name of our <code>PHPSESSID</code> cookie with the <code>sess_</code> prefix. For example, if the <code>PHPSESSID</code> cookie is set to <code>el4ukv0kqbvoirg7nkp4dncpk3</code>, then its location on disk would be <code>/var/lib/php/sessions/sess_el4ukv0kqbvoirg7nkp4dncpk3</code>.</p>
<p>The first thing we need to do in a PHP Session Poisoning attack is to examine our PHPSESSID session file and see if it contains any data we can control and poison. So, let's first check if we have a <code>PHPSESSID</code> cookie set to our session:
<img alt="image" src="https://academy.hackthebox.com/storage/modules/23/rfi_cookies_storage.png"/></p>
<p>As we can see, our <code>PHPSESSID</code> cookie value is <code>nhhv8i0o6ua4g88bkdl9u1fdsd</code>, so it should be stored at <code>/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd</code>. Let's try include this session file through the LFI vulnerability and view its contents:
<img alt="Shipping containers and cranes at a port with browser console displaying PHP session information." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd" src="/storage/modules/23/rfi_session_include.png"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> As you may easily guess, the cookie value will differ from one session to another, so you need to use the cookie value you find in your own session to perform the same attack.</p>
</div>
</div>
<p>We can see that the session file contains two values: <code>page</code>, which shows the selected language page, and <code>preference</code>, which shows the selected language. The <code>preference</code> value is not under our control, as we did not specify it anywhere and must be automatically specified. However, the <code>page</code> value is under our control, as we can control it through the <code>?language=</code> parameter.</p>
<p>Let's try setting the value of <code>page</code> a custom value (e.g. <code>language parameter</code>) and see if it changes in the session file. We can do so by simply visiting the page with <code>?language=session_poisoning</code> specified, as follows:</p>
<pre><code class="language-url">http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=session_poisoning
</code></pre>
<p>Now, let's include the session file once again to look at the contents:
<img alt="Shipping containers and cranes at a port with PHP notice about an undefined variable." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd" src="/storage/modules/23/lfi_poisoned_sessid.png"/></p>
<p>This time, the session file contains <code>session_poisoning</code> instead of <code>es.php</code>, which confirms our ability to control the value of <code>page</code> in the session file. Our next step is to perform the <code>poisoning</code> step by writing PHP code to the session file. We can write a basic PHP web shell by changing the <code>?language=</code> parameter to a URL encoded web shell, as follows:</p>
<pre><code class="language-url">http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%3B%3F%3E
</code></pre>
<p>Finally, we can include the session file and use the <code>&amp;cmd=id</code> to execute a commands:
<img alt="Shipping containers and cranes at a port with PHP notice about an undefined variable." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd&amp;cmd=id" src="/storage/modules/23/rfi_session_id.png"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: To execute another command, the session file has to be poisoned with the web shell again, as it gets overwritten with <code>/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd</code> after our last inclusion. Ideally, we would use the poisoned web shell to write a permanent web shell to the web directory, or send a reverse shell for easier interaction.</p>
</div>
</div>
<hr/>
<h2>Server Log Poisoning</h2>
<p>Both <code>Apache</code> and <code>Nginx</code> maintain various log files, such as <code>access.log</code> and <code>error.log</code>. The <code>access.log</code> file contains various information about all requests made to the server, including each request's <code>User-Agent</code> header. As we can control the <code>User-Agent</code> header in our requests, we can use it to poison the server logs as we did above.</p>
<p>Once poisoned, we need to include the logs through the LFI vulnerability, and for that we need to have read-access over the logs. <code>Nginx</code> logs are readable by low privileged users by default (e.g. <code>www-data</code>), while the <code>Apache</code> logs are only readable by users with high privileges (e.g. <code>root</code>/<code>adm</code> groups). However, in older or misconfigured <code>Apache</code> servers, these logs may be readable by low-privileged users.</p>
<p>By default, <code>Apache</code> logs are located in <code>/var/log/apache2/</code> on Linux and in <code>C:\xampp\apache\logs\</code> on Windows, while <code>Nginx</code> logs are located in <code>/var/log/nginx/</code> on Linux and in <code>C:\nginx\log\</code> on Windows. However, the logs may be in a different location in some cases, so we may use an <a href="https://github.com/danielmiessler/SecLists/tree/master/Fuzzing/LFI">LFI Wordlist</a> to fuzz for their locations, as will be discussed in the next section.</p>
<p>So, let's try including the Apache access log from <code>/var/log/apache2/access.log</code>, and see what we get:
<img alt="Shipping containers and cranes at a port with server log entries displayed." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=/var/log/apache2/access.log" src="/storage/modules/23/rfi_access_log.png"/></p>
<p>As we can see, we can read the log. The log contains the <code>remote IP address</code>, <code>request page</code>, <code>response code</code>, and the <code>User-Agent</code> header. As mentioned earlier, the <code>User-Agent</code> header is controlled by us through the HTTP request headers, so we should be able to poison this value.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Tip:</b> Logs tend to be huge, and loading them in an LFI vulnerability may take a while to load, or even crash the server in worst-case scenarios. So, be careful and efficient with them in a production environment, and don't send unnecessary requests.</p>
</div>
</div>
<p>To do so, we will use <code>Burp Suite</code> to intercept our earlier LFI request and modify the <code>User-Agent</code> header to <code>Apache Log Poisoning</code>:
<img alt="image" src="https://academy.hackthebox.com/storage/modules/23/rfi_repeater_ua.png"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> As all requests to the server get logged, we can poison any request to the web application, and not necessarily the LFI one as we did above.</p>
</div>
</div>
<p>As expected, our custom User-Agent value is visible in the included log file. Now, we can poison the <code>User-Agent</code> header by setting it to a basic PHP web shell:
<img alt="HTTP request and response showing Apache log poisoning with PHP notice about an undefined variable." src="https://academy.hackthebox.com/storage/modules/23/rfi_cmd_repeater.png"/></p>
<p>We may also poison the log by sending a request through cURL, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ curl -s "http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php" -A "&lt;?php system($_GET['cmd']); ?&gt;"
</code></pre>
<p>As the log should now contain PHP code, the LFI vulnerability should execute this code, and we should be able to gain remote code execution. We can specify a command to be executed with (<code>&amp;cmd=id</code>):
<img alt="HTTP request and response showing Apache log poisoning with PHP code execution using system command." src="https://academy.hackthebox.com/storage/modules/23/rfi_id_repeater.png"/></p>
<p>We see that we successfully executed the command. The exact same attack can be carried out on <code>Nginx</code> logs as well.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Tip:</b> The <code>User-Agent</code> header is also shown on process files under the Linux <code>/proc/</code> directory. So, we can try including the <code>/proc/self/environ</code> or <code>/proc/self/fd/N</code> files (where N is a PID usually between 0-50), and we may be able to perform the same attack on these files. This may become handy in case we did not have read access over the server logs, however, these files may only be readable by privileged users as well. </p>
</div>
</div>
<p>Finally, there are other similar log poisoning techniques that we may utilize on various system logs, depending on which logs we have read access over. The following are some of the service logs we may be able to read:</p>
<ul>
<li>
<code>/var/log/sshd.log</code>
</li>
<li>
<code>/var/log/mail</code>
</li>
<li>
<code>/var/log/vsftpd.log</code>
</li>
</ul>
<p>We should first attempt reading these logs through LFI, and if we do have access to them, we can try to poison them as we did above. For example, if the <code>ssh</code> or <code>ftp</code> services are exposed to us, and we can read their logs through LFI, then we can try logging into them and set the username to PHP code, and upon including their logs, the PHP code would execute. The same applies the <code>mail</code> services, as we can send an email containing PHP code, and upon its log inclusion, the PHP code would execute. We can generalize this technique to any logs that log a parameter we control and that we can read through the LFI vulnerability.</p>
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
<label class="module-question" for="90"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> Use any of the techniques covered in this section to gain RCE, then submit the output of the following command: pwd
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer90" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-90">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="90" id="btnAnswer90">
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
<label class="module-question" for="169"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Try to use a different technique to gain RCE and read the flag at /
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer169" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-169">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="169" id="btnAnswer169">
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
