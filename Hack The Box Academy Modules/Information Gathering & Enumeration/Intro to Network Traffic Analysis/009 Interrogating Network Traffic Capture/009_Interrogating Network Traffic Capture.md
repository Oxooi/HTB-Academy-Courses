
<h1>Interrogating Network Traffic With Capture and Display Filters</h1>
<hr/>
<p>This lab aims to provide some exposure to interrogating network traffic and give everyone some valuable practice implementing packet filters. We will be utilizing filters like <code>host</code>, <code>port</code>, <code>protocol</code>, and more to change our view while digging through a .PCAP file.</p>
<p>Now that we have proven capable of capturing network traffic for the Corporation, management has tasked us with performing a quick analysis of the traffic our team has captured while surveying the network. The goal is to determine what servers are answering DNS and HTTP/S requests in our local network.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">If you wish to take a more exploratory approach to this lab, I have posted the overall tasks to accomplish. For a more detailed walkthrough of how to complete each step, look below each task in the solution bubble.</p>
</div></div>
<hr/>
<h2>Tasks</h2>
<p>Utilizing <code>TCPDump-lab-2.zip</code> in the optional resources, perform the lab to the best of your ability. Finding everything on the first shot is not the goal. Our understanding of the concepts is our primary concern. As we perform these actions repeatedly, it will get easier.</p>
<h4>Task #1</h4>
<p><code>Read a capture from a file without filters implemented.</code></p>
<p>To start, let's examine this pcap with no filters applied.</p>
<details>
<summary><b>Click to show answer</b></summary>
<pre><code class="language-shell-session">[!bash!]$ tcpdump -r (file.pcap)
</code></pre>
</details>
<hr/>
<h4>Task #2</h4>
<p><code>Identify the type of traffic seen.</code></p>
<p>Take note of what types of traffic can be seen. (Ports utilized, protocols, any other information you deem relevant.) What filters can we use to make this task easier?</p>
<p>What type of traffic do we see?</p>
<p>Common protocols:</p>
<p>Ports utilized:</p>
<details>
<summary><b>Click to show answers</b></summary>
<p>What type of traffic do we see?</p>
<p>Common protocols: We should notice a bunch of <code>DNS, HTTP, and HTTPS</code> traffic.</p>
<p>Ports utilized: <code>53 80 443</code></p>
</details>
<hr/>
<h4>Task #3</h4>
<p><code>Identify conversations.</code></p>
<p>We have examined the basics of this traffic, now determine if you notice any patterns with the traffic.<br/>
Are you noticing any common connections between a server and host? If so, who?</p>
<p>What are the client and server port numbers used in the first full TCP three-way handshake?</p>
<p>Who are the servers in these conversations? How do we know?</p>
<p>Who are the receiving hosts?</p>
<details>
<summary><b>Click to show answer</b></summary>
<p>To help make this more straightforward, turning absolute sequence numbers on <code>(-S)</code> will be extremely helpful in determining conversations.</p>
<p>We can also examine the different hosts involved. Servers typically communicate over the well-known port number assigned to the protocol <code>(80 for HTTP, 443 for HTTPS, for example)</code>. Hosts or recipients in the conversations will typically utilize a random high port number.</p>
</details>
<hr/>
<h4>Task #4</h4>
<p><code>Interpret the capture in depth.</code></p>
<p>Now that we have some familiarity with the pcap file, let's do some analysis. Utilize whatever syntax necessary to accomplish answering the questions below.</p>
<p>What is the timestamp of the first established conversation in the pcap file?</p>
<p>What is the IP address/s of apache.org from the DNS server responses?</p>
<p>What protocol is being utilized in that first conversation? (name/#)</p>
<details>
<summary><b>Click to show answer</b></summary>
<p>To determine the correct timestamp: Read the file with (-r) and then examine the conversations. Find the first one established ( Full TCP Handshake "Syn / SYN-ACK / ACK") and look at the first field in the output to find the timestamp.
To find the IP of Host ( ), we can filter the traffic only to see conversations Sourcing from it ( src 'name-of-host' ) and then disable Name resolution with (-n).
To determine the protocol being utilized in the first conversation, look for the well-known port # while disabling hostname and port name resolution (-nn) or leave off the (-nn), and it will tell you the name of the protocol in the output.</p>
</details>
<hr/>
<h4>Task #5</h4>
<p><code>Filter out traffic.</code></p>
<p>It's time to clear some of this data out now. Reload the pcap file and filter out all traffic that is not DNS. What can you see?</p>
<p>Who is the DNS server for this segment?</p>
<p>What domain name/s were requested in the pcap file?</p>
<p>What type of DNS Records could be seen?</p>
<details>
<summary><b>Click to show answer</b></summary>
To clear out everything that is not DNS, we can utilize:
<pre><code class="language-shell-session">[!bash!]$ sudo tcpdump -r (file.pcap) udp and port 53    
</code></pre>
<p>Keep in mind that DNS is a protocol that utilizes both UDP and TCP for different functions. This means we may have to filter for both to ensure we don't miss anything.</p>
<p>If the -X switch is utilized, we can get a Hex and ASCII output to look at cleartext names in the output.</p>
<p>Understanding the DNS protocol requests and responses will help determine what type of records are being requested. The protocol-specific information field will often hold our answer.</p>
</details>
<p>Now that we are only seeing DNS traffic and have a better grasp on how the packet appears, try to answer the following questions regarding name resolution in the enterprise:
Who requests an A record for apache.org? (hostname or IP)</p>
<p>What information does an A record provide?</p>
<p>Who is the responding DNS server in the pcap? (hostname or IP)</p>
<hr/>
<h4>Task #6</h4>
<p><code>Filter for TCP traffic.</code></p>
<p>Now that we have a clear idea of our DNS server let's look for any webservers present. Filter out the view so that we only see the traffic pertaining to HTTP or HTTPS.
What web pages were requested?</p>
<p>What are the most common HTTP request methods from this PCAP?</p>
<p>What is the most common HTTP response from this PCAP?</p>
<details>
<summary><b>Click to show answer</b></summary>
Filtering on port 80 OR 443 is a great start. You can also filter on the protocol name HTTP OR HTTPS. 
Keep in mind that ports are more like guidelines. I can host a webserver on any open port that can be bound. (8080 or 8001, for example)
</details>
<h4>Task #7</h4>
<p><code>What can you determine about the server in the first conversation.</code></p>
<p>Let's take a closer look. What can be determined about the webserver in the first conversation? Does anything stick out?
For some clarity, make sure our view includes the Hex and ASCII output for the pcap.</p>
<p>Can we determine what application is running the webserver?</p>
<details>
<summary><b>Click to show answer</b></summary>
Often the webserver will include pertinent information in the post responses such as OS or web server name. You may also be able to determine what service is running the webserver based on these responses. This task is a bit difficult to perform utilizing tcpdump. It requires us to look at the ASCII of the HTTP responses. In future sections, when we move into Wireshark, this will be much easier to do.
</details>
<hr/>
<h2>Summary</h2>
<p>Through this lab, we expanded our horizons while utilizing TCPDump to analyze PCAP traffic. We learned how to capture and display filters effectively, dissected traffic to determine what protocols were running in the environment, and even gleaned some critical information about our enterprise segments, DNS, and Webservers. Continue to play on your own and see how deep the rabbit hole goes. Can you capture traffic in your home network and answer the same questions?</p>
<hr/>
<h2>Tips For Analysis</h2>
<p>Below is a list of questions we can ask ourselves during the analysis process to keep on track.</p>
<table>
<thead>
<tr>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>what type of traffic do you see? (protocol, port, etc.)</td>
</tr>
<tr>
<td>Is there more than one conversation? (how many?)</td>
</tr>
<tr>
<td>How many unique hosts?</td>
</tr>
<tr>
<td>What is the timestamp of the first conversation in the pcap (tcp traffic)</td>
</tr>
<tr>
<td>What traffic can I filter out to clean up my view?</td>
</tr>
<tr>
<td>Who are the servers in the PCAP? (answering on well-known ports, 53, 80, etc.)</td>
</tr>
<tr>
<td>What records were requested or methods used? (GET, POST, DNS A records, etc.)</td>
</tr>
</tbody>
</table>
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
<label class="module-question" for="640"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What are the client and server port numbers used in first full TCP three-way handshake? (low number first then high number)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer640" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-640">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="640" id="btnAnswer640">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint640" data-toggle="modal" id="hintBtn640"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="641"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Based on the traffic seen in the pcap file, who is the DNS server in this network segment? (ip address)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer641" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-641">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="641" id="btnAnswer641">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint641" data-toggle="modal" id="hintBtn641"><i class="fad fa-life-ring mr-2"></i> Hint
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
