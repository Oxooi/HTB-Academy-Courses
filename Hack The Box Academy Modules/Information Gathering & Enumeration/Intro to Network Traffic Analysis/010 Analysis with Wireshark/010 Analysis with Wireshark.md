
<h1>Analysis with Wireshark</h1>
<hr/>
<p><code>Wireshark</code> is a free and open-source network traffic analyzer much like tcpdump but with a graphical interface.
Wireshark is multi-platform and capable of capturing live data off many different interface types (to include WiFi, USB, and Bluetooth) and saving the traffic to several different formats. Wireshark allows the user to dive much deeper into the inspection of network packets than other tools. What makes Wireshark truly powerful is the analysis capability it provides, giving a detailed insight into the traffic.</p>
<p>Depending on the host we are using, we may not always have a GUI to utilize traditional Wireshark. Lucky for us, several variants allow us to use it from the command line.</p>
<h4>Features and Capabilities:</h4>
<ul>
<li>Deep packet inspection for hundreds of different protocols</li>
<li>Graphical and TTY interfaces</li>
<li>Capable of running on most Operating systems</li>
<li>Ethernet, IEEE 802.11, PPP/HDLC, ATM, Bluetooth, USB, Token Ring, Frame Relay, FDDI, among others</li>
<li>Decryption capabilities for IPsec, ISAKMP, Kerberos, SNMPv3, SSL/TLS, WEP, and WPA/WPA2</li>
<li>Many many more...</li>
</ul>
<hr/>
<h2>Requirements for Use</h2>
<p>Wireshark requires the following for use:</p>
<h4>Windows:</h4>
<ul>
<li>The Universal C Runtime. This is included with Windows 10 and Windows Server 2019 and is installed automatically on earlier versions if Microsoft Windows Update is enabled. Otherwise, KB2999226 or KB3118401 must be installed.</li>
<li>Any modern 64-bit AMD64/x86-64 or 32-bit x86 processor.</li>
<li>500 MB available RAM. Larger capture files require more RAM.</li>
<li>500 MB available disk space. Capture files require additional disk space.</li>
<li>Any modern display. 1280 × 1024 or higher resolution is recommended. Wireshark will make use of HiDPI or Retina resolutions if available. Power users will find multiple monitors useful.</li>
<li>A supported network card for capturing:
<ul>
<li>Ethernet. Any card supported by Windows should work.</li>
<li>802.11. See the Wireshark wiki page. Capturing raw 802.11 information may be difficult without special equipment.</li>
</ul>
</li>
<li>To install, download the executable from wireshark.org, validate the hash, and install.</li>
</ul>
<h4>Linux:</h4>
<ul>
<li>Wireshark runs on most UNIX and UNIX-like platforms, including Linux and most BSD variants. The system requirements should be comparable to the specifications listed above for Windows.</li>
<li>Binary packages are available for most Unix and Linux distributions.</li>
<li>To validate if the package exists on a host, use the following command:</li>
</ul>
<h4>Locating Wireshark</h4>
<pre><code class="language-shell-session">[!bash!]$ which wireshark
</code></pre>
<p>If the package does not exist, (It can often be found in <code>/usr/sbin/wireshark</code>) you can install it with:</p>
<h4>Installing Wireshark On Linux</h4>
<pre><code class="language-shell-session">[!bash!]$ sudo apt install wireshark 
</code></pre>
<hr/>
<h2>TShark VS. Wireshark (Terminal vs. GUI)</h2>
<p>Both options have their merits. TShark is a purpose-built terminal tool based on Wireshark. TShark shares many of the same features that are included in Wireshark and even shares syntax and options. TShark is perfect for use on machines with little or no desktop environment and can easily pass the capture information it receives to another tool via the command line. Wireshark is the feature-rich GUI option for traffic capture and analysis. If you wish to have the full-featured experience and work from a machine with a desktop environment, the Wireshark GUI is the way to go.</p>
<h4>Basic TShark Switches</h4>
<table>
<thead>
<tr>
<th align="center"><strong>Switch Command</strong></th>
<th><strong>Result</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">D</td>
<td>Will display any interfaces available to capture from and then exit out.</td>
</tr>
<tr>
<td align="center">L</td>
<td>Will list the Link-layer mediums you can capture from and then exit out. (ethernet as an example)</td>
</tr>
<tr>
<td align="center">i</td>
<td>choose an interface to capture from. (-i eth0)</td>
</tr>
<tr>
<td align="center">f</td>
<td>packet filter in libpcap syntax. Used during capture.</td>
</tr>
<tr>
<td align="center">c</td>
<td>Grab a specific number of packets, then quit the program. Defines a stop condition.</td>
</tr>
<tr>
<td align="center">a</td>
<td>Defines an autostop condition. Can be after a duration, specific file size, or after a certain number of packets.</td>
</tr>
<tr>
<td align="center">r (pcap-file)</td>
<td>Read from a file.</td>
</tr>
<tr>
<td align="center">W (pcap-file)</td>
<td>Write into a file using the pcapng format.</td>
</tr>
<tr>
<td align="center">P</td>
<td>Will print the packet summary while writing into a file (-W)</td>
</tr>
<tr>
<td align="center">x</td>
<td>will add Hex and ASCII output into the capture.</td>
</tr>
<tr>
<td align="center">h</td>
<td>See the help menu</td>
</tr>
</tbody>
</table>
<p><code>To see the full list of switches you can utilize:</code></p>
<h4>TShark Help</h4>
<pre><code class="language-shell-session">[!bash!]$ tshark -h
</code></pre>
<h4>TShark Basic Usage</h4>
<p>TShark can use filters for protocols, common items like hosts and ports, and even the ability to dig deeper into the packets and dissect individual fields from the packet.</p>
<h4>Locating TShark</h4>
<pre><code class="language-shell-session">[!bash!]$ which tshark

