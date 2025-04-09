
<h1>Burp Intruder</h1>
<hr/>
<p>Both Burp and ZAP provide additional features other than the default web proxy, which are essential for web application penetration testing. Two of the most important extra features are <code>web fuzzers</code> and <code>web scanners</code>. The built-in web fuzzers are powerful tools that act as web fuzzing, enumeration, and brute-forcing tools. This may also act as an alternative for many of the CLI-based fuzzers we use, like <code>ffuf</code>, <code>dirbuster</code>, <code>gobuster</code>, <code>wfuzz</code>, among others.</p>
<p>Burp's web fuzzer is called <code>Burp Intruder</code>, and can be used to fuzz pages, directories, sub-domains, parameters, parameters values, and many other things. Though it is much more advanced than most CLI-based web fuzzing tools, the free <code>Burp Community</code> version is throttled at a speed of 1 request per second, making it extremely slow compared to CLI-based web fuzzing tools, which can usually read up to 10k requests per second. This is why we would only use the free version of Burp Intruder for short queries. The <code>Pro</code> version has unlimited speed, which can rival common web fuzzing tools, in addition to the very useful features of Burp Intruder. This makes it one of the best web fuzzing and brute-forcing tools.</p>
<p>In this section, we will demonstrate the various uses of Burp Intruder for web fuzzing and enumeration.</p>
<hr/>
<h2>Target</h2>
<p>As usual, we'll start up Burp and its pre-configured browser and then visit the web application from the exercise at the end of this section. Once we do, we can go to the Proxy History, locate our request, then right-click on the request and select <code>Send to Intruder</code>, or use the shortcut [<code>CTRL+I</code>] to send it to <code>Intruder</code>.</p>
<p>We can then go to <code>Intruder</code> by clicking on its tab or with the shortcut [<code>CTRL+SHIFT+I</code>], which takes us right to <code>Burp Intruder</code>:</p>
<p><img alt="intruder_target" src="https://academy.hackthebox.com/storage/modules/110/burp_intruder_target.jpg"/></p>
<p>On the first tab, '<code>Target</code>', we see the details of the target we will be fuzzing, which is fed from the request we sent to <code>Intruder</code>.</p>
<hr/>
<h2>Positions</h2>
<p>The second tab, '<code>Positions</code>', is where we place the payload position pointer, which is the point where words from our wordlist will be placed and iterated over. We will be demonstrating how to fuzz web directories, which is similar to what's done by tools like <code>ffuf</code> or <code>gobuster</code>.</p>
<p>To check whether a web directory exists, our fuzzing should be in '<code>GET /DIRECTORY/</code>', such that existing pages would return <code>200 OK</code>, otherwise we'd get <code>404 NOT FOUND</code>. So, we will need to select <code>DIRECTORY</code> as the payload position, by either wrapping it with <code>§</code> or by selecting the word <code>DIRECTORY</code> and clicking on the <code>Add §</code> button:</p>
<p><img alt="intruder_position" src="https://academy.hackthebox.com/storage/modules/110/burp_intruder_position.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: the <code>DIRECTORY</code> in this case is the pointer's name, which can be anything, and can be used to refer to each pointer, in case we are using more than position with different wordlists for each.</p>
</div>
</div>
<p>The final thing to select in the target tab is the <code>Attack Type</code>. The attack type defines how many payload pointers are used and determines which payload is assigned to which position. For simplicity, we'll stick to the first type, <code>Sniper</code>, which uses only one position. Try clicking on the <code>?</code> at the top of the window to read more about attack types, or check out this <a href="https://portswigger.net/burp/documentation/desktop/tools/intruder/positions#attack-type">link</a>.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: Be sure to leave the extra two lines at the end of the request, otherwise we may get an error response from the server.</p>
</div>
</div>
<hr/>
<h2>Payloads</h2>
<p>On the third tab, '<code>Payloads</code>', we get to choose and customize our payloads/wordlists. This payload/wordlist is what would be iterated over, and each element/line of it would be placed and tested one by one in the Payload Position we chose earlier. There are four main things we need to configure:</p>
<ul>
<li>Payload Sets</li>
<li>Payload Options</li>
<li>Payload Processing</li>
<li>Payload Encoding</li>
</ul>
<h4>Payload Sets</h4>
<p>The first thing we must configure is the <code>Payload Set</code>. The payload set identifies the Payload number, depending on the attack type and number of Payloads we used in the Payload Position Pointers:</p>
<p><img alt="Payload Sets" src="https://academy.hackthebox.com/storage/modules/110/burp_intruder_payload_set.jpg"/></p>
<p>In this case, we only have one Payload Set, as we chose the '<code>Sniper</code>' Attack type with only one payload position. If we have chosen the '<code>Cluster Bomb</code>' attack type, for example, and added several payload positions, we would get more payload sets to choose from and choose different options for each. In our case, we'll select <code>1</code> for the payload set.</p>
<p>Next, we need to select the <code>Payload Type</code>, which is the type of payloads/wordlists we will be using. Burp provides a variety of Payload Types, each of which acts in a certain way. For example:</p>
<ul>
<li>
<p><code>Simple List</code>: The basic and most fundamental type. We provide a wordlist, and Intruder iterates over each line in it.</p>
</li>
<li>
<p><code>Runtime file</code>: Similar to <code>Simple List</code>, but loads line-by-line as the scan runs to avoid excessive memory usage by Burp.</p>
</li>
<li>
<p><code>Character Substitution</code>: Lets us specify a list of characters and their replacements, and Burp Intruder tries all potential permutations.</p>
</li>
</ul>
<p>There are many other Payload Types, each with its own options, and many of which can build custom wordlists for each attack. Try clicking on the <code>?</code> next to <code>Payload Sets</code>, and then click on <code>Payload Type</code>, to learn more about each Payload Type. In our case, we'll be going with a basic <code>Simple List</code>.</p>
<h4>Payload Options</h4>
<p>Next, we must specify the Payload Options, which is different for each Payload Type we select in <code>Payload Sets</code>.  For a <code>Simple List</code>, we have to create or load a wordlist. To do so, we can input each item manually by clicking <code>Add</code>, which would build our wordlist on the fly. The other more common option is to click on <code>Load</code>, and then select a file to load into Burp Intruder.</p>
<p>We will select <code>/opt/useful/seclists/Discovery/Web-Content/common.txt</code> as our wordlist. We can see that Burp Intruder loads all lines of our wordlist into the Payload Options table:</p>
<p><img alt="Payload Options" src="https://academy.hackthebox.com/storage/modules/110/burp_intruder_payload_wordlist.jpg"/></p>
<p>We can add another wordlist or manually add a few items, and they would be appended to the same list of items. We can use this to combine multiple wordlists or create customized wordlists. In Burp Pro, we also can select from a list of existing wordlists contained within Burp by choosing from the <code>Add from list</code> menu option.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: In case you wanted to use a very large wordlist, it's best to use <code>Runtime file</code> as the Payload Type instead of <code>Simple List</code>, so that Burp Intruder won't have to load the entire wordlist in advance, which may throttle memory usage.</p>
</div>
</div>
<h4>Payload Processing</h4>
<p>Another option we can apply is <code>Payload Processing</code>, which allows us to determine fuzzing rules over the loaded wordlist. For example, if we wanted to add an extension after our payload item, or if we wanted to filter the wordlist based on specific criteria, we can do so with payload processing.</p>
<p>Let's try adding a rule that skips any lines that start with a <code>.</code> (as shown in the wordlist screenshot earlier). We can do that by clicking on the <code>Add</code> button and then selecting <code>Skip if matches regex</code>, which allows us to provide a regex pattern for items we want to skip. Then, we can provide a regex pattern that matches lines starting with <code>.</code>, which is: <code>^\..*$</code>:</p>
<p><img alt="payload processing" src="https://academy.hackthebox.com/storage/modules/110/burp_intruder_payload_processing_1.jpg"/></p>
<p>We can see that our rule gets added and enabled:
<img alt="payload processing" src="https://academy.hackthebox.com/storage/modules/110/burp_intruder_payload_processing_2.jpg"/></p>
<h4>Payload Encoding</h4>
<p>The fourth and final option we can apply is <code>Payload Encoding</code>, enabling us to enable or disable Payload URL-encoding.</p>
<p><img alt="payload encoding" src="https://academy.hackthebox.com/storage/modules/110/burp_intruder_payload_encoding.jpg"/></p>
<p>We'll leave it enabled.</p>
<hr/>
<h2>Options</h2>
<p>Finally, we can customize our attack options from the <code>Options</code> tab. There are many options we can customize (or leave at default) for our attack. For example, we can set the number of <code>retried on failure</code> and <code>pause before retry</code> to 0.</p>
<p>Another useful option is the <code>Grep - Match</code>, which enables us to flag specific requests depending on their responses. As we are fuzzing web directories, we are only interested in responses with HTTP code <code>200 OK</code>. So, we'll first enable it and then click <code>Clear</code> to clear the current list. After that, we can type <code>200 OK</code> to match any requests with this string and click <code>Add</code> to add the new rule. Finally, we'll also disable <code>Exclude HTTP Headers</code>, as what we are looking for is in the HTTP header:</p>
<p><img alt="options match" src="https://academy.hackthebox.com/storage/modules/110/burp_intruder_options_match.jpg"/></p>
<p>We may also utilize the <code>Grep - Extract</code> option, which is useful if the HTTP responses are lengthy, and we're only interested in a certain part of the response. So, this helps us in only showing a specific part of the response. We are only looking for responses with HTTP Code <code>200 OK</code>, regardless of their content, so we will not opt for this option.</p>
<p>Try other <code>Intruder</code> options, and use Burp help by clicking on <code>?</code> next to each one to learn more about each option.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: We may also use the <code>Resource Pool</code> tab to specify how much network resources Intruder will use, which may be useful for very large attacks. For our example, we'll leave it at its default values.</p>
</div>
</div>
<hr/>
<h2>Attack</h2>
<p>Now that everything is properly set up, we can click on the <code>Start Attack</code> button and wait for our attack to finish. Once again, in the free <code>Community Version</code>, these attacks would be very slow and take a considerable amount of time for longer wordlists.</p>
<p>The first thing we will notice is that all lines starting with <code>.</code> were skipped, and we directly started with the lines after them:</p>
<p><img alt="intruder_attack_exclude" src="https://academy.hackthebox.com/storage/modules/110/burp_intruder_attack_exclude.jpg"/></p>
<p>We can also see the <code>200 OK</code> column, which shows requests that match the <code>200 OK</code> grep value we specified in the Options tab. We can click on it to sort by it, such that we'll have matching results at the top. Otherwise, we can sort by <code>status</code> or by <code>Length</code>. Once our scan is done, we see that we get one hit <code>/admin</code>:</p>
<p><img alt="intruder_attack" src="https://academy.hackthebox.com/storage/modules/110/burp_intruder_attack.jpg"/></p>
<p>We may now manually visit the page <code>&lt;http://SERVER_IP:PORT/admin/&gt;</code>, to make sure that it does exist.</p>
<p>Similarly, we can use <code>Burp Intruder</code> to do any type of web fuzzing and brute-forcing, including brute forcing for passwords, or fuzzing for certain PHP parameters, and so on. We can even use <code>Intruder</code> to perform password spraying against applications that use Active Directory (AD) authentication such as Outlook Web Access (OWA), SSL VPN portals, Remote Desktop Services (RDS), Citrix, custom web applications that use AD authentication, and more. However, as the free version of <code>Intruder</code> is extremely throttled, in the next section, we will see ZAP's fuzzer and its various options, which do not have a paid tier.</p>
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
<img alt="sparkles-icon-decoration" class="ml-2 w-auto sparkles-icon" height="20" src="/images/sparkles-solid.svg"/>
</div>
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
<label class="module-question" for="711"><span class="badge badge-soft-dark font-size-14 mr-2">+ 2 <i class="fad fa-cube text-success"></i></span> Use Burp Intruder to fuzz for '.html' files under the /admin directory, to find a file containing the flag.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{burp_1n7rud3r_fuzz3r!}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="711" disabled="true" id="btnAnswer711">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint711" data-toggle="modal" id="hintBtn711"><i class="fad fa-life-ring mr-2"></i> Hint
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
