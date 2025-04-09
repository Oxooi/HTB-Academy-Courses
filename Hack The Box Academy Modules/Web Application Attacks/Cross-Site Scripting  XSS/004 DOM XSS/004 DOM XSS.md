
<h1>DOM XSS</h1>
<hr/>
<p>The third and final type of XSS is another <code>Non-Persistent</code> type called <code>DOM-based XSS</code>. While <code>reflected XSS</code> sends the input data to the back-end server through HTTP requests, DOM XSS is completely processed on the client-side through JavaScript. DOM XSS occurs when JavaScript is used to change the page source through the <code>Document Object Model (DOM)</code>.</p>
<p>We can run the server below to see an example of a web application vulnerable to DOM XSS. We can try adding a <code>test</code> item, and we see that the web application is similar to the <code>To-Do List</code> web applications we previously used:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/103/xss_dom_1.jpg"/>
<p>However, if we open the <code>Network</code> tab in the Firefox Developer Tools, and re-add the <code>test</code> item, we would notice that no HTTP requests are being made:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/103/xss_dom_network.jpg"/>
<p>We see that the input parameter in the URL is using a hashtag <code>#</code> for the item we added, which means that this is a client-side parameter that is completely processed on the browser. This indicates that the input is being processed at the client-side through JavaScript and never reaches the back-end; hence it is a <code>DOM-based XSS</code>.</p>
<p>Furthermore, if we look at the page source by hitting [<code>CTRL+U</code>], we will notice that our <code>test</code> string is nowhere to be found. This is because the JavaScript code is updating the page when we click the <code>Add</code> button, which is after the page source is retrieved by our browser, hence the base page source will not show our input, and if we refresh the page, it will not be retained (i.e. <code>Non-Persistent</code>). We can still view the rendered page source with the Web Inspector tool by clicking [<code>CTRL+SHIFT+C</code>]:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/103/xss_dom_inspector.jpg"/></p>
<hr/>
<h2>Source &amp; Sink</h2>
<p>To further understand the nature of the DOM-based XSS vulnerability, we must understand the concept of the <code>Source</code> and <code>Sink</code> of the object displayed on the page. The <code>Source</code> is the JavaScript object that takes the user input, and it can be any input parameter like a URL parameter or an input field, as we saw above.</p>
<p>On the other hand, the <code>Sink</code> is the function that writes the user input to a DOM Object on the page. If the <code>Sink</code> function does not properly sanitize the user input, it would be vulnerable to an XSS attack. Some of the commonly used JavaScript functions to write to DOM objects are:</p>
<ul>
<li>
<code>document.write()</code>
</li>
<li>
<code>DOM.innerHTML</code>
</li>
<li>
<code>DOM.outerHTML</code>
</li>
</ul>
<p>Furthermore, some of the <code>jQuery</code> library functions that write to DOM objects are:</p>
<ul>
<li>
<code>add()</code>
</li>
<li>
<code>after()</code>
</li>
<li>
<code>append()</code>
</li>
</ul>
<p>If a <code>Sink</code> function writes the exact input without any sanitization (like the above functions), and no other means of sanitization were used, then we know that the page should be vulnerable to XSS.</p>
<p>We can look at the source code of the <code>To-Do</code> web application, and check <code>script.js</code>, and we will see that the <code>Source</code> is being taken from the <code>task=</code> parameter:</p>
<pre><code class="language-javascript">var pos = document.URL.indexOf("task=");
var task = document.URL.substring(pos + 5, document.URL.length);
</code></pre>
<p>Right below these lines, we see that the page uses the <code>innerHTML</code> function to write the <code>task</code> variable in the <code>todo</code> DOM:</p>
<pre><code class="language-javascript">document.getElementById("todo").innerHTML = "&lt;b&gt;Next Task:&lt;/b&gt; " + decodeURIComponent(task);
</code></pre>
<p>So, we can see that we can control the input, and the output is not being sanitized, so this page should be vulnerable to DOM XSS.</p>
<hr/>
<h2>DOM Attacks</h2>
<p>If we try the XSS payload we have been using previously, we will see that it will not execute. This is because the <code>innerHTML</code> function does not allow the use of the <code>&lt;script&gt;</code> tags within it as a security feature. Still, there are many other XSS payloads we use that do not contain <code>&lt;script&gt;</code> tags, like the following XSS payload:</p>
<pre><code class="language-html">&lt;img src="" onerror=alert(window.origin)&gt;
</code></pre>
<p>The above line creates a new HTML image object, which has a <code>onerror</code> attribute that can execute JavaScript code when the image is not found. So, as we provided an empty image link (<code>""</code>), our code should always get executed without having to use <code>&lt;script&gt;</code> tags:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/#task=&lt;img src='' onerror=alert(window.origin)&gt;" src="/storage/modules/103/xss_dom_alert.jpg"/>
<p>To target a user with this DOM XSS vulnerability, we can once again copy the URL from the browser and share it with them, and once they visit it, the JavaScript code should execute. Both of these payloads are among the most basic XSS payloads. There are many instances where we may need to use various payloads depending on the security of the web application and the browser, which we will discuss in the next section.</p>
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
<label class="module-question" for="637"><span class="badge badge-soft-dark font-size-14 mr-2">+ 2 <i class="fad fa-cube text-success"></i></span> To get the flag, use the same payload we used above, but change its JavaScript code to show the cookie instead of showing the url.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{pur3ly_cl13n7_51d3}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="637" disabled="true" id="btnAnswer637">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint637" data-toggle="modal" id="hintBtn637"><i class="fad fa-life-ring mr-2"></i> Hint
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
