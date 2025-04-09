
<h1>Wireshark Advanced Usage</h1>
<hr/>
<p>In this section, we will cover some advanced usage with Wireshark. The project developers have included many different capabilities ranging from tracking TCP conversations to cracking wireless credentials. The inclusion of many different plugins makes Wireshark one of the best traffic analysis tools.</p>
<hr/>
<h2>Plugins</h2>
<p>The analyze and statistics radials provide a plethora of plugins to run against the capture. In this section, we will work through a couple of them. We would cover all of which Wireshark offers, but sadly, it is simply not achievable in an introductory module. I urge everyone to experiment and play as we go through this journey.</p>
<h4>The Statistics and Analyze Tabs</h4>
<p>The Statistics and Analyze tabs can provide us with great insight into the data we are examining. From these points, we can utilize many of the baked-in plugins Wireshark has to offer.</p>
<p>The plugins here can give us detailed reports about the network traffic being utilized. It can show us everything from the top talkers in our environment to specific conversations and even breakdown by IP and protocol.</p>
<h4>Statistics Tab</h4>
<p><img alt="Wireshark interface showing address statistics, protocol hierarchy, and conversation details for network traffic analysis, including IP addresses, packet counts, and protocol breakdowns." src="https://academy.hackthebox.com/storage/modules/81/wireshark-statistics.png"/></p>
<h4>Analyze</h4>
<p>From the Analyze tab, we can utilize plugins that allow us to do things such as following TCP streams, filter on conversation types, prepare new packet filters and examine the expert info Wireshark generates about the traffic. Below are a few examples of how to use these plugins.</p>
<h4>Analyze Tab</h4>
<p><img alt="Wireshark Analyze menu showing options for display filters, applying filters, enabled protocols, and expert information." src="https://academy.hackthebox.com/storage/modules/81/analyze.png"/></p>
<h4>Following TCP Streams</h4>
<p>Wireshark can stitch TCP packets back together to recreate the entire stream in a readable format. This ability also allows us to pull data (<code>images, files, etc.</code>) out of the capture. This works for almost any protocol that utilizes TCP as a transport mechanism.</p>
<p>To utilize this feature:</p>
<ul>
<li>right-click on a packet from the stream we wish to recreate.</li>
<li>select follow → TCP</li>
<li>this will open a new window with the stream stitched back together.
From here, we can see the entire conversation.</li>
</ul>
<h4>Follow A Stream Via GUI</h4>
<p><img alt="GIF showcasing the 'Follow a Stream' functionality." src="https://academy.hackthebox.com/storage/modules/81/follow-tcp.gif"/></p>
<p>Alternatively, we can utilize the filter <code>tcp.stream eq #</code> to find and track conversations captured in the pcap file.</p>
<h2>Filter For A Specific TCP Stream</h2>
<p><img alt="Wireshark capture showing TCP and Telnet packets between IPs 10.100.18.5 and 10.100.16.1, with sequence and acknowledgment numbers." src="https://academy.hackthebox.com/storage/modules/81/tcp-stream.gif"/></p>
<p>Notice that the first three packets in the image above have a full TCP handshake. Following those packets, we can see the stream transferring data. We have cleared anything not related out of view by utilizing the filter, and we now can see the conversation in order.</p>
<h4>Extracting Data and Files From a Capture</h4>
<p>Wireshark can recover many different types of data from streams. It requires you to have captured the entire conversation. Otherwise, this ability will fail to put an incomplete datagram back together.
If we want a more in-depth understanding of how this capability works, check out the Networking 101 Module or research TCP/IP fragmentation.</p>
<p>To extract files from a stream:</p>
<ul>
<li>stop your capture.</li>
<li>Select the File radial → Export → , then select the protocol format to extract from.</li>
<li>(DICOM, HTTP, SMB, etc.)</li>
</ul>
<h4>Extract Files From The GUI</h4>
<p><img alt="GIF showcasing the extraction of files from an HTTP stream." src="https://academy.hackthebox.com/storage/modules/81/extract-http.gif"/></p>
<p>Another exciting way to grab data out of the pcap file comes from FTP. The File Transfer Protocol moves data between a server and host to pull it out of the raw bytes and reconstruct the file. (image, text documents, etc.)
FTP utilizes TCP as its transport protocol and uses ports <code>20 &amp; 21</code> to function. TCP port 20 is used to transfer data between the server and host, while port 21 is used as the FTP control port. Any commands such as login, listing files, and issuing download or uploads happen over this port. To do so, we need to look at the different <code>FTP</code> display filters in Wireshark. A complete list of these can be found <a href="https://www.wireshark.org/docs/dfref/f/ftp.html">here</a>.
For now, we will look at three:</p>
<ul>
<li>
<code>ftp</code> - Will display anything about the FTP protocol.
<ul>
<li>We can utilize this to get a feel for what hosts/servers are transferring data over FTP.</li>
</ul>
</li>
</ul>
<h4>FTP Disector</h4>
<p><img alt="Wireshark capture showing FTP requests and responses between IPs 172.16.146.1 and 172.16.146.2, including anonymous login and directory changes." src="https://academy.hackthebox.com/storage/modules/81/ftp-disector.png"/></p>
<ul>
<li>
<code>ftp.request.command</code> - Will show any commands sent across the ftp-control channel ( port 21 )
<ul>
<li>We can look for information like usernames and passwords with this filter. It can also show us filenames for anything requested.</li>
</ul>
</li>
</ul>
<h4>FTP-Request-Command Filter</h4>
<p><img alt="Wireshark capture showing FTP requests between IPs 172.16.146.1 and 172.16.146.2, including anonymous login and directory commands." src="https://academy.hackthebox.com/storage/modules/81/ftp-request-command.png"/></p>
<ul>
<li>
<code>ftp-data</code> - Will show any data transferred over the data channel ( port 20 )
<ul>
<li>If we filter on a conversation and utilize <code>ftp-data</code>, we can capture anything sent during the conversation. We can reconstruct anything transferred by placing the raw data back into a new file and naming it appropriately.</li>
</ul>
</li>
</ul>
<h4>FTP-Data Filter</h4>
<p><img alt="Wireshark capture showing FTP data transfer between IPs 172.16.146.2 and 172.16.146.1, including retrieval of 'secrets.txt' and 'Shield-prototype-plans' files." src="https://academy.hackthebox.com/storage/modules/81/ftp-data.png"/></p>
<p>Since FTP utilizes TCP as its transport mechanism, we can utilize the <code>follow tcp stream</code> function we utilized earlier in the section to group any conversation we wish to explore. The basic steps to dissect FTP data from a pcap are as follows:</p>
<ol>
<li>Identify any FTP traffic using the <code>ftp</code> display filter.</li>
<li>Look at the command controls sent between the server and hosts to determine if anything was transferred and who did so with the <code>ftp.request.command</code> filter.</li>
<li>Choose a file, then filter for <code>ftp-data</code>. Select a packet that corresponds with our file of interest and follow the TCP stream that correlates to it.</li>
<li>Once done, Change "<code>Show and save data as</code>" to "<code>Raw</code>" and save the content as the original file name.</li>
<li>Validate the extraction by checking the file type.</li>
</ol>
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
<label class="module-question" for="604"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> Which plugin tab can provide us with a way to view conversation metadata and even protocol breakdowns for the entire PCAP file?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer604" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-604">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="604" id="btnAnswer604">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint604" data-toggle="modal" id="hintBtn604"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="605"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> What plugin tab will allow me to accomplish tasks such as applying filters, following streams, and viewing expert info?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer605" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-605">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="605" id="btnAnswer605">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint605" data-toggle="modal" id="hintBtn605"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="606"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> What stream oriented Transport protocol enables us to follow and rebuild conversations and the included data?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer606" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-606">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="606" id="btnAnswer606">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint606" data-toggle="modal" id="hintBtn606"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="607"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> True or False: Wireshark can extract files from HTTP traffic.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer607" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-607">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="607" id="btnAnswer607">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint607" data-toggle="modal" id="hintBtn607"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="608"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> True or False: The ftp-data filter will show us any data sent over TCP port 21.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer608" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-608">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="608" id="btnAnswer608">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint608" data-toggle="modal" id="hintBtn608"><i class="fad fa-life-ring mr-2"></i> Hint
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