/usr/local/bin/tshark

[!bash!]$ tshark -D

1. en0 (Wi-Fi)
2. awdl0
3. llw0
4. utun0
5. utun1
6. lo0 (Loopback)
7. bridge0 (Thunderbolt Bridge)
8. en1 (Thunderbolt 0)
9. en2 (Thunderbolt 0)
10. en3 (Thunderbolt 1)
11. en4 (Thunderbolt 2)
12. gif0
13. stf0
14. ap1
15. ciscodump (Cisco remote capture)
16. randpkt (Random packet generator)
17. sshdump (SSH remote capture)
18. udpdump (UDP Listener remote capture)

[!bash!]$ tshark -i 1 -w /tmp/test.pcap

Capturing on 'Wi-Fi: en0'
484
</code></pre>
<p>With the basic string in the command line above, we utilize TShark to capture on en0, specified with the <code>-i</code> flag and the <code>-w</code> option to save the capture to a specified output file.
Utilizing TShark is very similar to TCPDump in the filters and switches we can use. Both tools utilize BPF syntax. To read the capture, tshark can be passed the <code>-r</code> switch just like in TCPDump, or we can pass the <code>-P</code> switch to have tshark print the packet summaries while writing out to a file. Below is an example of reading from the PCAP file we previously captured.</p>
<h4>Selecting an Interface &amp; Writing to a File</h4>
<pre><code class="language-shell-session">[!bash!]$ sudo tshark -i eth0 -w /tmp/test.pcap
</code></pre>
<h4>Applying Filters</h4>
<pre><code class="language-shell-session">[!bash!]$ sudo tshark -i eth0 -f "host 172.16.146.2"

