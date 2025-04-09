
<h1>Familiarity With Wireshark</h1>
<hr/>
<p>This lab aims to give Wireshark a basic familiarity and utilize its graphical interface to perform traffic captures. We will spend time using capture and display filters and getting used to the different outputs shown by the tool.</p>
<p>A user has brought their laptop to the helpdesk complaining of unusually long load times when they try to surf the web. They said it is almost as if the network is bogged down and the computer is making many different connections. We have been tasked with validating the pc is functioning correctly. To do so, we connect it to the network and start a packet capture while surfing the web. Analyze what can be seen in the output to determine if something is amiss. We only care about the laptop in question at this time, so filter out any traffic not destined to or sourcing from it.</p>
<div class="alert alert-primary fade show" role="alert">
<i class="mdi mdi-information-outline mr-2"></i>
If you wish to take a more exploratory approach to this lab, I have posted the overall tasks to accomplish. For a more detailed walkthrough of how to complete each step, look below each task in the solution bubble.
</div>
<hr/>
<h2>Tasks</h2>
<h4>Task #1</h4>
<p><code>Validate Wireshark is installed, then open Wireshark and familiarize yourself with the GUI windows and toolbars.</code></p>
<p>Take a minute and explore the Wireshark GUI. Ensure we know what options reside under which tabs in the command menus. Please pay special attention to the Capture tab and what resides within it.</p>
<hr/>
<h4>Task #2</h4>
<p><code>Select an interface to run a capture on and create a capture filter to show only traffic to and from your host IP.</code></p>
<p>Choose your active interface (eth0, or your Wifi card) to capture from.</p>
<details>
<summary><b>Click to show answer</b></summary>
<p>From your home screen, select the interface you would like to capture on from the drop-down menu. You could also click on the Capture tab → options → interface → then select the appropriate interface.</p>
</details>
<hr/>
<h4>Task #3</h4>
<p><code>Create a capture filter.</code></p>
<p>Next, we want to create a capture filter to only show us traffic sourcing from or destined to our IP address and apply it.</p>
<details>
<summary><b>Click to show answer</b></summary>
<p>To do so, from the home screen, select capture options and type the filter host X.X.X.X (or the IP on your interface)<br/>
Once your capture filter is correct, select Start.</p>
</details>
<hr/>
<h4>Task #4</h4>
<p><code>Navigate to a webpage to generate some traffic.</code></p>
<p>Open a web browser and navigate to pepsi.com. Repeat this step for http://apache.org. While the page is loading, switch back to the Wireshark window. We should see traffic flowing through our capture window. Once the page has loaded, stop the capture by clicking on the red square labeled Stop in the action bar.</p>
<hr/>
<h4>Task #5</h4>
<p><code>Use the capture results to answer the following questions.</code></p>
<p>Are multiple sessions being established between the machine and the webserver? How can you tell?</p>
<p>What application-level protocols are displayed in the results?</p>
<p>Can we discern anything in clear text? What was it?</p>
<details>
<summary><b>Click to show answer</b></summary>
<p>When visiting pepsi.com and http://apache.org you would have gotten several different streams and many different protocols. DNS to request the records for the pages, HTTP for the apache.org site, HTTPS for Pepsi.com, along with any other traffic happening in your network segment at the time.
If you noticed a difference between the traffic, you are on the right track. If you look at the output from apache.org it will be in plain text. This happens because HTTP is not encrypted. Looking at HTTPS traffic will be much different, however.</p>
</details>
<p>Don't stop here. Take some time to familiarize ourselves with the output Wireshark provides and how we can transform our view. We can also utilize the sample PCAP files found at https://wiki.wireshark.org/SampleCaptures to analyze different protocols and even things like ICS SCADA traffic and viruses. If you are connected to the Academy network to perform this lab, take some time to capture traffic on the interface provided. Some interesting network traffic can be found if one looks hard enough.</p>
<hr/>
<h2>Summary</h2>
<p>By the end of this lab, we should be familiar with Wireshark and how the GUI looks and operates. We have familiarized ourselves with the command bar and action bar and what resides within each respective tab. One should understand how to select an interface to capture with and successfully start a capture with a filter applied. Experiment with a few filters of your own design to see what different combinations can be used and how it shapes the results.</p>
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
