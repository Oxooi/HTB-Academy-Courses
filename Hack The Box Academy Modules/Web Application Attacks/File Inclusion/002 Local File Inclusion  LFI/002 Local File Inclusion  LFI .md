
<h1>Local File Inclusion (LFI)</h1>
<p>Now that we understand what File Inclusion vulnerabilities are and how they occur, we can start learning how we can exploit these vulnerabilities in different scenarios to be able to read the content of local files on the back-end server.</p>
<hr/>
<h2>Basic LFI</h2>
<p>The exercise we have at the end of this section shows us an example of a web app that allows users to set their language to either English or Spanish:
<img alt="Webpage showing 'Inlane Freight' with a language dropdown menu open, displaying options for 'English' and 'Spanish'." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/" src="/storage/modules/23/basic_lfi_lang.png"/></p>
<p>If we select a language by clicking on it (e.g. <code>Spanish</code>), we see that the content text changes to spanish:
<img alt="Shipping containers stacked at a port with cranes in the background, illustrating the history and industry of container shipping." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=es.php" src="/storage/modules/23/basic_lfi_es.png"/></p>
<p>We also notice that the URL includes a <code>language</code> parameter that is now set to the language we selected (<code>es.php</code>). There are several ways the content could be changed to match the language we specified. It may be pulling the content from a different database table based on the specified parameter, or it may be loading an entirely different version of the web app. However, as previously discussed, loading part of the page using template engines is the easiest and most common method utilized.</p>
<p>So, if the web application is indeed pulling a file that is now being included in the page, we may be able to change the file being pulled to read the content of a different local file. Two common readable files that are available on most back-end servers are <code>/etc/passwd</code> on Linux and <code>C:\Windows\boot.ini</code> on Windows. So, let's change the parameter from <code>es</code> to <code>/etc/passwd</code>:
<img alt="Shipping containers and cranes at a port, with a list of system user accounts displayed." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=/etc/passwd" src="/storage/modules/23/basic_lfi_lang_passwd.png"/></p>
<p>As we can see, the page is indeed vulnerable, and we are able to read the content of the <code>passwd</code> file and identify what users exist on the back-end server.</p>
<hr/>
<h2>Path Traversal</h2>
<p>In the earlier example, we read a file by specifying its <code>absolute path</code> (e.g. <code>/etc/passwd</code>). This would work if the whole input was used within the <code>include()</code> function without any additions, like the following example:</p>
<pre><code class="language-php">include($_GET['language']);
</code></pre>
<p>In this case, if we try to read <code>/etc/passwd</code>, then the <code>include()</code> function would fetch that file directly. However, in many occasions, web developers may append or prepend a string to the <code>language</code> parameter. For example, the <code>language</code> parameter may be used for the filename, and may be added after a directory, as follows:</p>
<pre><code class="language-php">include("./languages/" . $_GET['language']);
</code></pre>
<p>In this case, if we attempt to read <code>/etc/passwd</code>, then the path passed to <code>include()</code> would be (<code>./languages//etc/passwd</code>), and as this file does not exist, we will not be able to read anything:
<img alt="Shipping containers and cranes at a port with PHP include error messages displayed." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=/etc/passwd" src="/storage/modules/23/traversal_passwd_failed.png"/></p>
<p>As expected, the verbose error returned shows us the string passed to the <code>include()</code> function, stating that there is no <code>/etc/passwd</code> in the languages directory.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> We are only enabling PHP errors on this web application for educational purposes, so we can properly understand how the web application is handling our input. For production web applications, such errors should never be shown. Furthermore, all of our attacks should be possible without errors, as they do not rely on them.</p>
</div>
</div>
<p>We can easily bypass this restriction by traversing directories using <code>relative paths</code>. To do so, we can add <code>../</code> before our file name, which refers to the parent directory. For example, if the full path of the languages directory is <code>/var/www/html/languages/</code>, then using <code>../index.php</code> would refer to the <code>index.php</code> file on the parent directory (i.e. <code>/var/www/html/index.php</code>).</p>
<p>So, we can use this trick to go back several directories until we reach the root path (i.e. <code>/</code>), and then specify our absolute file path (e.g. <code>../../../../etc/passwd</code>), and the file should exist:
<img alt="Shipping containers and cranes at a port with a list of system user accounts displayed." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=../../../../etc/passwd" src="/storage/modules/23/traversal_passwd.png"/></p>
<p>As we can see, this time we were able to read the file regardless of the directory we were in. This trick would work even if the entire parameter was used in the <code>include()</code> function, so we can default to this technique, and it should work in both cases. Furthermore, if we were at the root path (<code>/</code>) and used <code>../</code> then we would still remain in the root path. So, if we were not sure of the directory the web application is in, we can add <code>../</code> many times, and it should not break the path (even if we do it a hundred times!).</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Tip:</b> It can always be useful to be efficient and not add unnecessary <code>../</code> several times, especially if we were writing a report or writing an exploit. So, always try to find the minimum number of <code>../</code> that works and use it. You may also be able to calculate how many directories you are away from the root path and use that many. For example, with <code>/var/www/html/</code> we are <code>3</code> directories away from the root path, so we can use <code>../</code> 3 times (i.e. <code>../../../</code>).</p>
</div>
</div>
<hr/>
<h2>Filename Prefix</h2>
<p>In our previous example, we used the <code>language</code> parameter after the directory, so we could traverse the path to read the <code>passwd</code> file. On some occasions, our input may be appended after a different string. For example, it may be used with a prefix to get the full filename, like the following example:</p>
<pre><code class="language-php">include("lang_" . $_GET['language']);
</code></pre>
<p>In this case, if we try to traverse the directory with <code>../../../etc/passwd</code>, the final string would be <code>lang_../../../etc/passwd</code>, which is invalid:
<img alt="Shipping containers and cranes at a port with a PHP include error message displayed." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=../../../etc/passwd" src="/storage/modules/23/lfi_another_example1.png"/></p>
<p>As expected, the error tells us that this file does not exist. so, instead of directly using path traversal, we can prefix a <code>/</code> before our payload, and this should consider the prefix as a directory, and then we should bypass the filename and be able to traverse directories:
<img alt="Shipping containers and cranes at a port with a list of system user accounts displayed." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=/../../../etc/passwd" src="/storage/modules/23/lfi_another_example_passwd1.png"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> This may not always work, as in this example a directory named <code>lang_/</code> may not exist, so our relative path may not be correct. Furthermore, <code>any prefix appended to our input may break some file inclusion techniques</code> we will discuss in upcoming sections, like using PHP wrappers and filters or RFI.</p>
</div>
</div>
<hr/>
<h2>Appended Extensions</h2>
<p>Another very common example is when an extension is appended to the <code>language</code> parameter, as follows:</p>
<pre><code class="language-php">include($_GET['language'] . ".php");
</code></pre>
<p>This is quite common, as in this case, we would not have to write the extension every time we need to change the language. This may also be safer as it may restrict us to only including PHP files. In this case, if we try to read <code>/etc/passwd</code>, then the file included would be <code>/etc/passwd.php</code>, which does not exist:
<img alt="Shipping containers and cranes at a port with PHP include error messages displayed." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/extension/index.php?language=/etc/passwd" src="/storage/modules/23/lfi_extension_failed.png"/></p>
<p>There are several techniques that we can use to bypass this, and we will discuss them in upcoming sections.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Exercise:</b> Try to read any php file (e.g. index.php) through LFI, and see whether you would get its source code or if the file gets rendered as HTML instead.</p>
</div>
</div>
<hr/>
<h2>Second-Order Attacks</h2>
<p>As we can see, LFI attacks can come in different shapes. Another common, and a little bit more advanced, LFI attack is a <code>Second Order Attack</code>. This occurs because many web application functionalities may be insecurely pulling files from the back-end server based on user-controlled parameters.</p>
<p>For example, a web application may allow us to download our avatar through a URL like (<code>/profile/$username/avatar.png</code>). If we craft a malicious LFI username (e.g. <code>../../../etc/passwd</code>), then it may be possible to change the file being pulled to another local file on the server and grab it instead of our avatar.</p>
<p>In this case, we would be poisoning a database entry with a malicious LFI payload in our username. Then, another web application functionality would utilize this poisoned entry to perform our attack (i.e. download our avatar based on username value). This is why this attack is called a <code>Second-Order</code> attack.</p>
<p>Developers often overlook these vulnerabilities, as they may protect against direct user input (e.g. from a <code>?page</code> parameter), but they may trust values pulled from their database, like our username in this case. If we managed to poison our username during our registration, then the attack would be possible.</p>
<p>Exploiting LFI vulnerabilities using second-order attacks is similar to what we have discussed in this section. The only variance is that we need to spot a function that pulls a file based on a value we indirectly control and then try to control that value to exploit the vulnerability.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> All techniques mentioned in this section should work with any LFI vulnerability, regardless of the back-end development language or framework.</p>
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
<label class="module-question" for="89"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> Using the file inclusion find the name of a user on the system that starts with "b".
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer89" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-89">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="89" id="btnAnswer89">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint89" data-toggle="modal" id="hintBtn89"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="168"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Submit the contents of the flag.txt file located in the /usr/share/flags directory.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer168" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-168">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="168" id="btnAnswer168">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint168" data-toggle="modal" id="hintBtn168"><i class="fad fa-life-ring mr-2"></i> Hint
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
