
<h1>Type Filters</h1>
<hr/>
<p>So far, we have only been dealing with type filters that only consider the file extension in the file name. However, as we saw in the previous section, we may still be able to gain control over the back-end server even with image extensions (e.g. <code>shell.php.jpg</code>). Furthermore, we may utilize some allowed extensions (e.g., SVG) to perform other attacks. All of this indicates that only testing the file extension is not enough to prevent file upload attacks.</p>
<p>This is why many modern web servers and web applications also test the content of the uploaded file to ensure it matches the specified type. While extension filters may accept several extensions, content filters usually specify a single category (e.g., images, videos, documents), which is why they do not typically use blacklists or whitelists. This is because web servers provide functions to check for the file content type, and it usually falls under a specific category.</p>
<p>There are two common methods for validating the file content: <code>Content-Type Header</code> or <code>File Content</code>. Let's see how we can identify each filter and how to bypass both of them.</p>
<hr/>
<h2>Content-Type</h2>
<p>Let's start the exercise at the end of this section and attempt to upload a PHP script:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_content_type_upload.jpg"/></p>
<p>We see that we get a message saying <code>Only images are allowed</code>. The error message persists, and our file fails to upload even if we try some of the tricks we learned in the previous sections. If we change the file name to <code>shell.jpg.phtml</code> or <code>shell.php.jpg</code>, or even if we use <code>shell.jpg</code> with a web shell content, our upload will fail. As the file extension does not affect the error message, the web application must be testing the file content for type validation. As mentioned earlier, this can be either in the <code>Content-Type Header</code> or the <code>File Content</code>.</p>
<p>The following is an example of how a PHP web application tests the Content-Type header to validate the file type:</p>
<pre><code class="language-php">$type = $_FILES['uploadFile']['type'];

if (!in_array($type, array('image/jpg', 'image/jpeg', 'image/png', 'image/gif'))) {
    echo "Only images are allowed";
    die();
}
</code></pre>
<p>The code sets the (<code>$type</code>) variable from the uploaded file's <code>Content-Type</code> header. Our browsers automatically set the Content-Type header when selecting a file through the file selector dialog, usually derived from the file extension. However, since our browsers set this, this operation is a client-side operation, and we can manipulate it to change the perceived file type and potentially bypass the type filter.</p>
<p>We may start by fuzzing the Content-Type header with SecLists' <a href="https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/web-all-content-types.txt">Content-Type Wordlist</a> through Burp Intruder, to see which types are allowed. However, the message tells us that only images are allowed, so we can limit our scan to image types, which reduces the wordlist to <code>45</code> types only (compared to around 700 originally). We can do so as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ wget https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/web-all-content-types.txt
[!bash!]$ cat web-all-content-types.txt | grep 'image/' &gt; image-content-types.txt
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Exercise:</b> Try to run the above scan to find what Content-Types are allowed.</p>
</div>
</div>
<p>For the sake of simplicity, let's just pick an image type (e.g. <code>image/jpg</code>), then intercept our upload request and change the Content-Type header to it:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_bypass_content_type_request.jpg"/></p>
<p>This time we get <code>File successfully uploaded</code>, and if we visit our file, we see that it was successfully uploaded:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/profile_images/shell.php?cmd=id" src="/storage/modules/136/file_uploads_php_manual_shell.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> A file upload HTTP request has two Content-Type headers, one for the attached file (at the bottom), and one for the full request (at the top). We usually need to modify the file's Content-Type header, but in some cases the request will only contain the main Content-Type header (e.g. if the uploaded content was sent as <code>POST</code> data), in which case we will need to modify the main Content-Type header.</p>
</div>
</div>
<hr/>
<h2>MIME-Type</h2>
<p>The second and more common type of file content validation is testing the uploaded file's <code>MIME-Type</code>. <code>Multipurpose Internet Mail Extensions (MIME)</code> is an internet standard that determines the type of a file through its general format and bytes structure.</p>
<p>This is usually done by inspecting the first few bytes of the file's content, which contain the <a href="https://en.wikipedia.org/wiki/List_of_file_signatures">File Signature</a> or <a href="https://web.archive.org/web/20240522030920/https://opensource.apple.com/source/file/file-23/file/magic/magic.mime">Magic Bytes</a>. For example, if a file starts with (<code>GIF87a</code> or <code>GIF89a</code>), this indicates that it is a <code>GIF</code> image, while a file starting with plaintext is usually considered a <code>Text</code> file. If we change the first bytes of any file to the GIF magic bytes, its MIME type would be changed to a GIF image, regardless of its remaining content or extension.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Tip:</b> Many other image types have non-printable bytes for their file signatures, while a <code>GIF</code> image starts with ASCII printable bytes (as shown above), so it is the easiest to imitate. Furthermore, as the string <code>GIF8</code> is common between both GIF signatures, it is usually enough to imitate a GIF image.</p>
</div>
</div>
<p>Let's take a basic example to demonstrate this. The <code>file</code> command on Unix systems finds the file type through the MIME type. If we create a basic file with text in it, it would be considered as a text file, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ echo "this is a text file" &gt; text.jpg 
[!bash!]$ file text.jpg 
text.jpg: ASCII text
</code></pre>
<p>As we see, the file's MIME type is <code>ASCII text</code>, even though its extension is <code>.jpg</code>. However, if we write <code>GIF8</code> to the beginning of the file, it will be considered as a <code>GIF</code> image instead, even though its extension is still <code>.jpg</code>:</p>
<pre><code class="language-shell-session">[!bash!]$ echo "GIF8" &gt; text.jpg 
[!bash!]$file text.jpg
text.jpg: GIF image data
</code></pre>
<p>Web servers can also utilize this standard to determine file types, which is usually more accurate than testing the file extension. The following example shows how a PHP web application can test the MIME type of an uploaded file:</p>
<pre><code class="language-php">$type = mime_content_type($_FILES['uploadFile']['tmp_name']);

