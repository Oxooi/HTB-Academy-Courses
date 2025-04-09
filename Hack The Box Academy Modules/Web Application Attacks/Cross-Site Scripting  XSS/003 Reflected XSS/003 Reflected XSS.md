
<h1>Reflected XSS</h1>
<hr/>
<p>There are two types of <code>Non-Persistent XSS</code> vulnerabilities: <code>Reflected XSS</code>, which gets processed by the back-end server, and <code>DOM-based XSS</code>, which is completely processed on the client-side and never reaches the back-end server. Unlike Persistent XSS, <code>Non-Persistent XSS</code> vulnerabilities are temporary and are not persistent through page refreshes. Hence, our attacks only affect the targeted user and will not affect other users who visit the page.</p>
<p><code>Reflected XSS</code> vulnerabilities occur when our input reaches the back-end server and gets returned to us without being filtered or sanitized. There are many cases in which our entire input might get returned to us, like error messages or confirmation messages. In these cases, we may attempt using XSS payloads to see whether they execute. However, as these are usually temporary messages, once we move from the page, they would not execute again, and hence they are <code>Non-Persistent</code>.</p>
<p>We can start the server below to practice on a web page vulnerable to a Reflected XSS vulnerability. It is a similar <code>To-Do List</code> app to the one we practiced with in the previous section. We can try adding any <code>test</code> string to see how it's handled:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/103/xss_reflected_1.jpg"/>
<p>As we can see, we get <code>Task 'test' could not be added.</code>, which includes our input <code>test</code> as part of the error message. If our input was not filtered or sanitized, the page might be vulnerable to XSS. We can try the same XSS payload we used in the previous section and click <code>Add</code>:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/103/xss_reflected_2.jpg"/>
<p>Once we click <code>Add</code>, we get the alert pop-up:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/103/xss_stored_xss_alert.jpg"/>
<p>In this case, we see that the error message now says <code>Task '' could not be added.</code>. Since our payload is wrapped with a <code>&lt;script&gt;</code> tag, it does not get rendered by the browser, so we get empty single quotes <code>''</code> instead. We can once again view the page source to confirm that the error message includes our XSS payload:</p>
<pre><code class="language-html">&lt;div&gt;&lt;/div&gt;&lt;ul class="list-unstyled" id="todo"&gt;&lt;div style="padding-left:25px"&gt;Task '&lt;script&gt;alert(window.origin)&lt;/script&gt;' could not be added.&lt;/div&gt;&lt;/ul&gt;
</code></pre>
<p>As we can see, the single quotes indeed contain our XSS payload <code>'&lt;script&gt;alert(window.origin)&lt;/script&gt;'</code>.</p>
<p>If we visit the <code>Reflected</code> page again, the error message no longer appears, and our XSS payload is not executed, which means that this XSS vulnerability is indeed <code>Non-Persistent</code>.</p>
<p><code>But if the XSS vulnerability is Non-Persistent, how would we target victims with it?</code></p>
<p>This depends on which HTTP request is used to send our input to the server. We can check this through the Firefox <code>Developer Tools</code> by clicking [<code>CTRL+Shift+I</code>] and selecting the <code>Network</code> tab. Then, we can put our <code>test</code> payload again and click <code>Add</code> to send it:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/103/xss_reflected_network.jpg"/>
<p>As we can see, the first row shows that our request was a <code>GET</code> request. <code>GET</code> request sends their parameters and data as part of the URL. So, <code>to target a user, we can send them a URL containing our payload</code>. To get the URL, we can copy the URL from the URL bar in Firefox after sending our XSS payload, or we can right-click on the <code>GET</code> request in the <code>Network</code> tab and select <code>Copy&gt;Copy URL</code>. Once the victim visits this URL, the XSS payload would execute:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/index.php?task=&lt;script&gt;alert(window.origin)&lt;/script&gt;" src="/storage/modules/103/xss_stored_xss_alert.jpg"/>
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
<label class="module-question" for="636"><span class="badge badge-soft-dark font-size-14 mr-2">+ 2 <i class="fad fa-cube text-success"></i></span> To get the flag, use the same payload we used above, but change its JavaScript code to show the cookie instead of showing the url.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{r3fl3c73d_b4ck_2_m3}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="636" disabled="true" id="btnAnswer636">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint636" data-toggle="modal" id="hintBtn636"><i class="fad fa-life-ring mr-2"></i> Hint
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
