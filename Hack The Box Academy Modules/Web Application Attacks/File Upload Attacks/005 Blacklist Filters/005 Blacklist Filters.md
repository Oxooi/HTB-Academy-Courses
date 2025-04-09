
<h1>Blacklist Filters</h1>
<hr/>
<p>In the previous section, we saw an example of a web application that only applied type validation controls on the front-end (i.e., client-side), which made it trivial to bypass these controls. This is why it is always recommended to implement all security-related controls on the back-end server, where attackers cannot directly manipulate it.</p>
<p>Still, if the type validation controls on the back-end server were not securely coded, an attacker can utilize multiple techniques to bypass them and reach PHP file uploads.</p>
<p>The exercise we find in this section is similar to the one we saw in the previous section, but it has a blacklist of disallowed extensions to prevent uploading web scripts. We will see why using a blacklist of common extensions may not be enough to prevent arbitrary file uploads and discuss several methods to bypass it.</p>
<hr/>
<h2>Blacklisting Extensions</h2>
<p>Let's start by trying one of the client-side bypasses we learned in the previous section to upload a PHP script to the back-end server. We'll intercept an image upload request with Burp, replace the file content and filename with our PHP script's, and forward the request:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_disallowed_type.jpg"/></p>
<p>As we can see, our attack did not succeed this time, as we got <code>Extension not allowed</code>. This indicates that the web application may have some form of file type validation on the back-end, in addition to the front-end validations.</p>
<p>There are generally two common forms of validating a file extension on the back-end:</p>
<ol>
<li>Testing against a <code>blacklist</code> of types</li>
<li>Testing against a <code>whitelist</code> of types</li>
</ol>
<p>Furthermore, the validation may also check the <code>file type</code> or the <code>file content</code> for type matching. The weakest form of validation amongst these is <code>testing the file extension against a blacklist of extension</code> to determine whether the upload request should be blocked. For example, the following piece of code checks if the uploaded file extension is <code>PHP</code> and drops the request if it is:</p>
<pre><code class="language-php">$fileName = basename($_FILES["uploadFile"]["name"]);
$extension = pathinfo($fileName, PATHINFO_EXTENSION);
$blacklist = array('php', 'php7', 'phps');

if (in_array($extension, $blacklist)) {
    echo "File type not allowed";
    die();
}
</code></pre>
<p>The code is taking the file extension (<code>$extension</code>) from the uploaded file name (<code>$fileName</code>) and then comparing it against a list of blacklisted extensions (<code>$blacklist</code>). However, this validation method has a major flaw. <code>It is not comprehensive</code>, as many other extensions are not included in this list, which may still be used to execute PHP code on the back-end server if uploaded.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Tip:</b> The comparison above is also case-sensitive, and is only considering lowercase extensions. In Windows Servers, file names are case insensitive, so we may try uploading a <code>php</code> with a mixed-case (e.g. <code>pHp</code>), which may bypass the blacklist as well, and should still execute as a PHP script.</p>
</div>
</div>
<p>So, let's try to exploit this weakness to bypass the blacklist and upload a PHP file.</p>
<hr/>
<h2>Fuzzing Extensions</h2>
<p>As the web application seems to be testing the file extension, our first step is to fuzz the upload functionality with a list of potential extensions and see which of them return the previous error message. Any upload requests that do not return an error message, return a different message, or succeed in uploading the file, may indicate an allowed file extension.</p>
<p>There are many lists of extensions we can utilize in our fuzzing scan. <code>PayloadsAllTheThings</code> provides lists of extensions for <a href="https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Extension%20PHP/extensions.lst">PHP</a> and <a href="https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files/Extension%20ASP">.NET</a> web applications. We may also use <code>SecLists</code> list of common <a href="https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/web-extensions.txt">Web Extensions</a>.</p>
<p>We may use any of the above lists for our fuzzing scan. As we are testing a PHP application, we will download and use the above <a href="https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Extension%20PHP/extensions.lst">PHP</a> list. Then, from <code>Burp History</code>, we can locate our last request to <code>/upload.php</code>, right-click on it, and select <code>Send to Intruder</code>. From the <code>Positions</code> tab, we can <code>Clear</code> any automatically set positions, and then select the <code>.php</code> extension in <code>filename="HTB.php"</code> and click the <code>Add</code> button to add it as a fuzzing position:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_burp_fuzz_extension.jpg"/>
<p>We'll keep the file content for this attack, as we are only interested in fuzzing file extensions. Finally, we can <code>Load</code> the PHP extensions list from above in the <code>Payloads</code> tab under <code>Payload Options</code>. We will also un-tick the <code>URL Encoding</code> option to avoid encoding the (<code>.</code>) before the file extension. Once this is done, we can click on <code>Start Attack</code> to start fuzzing for file extensions that are not blacklisted:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_burp_intruder_result.jpg"/>
<p>We can sort the results by <code>Length</code>, and we will see that all requests with the Content-Length (<code>193</code>) passed the extension validation, as they all responded with <code>File successfully uploaded</code>. In contrast, the rest responded with an error message saying <code>Extension not allowed</code>.</p>
<hr/>
<h2>Non-Blacklisted Extensions</h2>
<p>Now, we can try uploading a file using any of the <code>allowed extensions</code> from above, and some of them may allow us to execute PHP code. <code>Not all extensions will work with all web server configurations</code>, so we may need to try several extensions to get one that successfully executes PHP code.</p>
<p>Let's use the <code>.phtml</code> extension, which PHP web servers often allow for code execution rights. We can right-click on its request in the Intruder results and select <code>Send to Repeater</code>. Now, all we have to do is repeat what we have done in the previous two sections by changing the file name to use the <code>.phtml</code> extension and changing the content to that of a PHP web shell:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_php5_web_shell.jpg"/></p>
<p>As we can see, our file seems to have indeed been uploaded. The final step is to visit our upload file, which should be under the image upload directory (<code>profile_images</code>), as we saw in the previous section. Then, we can test executing a command, which should confirm that we successfully bypassed the blacklist and uploaded our web shell:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/profile_images/shell.phtml?cmd=id" src="/storage/modules/136/file_uploads_php_manual_shell.jpg"/></p>
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
<label class="module-question" for="867"><span class="badge badge-soft-dark font-size-14 mr-2">+ 2 <i class="fad fa-cube text-success"></i></span> Try to find an extension that is not blacklisted and can execute PHP code on the web server, and use it to read "/flag.txt"
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer867" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-867">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="867" id="btnAnswer867">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint867" data-toggle="modal" id="hintBtn867"><i class="fad fa-life-ring mr-2"></i> Hint
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