if (!in_array($type, array('image/jpg', 'image/jpeg', 'image/png', 'image/gif'))) {
    echo "Only images are allowed";
    die();
}
</code></pre>
<p>As we can see, the MIME types are similar to the ones found in the Content-Type headers, but their source is different, as PHP uses the <code>mime_content_type()</code> function to get a file's MIME type. Let's try to repeat our last attack, but now with an exercise that tests both the Content-Type header and the MIME type:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_bypass_content_type_request.jpg"/>
<p>Once we forward our request, we notice that we get the error message <code>Only images are allowed</code>. Now, let's try to add <code>GIF8</code> before our PHP code to try to imitate a GIF image while keeping our file extension as <code>.php</code>, so it would execute PHP code regardless:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_bypass_mime_type_request.jpg"/>
<p>This time we get <code>File successfully uploaded</code>, and our file is successfully uploaded to the server:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/136/file_uploads_bypass_mime_type.jpg"/></p>
<p>We can now visit our uploaded file, and we will see that we can successfully execute system commands:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/profile_images/shell.php?cmd=id" src="/storage/modules/136/file_uploads_php_manual_shell_gif.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> We see that the command output starts with <code>GIF8</code> , as this was the first line in our PHP script to imitate the GIF magic bytes, and is now outputted as a plaintext before our PHP code is executed.</p>
</div>
</div>
<p>We can use a combination of the two methods discussed in this section, which may help us bypass some more robust content filters. For example, we can try using an <code>Allowed MIME type with a disallowed Content-Type</code>, an <code>Allowed MIME/Content-Type with a disallowed extension</code>, or a <code>Disallowed MIME/Content-Type with an allowed extension</code>, and so on. Similarly, we can attempt other combinations and permutations to try to confuse the web server, and depending on the level of code security, we may be able to bypass various filters.</p>
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
<label class="module-question" for="869"><span class="badge badge-soft-dark font-size-14 mr-2">+ 2 <i class="fad fa-cube text-success"></i></span> The above server employs Client-Side, Blacklist, Whitelist, Content-Type, and MIME-Type filters to ensure the uploaded file is an image. Try to combine all of the attacks you learned so far to bypass these filters and upload a PHP file and read the flag at "/flag.txt"
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer869" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-869">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="869" id="btnAnswer869">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint869" data-toggle="modal" id="hintBtn869"><i class="fad fa-life-ring mr-2"></i> Hint
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
