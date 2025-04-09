
<h1>Whitelist Filters</h1>
<hr/>
<p>As discussed in the previous section, the other type of file extension validation is by utilizing a <code>whitelist of allowed file extensions</code>. A whitelist is generally more secure than a blacklist. The web server would only allow the specified extensions, and the list would not need to be comprehensive in covering uncommon extensions.</p>
<p>Still, there are different use cases for a blacklist and for a whitelist. A blacklist may be helpful in cases where the upload functionality needs to allow a wide variety of file types (e.g., File Manager), while a whitelist is usually only used with upload functionalities where only a few file types are allowed. Both may also be used in tandem.</p>
<hr/>
<h2>Whitelisting Extensions</h2>
<p>Let's start the exercise at the end of this section and attempt to upload an uncommon PHP extension, like <code>.phtml</code>, and see if we are still able to upload it as we did in the previous section:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_whitelist_message.jpg"/></p>
<p>We see that we get a message saying <code>Only images are allowed</code>, which may be more common in web apps than seeing a blocked extension type. However, error messages do not always reflect which form of validation is being utilized, so let's try to fuzz for allowed extensions as we did in the previous section, using the same wordlist that we used previously:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_whitelist_fuzz.jpg"/></p>
<p>We can see that all variations of PHP extensions are blocked (e.g. <code>php5</code>, <code>php7</code>, <code>phtml</code>). However, the wordlist we used also contained other 'malicious' extensions that were not blocked and were successfully uploaded. So, let's try to understand how we were able to upload these extensions and in which cases we may be able to utilize them to execute PHP code on the back-end server.</p>
<p>The following is an example of a file extension whitelist test:</p>
<pre><code class="language-php">$fileName = basename($_FILES["uploadFile"]["name"]);

if (!preg_match('^.*\.(jpg|jpeg|png|gif)', $fileName)) {
    echo "Only images are allowed";
    die();
}
</code></pre>
<p>We see that the script uses a Regular Expression (<code>regex</code>) to test whether the filename contains any whitelisted image extensions. The issue here lies within the <code>regex</code>, as it only checks whether the file name <code>contains</code> the extension and not if it actually <code>ends</code> with it. Many developers make such mistakes due to a weak understanding of regex patterns.</p>
<p>So, let's see how we can bypass these tests to upload PHP scripts.</p>
<hr/>
<h2>Double Extensions</h2>
<p>The code only tests whether the file name contains an image extension; a straightforward method of passing the regex test is through <code>Double Extensions</code>. For example, if the <code>.jpg</code> extension was allowed, we can add it in our uploaded file name and still end our filename with <code>.php</code> (e.g. <code>shell.jpg.php</code>), in which case we should be able to pass the whitelist test, while still uploading a PHP script that can execute PHP code.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Exercise:</b> Try to fuzz the upload form with <a href="https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/web-extensions.txt">This Wordlist</a> to find what extensions are whitelisted by the upload form.</p>
</div>
</div>
<p>Let's intercept a normal upload request, and modify the file name to (<code>shell.jpg.php</code>), and modify its content to that of a web shell:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_double_ext_request.jpg"/></p>
<p>Now, if we visit the uploaded file and try to send a command, we can see that it does indeed successfully execute system commands, meaning that the file we uploaded is a fully working PHP script:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/profile_images/shell.jpg.php?cmd=id" src="/storage/modules/136/file_uploads_php_manual_shell.jpg"/></p>
<p>However, this may not always work, as some web applications may use a strict <code>regex</code> pattern, as mentioned earlier, like the following:</p>
<pre><code class="language-php">if (!preg_match('/^.*\.(jpg|jpeg|png|gif)$/', $fileName)) { ...SNIP... }
</code></pre>
<p>This pattern should only consider the final file extension, as it uses (<code>^.*\.</code>) to match everything up to the last (<code>.</code>), and then uses (<code>$</code>) at the end to only match extensions that end the file name. So, the <code>above attack would not work</code>. Nevertheless, some exploitation techniques may allow us to bypass this pattern, but most rely on misconfigurations or outdated systems.</p>
<hr/>
<h2>Reverse Double Extension</h2>
<p>In some cases, the file upload functionality itself may not be vulnerable, but the web server configuration may lead to a vulnerability. For example, an organization may use an open-source web application, which has a file upload functionality. Even if the file upload functionality uses a strict regex pattern that only matches the final extension in the file name, the organization may use the insecure configurations for the web server.</p>
<p>For example, the <code>/etc/apache2/mods-enabled/php7.4.conf</code> for the <code>Apache2</code> web server may include the following configuration:</p>
<pre><code class="language-xml">&lt;FilesMatch ".+\.ph(ar|p|tml)"&gt;
    SetHandler application/x-httpd-php
