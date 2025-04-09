
<h1>PHP Filters</h1>
<p>Many popular web applications are developed in PHP, along with various custom web applications built with different PHP frameworks, like Laravel or Symfony. If we identify an LFI vulnerability in PHP web applications, then we can utilize different <a href="https://www.php.net/manual/en/wrappers.php.php">PHP Wrappers</a> to be able to extend our LFI exploitation, and even potentially reach remote code execution.</p>
<p>PHP Wrappers allow us to access different I/O streams at the application level, like standard input/output, file descriptors, and memory streams. This has a lot of uses for PHP developers. Still, as web penetration testers, we can utilize these wrappers to extend our exploitation attacks and be able to read PHP source code files or even execute system commands. This is not only beneficial with LFI attacks, but also with other web attacks like XXE, as covered in the <a href="/module/details/134">Web Attacks</a> module.</p>
<p>In this section, we will see how basic PHP filters are used to read PHP source code, and in the next section, we will see how different PHP wrappers can help us in gaining remote code execution through LFI vulnerabilities.</p>
<hr/>
<h2>Input Filters</h2>
<p><a href="https://www.php.net/manual/en/filters.php">PHP Filters</a> are a type of PHP wrappers, where we can pass different types of input and have it filtered by the filter we specify. To use PHP wrapper streams, we can use the <code>php://</code> scheme in our string, and we can access the PHP filter wrapper with <code>php://filter/</code>.</p>
<p>The <code>filter</code> wrapper has several parameters, but the main ones we require for our attack are <code>resource</code> and <code>read</code>. The <code>resource</code> parameter is required for filter wrappers, and with it we can specify the stream we would like to apply the filter on (e.g. a local file), while the <code>read</code> parameter can apply different filters on the input resource, so we can use it to specify which filter we want to apply on our resource.</p>
<p>There are four different types of filters available for use, which are <a href="https://www.php.net/manual/en/filters.string.php">String Filters</a>, <a href="https://www.php.net/manual/en/filters.convert.php">Conversion Filters</a>, <a href="https://www.php.net/manual/en/filters.compression.php">Compression Filters</a>, and <a href="https://www.php.net/manual/en/filters.encryption.php">Encryption Filters</a>. You can read more about each filter on their respective link, but the filter that is useful for LFI attacks is the <code>convert.base64-encode</code> filter, under <code>Conversion Filters</code>.</p>
<hr/>
<h2>Fuzzing for PHP Files</h2>
<p>The first step would be to fuzz for different available PHP pages with a tool like <code>ffuf</code> or <code>gobuster</code>, as covered in the <a href="/module/details/54">Attacking Web Applications with Ffuf</a> module:</p>
<pre><code class="language-shell-session">[!bash!]$ ffuf -w /opt/useful/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/FUZZ.php

...SNIP...

index                   [Status: 200, Size: 2652, Words: 690, Lines: 64]
config                  [Status: 302, Size: 0, Words: 1, Lines: 1]
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Tip:</b> Unlike normal web application usage, we are not restricted to pages with HTTP response code 200, as we have local file inclusion access, so we should be scanning for all codes, including `301`, `302` and `403` pages, and we should be able to read their source code as well.</p>
</div>
</div>
<p>Even after reading the sources of any identified files, we can <code>scan them for other referenced PHP files</code>, and then read those as well, until we are able to capture most of the web application's source or have an accurate image of what it does. It is also possible to start by reading <code>index.php</code> and scanning it for more references and so on, but fuzzing for PHP files may reveal some files that may not otherwise be found that way.</p>
<hr/>
<h2>Standard PHP Inclusion</h2>
<p>In previous sections, if you tried to include any php files through LFI, you would have noticed that the included PHP file gets executed, and eventually gets rendered as a normal HTML page. For example, let's try to include the <code>config.php</code> page (<code>.php</code> extension appended by web application):
<img alt="Shipping containers and cranes at a port." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=config" src="/storage/modules/23/lfi_config_failed.png"/></p>
<p>As we can see, we get an empty result in place of our LFI string, since the <code>config.php</code> most likely only sets up the web app configuration and does not render any HTML output.</p>
<p>This may be useful in certain cases, like accessing local PHP pages we do not have access over (i.e. SSRF), but in most cases, we would be more interested in reading the PHP source code through LFI, as source codes tend to reveal important information about the web application. This is where the <code>base64</code> php filter gets useful, as we can use it to base64 encode the php file, and then we would get the encoded source code instead of having it being executed and rendered. This is especially useful for cases where we are dealing with LFI with appended PHP extensions, because we may be restricted to including PHP files only, as discussed in the previous section.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> The same applies to web application languages other than PHP, as long as the vulnerable function can execute files. Otherwise, we would directly get the source code, and would not need to use extra filters/functions to read the source code. Refer to the functions table in section 1 to see which functions have which privileges.</p>
</div>
</div>
<hr/>
<h2>Source Code Disclosure</h2>
<p>Once we have a list of potential PHP files we want to read, we can start disclosing their sources with the <code>base64</code> PHP filter. Let's try to read the source code of <code>config.php</code> using the base64 filter, by specifying <code>convert.base64-encode</code> for the <code>read</code> parameter and <code>config</code> for the <code>resource</code> parameter, as follows:</p>
<pre><code class="language-url">php://filter/read=convert.base64-encode/resource=config
</code></pre>
<img alt="Shipping containers and cranes at a port with encoded text displayed." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=php://filter/read=convert.base64-encode/resource=config" src="/storage/modules/23/lfi_config_wrapper.png"/>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> We intentionally left the resource file at the end of our string, as the <code>.php</code> extension is automatically appended to the end of our input string, which would make the resource we specified be <code>config.php</code>.</p>
</div>
</div>
<p>As we can see, unlike our attempt with regular LFI, using the base64 filter returned an encoded string instead of the empty result we saw earlier. We can now decode this string to get the content of the source code of <code>config.php</code>, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ echo 'PD9waHAK...SNIP...KICB9Ciov' | base64 -d

...SNIP...

if ($_SERVER['REQUEST_METHOD'] == 'GET' &amp;&amp; realpath(__FILE__) == realpath($_SERVER['SCRIPT_FILENAME'])) {
  header('HTTP/1.0 403 Forbidden', TRUE, 403);
  die(header('location: /index.php'));
}

...SNIP...
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Tip:</b> When copying the base64 encoded string, be sure to copy the entire string or it will not fully decode. You can view the page source to ensure you copy the entire string.</p>
</div>
</div>
<p>We can now investigate this file for sensitive information like credentials or database keys and start identifying further references and then disclose their sources.</p>
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
<label class="module-question" for="1071"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Fuzz the web application for other php scripts, and then read one of the configuration files and submit the database password as the answer
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer1071" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-1071">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="1071" id="btnAnswer1071">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint1071" data-toggle="modal" id="hintBtn1071"><i class="fad fa-life-ring mr-2"></i> Hint
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
