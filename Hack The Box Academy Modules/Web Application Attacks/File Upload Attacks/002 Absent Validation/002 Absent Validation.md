
<h1>Absent Validation</h1>
<hr/>
<p>The most basic type of file upload vulnerability occurs when the web application <code>does not have any form of validation filters</code> on the uploaded files, allowing the upload of any file type by default.</p>
<p>With these types of vulnerable web apps, we may directly upload our web shell or reverse shell script to the web application, and then by just visiting the uploaded script, we can interact with our web shell or send the reverse shell.</p>
<hr/>
<h2>Arbitrary File Upload</h2>
<p>Let's start the exercise at the end of this section, and we will see an <code>Employee File Manager</code> web application, which allows us to upload personal files to the web application:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_file_manager.jpg"/></p>
<p>The web application does not mention anything about what file types are allowed, and we can drag and drop any file we want, and its name will appear on the upload form, including <code>.php</code> files:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_file_selected_php_file.jpg"/></p>
<p>Furthermore, if we click on the form to select a file, the file selector dialog does not specify any file type, as it says <code>All Files</code> for the file type, which may also suggest that no type of restrictions or limitations are specified for the web application:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_file_selection_dialog.jpg"/></p>
<p>All of this tells us that the program appears to have no file type restrictions on the front-end, and if no restrictions were specified on the back-end, we might be able to upload arbitrary file types to the back-end server to gain complete control over it.</p>
<hr/>
<h2>Identifying Web Framework</h2>
<p>We need to upload a malicious script to test whether we can upload any file type to the back-end server and test whether we can use this to exploit the back-end server. Many kinds of scripts can help us exploit web applications through arbitrary file upload, most commonly a <code>Web Shell</code> script and a <code>Reverse Shell</code> script.</p>
<p>A Web Shell provides us with an easy method to interact with the back-end server by accepting shell commands and printing their output back to us within the web browser. A web shell has to be written in the same programming language that runs the web server, as it runs platform-specific functions and commands to execute system commands on the back-end server, making web shells non-cross-platform scripts. So, the first step would be to identify what language runs the web application.</p>
<p>This is usually relatively simple, as we can often see the web page extension in the URLs, which may reveal the programming language that runs the web application. However, in certain web frameworks and web languages, <code>Web Routes</code> are used to map URLs to web pages, in which case the web page extension may not be shown. Furthermore, file upload exploitation would also be different, as our uploaded files may not be directly routable or accessible.</p>
<p>One easy method to determine what language runs the web application is to visit the <code>/index.ext</code> page, where we would swap out <code>ext</code> with various common web extensions, like <code>php</code>, <code>asp</code>, <code>aspx</code>, among others, to see whether any of them exist.</p>
<p>For example, when we visit our exercise below, we see its URL as <code>http://SERVER_IP:PORT/</code>, as the <code>index</code> page is usually hidden by default. But, if we try visiting <code>http://SERVER_IP:PORT/index.php</code>, we would get the same page, which means that this is indeed a <code>PHP</code> web application. We do not need to do this manually, of course, as we can use a tool like Burp Intruder for fuzzing the file extension using a <a href="https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/web-extensions.txt">Web Extensions</a> wordlist, as we will see in upcoming sections. This method may not always be accurate, though, as the web application may not utilize index pages or may utilize more than one web extension.</p>
<p>Several other techniques may help identify the technologies running the web application, like using the <a href="https://www.wappalyzer.com">Wappalyzer</a> extension, which is available for all major browsers. Once added to our browser, we can click its icon to view all technologies running the web application:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_wappalyzer.jpg"/></p>
<p>As we can see, not only did the extension tell us that the web application runs on <code>PHP</code>, but it also identified the type and version of the web server, the back-end operating system, and other technologies in use. These extensions are essential in a web penetration tester's arsenal, though it is always better to know alternative manual methods to identify the web framework, like the earlier method we discussed.</p>
<p>We may also run web scanners to identify the web framework, like Burp/ZAP scanners or other Web Vulnerability Assessment tools. In the end, once we identify the language running the web application, we may upload a malicious script written in the same language to exploit the web application and gain remote control over the back-end server.</p>
<hr/>
<h2>Vulnerability Identification</h2>
<p>Now that we have identified the web framework running the web application and its programming language, we can test whether we can upload a file with the same extension. As an initial test to identify whether we can upload arbitrary <code>PHP</code> files, let's create a basic <code>Hello World</code> script to test whether we can execute <code>PHP</code> code with our uploaded file.</p>
<p>To do so, we will write <code>&lt;?php echo "Hello HTB";?&gt;</code> to <code>test.php</code>, and try uploading it to the web application:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_upload_php.jpg"/></p>
<p>The file appears to have successfully been uploaded, as we get a message saying <code>File successfully uploaded</code>, which means that <code>the web application has no file validation whatsoever on the back-end</code>. Now, we can click the <code>Download</code> button, and the web application will take us to our uploaded file:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/uploads/test.php" src="/storage/modules/136/file_uploads_hello_htb.jpg"/></p>
<p>As we can see, the page prints our <code>Hello HTB</code> message, which means that the <code>echo</code> function was executed to print our string, and we successfully executed <code>PHP</code> code on the back-end server. If the page could not run PHP code, we would see our source code printed on the page.</p>
<p>In the next section, we will see how to exploit this vulnerability to execute code on the back-end server and take control over it.</p>
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
<label class="module-question" for="858"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Try to upload a PHP script that executes the (hostname) command on the back-end server, and submit the first word of it as the answer.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="fileuploadsabsentverification"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="858" disabled="true" id="btnAnswer858">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint858" data-toggle="modal" id="hintBtn858"><i class="fad fa-life-ring mr-2"></i> Hint
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