&lt;/FilesMatch&gt;
</code></pre>
<p>The above configuration is how the web server determines which files to allow PHP code execution. It specifies a whitelist with a regex pattern that matches <code>.phar</code>, <code>.php</code>, and <code>.phtml</code>. However, this regex pattern can have the same mistake we saw earlier if we forget to end it with (<code>$</code>). In such cases, any file that contains the above extensions will be allowed PHP code execution, even if it does not end with the PHP extension. For example, the file name (<code>shell.php.jpg</code>) should pass the earlier whitelist test as it ends with (<code>.jpg</code>), and it would be able to execute PHP code due to the above misconfiguration, as it contains (<code>.php</code>) in its name.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Exercise:</b> The web application may still utilize a blacklist to deny requests containing <code>PHP</code> extensions. Try to fuzz the upload form with the <a href="https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Extension%20PHP/extensions.lst">PHP Wordlist</a> to find what extensions are blacklisted by the upload form.</p>
</div>
</div>
<p>Let's try to intercept a normal image upload request, and use the above file name to pass the strict whitelist test:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_reverse_double_ext_request.jpg"/></p>
<p>Now, we can visit the uploaded file, and attempt to execute a command:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/profile_images/shell.php.jpg?cmd=id" src="/storage/modules/136/file_uploads_php_manual_shell.jpg"/></p>
<p>As we can see, we successfully bypassed the strict whitelist test and exploited the web server misconfiguration to execute PHP code and gain control over the server.</p>
<h2>Character Injection</h2>
<p>Finally, let's discuss another method of bypassing a whitelist validation test through <code>Character Injection</code>. We can inject several characters before or after the final extension to cause the web application to misinterpret the filename and execute the uploaded file as a PHP script.</p>
<p>The following are some of the characters we may try injecting:</p>
<ul>
<li>
<code>%20</code>
</li>
<li>
<code>%0a</code>
</li>
<li>
<code>%00</code>
</li>
<li>
<code>%0d0a</code>
</li>
<li>
<code>/</code>
</li>
<li>
<code>.\</code>
</li>
<li>
<code>.</code>
</li>
<li>
<code>…</code>
</li>
<li>
<code>:</code>
</li>
</ul>
<p>Each character has a specific use case that may trick the web application to misinterpret the file extension. For example, (<code>shell.php%00.jpg</code>) works with PHP servers with version <code>5.X</code> or earlier, as it causes the PHP web server to end the file name after the (<code>%00</code>), and store it as (<code>shell.php</code>), while still passing the whitelist. The same may be used with web applications hosted on a Windows server by injecting a colon (<code>:</code>) before the allowed file extension (e.g. <code>shell.aspx:.jpg</code>), which should also write the file as (<code>shell.aspx</code>). Similarly, each of the other characters has a use case that may allow us to upload a PHP script while bypassing the type validation test.</p>
<p>We can write a small bash script that generates all permutations of the file name, where the above characters would be injected before and after both the <code>PHP</code> and <code>JPG</code> extensions, as follows:</p>
<pre><code class="language-bash">for char in '%20' '%0a' '%00' '%0d0a' '/' '.\\' '.' '…' ':'; do
    for ext in '.php' '.phps'; do
        echo "shell$char$ext.jpg" &gt;&gt; wordlist.txt
        echo "shell$ext$char.jpg" &gt;&gt; wordlist.txt
        echo "shell.jpg$char$ext" &gt;&gt; wordlist.txt
        echo "shell.jpg$ext$char" &gt;&gt; wordlist.txt
    done
done
</code></pre>
<p>With this custom wordlist, we can run a fuzzing scan with <code>Burp Intruder</code>, similar to the ones we did earlier. If either the back-end or the web server is outdated or has certain misconfigurations, some of the generated filenames may bypass the whitelist test and execute PHP code.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Exercise:</b> Try to add more PHP extensions to the above script to generate more filename permutations, then fuzz the upload functionality with the generated wordlist to see which of the generated file names can be uploaded, and which may execute PHP code after being uploaded.</p>
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
<label class="module-question" for="868"><span class="badge badge-soft-dark font-size-14 mr-2">+ 2 <i class="fad fa-cube text-success"></i></span> The above exercise employs a blacklist and a whitelist test to block unwanted extensions and only allow image extensions. Try to bypass both to upload a PHP script and execute code to read "/flag.txt"
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer868" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-868">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="868" id="btnAnswer868">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint868" data-toggle="modal" id="hintBtn868"><i class="fad fa-life-ring mr-2"></i> Hint
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
