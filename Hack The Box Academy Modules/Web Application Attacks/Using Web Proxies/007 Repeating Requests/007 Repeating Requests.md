
<h1>Repeating Requests</h1>
<hr/>
<p>In the previous sections, we successfully bypassed the input validation to use a non-numeric input to reach command injection on the remote server. If we want to repeat the same process with a different command, we would have to intercept the request again, provide a different payload, forward it again, and finally check our browser to get the final result.</p>
<p>As you can imagine, if we would do this for each command, it would take us forever to enumerate a system, as each command would require 5-6 steps to get executed. However, for such repetitive tasks, we can utilize request repeating to make this process significantly easier.</p>
<p>Request repeating allows us to resend any web request that has previously gone through the web proxy. This allows us to make quick changes to any request before we send it, then get the response within our tools without intercepting and modifying each request.</p>
<hr/>
<h2>Proxy History</h2>
<p>To start, we can view the HTTP requests history in <code>Burp</code> at (<code>Proxy&gt;HTTP History</code>):</p>
<p><img alt="Burp history tab" src="https://academy.hackthebox.com/storage/modules/110/burp_history_tab.jpg"/></p>
<p>In <code>ZAP</code> HUD, we can find it in the bottom History pane or ZAP's main UI at the bottom <code>History</code> tab as well:</p>
<p><img alt="ZAP history tab" src="https://academy.hackthebox.com/storage/modules/110/zap_history_tab.jpg"/></p>
<p>Both tools also provide filtering and sorting options for requests history, which may be helpful if we deal with a huge number of requests and want to locate a specific request. <code>Try to see how filters work on both tools.</code></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: Both tools also maintain WebSockets history, which shows all connections initiated by the web application even after being loaded, like asynchronous updates and data fetching. WebSockets can be useful when performing advanced web penetration testing, and are out of the scope of this module.</p>
</div>
</div>
<p>If we click on any request in the history in either tool, its details will be shown:</p>
<p><code>Burp</code>:
<img alt="Burp request details" src="https://academy.hackthebox.com/storage/modules/110/burp_history_details.jpg"/></p>
<p><code>ZAP</code>:
<img alt="ZAP request details" src="https://academy.hackthebox.com/storage/modules/110/zap_history_details.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: While ZAP only shows the final/modified request that was sent, Burp provides the ability to examine both the original request and the modified request. If a request was edited, the pane header would say <code>Original Request</code>, and we can click on it and select <code>Edited Request</code> to examine the final request that was sent.</p>
</div>
</div>
<hr/>
<h2>Repeating Requests</h2>
<h4>Burp</h4>
<p>Once we locate the request we want to repeat, we can click [<code>CTRL+R</code>] in Burp to send it to the <code>Repeater</code> tab, and then we can either navigate to the <code>Repeater</code> tab or click [<code>CTRL+SHIFT+R</code>] to go to it directly. Once in <code>Repeater</code>, we can click on <code>Send</code> to send the request:</p>
<p><img alt="Burp repeat request" src="https://academy.hackthebox.com/storage/modules/110/burp_repeater_request.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: We can also right-click on the request and select <code>Change Request Method</code> to change the HTTP method between POST/GET without having to rewrite the entire request.</p>
</div>
</div>
<h4>ZAP</h4>
<p>In ZAP, once we locate our request, we can right-click on it and select <code>Open/Resend with Request Editor</code>, which would open the request editor window, and allow us to resend the request with the <code>Send</code> button to send our request:
<img alt="ZAP resend request" src="https://academy.hackthebox.com/storage/modules/110/zap_repeater_request.jpg"/></p>
<p>We can also see the <code>Method</code> drop-down menu, allowing us to quickly switch the request method to any other HTTP method.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: By default, the Request Editor window in ZAP has the Request/Response in different tabs. You can click on the display buttons to change how they are organized. To match the above look choose the same display options shown in the screenshot.</p>
</div>
</div>
<p>We can achieve the same result within the pre-configured browser with <code>ZAP HUD</code>. We can locate the request in the bottom History pane, and once we click on it, the <code>Request Editor</code> window will show, allowing us to resend it. We can select <code>Replay in Console</code> to get the response in the same <code>HUD</code> window, or select <code>Replay in Browser</code> to see the response rendered in the browser:</p>
<p><img alt="ZAP HUD resend" src="https://academy.hackthebox.com/storage/modules/110/zap_hud_resend.jpg"/></p>
<p>So, let us try to modify our request and send it. In all three options (<code>Burp Repeater</code>, <code>ZAP Request Editor</code>, and <code>ZAP HUD</code>), we see that the requests are modifiable, and we can select the text we want to change and replace it with whatever we want, and then click the <code>Send</code> button to send it again:</p>
<p><img alt="Burp modify repeat" src="https://academy.hackthebox.com/storage/modules/110/burp_repeat_modify.jpg"/></p>
<p>As we can see, we could easily modify the command and instantly get its output by using Burp <code>Repeater</code>. Try doing the same in <code>ZAP Request Editor</code> and <code>ZAP HUD</code> to see how they work.</p>
<p>Finally, we can see in our previous POST request that the data is URL-encoded. This is an essential part of sending custom HTTP requests, which we will discuss in the next section.</p>
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
<label class="module-question" for="708"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Try using request repeating to be able to quickly test commands. With that, try looking for the other flag.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{qu1ckly_r3p3471n6_r3qu3575}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="708" disabled="true" id="btnAnswer708">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint708" data-toggle="modal" id="hintBtn708"><i class="fad fa-life-ring mr-2"></i> Hint
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
