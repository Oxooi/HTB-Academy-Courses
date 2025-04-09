
<h1>Bypassing Web Application Protections</h1>
<hr/>
<p>There won't be any protection(s) deployed on the target side in an ideal scenario, thus not preventing automatic exploitation. Otherwise, we can expect problems when running an automated tool of any kind against such a target. Nevertheless, many mechanisms are incorporated into SQLMap, which can help us successfully bypass such protections.</p>
<hr/>
<h2>Anti-CSRF Token Bypass</h2>
<p>One of the first lines of defense against the usage of automation tools is the incorporation of anti-CSRF (i.e., Cross-Site Request Forgery) tokens into all HTTP requests, especially those generated as a result of web-form filling.</p>
<p>In most basic terms, each HTTP request in such a scenario should have a (valid) token value available only if the user actually visited and used the page. While the original idea was the prevention of scenarios with malicious links, where just opening these links would have undesired consequences for unaware logged-in users (e.g., open administrator pages and add a new user with predefined credentials), this security feature also inadvertently hardened the applications against the (unwanted) automation.</p>
<p>Nevertheless, SQLMap has options that can help in bypassing anti-CSRF protection. Namely, the most important option is <code>--csrf-token</code>. By specifying the token parameter name (which should already be available within the provided request data), SQLMap will automatically attempt to parse the target response content and search for fresh token values so it can use them in the next request.</p>
<p>Additionally, even in a case where the user does not explicitly specify the token's name via <code>--csrf-token</code>, if one of the provided parameters contains any of the common infixes (i.e. <code>csrf</code>, <code>xsrf</code>, <code>token</code>), the user will be prompted whether to update it in further requests:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u "http://www.example.com/" --data="id=1&amp;csrf-token=WfF1szMUHhiokx9AHFply5L2xAOfjRkE" --csrf-token="csrf-token"

        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.4.9}