Capturing on 'eth0'
    1 0.000000000 172.16.146.2 → 172.16.146.1 DNS 70 Standard query 0x0804 A github.com
    2 0.258861645 172.16.146.1 → 172.16.146.2 DNS 86 Standard query response 0x0804 A github.com A 140.82.113.4
    3 0.259866711 172.16.146.2 → 140.82.113.4 TCP 74 48256 → 443 [SYN] Seq=0 Win=64240 Len=0 MSS=1460 SACK_PERM=1 TSval=1321417850 TSecr=0 WS=128
    4 0.299681376 140.82.113.4 → 172.16.146.2 TCP 74 443 → 48256 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=1436 SACK_PERM=1 TSval=3885991869 TSecr=1321417850 WS=1024
    5 0.299771728 172.16.146.2 → 140.82.113.4 TCP 66 48256 → 443 [ACK] Seq=1 Ack=1 Win=64256 Len=0 TSval=1321417889 TSecr=3885991869
    6 0.306888828 172.16.146.2 → 140.82.113.4 TLSv1 579 Client Hello
    7 0.347570701 140.82.113.4 → 172.16.146.2 TLSv1.3 2785 Server Hello, Change Cipher Spec, Application Data, Application Data, Application Data, Application Data
    8 0.347653593 172.16.146.2 → 140.82.113.4 TCP 66 48256 → 443 [ACK] Seq=514 Ack=2720 Win=63488 Len=0 TSval=1321417937 TSecr=3885991916
    9 0.358887130 172.16.146.2 → 140.82.113.4 TLSv1.3 130 Change Cipher Spec, Application Data
   10 0.359781588 172.16.146.2 → 140.82.113.4 TLSv1.3 236 Application Data
   11 0.360037927 172.16.146.2 → 140.82.113.4 TLSv1.3 758 Application Data
   12 0.360482668 172.16.146.2 → 140.82.113.4 TLSv1.3 258 Application Data
   13 0.397331368 140.82.113.4 → 172.16.146.2 TLSv1.3 145 Application Data 
