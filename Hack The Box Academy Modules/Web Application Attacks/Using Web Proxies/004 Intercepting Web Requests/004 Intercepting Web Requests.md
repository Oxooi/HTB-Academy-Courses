
<h1>Intercepting Web Requests</h1>
<hr/>
<p>Now that we have set up our proxy, we can use it to intercept and manipulate various HTTP requests sent by the web application we are testing. We'll start by learning how to intercept web requests, change them, and then send them through to their intended destination.</p>
<hr/>
<h2>Intercepting Requests</h2>
<h4>Burp</h4>
<p>In Burp, we can navigate to the <code>Proxy</code> tab, and request interception should be on by default. If we want to turn request interception on or off, we may go to the <code>Intercept</code> sub-tab and click on <code>Intercept is on/off</code> button to do so:</p>
<p><img alt="Burp Intercept On" src="https://academy.hackthebox.com/storage/modules/110/burp_intercept_htb_on.jpg"/></p>
<p>Once we turn request interception on, we can start up the pre-configured browser and then visit our target website after spawning it from the exercise at the end of this section. Then, once we go back to Burp, we will see the intercepted request awaiting our action, and we can click on <code>forward</code> to forward the request:</p>
<p><img alt="Burp Intercept Page" src="https://academy.hackthebox.com/storage/modules/110/burp_intercept_page.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: as all Firefox traffic will be intercepted in this case, we may see another request has been intercepted before this one. If this happens, click 'Forward', until we get the request to our target IP, as shown above.</p>
</div>
</div>
<h4>ZAP</h4>
<p>In ZAP, interception is off by default, as shown by the green button on the top bar (green indicates that requests can pass and not be intercepted). We can click on this button to turn the Request Interception on or off, or we can use the shortcut [<code>CTRL+B</code>] to toggle it on or off:</p>
<p><img alt="ZAP Intercept On" src="https://academy.hackthebox.com/storage/modules/110/zap_intercept_htb_on.jpg"/></p>
<p>Then, we can start the pre-configured browser and revisit the exercise webpage. We will see the intercepted request in the top-right pane, and we can click on the step (right to the red <code>break</code> button) to forward the request:</p>
<p><img alt="ZAP Intercept Page" src="https://academy.hackthebox.com/storage/modules/110/zap_intercept_page.jpg"/></p>
<p>ZAP also has a powerful feature called <code>Heads Up Display (HUD)</code>, which allows us to control most of the main ZAP features from right within the pre-configured browser. We can enable the <code>HUD</code> by clicking its button at the end of the top menu bar:</p>
<p><img alt="ZAP HUD On" src="https://academy.hackthebox.com/storage/modules/110/zap_enable_HUD.jpg"/></p>
<p>The HUD has many features that we will cover as we go through the module. For intercepting requests, we can click on the second button from the top on the left pane to turn request interception on:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/110/zap_hud_break.jpg"/>
<p>Now, once we refresh the page or send another request, the HUD will intercept the request and will present it to us for action:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/110/zap_hud_break_request.jpg"/>
<p>We can choose to <code>step</code> to send the request and examine its response and break any further requests, or we can choose to <code>continue</code> and let the page send the remaining requests. The <code>step</code> button is helpful when we want to examine every step of the page's functionality, while <code>continue</code> is useful when we are only interested in a single request and can forward the remaining requests once we reach our target request.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Tip:</b> The first time you use the pre-configured ZAP browser you will be presented with the HUD tutorial. You may consider taking this tutorial after this section, as it will teach you the basics of the HUD. Even if you do not grasp everything, the upcoming sections should cover whatever you missed. If you do not get the tutorial, you can click on the configuration button on the bottom right and choose "Take the HUD tutorial".</p>
</div>
</div>
<hr/>
<h2>Manipulating Intercepted Requests</h2>
<p>Once we intercept the request, it will remain hanging until we forward it, as we did above. We can examine the request, manipulate it to make any changes we want, and then send it to its destination. This helps us better understand what information a particular web application is sending in its web requests and how it may respond to any changes we make in that request.</p>
<p>There are numerous applications for this in Web Penetration Testing, such as testing for:</p>
<ol>
<li>SQL injections</li>
<li>Command injections</li>
<li>Upload bypass</li>
<li>Authentication bypass</li>
<li>XSS</li>
<li>XXE</li>
<li>Error handling</li>
<li>Deserialization</li>
</ol>
<p>And many other potential web vulnerabilities, as we will see in other web modules in HTB Academy. So, let's show this with a basic example to demonstrate intercepting and manipulating web requests.</p>
<p>Let us turn request interception back on in the tool of our choosing, set the <code>IP</code> value on the page, then click on the <code>Ping</code> button. Once our request is intercepted, we should get a similar HTTP request to the following :</p>
<pre><code class="language-http">POST /ping HTTP/1.1
Host: 46.101.23.188:30820
Content-Length: 4
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://46.101.23.188:30820
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://46.101.23.188:30820/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

ip=1
</code></pre>
<p>Typically, we can only specify numbers in the <code>IP</code> field using the browser, as the web page prevents us from sending any non-numeric characters using front-end JavaScript. However, with the power of intercepting and manipulating HTTP requests, we can try using other characters to "break" the application ("breaking" the request/response flow by manipulating the target parameter, not damaging the target web application).  If the web application does not verify and validate the HTTP requests on the back-end, we may be able to manipulate it and exploit it.</p>
<p>So, let us change the <code>ip</code> parameter's value from <code>1</code> to <code>;ls;</code> and see how the web application handles our input:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/110/ping_manipulate_request.jpg"/>
<p>Once we click continue/forward, we will see that the response changed from the default ping output to the <code>ls</code> output, meaning that we successfully manipulated the request to inject our command:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/110/ping_inject.jpg"/>
<p>This demonstrates a basic example of how request interception and manipulation can help with testing web applications for various vulnerabilities, which is considered an essential tool to be able to test different web applications effectively.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: As previously mentioned, we will not be covering specific web attacks in this module, but rather how Web Proxies can facilitate various types of attacks. Other web modules in HTB Academy cover these types of attacks in depth.</p>
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
<label class="module-question" for="707"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Try intercepting the ping request on the server shown above, and change the post data similarly to what we did in this section. Change the command to read 'flag.txt'
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{1n73rc3p73d_1n_7h3_m1ddl3}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="707" disabled="true" id="btnAnswer707">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint707" data-toggle="modal" id="hintBtn707"><i class="fad fa-life-ring mr-2"></i> Hint
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
