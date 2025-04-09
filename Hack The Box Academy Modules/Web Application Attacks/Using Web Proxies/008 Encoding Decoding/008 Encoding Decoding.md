
<h1>Encoding/Decoding</h1>
<hr/>
<p>As we modify and send custom HTTP requests, we may have to perform various types of encoding and decoding to interact with the webserver properly. Both tools have built-in encoders that can help us in quickly encoding and decoding various types of text.</p>
<hr/>
<h2>URL Encoding</h2>
<p>It is essential to ensure that our request data is URL-encoded and our request headers are correctly set. Otherwise, we may get a server error in the response. This is why encoding and decoding data becomes essential as we modify and repeat web requests. Some of the key characters we need to encode are:</p>
<ul>
<li>
<code>Spaces</code>: May indicate the end of request data if not encoded</li>
<li>
<code>&amp;</code>: Otherwise interpreted as a parameter delimiter</li>
<li>
<code>#</code>: Otherwise interpreted as a fragment identifier</li>
</ul>
<p>To URL-encode text in Burp Repeater, we can select that text and right-click on it, then select (<code>Convert Selection&gt;URL&gt;URL encode key characters</code>), or by selecting the text and clicking [<code>CTRL+U</code>]. Burp also supports URL-encoding as we type if we right-click and enable that option, which will encode all of our text as we type it. On the other hand, ZAP should automatically URL-encode all of our request data in the background before sending the request, though we may not see that explicitly.</p>
<p>There are other types of URL-encoding, like <code>Full URL-Encoding</code> or <code>Unicode URL</code> encoding, which may also be helpful for requests with many special characters.</p>
<hr/>
<h2>Decoding</h2>
<p>While URL-encoding is key to HTTP requests, it is not the only type of encoding we will encounter. It is very common for web applications to encode their data, so we should be able to quickly decode that data to examine the original text. On the other hand, back-end servers may expect data to be encoded in a particular format or with a specific encoder, so we need to be able to quickly encode our data before we send it.</p>
<p>The following are some of the other types of encoders supported by both tools:</p>
<ul>
<li>HTML</li>
<li>Unicode</li>
<li>Base64</li>
<li>ASCII hex</li>
</ul>
<p>To access the full encoder in Burp, we can go to the <code>Decoder</code> tab. In ZAP, we can use the <code>Encoder/Decoder/Hash</code> by clicking [<code>CTRL+E</code>]. With these encoders, we can input any text and have it quickly encoded or decoded. For example, perhaps we came across the following cookie that is base64 encoded, and we need to decode it: <code>eyJ1c2VybmFtZSI6Imd1ZXN0IiwgImlzX2FkbWluIjpmYWxzZX0=</code></p>
<p>We can input the above string in Burp Decoder and select <code>Decode as &gt; Base64</code>, and we'll get the decoded value:</p>
<p><img alt="Burp B64 Decode" src="https://academy.hackthebox.com/storage/modules/110/burp_b64_decode.jpg"/></p>
<p>In recent versions of Burp, we can also use the <code>Burp Inspector</code> tool to perform encoding and decoding (among other things), which can be found in various places like <code>Burp Proxy</code> or <code>Burp Repeater</code>:</p>
<p><img alt="Burp Inspector" src="https://academy.hackthebox.com/storage/modules/110/burp_inspector.jpg"/></p>
<p>In ZAP, we can use the <code>Encoder/Decoder/Hash</code> tool, which will automatically decode strings using various decoders in the <code>Decode</code> tab:
<img alt="ZAP B64 Decode" src="https://academy.hackthebox.com/storage/modules/110/zap_b64_decode.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: We can create customized tabs in ZAP's Encoder/Decoder/Hash with the "Add New Tab" button, and then we can add any type of encoder/decoder we want the text to be shown in. Try to create your own tab with a few encoders/decoders.</p>
</div>
</div>
<hr/>
<h2>Encoding</h2>
<p>As we can see, the text holds the value <code>{"username":"guest", "is_admin":false}</code>. So, if we were performing a penetration test on a web application and find that the cookie holds this value, we may want to test modifying it to see whether it changes our user privileges. So, we can copy the above value, change <code>guest</code> to <code>admin</code> and <code>false</code> to <code>true</code>, and try to encode it again using its original encoding method (<code>base64</code>):</p>
<p><img alt="Burp B64 Encode" src="https://academy.hackthebox.com/storage/modules/110/burp_b64_encode.jpg"/></p>
<p><img alt="ZAP B64 Encode" src="https://academy.hackthebox.com/storage/modules/110/zap_b64_encode.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: Burp Decoder output can be directly encoded/decoded with a different encoder. Select the new encoder method in the output pane at the bottom, and it will be encoded/decoded again. In ZAP, we can copy the output text and paste it in the input field above.</p>
</div>
</div>
<p>We can then copy the base64 encoded string and use it with our request in Burp <code>Repeater</code> or ZAP <code>Request Editor</code>. The same concept can be used to encode and decode various types of encoded text to perform effective web penetration testing without utilizing other tools to do the encoding.</p>
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
<label class="module-question" for="709"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> The string found in the attached file has been encoded several times with various encoders. Try to use the decoding tools we discussed to decode it and get the flag.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{3nc0d1n6_n1nj4}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="709" disabled="true" id="btnAnswer709">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<a class="btn btn-outline-success btn-block" href="/storage/modules/110/encoded_flag.zip"><i class="fas fa-download mr-2"></i> encoded_flag.zip
                                        </a>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint709" data-toggle="modal" id="hintBtn709"><i class="fad fa-life-ring mr-2"></i> Hint
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
