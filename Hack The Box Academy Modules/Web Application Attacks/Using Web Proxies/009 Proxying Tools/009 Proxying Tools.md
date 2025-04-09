
<h1>Proxying Tools</h1>
<hr/>
<p>An important aspect of using web proxies is enabling the interception of web requests made by command-line tools and thick client applications. This gives us transparency into the web requests made by these applications and allows us to utilize all of the different proxy features we have used with web applications.</p>
<p>To route all web requests made by a specific tool through our web proxy tools, we have to set them up as the tool's proxy  (i.e. <code>http://127.0.0.1:8080</code>), similarly to what we did with our browsers. Each tool may have a different method for setting its proxy, so we may have to investigate how to do so for each one.</p>
<p>This section will cover a few examples of how to use web proxies to intercept web requests made by such tools. You may use either Burp or ZAP, as the setup process is the same.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: Proxying tools usually slows them down, therefore, only proxy tools when you need to investigate their requests, and not for normal usage.</p>
</div>
</div>
<hr/>
<h2>Proxychains</h2>
<p>One very useful tool in Linux is <a href="https://github.com/haad/proxychains">proxychains</a>, which routes all traffic coming from any command-line tool to any proxy we specify. <code>Proxychains</code> adds a proxy to any command-line tool and is hence the simplest and easiest method to route web traffic of command-line tools through our web proxies.</p>
<p>To use <code>proxychains</code>, we first have to edit <code>/etc/proxychains.conf</code>, comment out the final line and add the following line at the end of it:</p>
<pre><code class="language-shell-session">#socks4         127.0.0.1 9050
http 127.0.0.1 8080
</code></pre>
<p>We should also enable <code>Quiet Mode</code> to reduce noise by un-commenting <code>quiet_mode</code>. Once that's done, we can prepend <code>proxychains</code> to any command, and the traffic of that command should be routed through <code>proxychains</code> (i.e., our web proxy). For example, let's try using <code>cURL</code> on one of our previous exercises:</p>
<pre><code class="language-shell-session">[!bash!]$ proxychains curl http://SERVER_IP:PORT

ProxyChains-3.1 (http://proxychains.sf.net)
&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;

&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;Ping IP&lt;/title&gt;
    &lt;link rel="stylesheet" href="./style.css"&gt;
&lt;/head&gt;
...SNIP...
&lt;/html&gt;    
</code></pre>
<p>We see that it worked just as it normally would, with the additional <code>ProxyChains-3.1</code> line at the beginning, to note that it is being routed through <code>ProxyChains</code>. If we go back to our web proxy (Burp in this case), we will see that the request has indeed gone through it:</p>
<p><img alt="Proxychains Curl" src="https://academy.hackthebox.com/storage/modules/110/proxying_proxychains_curl.jpg"/></p>
<hr/>
<h2>Nmap</h2>
<p>Next, let's try to proxy <code>nmap</code> through our web proxy. To find out how to use the proxy configurations for any tool, we can view its manual with <code>man nmap</code>, or its help page with <code>nmap -h</code>:</p>
<pre><code class="language-shell-session">[!bash!]$ nmap -h | grep -i prox

  --proxies &lt;url1,[url2],...&gt;: Relay connections through HTTP/SOCKS4 proxies
</code></pre>
<p>As we can see, we can use the <code>--proxies</code> flag. We should also add the <code>-Pn</code> flag to skip host discovery (as recommended on the man page). Finally, we'll also use the <code>-sC</code> flag to examine what an nmap script scan does:</p>
<pre><code class="language-shell-session">[!bash!]$ nmap --proxies http://127.0.0.1:8080 SERVER_IP -pPORT -Pn -sC

Starting Nmap 7.91 ( https://nmap.org )
Nmap scan report for SERVER_IP
Host is up (0.11s latency).

PORT      STATE SERVICE
PORT/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 0.49 seconds
</code></pre>
<p>Once again, if we go to our web proxy tool, we will see all of the requests made by nmap in the proxy history:</p>
<p><img alt="nmap proxy" src="https://academy.hackthebox.com/storage/modules/110/proxying_nmap.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: Nmap's built-in proxy is still in its experimental phase, as mentioned by its manual (<code>man nmap</code>), so not all functions or traffic may be routed through the proxy. In these cases, we can simply resort to <code>proxychains</code>, as we did earlier.</p>
</div>
</div>
<hr/>
<h2>Metasploit</h2>
<p>Finally, let's try to proxy web traffic made by Metasploit modules to better investigate and debug them. We should begin by starting Metasploit with <code>msfconsole</code>. Then, to set a proxy for any exploit within Metasploit, we can use the <code>set PROXIES</code> flag. Let's try the <code>robots_txt</code> scanner as an example and run it against one of our previous exercises:</p>
<pre><code class="language-shell-session">[!bash!]$ msfconsole

msf6 &gt; use auxiliary/scanner/http/robots_txt
msf6 auxiliary(scanner/http/robots_txt) &gt; set PROXIES HTTP:127.0.0.1:8080

PROXIES =&gt; HTTP:127.0.0.1:8080


msf6 auxiliary(scanner/http/robots_txt) &gt; set RHOST SERVER_IP

RHOST =&gt; SERVER_IP


msf6 auxiliary(scanner/http/robots_txt) &gt; set RPORT PORT

RPORT =&gt; PORT


msf6 auxiliary(scanner/http/robots_txt) &gt; run

[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
</code></pre>
<p>Once again, we can go back to our web proxy tool of choice and examine the proxy history to view all sent requests:</p>
<p><img alt="msf proxy" src="https://academy.hackthebox.com/storage/modules/110/proxying_msf.jpg"/></p>
<p>We see that the request has indeed gone through our web proxy. The same method can be used with other scanners, exploits, and other features in Metasploit.</p>
<p>We can similarly use our web proxies with other tools and applications, including scripts and thick clients. All we have to do is set the proxy of each tool to use our web proxy. This allows us to examine exactly what these tools are sending and receiving and potentially repeat and modify their requests while performing web application penetration testing.</p>
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
<label class="module-question" for="710"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Try running 'auxiliary/scanner/http/http_put' in Metasploit on any website, while routing the traffic through Burp. Once you view the requests sent, what is the last line in the request?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="msf test file"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="710" disabled="true" id="btnAnswer710">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint710" data-toggle="modal" id="hintBtn710"><i class="fad fa-life-ring mr-2"></i> Hint
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
