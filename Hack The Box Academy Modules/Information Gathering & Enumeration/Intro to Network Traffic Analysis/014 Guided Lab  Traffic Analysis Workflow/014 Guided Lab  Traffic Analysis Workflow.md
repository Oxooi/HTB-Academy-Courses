
<h1>Guided Lab: Traffic Analysis Workflow</h1>
<hr/>
<p>One of our fellow admins noticed a weird connection from Bob's host <code>IP = 172.16.10.90</code> when analyzing the baseline captures we have been gathering. He asked us to check it out and see what we think is happening.</p>
<p>Attempt to utilize the concepts from the Analysis Process sections to complete an analysis of the guided-analysis.zip provided in the optional resources and live traffic from the academy network. Once done, a guided answer key is included with the PCAP in the zip to check your work.</p>
<hr/>
<h2>Tasks:</h2>
<h4>Task #1</h4>
<p><code>Connect to the live host for capture.</code></p>
<p><code>Connection Instructions</code>:
Access to the lab environment to complete the following tasks will require the use of <a href="https://manpages.ubuntu.com/manpages/trusty/man1/xfreerdp.1.html">XfreeRDP</a> to provide GUI access to the virtual machine so we can utilize Wireshark from within the environment.</p>
<p>We will be connecting to the Academy lab like normal utilizing your own VM with a HTB Academy VPN key or the Pwnbox built into the module section. You can start the FreeRDP client on the Pwnbox by typing the following into your shell once the target spawns:</p>
<pre><code class="language-bash">xfreerdp /v:&lt;target IP&gt; /u:htb-student /p:HTB_@cademy_stdnt!
</code></pre>
<p>You can find the <code>target IP</code>, <code>Username</code>, and <code>Password</code> needed below:</p>
<ul>
<li>Click below in the Questions section to spawn the target host and obtain an IP address.
<ul>
<li>
<code>IP</code> == <span class="targetIp"></span>
</li>
<li>
<code>Username</code> ==  htb-student</li>
<li>
<code>Password</code> == HTB_@cademy_stdnt!</li>
</ul>
</li>
</ul>
<p>Once connected, open Wireshark and begin capturing on interface ENS224.</p>
<hr/>
<h3>Analysis</h3>
<p>Follow this workflow template and examine the suspicious traffic. The goal is to determine what is happening with the host in question.</p>
<ol>
<li>what is the issue?
<ol>
<li>a brief summary of the issue.</li>
</ol>
</li>
<li>define our scope and the goal (what are we looking for? which time period?)
<ol>
<li>Scope: what are we looking for, where?</li>
<li>when the issue started:</li>
<li>supporting info: Files, data sources, anything helpful.</li>
</ol>
</li>
<li>define our target(s) (net / host(s) / protocol)
<ol>
<li>Target hosts: Network or address of hosts.</li>
</ol>
</li>
<li>capture network traffic / read from previously captured PCAP.
<ol>
<li>Perform actions as needed to analyze the traffic for signs of intrusion.</li>
</ol>
</li>
<li>identification of required network traffic components (filtering)
<ol>
<li>once we have our traffic, filter out any traffic not necessary for this investigation to include; any traffic that matches our common baseline, and keep anything relevant to the scope of the investigation.</li>
</ol>
</li>
<li>An understanding of captured network traffic
<ol>
<li>Once we have filtered out the noise, it's time to dig for our targets. Start broad and close the circle around our scope.</li>
</ol>
</li>
<li>note taking / mind mapping of the found results.
<ol>
<li>Annotating everything we do, see, or find throughout the investigation is crucial. Ensure you are taking ample notes, including:</li>
</ol>
<ul>
<li>Timeframes we captured traffic during.</li>
<li>Suspicious hosts/ports within the network.</li>
<li>Conversations containing anything suspicious. ( to include timestamps, and packet numbers, files, etc.)</li>
</ul>
</li>
<li>summary of the analysis (what did we find?)
<ol>
<li>Finally, summarize what has been found, explaining the relevant details so that superiors can decide to quarantine the affected hosts or perform a more critical incident response mission.</li>
<li>Our analysis will affect decisions made, so it is essential to be as clear and concise as possible.</li>
</ol>
</li>
</ol>
<p><code>Complete an attempt on your own first to examine and follow the workflow, then look below for a guided walkthrough of the lab.</code></p>
<details>
<summary><b>Click to show walkthrough</b></summary>
<p>This task was best completed using the PCAP file provided for the lesson.
Following the steps in the workflow, we filled in the information and performed our analysis.</p>
<ol>
<li>what is the issue?
<ol>
<li>Suspicious traffic coming from within the network.</li>
</ol>
</li>
<li>define our scope and the goal (what are we looking for? which time period?)
<ol>
<li>target: traffic is originating from 10.129.43.4</li>
<li>when: within the last 48 hours. Capture traffic to determine if it is still happening.</li>
<li>supporting info: file: NTA-guided.pcap</li>
</ol>
</li>
<li>define our target(s) (net / host(s) / protocol)
<ol>
<li>scope: 10.129.43.4 and anyone with a connection to it. Unknown protocol over port 4444.</li>
</ol>
</li>
<li>capture network traffic
<ol>
<li>plug into a link with access to the 10.129.43.0/24 network to capture live traffic attempting to see if anything is happening.</li>
<li>We have been given a PCAP with historical data that contains some of the suspect traffic. We will examine this to analyze the issue.</li>
</ol>
</li>
<li>identification of required network traffic components (filtering)
<ol>
<li>First, we will filter out anything that does not have a connection to 10.129.43.4, since this is our primary suspicious target for the moment.</li>
</ol>
</li>
</ol>
<h4>Conversations</h4>
<p><img alt="Wireshark capture showing ARP and TCP packets between IPs 10.129.43.4 and 10.129.43.29, with conversation statistics below." src="https://academy.hackthebox.com/storage/modules/81/guided-conversations.png"/></p>
<p>After checking out the conversations plugin pictured above, we can see there are only three conversations captured in this pcap file, and they all pertain to our suspicious host. Next, we will look at the <code>protocol hierarchy</code> plugin to see what our traffic is.</p>
<h4>Protocol Statistics</h4>
<p><img alt="Wireshark Protocol Hierarchy Statistics showing percentages and bytes for various protocols, including TCP and UDP." src="https://academy.hackthebox.com/storage/modules/81/guided-proto.png"/></p>
<p>We can see here that this PCAP is mostly TCP traffic, with a bit of UDP traffic. Since there is less UDP than TCP traffic, let us look into that first.</p>
<ol start="2">
<li>Once we have filtered out the noise, it's time to dig for anything unusual. We are going to filter out everything but `UDP traffic first.</li>
</ol>
<h4>UDP</h4>
<p><img alt="Wireshark capture showing ARP and NAT-PMP packets between VMware and IPs 10.129.43.4 and 10.129.0.1, including M-SEARCH and TCP requests." src="https://academy.hackthebox.com/storage/modules/81/guided-udp.png"/></p>
<p>When filtering on just UDP traffic, we only see nine packets. Four arp packets, four Network Address Translation <code>NAT</code>, and one Simple Sevice Discovery Protocol <code>SSDP</code> packet. We can determine based on their packet types and information they contain that this traffic is normal network traffic and nothing to be concerned about.</p>
<ol start="3">
<li>Now, let's move on to looking at <code>TCP</code> traffic. We should have quite a bit more here to sift through. We are going to utilize the display filter <code>!udp &amp;&amp; !arp</code>. This filter will clear out anything we have already analyzed.</li>
</ol>
<h4>TCP</h4>
<p><img alt="Wireshark capture showing TCP packets between IPs 10.129.43.4 and 10.129.43.29, filtered by UDP and ARP protocols." src="https://academy.hackthebox.com/storage/modules/81/guided-tcp.png"/></p>
<ol start="4">
<li>Now that we have cleared our view a bit, we can see the remaining packets are all TCP, and all appear to be the same conversation between hosts <code>10.129.43.4</code> and <code>10.129.43.29</code>. We can determine this since we can see the session establishment via a three-way handshake at packet 3, and the same ports are used through the rest of the packets in the output below.</li>
</ol>
<h4>TCP Session Establishment</h4>
<p><img alt="Wireshark capture showing TCP packets between IPs 10.129.43.4 and 10.129.43.29, with sequence and acknowledgment details." src="https://academy.hackthebox.com/storage/modules/81/guided-handshake.png"/></p>
<ol start="5">
<li>What does appear interesting is that we do not see a TCP session teardown in this PCAP file. This could mean the session was still active and not terminated. We believe this to be true since we do not see any Reset packets either.</li>
<li>We can also examine the conversation by following the <code>TCP stream</code> from packet 3 to determine what it encompasses.</li>
</ol>
<h4>Follow TCP Stream</h4>
<p><img alt="Command prompt showing Windows version, IP configuration, directory listing, and user creation commands." src="https://academy.hackthebox.com/storage/modules/81/guided-stream.png"/></p>
<p>Now that we followed the TCP stream, we should have alarm bells ringing for us. We can see this entire conversation between the two hosts in plain text, and it appears that someone was performing several different actions on the host.</p>
<ol start="7">
<li>Looking at the image above, it appears that someone is performing basic recon of the host. They are issuing commands like <code>whoami</code>, <code>ipconfig</code>, <code>dir</code>. It would appear they are trying to get a lay of the land and figure out what user they landed as on the host. <code>highlighted in orange in the image above.</code>
</li>
<li>What is truly alarming is that we can now see someone made the account <code>hacker</code> and assigned it to the <code>administrators group</code> on this host. Either this is a joke by a poor administrator. Or someone has infiltrated the corporate infrastructure.</li>
<li>note taking / mind mapping of the found results.
<ol>
<li>Annotating everything we do, see, or find throughout the investigation is crucial. If needed, make a picture to depict the flow of actions.</li>
<li>Using this example workflow, we have already documented our actions and have included screenshots of everything we included for analysis. These will help influence the decision made for a response.</li>
</ol>
</li>
<li>summary of the analysis (what did we find?)
<ol>
<li>Based on our analysis, we determined that a malicious actor has infiltrated at least one host on the network. Host 10.129.43.29 shows signs of someone executing commands to include user creation and assigning local administrator permissions via the <code>net</code> commands. It would look like the actor was using Bob's host to perform said actions. Since Bob was previously under investigation for the exfil of corporate secrets and disguising it as web traffic, I think it is safe to say the issue has spread further. The screenshots included with this document show the flow of traffic and commands utilized.</li>
<li>It is our opinion that a complete Incident Response <code>IR</code> procedure be enacted to ensure the threat is stopped from spreading further. We can dedicate resources to clearing the malicious presence and cleaning the affected hosts.</li>
</ol>
</li>
</ol>
</details>
<hr/>
<h2>Summary</h2>
<p>After analyzing the actions taken, the IR team determined that The actor got lazy and decided to utilize a Netcat shell and directly interact with Bob's host while gathering more information. While doing so, he used RDP from Bob's host to another windows desktop in the environment to try and establish another foothold. Luckily, the IR team was able to capture some PCAP of the RDP traffic. Bob's host was quarantined, and incident response was initiated to determine what was taken and what other potential hosts were compromised. Great job spotting the intrusion.</p>
<div class="my-3 p-3 vpn-switch-card" id="vpn-switch">
<p class="font-size-14 color-white mb-0">VPN Servers</p>
<p class="font-size-13 mb-0">
<i class="fas fa-exclamation-triangle text-warning"></i><span class="color-white ml-1">Warning:</span> Each
                    time you "Switch",
                    your connection keys are regenerated and you must re-download your VPN connection file.
                </p>