|_ -| . [']     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org

[*] starting @ 22:18:01 /2020-09-18/

POST parameter 'csrf-token' appears to hold anti-CSRF token. Do you want sqlmap to automatically update it in further requests? [y/N] y
</code></pre>
<hr/>
<h2>Unique Value Bypass</h2>
<p>In some cases, the web application may only require unique values to be provided inside predefined parameters. Such a mechanism is similar to the anti-CSRF technique described above, except that there is no need to parse the web page content. So, by simply ensuring that each request has a unique value for a predefined parameter, the web application can easily prevent CSRF attempts while at the same time averting some of the automation tools. For this, the option <code>--randomize</code> should be used, pointing to the parameter name containing a value which should be randomized before being sent:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u "http://www.example.com/?id=1&amp;rp=29125" --randomize=rp --batch -v 5 | grep URI

URI: http://www.example.com:80/?id=1&amp;rp=99954
URI: http://www.example.com:80/?id=1&amp;rp=87216
URI: http://www.example.com:80/?id=9030&amp;rp=36456
URI: http://www.example.com:80/?id=1.%2C%29%29%27.%28%28%2C%22&amp;rp=16689
URI: http://www.example.com:80/?id=1%27xaFUVK%3C%27%22%3EHKtQrg&amp;rp=40049
URI: http://www.example.com:80/?id=1%29%20AND%209368%3D6381%20AND%20%287422%3D7422&amp;rp=95185
</code></pre>
<hr/>
<h2>Calculated Parameter Bypass</h2>
<p>Another similar mechanism is where a web application expects a proper parameter value to be calculated based on some other parameter value(s). Most often, one parameter value has to contain the message digest (e.g. <code>h=MD5(id)</code>) of another one. To bypass this, the option <code>--eval</code> should be used, where a valid Python code is being evaluated just before the request is being sent to the target:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u "http://www.example.com/?id=1&amp;h=c4ca4238a0b923820dcc509a6f75849b" --eval="import hashlib; h=hashlib.md5(id).hexdigest()" --batch -v 5 | grep URI

URI: http://www.example.com:80/?id=1&amp;h=c4ca4238a0b923820dcc509a6f75849b
URI: http://www.example.com:80/?id=1&amp;h=c4ca4238a0b923820dcc509a6f75849b
URI: http://www.example.com:80/?id=9061&amp;h=4d7e0d72898ae7ea3593eb5ebf20c744
URI: http://www.example.com:80/?id=1%2C.%2C%27%22.%2C%28.%29&amp;h=620460a56536e2d32fb2f4842ad5a08d
URI: http://www.example.com:80/?id=1%27MyipGP%3C%27%22%3EibjjSu&amp;h=db7c815825b14d67aaa32da09b8b2d42
URI: http://www.example.com:80/?id=1%29%20AND%209978%socks4://177.39.187.70:33283ssocks4://177.39.187.70:332833D1232%20AND%20%284955%3D4955&amp;h=02312acd4ebe69e2528382dfff7fc5cc
</code></pre>
<hr/>
<h2>IP Address Concealing</h2>
<p>In case we want to conceal our IP address, or if a certain web application has a protection mechanism that blacklists our current IP address, we can try to use a proxy or the anonymity network Tor. A proxy can be set with the option <code>--proxy</code> (e.g. <code>--proxy="socks4://177.39.187.70:33283"</code>), where we should add a working proxy.</p>
<p>In addition to that, if we have a list of proxies, we can provide them to SQLMap with the option <code>--proxy-file</code>. This way, SQLMap will go sequentially through the list, and in case of any problems (e.g., blacklisting of IP address), it will just skip from current to the next from the list. The other option is Tor network use to provide an easy to use anonymization, where our IP can appear anywhere from a large list of Tor exit nodes. When properly installed on the local machine, there should be a <code>SOCKS4</code> proxy service at the local port 9050 or 9150. By using switch <code>--tor</code>, SQLMap will automatically try to find the local port and use it appropriately.</p>
<p>If we wanted to be sure that Tor is properly being used, to prevent unwanted behavior, we could use the switch <code>--check-tor</code>. In such cases, SQLMap will connect to the <code>https://check.torproject.org/</code> and check the response for the intended result (i.e., <code>Congratulations</code> appears inside).</p>
<hr/>
<h2>WAF Bypass</h2>
<p>Whenever we run SQLMap, As part of the initial tests, SQLMap sends a predefined malicious looking payload using a non-existent parameter name (e.g. <code>?pfov=...</code>) to test for the existence of a WAF (Web Application Firewall). There will be a substantial change in the response compared to the original in case of any protection between the user and the target. For example, if one of the most popular WAF solutions (ModSecurity) is implemented, there should be a <code>406 - Not Acceptable</code> response after such a request.</p>
<p>In case of a positive detection, to identify the actual protection mechanism, SQLMap uses a third-party library <a href="https://github.com/stamparm/identYwaf">identYwaf</a>, containing the signatures of 80 different WAF solutions. If we wanted to skip this heuristical test altogether (i.e., to produce less noise), we can use switch <code>--skip-waf</code>.</p>
<hr/>
<h2>User-agent Blacklisting Bypass</h2>
<p>In case of immediate problems (e.g., HTTP error code 5XX from the start) while running SQLMap, one of the first things we should think of is the potential blacklisting of the default user-agent used by SQLMap (e.g. <code>User-agent: sqlmap/1.4.9 (http://sqlmap.org)</code>).</p>
<p>This is trivial to bypass with the switch <code>--random-agent</code>, which changes the default user-agent with a randomly chosen value from a large pool of values used by browsers.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: If some form of protection is detected during the run, we can expect problems with the target, even other security mechanisms. The main reason is the continuous development and new improvements in such protections, leaving smaller and smaller maneuver space for attackers.</p>
</div>
</div>
<hr/>
<h2>Tamper Scripts</h2>
<p>Finally, one of the most popular mechanisms implemented in SQLMap for bypassing WAF/IPS solutions is the so-called "tamper" scripts. Tamper scripts are a special kind of (Python) scripts written for modifying requests just before being sent to the target, in most cases to bypass some protection.</p>
<p>For example, one of the most popular tamper scripts <a href="https://github.com/sqlmapproject/sqlmap/blob/master/tamper/between.py">between</a> is replacing all occurrences of greater than operator (<code>&gt;</code>) with <code>NOT BETWEEN 0 AND #</code>, and the equals operator (<code>=</code>) with <code>BETWEEN # AND #</code>. This way, many primitive protection mechanisms (focused mostly on preventing XSS attacks) are easily bypassed, at least for SQLi purposes.</p>
<p>Tamper scripts can be chained, one after another, within the <code>--tamper</code> option (e.g. <code>--tamper=between,randomcase</code>), where they are run based on their predefined priority. A priority is predefined to prevent any unwanted behavior, as some scripts modify payloads by modifying their SQL syntax (e.g. <a href="https://github.com/sqlmapproject/sqlmap/blob/master/tamper/ifnull2ifisnull.py">ifnull2ifisnull</a>). In contrast, some tamper scripts do not care about the inner content (e.g. <a href="https://github.com/sqlmapproject/sqlmap/blob/master/tamper/appendnullbyte.py">appendnullbyte</a>).</p>
<p>Tamper scripts can modify any part of the request, although the majority change the payload content. The most notable tamper scripts are the following:</p>
<table>
<thead>
<tr>
<th><strong>Tamper-Script</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>0eunion</code></td>
<td>Replaces instances of <int> UNION with <int>e0UNION</int></int></td>
</tr>
<tr>
<td><code>base64encode</code></td>
<td>Base64-encodes all characters in a given payload</td>
</tr>
<tr>
<td><code>between</code></td>
<td>Replaces greater than operator (<code>&gt;</code>) with <code>NOT BETWEEN 0 AND #</code> and equals operator (<code>=</code>) with <code>BETWEEN # AND #</code></td>
</tr>
<tr>
<td><code>commalesslimit</code></td>
<td>Replaces (MySQL) instances like <code>LIMIT M, N</code> with <code>LIMIT N OFFSET M</code> counterpart</td>
</tr>
<tr>
<td><code>equaltolike</code></td>
<td>Replaces all occurrences of operator equal (<code>=</code>) with <code>LIKE</code> counterpart</td>
</tr>
<tr>
<td><code>halfversionedmorekeywords</code></td>
<td>Adds (MySQL) versioned comment before each keyword</td>
</tr>
<tr>
<td><code>modsecurityversioned</code></td>
<td>Embraces complete query with (MySQL) versioned comment</td>
</tr>
<tr>
<td><code>modsecurityzeroversioned</code></td>
<td>Embraces complete query with (MySQL) zero-versioned comment</td>
</tr>
<tr>
<td><code>percentage</code></td>
<td>Adds a percentage sign (<code>%</code>) in front of each character (e.g. SELECT -&gt; %S%E%L%E%C%T)</td>
</tr>
<tr>
<td><code>plus2concat</code></td>
<td>Replaces plus operator (<code>+</code>) with (MsSQL) function CONCAT() counterpart</td>
</tr>
<tr>
<td><code>randomcase</code></td>
<td>Replaces each keyword character with random case value (e.g. SELECT -&gt; SEleCt)</td>
</tr>
<tr>
<td><code>space2comment</code></td>
<td>Replaces space character (<code> </code>) with comments `/</td>
</tr>
<tr>
<td><code>space2dash</code></td>
<td>Replaces space character (<code> </code>) with a dash comment (<code>--</code>) followed by a random string and a new line (<code>\n</code>)</td>
</tr>
<tr>
<td><code>space2hash</code></td>
<td>Replaces (MySQL) instances of space character (<code> </code>) with a pound character (<code>#</code>) followed by a random string  and a new line (<code>\n</code>)</td>
</tr>
<tr>
<td><code>space2mssqlblank</code></td>
<td>Replaces (MsSQL) instances of space character (<code> </code>) with a random blank character from a valid set of alternate characters</td>
</tr>
<tr>
<td><code>space2plus</code></td>
<td>Replaces space character (<code> </code>) with plus (<code>+</code>)</td>
</tr>
<tr>
<td><code>space2randomblank</code></td>
<td>Replaces space character (<code> </code>) with a random blank character from a valid set of alternate characters</td>
</tr>
<tr>
<td><code>symboliclogical</code></td>
<td>Replaces AND and OR logical operators with their symbolic counterparts (<code>&amp;&amp;</code> and <code>||</code>)</td>
</tr>
<tr>
<td><code>versionedkeywords</code></td>
<td>Encloses each non-function keyword with (MySQL) versioned comment</td>
</tr>
<tr>
<td><code>versionedmorekeywords</code></td>
<td>Encloses each keyword with (MySQL) versioned comment</td>
</tr>
</tbody>
</table>
<p>To get a whole list of implemented tamper scripts, along with the description as above, switch <code>--list-tampers</code> can be used. We can also develop custom Tamper scripts for any custom type of attack, like a second-order SQLi.</p>
<hr/>
<h2>Miscellaneous Bypasses</h2>
<p>Out of other protection bypass mechanisms, there are also two more that should be mentioned. The first one is the <code>Chunked</code> transfer encoding, turned on using the switch <code>--chunked</code>, which splits the POST request's body into so-called "chunks." Blacklisted SQL keywords are split between chunks in a way that the request containing them can pass unnoticed.</p>
<p>The other bypass mechanisms is the <code>HTTP parameter pollution</code>  (<code>HPP</code>), where payloads are split in a similar way as in case of <code>--chunked</code> between different same parameter named values (e.g. <code>?id=1&amp;id=UNION&amp;id=SELECT&amp;id=username,password&amp;id=FROM&amp;id=users...</code>), which are concatenated by the target platform if supporting it (e.g. <code>ASP</code>).</p>
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
<label class="module-question" for="298"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What's the contents of table flag8? (Case #8)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer298" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-298">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="298" id="btnAnswer298">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint298" data-toggle="modal" id="hintBtn298"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="299"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What's the contents of table flag9? (Case #9)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer299" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-299">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="299" id="btnAnswer299">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint299" data-toggle="modal" id="hintBtn299"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="300"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What's the contents of table flag10? (Case #10)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer300" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-300">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="300" id="btnAnswer300">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint300" data-toggle="modal" id="hintBtn300"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="305"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What's the contents of table flag11? (Case #11)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer305" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-305">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="305" id="btnAnswer305">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint305" data-toggle="modal" id="hintBtn305"><i class="fad fa-life-ring mr-2"></i> Hint
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
