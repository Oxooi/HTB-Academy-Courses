
<h1>ZAP Fuzzer</h1>
<hr/>
<p>ZAP's Fuzzer is called (<code>ZAP Fuzzer</code>). It can be very powerful for fuzzing various web end-points, though it is missing some of the features provided by Burp Intruder. ZAP Fuzzer, however, does not throttle the fuzzing speed, which makes it much more useful than Burp's free Intruder.</p>
<p>In this section, we will try to replicate what we did in the previous section using ZAP Fuzzer to have an "apples to apples" comparison and decide which one we like best.</p>
<hr/>
<h2>Fuzz</h2>
<p>To start our fuzzing, we will visit the URL from the exercise at the end of this section to capture a sample request. As we will be fuzzing for directories, let's visit <code>&lt;http://SERVER_IP:PORT/test/&gt;</code> to place our fuzzing location on <code>test</code> later on. Once we locate our request in the proxy history, we will right-click on it and select (<code>Attack&gt;Fuzz</code>), which will open the <code>Fuzzer</code> window:</p>
<p><img alt="payload processing" src="https://academy.hackthebox.com/storage/modules/110/zap_fuzzer.jpg"/></p>
<p>The main options we need to configure for our Fuzzer attack are:</p>
<ul>
<li>Fuzz Location</li>
<li>Payloads</li>
<li>Processors</li>
<li>Options</li>
</ul>
<p>Let's try to configure them for our web directory fuzzing attack.</p>
<hr/>
<h2>Locations</h2>
<p>The <code>Fuzz Location</code> is very similar to <code>Intruder Payload Position</code>, where our payloads will be placed. To place our location on a certain word, we can select it and click on the <code>Add</code> button on the right pane. So, let's select <code>test</code> and click on <code>Add</code>:</p>
<p><img alt="payload processing" src="https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_add.jpg"/></p>
<p>As we can see, this placed a <code>green</code> marker on our selected location and opened the <code>Payloads</code> window for us to configure our attack payloads.</p>
<hr/>
<h2>Payloads</h2>
<p>The attack payloads in ZAP's Fuzzer are similar in concept to Intruder's Payloads, though they are not as advanced as Intruder's. We can click on the <code>Add</code> button to add our payloads and select from 8 different payload types. The following are some of them:</p>
<ul>
<li>
<code>File</code>: This allows us to select a payload wordlist from a file.</li>
<li>
<code>File Fuzzers</code>: This allows us to select wordlists from built-in databases of wordlists.</li>
<li>
<code>Numberzz</code>: Generates sequences of numbers with custom increments.</li>
</ul>
<p>One of the advantages of ZAP Fuzzer is having built-in wordlists we can choose from so that we do not have to provide our own wordlist. More databases can be installed from the ZAP Marketplace, as we will see in a later section. So, we can select <code>File Fuzzers</code> as the <code>Type</code>, and then we will select the first wordlist from <code>dirbuster</code>:</p>
<p><img alt="payload processing" src="https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_add_payload.jpg"/></p>
<p>Once we click the <code>Add</code> button, our payload wordlist will get added, and we can examine it with the <code>Modify</code> button.</p>
<hr/>
<h2>Processors</h2>
<p>We may also want to perform some processing on each word in our payload wordlist. The following are some of the payload processors we can use:</p>
<ul>
<li>Base64 Decode/Encode</li>
<li>MD5 Hash</li>
<li>Postfix String</li>
<li>Prefix String</li>
<li>SHA-1/256/512 Hash</li>
<li>URL Decode/Encode</li>
<li>Script</li>
</ul>
<p>As we can see, we have a variety of encoders and hashing algorithms to select from. We can also add a custom string before the payload with <code>Prefix String</code> or a custom string with <code>Postfix String</code>. Finally, the <code>Script</code> type allows us to select a custom script that we built and run on every payload before using it in the attack.</p>
<p>We will select the <code>URL Encode</code> processor for our exercise to ensure that our payload gets properly encoded and avoid server errors if our payload contains any special characters. We can click on the <code>Generate Preview</code> button to preview how our final payload will look in the request:</p>
<p><img alt="payload processing" src="https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_add_processor.jpg"/></p>
<p>Once that's done, we can click on <code>Add</code> to add the processor and click on <code>Ok</code> in the processors and payloads windows to close them.</p>
<hr/>
<h2>Options</h2>
<p>Finally, we can set a few options for our fuzzers, similar to what we did with Burp Intruder. For example, we can set the <code>Concurrent threads per scan</code> to <code>20</code>, so our scan runs very quickly:</p>
<p><img alt="payload processing" src="https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_options.jpg"/></p>
<p>The number of threads we set may be limited by how much computer processing power we want to use or how many connections the server allows us to establish.</p>
<p>We may also choose to run through the payloads <code>Depth first</code>, which would attempt all words from the wordlist on a single payload position before moving to the next (e.g., try all passwords for a single user before brute-forcing the following user). We could also use <code>Breadth first</code>, which would run every word from the wordlist on all payload positions before moving to the next word (e.g., attempt every password for all users before moving to the following password).</p>
<hr/>
<h2>Start</h2>
<p>With all of our options configured, we can finally click on the <code>Start Fuzzer</code> button to start our attack. Once our attack is started, we can sort the results by the <code>Response</code> code, as we are only interested in responses with code <code>200</code>:</p>
<p><img alt="payload processing" src="https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_attack.jpg"/></p>
<p>As we can see, we got one hit with code <code>200</code> with the <code>skills</code> payload, meaning that the <code>/skills/</code> directory exists on the server and is accessible. We can click on the request in the results window to view its details:
<img alt="payload processing" src="https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_dir.jpg"/></p>
<p>We can see from the response that this page is indeed accessible by us. There are other fields that may indicate a successful hit depending on the attack scenario, like <code>Size Resp. Body</code> which may indicate that we got a different page if its size was different than other responses, or <code>RTT</code> for attacks like <code>time-based SQL injections</code>, which are detected by a time delay in the server response.</p>
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
<label class="module-question" for="716"><span class="badge badge-soft-dark font-size-14 mr-2">+ 2 <i class="fad fa-cube text-success"></i></span> The directory we found above sets the cookie to the md5 hash of the username, as we can see the md5 cookie in the request for the (guest) user. Visit '/skills/' to get a request with a cookie, then try to use ZAP Fuzzer to fuzz the cookie for different md5 hashed usernames to get the flag. Use the "top-usernames-shortlist.txt" wordlist from Seclists.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer716" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-716">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="716" id="btnAnswer716">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint716" data-toggle="modal" id="hintBtn716"><i class="fad fa-life-ring mr-2"></i> Hint
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