<p class="font-size-13 mb-0">
                    All VM instances associated with the old VPN Server will be terminated when switching to
                    a new VPN server. <br/>
                    Existing PwnBox instances will automatically switch to the new VPN server.</p>
<div class="row mb-3">
<div class="col-12 mt-2">
<div class="d-none justify-content-center vpn-loader">
<div class="spinner-border text-success" role="status">
<span class="sr-only">Switching VPN...</span>
</div>
</div>
<select aria-label="vpn server" class="selectpicker custom-form-control vpnSelector badge-select" title="Select VPN Server">
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 6 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt; &lt;span class='recommended'&gt; &lt;img src='/images/sparkles-solid.svg'/&gt;Recommended&lt;/span&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="30" value="17">US Academy 6</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 5 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="31" value="16">US Academy 5</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 1 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="33" value="4">US Academy 1</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 2 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="33" value="5">US Academy 2</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 4 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="33" value="13">US Academy 4</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 5 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt; &lt;span class='recommended'&gt; &lt;img src='/images/sparkles-solid.svg'/&gt;Recommended&lt;/span&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="37" value="12">EU Academy 5</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 2 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="38" selected="" value="2">EU Academy 2</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 3 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="38" value="9">US Academy 3</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 1 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="40" value="1">EU Academy 1</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 3 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="41" value="14">EU Academy 3</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 4 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="44" value="11">EU Academy 4</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 6 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="48" value="15">EU Academy 6</option>
</select>
<p class="font-size-14 color-white mb-0 mt-2">PROTOCOL</p>
<div class="d-flex">
<div class="custom-control custom-radio custom-control-inline">
<input checked="" class="custom-control-input" id="rd_1" name="vpn-protocol" type="radio" value="udp"/>
<label class="custom-control-label green font-size-14" for="rd_1">UDP
                                    1337</label>
