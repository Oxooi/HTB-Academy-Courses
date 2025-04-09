
<h1>Client-Side Validation</h1>
<hr/>
<p>Many web applications only rely on front-end JavaScript code to validate the selected file format before it is uploaded and would not upload it if the file is not in the required format (e.g., not an image).</p>
<p>However, as the file format validation is happening on the client-side, we can easily bypass it by directly interacting with the server, skipping the front-end validations altogether. We may also modify the front-end code through our browser's dev tools to disable any validation in place.</p>
<hr/>
<h2>Client-Side Validation</h2>
<p>The exercise at the end of this section shows a basic <code>Profile Image</code> functionality, frequently seen in web applications that utilize user profile features, like social media web applications:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_profile_image_upload.jpg"/></p>
<p>However, this time, when we get the file selection dialog, we cannot see our <code>PHP</code> scripts (or it may be greyed out), as the dialog appears to be limited to image formats only:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_select_file_types.jpg"/></p>
<p>We may still select the <code>All Files</code> option to select our <code>PHP</code> script anyway, but when we do so, we get an error message saying (<code>Only images are allowed!</code>), and the <code>Upload</code> button gets disabled:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_select_denied.jpg"/></p>
<p>This indicates some form of file type validation, so we cannot just upload a web shell through the upload form as we did in the previous section. Luckily, all validation appears to be happening on the front-end, as the page never refreshes or sends any HTTP requests after selecting our file. So, we should be able to have complete control over these client-side validations.</p>
<p>Any code that runs on the client-side is under our control. While the web server is responsible for sending the front-end code, the rendering and execution of the front-end code happen within our browser. If the web application does not apply any of these validations on the back-end, we should be able to upload any file type.</p>
<p>As mentioned earlier, to bypass these protections, we can either <code>modify the upload request to the back-end server</code>, or we can <code>manipulate the front-end code to disable these type validations</code>.</p>
<hr/>
<h2>Back-end Request Modification</h2>
<p>Let's start by examining a normal request through <code>Burp</code>. When we select an image, we see that it gets reflected as our profile image, and when we click on <code>Upload</code>, our profile image gets updated and persists through refreshes. This indicates that our image was uploaded to the server, which is now displaying it back to us:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_normal_request.jpg"/></p>
<p>If we capture the upload request with <code>Burp</code>, we see the following request being sent by the web application:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_image_upload_request.jpg"/></p>
<p>The web application appears to be sending a standard HTTP upload request to <code>/upload.php</code>. This way, we can now modify this request to meet our needs without having the front-end type validation restrictions. If the back-end server does not validate the uploaded file type, then we should theoretically be able to send any file type/content, and it would be uploaded to the server.</p>
<p>The two important parts in the request are <code>filename="HTB.png"</code> and the file content at the end of the request. If we modify the <code>filename</code> to <code>shell.php</code> and modify the content to the web shell we used in the previous section; we would be uploading a <code>PHP</code> web shell instead of an image.</p>
<p>So, let's capture another image upload request, and then modify it accordingly:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_modified_upload_request.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> We may also modify the <code>Content-Type</code> of the uploaded file, though this should not play an important role at this stage, so we'll keep it unmodified.</p>
</div>
</div>
<p>As we can see, our upload request went through, and we got <code>File successfully uploaded</code> in the response. So, we may now visit our uploaded file and interact with it and gain remote code execution.</p>
<hr/>
<h2>Disabling Front-end Validation</h2>
<p>Another method to bypass client-side validations is through manipulating the front-end code. As these functions are being completely processed within our web browser, we have complete control over them. So, we can modify these scripts or disable them entirely. Then, we may use the upload functionality to upload any file type without needing to utilize <code>Burp</code> to capture and modify our requests.</p>
<p>To start, we can click [<code>CTRL+SHIFT+C</code>] to toggle the browser's <code>Page Inspector</code>, and then click on the profile image, which is where we trigger the file selector for the upload form:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_element_inspector.jpg"/></p>
<p>This will highlight the following HTML file input on line <code>18</code>:</p>
<pre><code class="language-html">&lt;input type="file" name="uploadFile" id="uploadFile" onchange="checkFile(this)" accept=".jpg,.jpeg,.png"&gt;
</code></pre>
<p>Here, we see that the file input specifies (<code>.jpg,.jpeg,.png</code>) as the allowed file types within the file selection dialog. However, we can easily modify this and select <code>All Files</code> as we did before, so it is unnecessary to change this part of the page.</p>
<p>The more interesting part is <code>onchange="checkFile(this)"</code>, which appears to run a JavaScript code whenever we select a file, which appears to be doing the file type validation. To get the details of this function, we can go to the browser's <code>Console</code> by clicking [<code>CTRL+SHIFT+K</code>], and then we can type the function's name (<code>checkFile</code>) to get its details:</p>
<pre><code class="language-javascript">function checkFile(File) {
...SNIP...
    if (extension !== 'jpg' &amp;&amp; extension !== 'jpeg' &amp;&amp; extension !== 'png') {
        $('#error_message').text("Only images are allowed!");
        File.form.reset();
        $("#submit").attr("disabled", true);
    ...SNIP...
    }
}
</code></pre>
<p>The key thing we take from this function is where it checks whether the file extension is an image, and if it is not, it prints the error message we saw earlier (<code>Only images are allowed!</code>) and disables the <code>Upload</code> button. We can add <code>PHP</code> as one of the allowed extensions or modify the function to remove the extension check.</p>
<p>Luckily, we do not need to get into writing and modifying JavaScript code. We can remove this function from the HTML code since its primary use appears to be file type validation, and removing it should not break anything.</p>
<p>To do so, we can go back to our inspector, click on the profile image again, double-click on the function name (<code>checkFile</code>) on line <code>18</code>, and delete it:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_removed_js_function.jpg"/>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Tip:</b> You may also do the same to remove <code>accept=".jpg,.jpeg,.png"</code>, which should make selecting the <code>PHP</code> shell easier in the file selection dialog, though this is not mandatory, as mentioned earlier.</p>
</div>
</div>
<p>With the <code>checkFile</code> function removed from the file input, we should be able to select our <code>PHP</code> web shell through the file selection dialog and upload it normally with no validations, similar to what we did in the previous section.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> The modification we made to the source code is temporary and will not persist through page refreshes, as we are only changing it on the client-side. However, our only need is to bypass the client-side validation, so it should be enough for this purpose.</p>
</div>
</div>
<p>Once we upload our web shell using either of the above methods and then refresh the page, we can use the <code>Page Inspector</code> once more with [<code>CTRL+SHIFT+C</code>], click on the profile image, and we should see the URL of our uploaded web shell:</p>
<pre><code class="language-html">&lt;img src="/profile_images/shell.php" class="profile-image" id="profile-image"&gt;
</code></pre>
<p>If we can click on the above link, we will get to our uploaded web shell, which we can interact with to execute commands on the back-end server:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/profile_images/shell.php?cmd=id" src="/storage/modules/136/file_uploads_php_manual_shell.jpg"/>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> The steps shown apply to Firefox, as other browsers may have slightly different methods for applying local changes to the source, like the use of <code>overrides</code> in Chrome.</p>
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
<label class="module-question" for="857"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Try to bypass the client-side file type validations in the above exercise, then upload a web shell to read /flag.txt (try both bypass methods for better practice)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{cl13n7_51d3_v4l1d4710n_w0n7_570p_m3}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="857" disabled="true" id="btnAnswer857">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint857" data-toggle="modal" id="hintBtn857"><i class="fad fa-life-ring mr-2"></i> Hint
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