</code></pre>
<p><code>-f</code> allows us to apply filters to the capture. In the example, we utilized <code>host</code>, but you can use almost any filter Wireshark recognizes.
We have touched on TShark a bit now. Let's take a look at a nifty tool called Termshark.</p>
<hr/>
<h2>Termshark</h2>
<p>Termshark is a Text-based User Interface (TUI) application that provides the user with a Wireshark-like interface right in your terminal window.</p>
<h4>Termshark</h4>
<p><img alt="Network packet capture in Termshark showing TCP and TLSv1.3 traffic between IPs 172.16.146.2 and 140.82.114.5, with details on Ethernet, IP, and TCP protocols." src="https://academy.hackthebox.com/storage/modules/81/termshark.png"/></p>
<p>Termshark can be found at <a href="https://github.com/gcla/termshark">Termshark</a>. It can be built from the source by cloning the repo, or pull down one of the current stable releases from https://github.com/gcla/termshark/releases , extract the file, and hit the ground running.</p>
<p>For help navigating this TUI, see the image below.</p>
<h4>Termshark Help</h4>
<p><img alt="Termshark interface showing network packet details with a help overlay listing keyboard shortcuts for navigation and filtering." src="https://academy.hackthebox.com/storage/modules/81/termshark-help.png"/></p>
<p>To start Termshark, issue the same strings, much like TShark or tcpdump. We can specify an interface to capture on, filters, and other settings from the terminal. The Termshark window will not open until it senses traffic in its capture filter. So give it a second if nothing happens.</p>
<hr/>
<h2>Wireshark GUI Walkthrough</h2>
<p>Now that we have spent time learning the art of packet capture from the command line let's spend some time in Wireshark. We will take a few minutes to examine what we are looking at in the output below. Let's dissect this view of the Wireshark GUI.</p>
<h4>Wireshark GUI</h4>
<p><img alt="Wireshark capture showing HTTP and TCP traffic between IPs 10.1.1.101 and 10.1.1.1, with details on GET requests and packet data in hex and ASCII." src="https://academy.hackthebox.com/storage/modules/81/wireshark-interface.png"/></p>
<p>Three Main Panes: <code>See Figure above</code></p>
<ol>
<li>
<p>Packet List: <code>Orange</code></p>
<ul>
<li>In this window, we see a summary line of each packet that includes the fields listed below by default. We can add or remove columns to change what information is presented.
<ul>
<li>Number- Order the packet arrived in Wireshark</li>
<li>Time- Unix time format</li>
<li>Source- Source IP</li>
<li>Destination- Destination IP</li>
<li>Protocol- The protocol used (TCP, UDP, DNS, ETC.)</li>
<li>Information- Information about the packet. This field can vary based on the type of protocol used within. It will show, for example, what type of query It is for a DNS packet.</li>
</ul>
</li>
</ul>
</li>
<li>
<p>Packet Details: <code>Blue</code></p>
<ul>
<li>The Packet Details window allows us to drill down into the packet to inspect the protocols with greater detail. It will break it down into chunks that we would expect following the typical OSI Model reference. <code>The packet is dissected into different encapsulation layers for inspection.</code>
</li>
<li>Keep in mind, Wireshark will show this encapsulation in reverse order with lower layer encapsulation at the top of the window and higher levels at the bottom.</li>
</ul>
</li>
<li>
<p>Packet Bytes: <code>Green</code></p>
<ul>
<li>The Packet Bytes window allows us to look at the packet contents in ASCII or hex output. As we select a field from the windows above, it will be highlighted in the Packet Bytes window and show us where that bit or byte falls within the overall packet.</li>
<li>This is a great way to validate that what we see in the Details pane is accurate and the interpretation Wireshark made matches the packet output.</li>
<li>Each line in the output contains the data offset, sixteen hexadecimal bytes, and sixteen ASCII bytes. Non-printable bytes are replaced with a period in the ASCII format.</li>
</ul>
</li>
</ol>
<h4>Other Notable Features</h4>
<p>When looking at the Wireshark interface, we will notice a few different option areas and radial buttons. These areas are control points in which we can modify the interface and our view of the packets in the current capture. <code>See Figure below</code></p>
<h4>Wireshark Menu</h4>
<p><img alt="Wireshark capture showing HTTP and TCP traffic between IPs 10.1.1.101 and 10.1.1.1, with details on GET requests and packet data in hex and ASCII." src="https://academy.hackthebox.com/storage/modules/81/wireshark-menu.png"/></p>
<h2>Performing our first capture in Wireshark</h2>
<p>Starting a capture with Wireshark is a simple endeavor. The gif below will show the steps.</p>
<h4>Steps To Start A Capture</h4>
<p><img alt="GIF showcasing the capture options." src="https://academy.hackthebox.com/storage/modules/81/first-capture-ws.gif"/></p>
<p>Keep in mind, any time we change the capture options, Wireshark will restart the trace. Much like TCPDump, Wireshark has capture and display filter options that can be used.</p>
<hr/>
<h2>The Basics</h2>
<h4>The Toolbar</h4>
<p><img alt="Toolbar with menu options and icons for file operations, search, and filter application." src="https://academy.hackthebox.com/storage/modules/81/wireshark-toolbar.jpg"/></p>
<p>Wireshark's Toolbar is a central point to manage the many features Wireshark includes. From here, we can start and stop captures, change interfaces, open and save .pcap files and apply different filters or analysis add-ins.</p>
<h4>How to Save a Capture</h4>
<p>Let's say we need to capture what we have in our window currently for troubleshooting later. Saving a capture is super simple:</p>
<ul>
<li>Select File  ⇢ save
OR</li>
<li>From the toolbar, select the file option and choose where to save the file and in what format.</li>
</ul>
<p>Be aware that Wireshark can save captures into multiple formats. Choose the one needed for the scenario, but we will use the <code>.pcap</code> format for now.</p>
<hr/>
<h2>Pre-capture and Post-capture Processing and Filtering</h2>
<p>While capturing traffic with Wireshark, we have several options regarding how and when we filter out traffic. This is accomplished utilizing Capture and Display filters. The Former initiated before the capture starts and the latter during or after capture is complete. While Wireshark has a bunch of useful baked-in functionality, it is worth mentioning that it has a bit of trouble handling large captures. The more packets captured, the longer it will take Wireshark to run the display or analysis filter against it. It can take from just a couple of seconds to a few minutes if it completes at all. If we are working with a large pcap file, it may be best to break it up into smaller chunks first.</p>
<h4>Capture Filters</h4>
<p><code>Capture Filters-</code> are entered before the capture is started. These use BPF syntax like <code>host 214.15.2.30</code> much in the same fashion as TCPDump. We have fewer filter options this way, and a capture filter will drop all other traffic not explicitly meeting the criteria set. This is a great way to trim down the data you write to disk when troubleshooting a connection, such as capturing the conversations between two hosts.</p>
<p>Here is a table of common and helpful capture filters with a description of each:</p>
<table>
<thead>
<tr>
<th align="center"><strong>Capture Filters</strong></th>
<th><strong>Result</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">host x.x.x.x</td>
<td>Capture only traffic pertaining to a certain host</td>
</tr>
<tr>
<td align="center">net x.x.x.x/24</td>
<td>Capture traffic to or from a specific network (using slash notation to specify the mask)</td>
</tr>
<tr>
<td align="center">src/dst net x.x.x.x/24</td>
<td>Using src or dst net will only capture traffic sourcing from the specified network or destined to the target network</td>
</tr>
<tr>
<td align="center">port #</td>
<td>will filter out all traffic except the port you specify</td>
</tr>
<tr>
<td align="center">not port #</td>
<td>will capture everything except the port specified</td>
</tr>
<tr>
<td align="center">port # and #</td>
<td>AND will concatenate your specified ports</td>
</tr>
<tr>
<td align="center">portrange x-x</td>
<td>portrange will grab traffic from all ports within the range only</td>
</tr>
<tr>
<td align="center">ip / ether / tcp</td>
<td>These filters will only grab traffic from specified protocol headers.</td>
</tr>
<tr>
<td align="center">broadcast / multicast / unicast</td>
<td>Grabs a specific type of traffic. one to one, one to many, or one to all.</td>
</tr>
</tbody>
</table>
<h4>Applying a Capture Filter</h4>
<p>Before we apply a capture filter, let us take a look at the built-in filters. To do so:
Click on the capture radial at the top of the Wireshark window → then select capture filters from the drop-down.</p>
<h4>Filter List</h4>
<p><img alt="Wireshark capture filters list with expressions for filtering by Ethernet, IP, TCP, UDP, and specific ports." src="https://academy.hackthebox.com/storage/modules/81/capture-filter-list.png"/></p>
<p>From here, we can modify the existing filters or add our own.</p>
<p>To apply the filter to a capture, we will:
Click on the capture radial at the top of the Wireshark window → then select Options from the drop-down → in the new window select the drop-down for Capture filter for selected interfaces or type in the filter we wish to use. <code>below the red arrow in the picture below</code></p>
<h4>Applying A Capture Filter</h4>
<p><img alt="Wireshark capture options showing interfaces, promiscuous mode enabled, and TCP filter applied." src="https://academy.hackthebox.com/storage/modules/81/how-to-add-cap.png"/></p>
<h4>Display Filters</h4>
<p><code>Display Filters-</code> are used while the capture is running and after the capture has stopped. Display filters are proprietary to Wireshark, which offers many different options for almost any protocol.</p>
<p>Here is a table of common and helpful display filters with a description of each:</p>
<table>
<thead>
<tr>
<th align="center"><strong>Display Filters</strong></th>
<th><strong>Result</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">ip.addr == x.x.x.x</td>
<td>Capture only traffic pertaining to a certain host. This is an OR statement.</td>
</tr>
<tr>
<td align="center">ip.addr == x.x.x.x/24</td>
<td>Capture traffic pertaining to a specific network. This is an OR statement.</td>
</tr>
<tr>
<td align="center">ip.src/dst == x.x.x.x</td>
<td>Capture traffic to or from a specific host</td>
</tr>
<tr>
<td align="center">dns / tcp / ftp / arp / ip</td>
<td>filter traffic by a specific protocol. There are many more options.</td>
</tr>
<tr>
<td align="center">tcp.port == x</td>
<td>filter by a specific tcp port.</td>
</tr>
<tr>
<td align="center">tcp.port / udp.port != x</td>
<td>will capture everything except the port specified</td>
</tr>
<tr>
<td align="center">and / or / not</td>
<td>AND will concatenate, OR will find either of two options, NOT will exclude your input option.</td>
</tr>
</tbody>
</table>
<div class="alert alert-primary fade show" role="alert">
<i class="mdi mdi-information-outline mr-2"></i>
Keep in mind, while utilizing Display filters traffic is processed to show only what is requested but the rest of the capture file will not be overwritten. Applying Display filters and analysis options will cause Wireshark to reprocess the pcap data in order to apply.
</div>
<h4>Applying a Display Filter</h4>
<p>Applying a display filter is even easier than a capture filter. From the main Wireshark capture window, all we need to do is:
select the bookmark in the Toolbar → , then select an option from the drop-down. Alternatively, place the cursor in the text radial → and type in the filter we wish to use. If the field turns green, the filter is correct. <code>Just like in the image below.</code></p>
<h4>Applying Display Filters</h4>
<p><img alt="Wireshark interface showing filtered TCP traffic between IPs 162.159.134.234 and 192.168.86.211, with protocols TLSv1.2 and TCP." src="https://academy.hackthebox.com/storage/modules/81/display-filter.png"/></p>
<p>When using capture and display filters, keep in mind that what we specify is taken in a literal sense. For example, filtering for port 80 traffic is not the same as filtering for HTTP. Think of ports and protocols more like guidelines instead of rigid rules. Ports can be bound and used for different purposes other than what they were originally intended. For example, filtering for HTTP will look for key markers that the protocol uses, such as GET/POST requests, and show results from them. Filtering for port 80 will show anything sent or received over that port regardless of the transport protocol.</p>
<p>In the next section, we will work with some of the more advanced features of Wireshark.</p>
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
<img alt="sparkles-icon-decoration" class="ml-2 w-auto sparkles-icon" height="20" src="/images/sparkles-solid.svg"/>
</div>
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
<label class="module-question" for="483"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> True or False: Wireshark can run on both Windows and Linux.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer483" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-483">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="483" id="btnAnswer483">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint483" data-toggle="modal" id="hintBtn483"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="484"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> Which Pane allows a user to see a summary of each packet grabbed during the capture?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer484" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-484">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="484" id="btnAnswer484">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint484" data-toggle="modal" id="hintBtn484"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="485"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> Which pane provides you insight into the traffic you captured and displays it in both ASCII and Hex?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer485" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-485">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="485" id="btnAnswer485">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="601"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> What switch is used with TShark to list possible interfaces to capture on?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer601" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-601">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="601" id="btnAnswer601">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint601" data-toggle="modal" id="hintBtn601"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="602"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> What switch allows us to apply filters in TShark?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer602" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-602">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="602" id="btnAnswer602">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint602" data-toggle="modal" id="hintBtn602"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="603"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> Is a capture filter applied before the capture starts or after? (answer before or after)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer603" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-603">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="603" id="btnAnswer603">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint603" data-toggle="modal" id="hintBtn603"><i class="fad fa-life-ring mr-2"></i> Hint
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