</div>
<div class="custom-control custom-radio">
<input class="custom-control-input" id="rd_2" name="vpn-protocol" type="radio" value="tcp"/>
<label class="custom-control-label green font-size-14" for="rd_2">TCP
                                    443</label>
</div>
</div>
<div class="d-flex justify-content-center">
<button class="btn btn-outline-success btn-lg download-vpn-settings mt-3 px-5 font-size-12">
                                DOWNLOAD VPN CONNECTION FILE
                            </button>
</div>
</div>
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
                            <button class="extendTargetSystemBtn btn btn-light btn-sm module-button" data-title="Extend Life by 1 hour (up to 6 hours total lifespan)" data-toggle="tooltip">
<i class="fa fa-plus text-success extend-icon"></i>
<div class="extend-loader spinner-border spinner-border-small text-success d-none" role="status">
</div>
</button>
<button class="text-danger btn btn-light btn-sm module-button font-size-16 mb-1" data-target="#terminateVmModal" data-toggle="modal">
                    Terminate <span class="fa-regular fa-x text-danger font-size-13 ml-2"></span>
</button>
</span>
</div>
</p>
</div>
<div class="col-3 text-right float-right">
<button class="btn btn-light bg-color-blue-nav mt-2 w-100 d-flex align-items-center" data-target="#cheatSheetModal" data-toggle="modal">
<div><i class="fad fa-file-alt mr-2"></i></div>
<div class="text-center w-100 ml-1">Cheat Sheet</div>
</button>
<a class="btn btn-light bg-color-blue-nav mt-2 d-flex align-items-center" data-title='Key is already installed in "My Workstation"' data-toggle="tooltip" href="https://academy.hackthebox.com/vpn/key">
<div><i class="fad fa-chart-network mr-2"></i></div>
<div class="text-center w-100">Download VPN Connection File</div>
</a>
</div>
</div>
<div>
<div>
<p class="mb-0 font-size-12"><i class="fad fa-chart-network text-success mr-2 font-size-medium"></i>
                                RDP
                                to <span class="target-protocol-ip target-protocol-ip-621 text-dark"></span> with user "<span class="text-success">htb-student</span>" and
                                password "<span class="text-danger">HTB_@cademy_stdnt!</span>" </p>
<label class="module-question" for="621"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What was the name of the new user created on mrb3n's host?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer621" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-621">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="621" id="btnAnswer621">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint621" data-toggle="modal" id="hintBtn621"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="622"><span class="badge badge-soft-dark font-size-14 mr-2">+ 2 <i class="fad fa-cube text-success"></i></span> How many total packets were there in the Guided-analysis PCAP?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer622" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-622">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="622" id="btnAnswer622">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint622" data-toggle="modal" id="hintBtn622"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="623"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What was the suspicious port that was being used?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer623" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-623">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="623" id="btnAnswer623">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint623" data-toggle="modal" id="hintBtn623"><i class="fad fa-life-ring mr-2"></i> Hint
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
