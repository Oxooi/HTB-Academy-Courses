
<h1>Basic Bypasses</h1>
<p>In the previous section, we saw several types of attacks that we can use for different types of LFI vulnerabilities. In many cases, we may be facing a web application that applies various protections against file inclusion, so our normal LFI payloads would not work. Still, unless the web application is properly secured against malicious LFI user input, we may be able to bypass the protections in place and reach file inclusion.</p>
<hr/>
<h2>Non-Recursive Path Traversal Filters</h2>
<p>One of the most basic filters against LFI is a search and replace filter, where it simply deletes substrings of (<code>../</code>) to avoid path traversals. For example:</p>
<pre><code class="language-php">$language = str_replace('../', '', $_GET['language']);
</code></pre>
<p>The above code is supposed to prevent path traversal, and hence renders LFI useless. If we try the LFI payloads we tried in the previous section, we get the following:
<img alt="Shipping containers and cranes at a port with PHP include error messages displayed." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=../../../../etc/passwd" src="/storage/modules/23/lfi_blacklist.png"/></p>
<p>We see that all <code>../</code> substrings were removed, which resulted in a final path being <code>./languages/etc/passwd</code>. However, this filter is very insecure, as it is not <code>recursively removing</code> the <code>../</code> substring, as it runs a single time on the input string and does not apply the filter on the output string. For example, if we use <code>....//</code> as our payload, then the filter would remove <code>../</code> and the output string would be <code>../</code>, which means we may still perform path traversal. Let's try applying this logic to include <code>/etc/passwd</code> again:
<img alt="Shipping containers and cranes at a port with a list of system user accounts displayed." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=....//....//....//....//etc/passwd" src="/storage/modules/23/lfi_blacklist_passwd.png"/></p>
<p>As we can see, the inclusion was successful this time, and we're able to read <code>/etc/passwd</code> successfully. The <code>....//</code> substring is not the only bypass we can use, as we may use <code>..././</code> or <code>....\/</code> and several other recursive LFI payloads. Furthermore, in some cases, escaping the forward slash character may also work to avoid path traversal filters (e.g. <code>....\/</code>), or adding extra forward slashes (e.g. <code>....////</code>)</p>
<hr/>
<h2>Encoding</h2>
<p>Some web filters may prevent input filters that include certain LFI-related characters, like a dot <code>.</code> or a slash <code>/</code> used for path traversals. However, some of these filters may be bypassed by URL encoding our input, such that it would no longer include these bad characters, but would still be decoded back to our path traversal string once it reaches the vulnerable function. Core PHP filters on versions 5.3.4 and earlier were specifically vulnerable to this bypass, but even on newer versions we may find custom filters that may be bypassed through URL encoding.</p>
<p>If the target web application did not allow <code>.</code> and <code>/</code> in our input, we can URL encode <code>../</code> into <code>%2e%2e%2f</code>, which may bypass the filter. To do so, we can use any online URL encoder utility or use the Burp Suite Decoder tool, as follows:
<img alt="burp_url_encode" src="https://academy.hackthebox.com/storage/modules/23/burp_url_encode.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> For this to work we must URL encode all characters, including the dots. Some URL encoders may not encode dots as they are considered to be part of the URL scheme.</p>
</div>
</div>
<p>Let's try to use this encoded LFI payload against our earlier vulnerable web application that filters <code>../</code> strings:
<img alt="Burp Suite Decoder showing path traversal input '../../etc/passwd' and its URL-encoded output." class="website-screenshot" data-url="&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64" src="/storage/modules/23/lfi_blacklist_passwd_filter.png"/></p>
<p>As we can see, we were also able to successfully bypass the filter and use path traversal to read <code>/etc/passwd</code>. Furthermore, we may also use Burp Decoder to encode the encoded string once again to have a <code>double encoded</code> string, which may also bypass other types of filters.</p>
<p>You may refer to the <a href="/module/details/109">Command Injections</a> module for more about bypassing various blacklisted characters, as the same techniques may be used with LFI as well.</p>
<hr/>
<h2>Approved Paths</h2>
<p>Some web applications may also use Regular Expressions to ensure that the file being included is under a specific path. For example, the web application we have been dealing with may only accept paths that are under the <code>./languages</code> directory, as follows:</p>
<pre><code class="language-php">if(preg_match('/^\.\/languages\/.+$/', $_GET['language'])) {
    include($_GET['language']);
} else {
    echo 'Illegal path specified!';
}
</code></pre>
<p>To find the approved path, we can examine the requests sent by the existing forms, and see what path they use for the normal web functionality. Furthermore, we can fuzz web directories under the same path, and try different ones until we get a match. To bypass this, we may use path traversal and start our payload with the approved path, and then use <code>../</code> to go back to the root directory and read the file we specify, as follows:
<img alt="Shipping containers and cranes at a port with a list of system user accounts displayed." class="website-screenshot" data-url="&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=./languages/../../../../etc/passwd" src="/storage/modules/23/lfi_blacklist_passwd_filter.png"/></p>
<p>Some web applications may apply this filter along with one of the earlier filters, so we may combine both techniques by starting our payload with the approved path, and then URL encode our payload or use recursive payload.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> All techniques mentioned so far should work with any LFI vulnerability, regardless of the back-end development language or framework.</p>
</div>
</div>
<hr/>
<h2>Appended Extension</h2>
<p>As discussed in the previous section, some web applications append an extension to our input string (e.g. <code>.php</code>), to ensure that the file we include is in the expected extension. With modern versions of PHP, we may not be able to bypass this and will be restricted to only reading files in that extension, which may still be useful, as we will see in the next section (e.g. for reading source code).</p>
<p>There are a couple of other techniques we may use, but they are <code>obsolete with modern versions of PHP and only work with PHP versions before 5.3/5.4</code>. However, it may still be beneficial to mention them, as some web applications may still be running on older servers, and these techniques may be the only bypasses possible.</p>
<h4>Path Truncation</h4>
<p>In earlier versions of PHP, defined strings have a maximum length of 4096 characters, likely due to the limitation of 32-bit systems. If a longer string is passed, it will simply be <code>truncated</code>, and any characters after the maximum length will be ignored. Furthermore, PHP also used to remove trailing slashes and single dots in path names, so if we call (<code>/etc/passwd/.</code>) then the <code>/.</code> would also be truncated, and PHP would call (<code>/etc/passwd</code>). PHP, and Linux systems in general, also disregard multiple slashes in the path (e.g. <code>////etc/passwd</code> is the same as <code>/etc/passwd</code>). Similarly, a current directory shortcut (<code>.</code>) in the middle of the path would also be disregarded (e.g. <code>/etc/./passwd</code>).</p>
<p>If we combine both of these PHP limitations together, we can create very long strings that evaluate to a correct path. Whenever we reach the 4096 character limitation, the appended extension (<code>.php</code>) would be truncated, and we would have a path without an appended extension. Finally, it is also important to note that we would also need to <code>start the path with a non-existing directory</code> for this technique to work.</p>
<p>An example of such payload would be the following:</p>
<pre><code class="language-url">?language=non_existing_directory/../../../etc/passwd/./././.[./ REPEATED ~2048 times]
</code></pre>
<p>Of course, we don't have to manually type <code>./</code> 2048 times (total of 4096 characters), but we can automate the creation of this string with the following command:</p>
<pre><code class="language-shell-session">[!bash!]$ echo -n "non_existing_directory/../../../etc/passwd/" &amp;&amp; for i in {1..2048}; do echo -n "./"; done
non_existing_directory/../../../etc/passwd/./././&lt;SNIP&gt;././././
</code></pre>
<p>We may also increase the count of <code>../</code>, as adding more would still land us in the root directory, as explained in the previous section. However, if we use this method, we should calculate the full length of the string to ensure only <code>.php</code> gets truncated and not our requested file at the end of the string (<code>/etc/passwd</code>). This is why it would be easier to use the first method.</p>
<h4>Null Bytes</h4>
<p>PHP versions before 5.5 were vulnerable to <code>null byte injection</code>, which means that adding a null byte (<code>%00</code>) at the end of the string would terminate the string and not consider anything after it. This is due to how strings are stored in low-level memory, where strings in memory must use a null byte to indicate the end of the string, as seen in Assembly, C, or C++ languages.</p>
<p>To exploit this vulnerability, we can end our payload with a null byte (e.g. <code>/etc/passwd%00</code>), such that the final path passed to <code>include()</code> would be (<code>/etc/passwd%00.php</code>). This way, even though <code>.php</code> is appended to our string, anything after the null byte would be truncated, and so the path used would actually be <code>/etc/passwd</code>, leading us to bypass the appended extension.</p>
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
<label class="module-question" for="1070"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> The above web application employs more than one filter to avoid LFI exploitation. Try to bypass these filters to read /flag.txt
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer1070" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-1070">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="1070" id="btnAnswer1070">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint1070" data-toggle="modal" id="hintBtn1070"><i class="fad fa-life-ring mr-2"></i> Hint
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
