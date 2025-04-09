
<h1>Running SQLMap on an HTTP Request</h1>
<hr/>
<p>SQLMap has numerous options and switches that can be used to properly set up the (HTTP) request before its usage.</p>
<p>In many cases, simple mistakes such as forgetting to provide proper cookie values, over-complicating setup with a lengthy command line, or improper declaration of formatted POST data, will prevent the correct detection and exploitation of the potential SQLi vulnerability.</p>
<hr/>
<h2>Curl Commands</h2>
<p>One of the best and easiest ways to properly set up an SQLMap request against the specific target (i.e., web request with parameters inside) is by utilizing <code>Copy as cURL</code> feature from within the Network (Monitor) panel inside the Chrome, Edge, or Firefox Developer Tools:
<img alt="Network panel showing a GET request to www.example.com with a 404 status, and a context menu with options like 'Copy as cURL'." src="https://academy.hackthebox.com/storage/modules/58/M5UVR6n.png"/></p>
<p>By pasting the clipboard content (<code>Ctrl-V</code>) into the command line, and changing the original command <code>curl</code> to <code>sqlmap</code>, we are able to use SQLMap with the identical <code>curl</code> command:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap 'http://www.example.com/?id=1' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0' -H 'Accept: image/webp,*/*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'DNT: 1'
</code></pre>
<p>When providing data for testing to SQLMap, there has to be either a parameter value that could be assessed for SQLi vulnerability or specialized options/switches for automatic parameter finding (e.g. <code>--crawl</code>, <code>--forms</code> or <code>-g</code>).</p>
<hr/>
<h2>GET/POST Requests</h2>
<p>In the most common scenario, <code>GET</code> parameters are provided with the usage of option <code>-u</code>/<code>--url</code>, as in the previous example. As for testing <code>POST</code> data, the <code>--data</code> flag can be used, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap 'http://www.example.com/' --data 'uid=1&amp;name=test'
</code></pre>
<p>In such cases, <code>POST</code> parameters <code>uid</code> and <code>name</code> will be tested for SQLi vulnerability. For example, if we have a clear indication that the parameter <code>uid</code> is prone to an SQLi vulnerability, we could narrow down the tests to only this parameter using <code>-p uid</code>. Otherwise, we could mark it inside the provided data with the usage of special marker <code>*</code> as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap 'http://www.example.com/' --data 'uid=1*&amp;name=test'
</code></pre>
<hr/>
<h2>Full HTTP Requests</h2>
<p>If we need to specify a complex HTTP request with lots of different header values and an elongated POST body, we can use the <code>-r</code> flag. With this option, SQLMap is provided with the "request file," containing the whole HTTP request inside a single textual file. In a common scenario, such HTTP request can be captured from within a specialized proxy application (e.g. <code>Burp</code>) and written into the request file, as follows:</p>
<p><img alt="HTTP GET request to www.example.com with headers including User-Agent and Accept-Language." src="https://academy.hackthebox.com/storage/modules/58/x7ND6VQ.png"/></p>
<p>An example of an HTTP request captured with <code>Burp</code> would look like:</p>
<pre><code class="language-http">GET /?id=1 HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
DNT: 1
If-Modified-Since: Thu, 17 Oct 2019 07:18:26 GMT
If-None-Match: "3147526947"
Cache-Control: max-age=0
</code></pre>
<p>We can either manually copy the HTTP request from within <code>Burp</code> and write it to a file, or we can right-click the request within <code>Burp</code> and choose <code>Copy to file</code>. Another way of capturing the full HTTP request would be through using the browser, as mentioned earlier in the section, and choosing the option <code>Copy</code> &gt; <code>Copy Request Headers</code>, and then pasting the request into a file.</p>
<p>To run SQLMap with an HTTP request file, we use the <code>-r</code> flag, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -r req.txt
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.4.9}
|_ -| . [(]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[*] starting @ 14:32:59 /2020-09-11/

[14:32:59] [INFO] parsing HTTP request from 'req.txt'
[14:32:59] [INFO] testing connection to the target URL
[14:32:59] [INFO] testing if the target URL content is stable
[14:33:00] [INFO] target URL content is stable
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: similarly to the case with the '--data' option, within the saved request file, we can specify the parameter we want to inject in with an asterisk (*), such as '/?id=*'.</p>
</div>
</div>
<hr/>
<h2>Custom SQLMap Requests</h2>
<p>If we wanted to craft complicated requests manually, there are numerous switches and options to fine-tune SQLMap.</p>
<p>For example, if there is a requirement to specify the (session) cookie value to <code>PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c</code> option <code>--cookie</code> would be used as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap ... --cookie='PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c'
</code></pre>
<p>The same effect can be done with the usage of option <code>-H/--header</code>:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap ... -H='Cookie:PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c'
</code></pre>
<p>We can apply the same to options like <code>--host</code>, <code>--referer</code>, and <code>-A/--user-agent</code>, which are used to specify the same HTTP headers' values.</p>
<p>Furthermore, there is a switch <code>--random-agent</code> designed to randomly select a <code>User-agent</code> header value from the included database of regular browser values. This is an important switch to remember, as more and more protection solutions automatically drop all HTTP traffic containing the recognizable default SQLMap's User-agent value (e.g. <code>User-agent: sqlmap/1.4.9.12#dev (http://sqlmap.org)</code>). Alternatively, the <code>--mobile</code> switch can be used to imitate the smartphone by using that same header value.</p>
<p>While SQLMap, by default, targets only the HTTP parameters, it is possible to test the headers for the SQLi vulnerability. The easiest way is to specify the "custom" injection mark after the header's value (e.g. <code>--cookie="id=1*"</code>). The same principle applies to any other part of the request.</p>
<p>Also, if we wanted to specify an alternative HTTP method, other than <code>GET</code> and <code>POST</code> (e.g., <code>PUT</code>), we can utilize the option <code>--method</code>, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u www.target.com --data='id=1' --method PUT
</code></pre>
<hr/>
<h2>Custom HTTP Requests</h2>
<p>Apart from the most common form-data <code>POST</code> body style (e.g. <code>id=1</code>), SQLMap also supports JSON formatted (e.g. <code>{"id":1}</code>) and XML formatted (e.g. <code>&lt;element&gt;&lt;id&gt;1&lt;/id&gt;&lt;/element&gt;</code>) HTTP requests.</p>
<p>Support for these formats is implemented in a "relaxed" manner; thus, there are no strict constraints on how the parameter values are stored inside. In case the <code>POST</code> body is relatively simple and short, the option <code>--data</code> will suffice.</p>
<p>However, in the case of a complex or long POST body, we can once again use the <code>-r</code> option:</p>
<pre><code class="language-shell-session">[!bash!]$ cat req.txt
HTTP / HTTP/1.0
Host: www.example.com

{
  "data": [{
    "type": "articles",
    "id": "1",
    "attributes": {
      "title": "Example JSON",
      "body": "Just an example",
      "created": "2020-05-22T14:56:29.000Z",
      "updated": "2020-05-22T14:56:28.000Z"
    },
    "relationships": {
      "author": {
        "data": {"id": "42", "type": "user"}
      }
    }
  }]
}
</code></pre>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -r req.txt
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.4.9}
|_ -| . [)]     | .'| . |
|___|_  [']_|_|_|__,|  _|
      |_|V...       |_|   http://sqlmap.org


[*] starting @ 00:03:44 /2020-09-15/

[00:03:44] [INFO] parsing HTTP request from 'req.txt'
JSON data found in HTTP body. Do you want to process it? [Y/n/q] 
[00:03:45] [INFO] testing connection to the target URL
[00:03:45] [INFO] testing if the target URL content is stable
[00:03:46] [INFO] testing if HTTP parameter 'JSON type' is dynamic
[00:03:46] [WARNING] HTTP parameter 'JSON type' does not appear to be dynamic
[00:03:46] [WARNING] heuristic (basic) test shows that HTTP parameter 'JSON type' might not be injectable
</code></pre>
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
<label class="module-question" for="291"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What's the contents of table flag2? (Case #2)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{700_much_c0n6r475_0n_p057_r3qu357}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="291" disabled="true" id="btnAnswer291">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint291" data-toggle="modal" id="hintBtn291"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="292"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What's the contents of table flag3? (Case #3)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{c00k13_m0n573r_15_7h1nk1n6_0f_6r475}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="292" disabled="true" id="btnAnswer292">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint292" data-toggle="modal" id="hintBtn292"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="293"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What's the contents of table flag4? (Case #4)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{j450n_v00rh335_53nd5_6r475}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="293" disabled="true" id="btnAnswer293">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint293" data-toggle="modal" id="hintBtn293"><i class="fad fa-life-ring mr-2"></i> Hint
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
