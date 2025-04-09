
<h1>Networking Primer - Layers 1-4</h1>
<hr/>
<p>This section serves as a quick refresher on networking and how some standard protocols we can see while performing traffic captures work. These concepts are at the core of capturing and dissecting traffic. Without a fundamental understanding of typical network flow and what ports and protocols are used, we cannot accurately analyze any traffic we capture. If this is the first time you encounter some of these terms or concepts, we suggest completing the <a href="https://academy.hackthebox.com/course/preview/introduction-to-networking">Introduction to Networking</a> Module first.</p>
<hr/>
<h2>OSI / TCP-IP Models</h2>
<h4>Networking Models</h4>
<p><img alt="Comparison of OSI and TCP/IP models: OSI has 7 layers including Application, Presentation, Session, Transport, Network, Data-Link, and Physical. TCP/IP has 4 layers: Application, Transport, Internet, and Link." src="https://academy.hackthebox.com/storage/modules/81/net_models4.png"/></p>
<p>The image above gives a great view of the Open Systems Interconnect (<code>OSI</code>) model and the Transmission Control Protocol - Internet Protocol (<code>TCP-IP</code>) model side by side. The models are a graphical representation of how communication is handled between networked computers. Let's take a second to compare the two:</p>
<h4>Model Traits Comparison.</h4>
<table>
<thead>
<tr>
<th>Trait</th>
<th>OSI</th>
<th>TCP-IP</th>
</tr>
</thead>
<tbody>
<tr>
<td>Layers</td>
<td>Seven</td>
<td>Four</td>
</tr>
<tr>
<td>Flexibility</td>
<td>Strict</td>
<td>Loose</td>
</tr>
<tr>
<td>Dependency</td>
<td>Protocol independent &amp; generic</td>
<td>Based on common communication protocols</td>
</tr>
</tbody>
</table>
<p>When examining these two models, we can notice that the OSI model is segmented more than the TCP-IP model. This is because it is broken down into small functional chunks. Layers one through four of the OSI model are focused on controlling the transportation of data between hosts. This control includes everything from the physical medium used for transmission to the protocol utilized to manage the conversation or lack thereof when transporting data. Layers five through seven handle the interpretation, management, and presentation of the encapsulated data presented to the end-user. Think of the OSI model as the theory behind how everything works, whereas the TCP-IP model is more closely aligned with the actual functionality of networking. The TCP-IP model is a bit more blended, and the rules are flexible. The TCP-IP model comprises four layers where layers five, six, and seven of the OSI model align with layer four of the TCP-IP model. Layer three deals with transportation, layer two is the internet layer which aligns with the network layer in OSI, and layer one is the link-layer which covers layers two and one of the OSI model.</p>
<p>Throughout this module, we will examine many different Protocol Data Units (<code>PDU</code>), so a functional understanding of how it appears in theory and on the wire is required. A PDU is a data packet made up of control information and data encapsulated from each layer of the OSI model. The breakout below will show how the layers in the two models match up to a PDU.</p>
<h4>PDU Example</h4>
<p><img alt="Comparison of OSI and TCP/IP models: OSI has 7 layers including Application, Presentation, Session, Transport, Network, Data-Link, and Physical. TCP/IP has 4 layers: Application, Transport, Internet, and Link. PDU types are Data, Segment/Datagram, Packet, Frame, and Bit." src="https://academy.hackthebox.com/storage/modules/81/net_models_pdu2.png"/></p>
<p>When inspecting a PDU, we need to keep the idea of encapsulation in mind. As our data moves down the protocol stack, each layer will wrap the previous layers' data in a new bubble we call encapsulation. This bubble adds the necessary information of that layer into the header of the PDU. This information can vary by level, but it includes what is held by the previous layer, operational flags, any options required to negotiate communications, the source and destination IP addresses, ports, transport, and application layer protocols.</p>
<h4>PDU Packet Breakdown</h4>
<p><img alt="Diagram showing PDU types: Data, Segment/Datagram, Packet, Frame, Bit. Network packet details include Ethernet II, IPv4, and UDP headers with source and destination addresses." src="https://academy.hackthebox.com/storage/modules/81/pdu-wireshark.png"/></p>
<p>The image above shows us the makeup of a PDU side by side with a packet breakout from Wireshark's Packet Details pane. Please take note that when we see the breakout in Wireshark, it is in reverse order. Wireshark shows us the PDU in reverse because it is in the order that it was unencapsulated.</p>
<hr/>
<h2>Addressing Mechanisms</h2>
<p>Now that we have gone over the basic concepts driving networking behavior let us take some time to discuss the addressing mechanisms that enable the delivery of our packets to the correct hosts. We will begin with Media Access Control addresses first.</p>
<h4>MAC-Addressing</h4>
<p>Each logical or physical interface attached to a host has a Media Access Control (<code>MAC</code>) address. This address is a 48-bit <code>six octet</code> address represented in hexadecimal format. If we look at the image below, we can see an example of one by the <code>red</code> arrow.</p>
<h4>Mac-Address</h4>
<p><img alt="Network interface configuration for en0: flags, MAC address, IPv6 and IPv4 addresses, netmask, and status details." src="https://academy.hackthebox.com/storage/modules/81/Addressing.png"/></p>
<p>MAC-addressing is utilized in Layer two ( <code>the data-link or link-layer depending on which model you look at</code> ) communications between hosts. This works through host-to-host communication within a broadcast domain. If layer two traffic needs to cross a layer three interface, that PDU is sent to the layer three egress interface, and it is routed to the correct network. At layer two, this looks as though the PDU is addressed to the router interface, and the router will take the layer three address into account when determining where to send it next. Once it makes a choice, it strips the encapsulation at layer two and replaces it with new information that indicates the next physical address in the route.</p>
<hr/>
<h2>IP Addressing</h2>
<p>The Internet Protocol (<code>IP</code>) was developed to deliver data from one host to another across network boundaries. IP is responsible for routing packets, the encapsulation of data, and fragmentation and reassembly of datagrams when they reach the destination host. By nature, IP is a connectionless protocol that provides no assurances that data will reach its intended recipient. For the reliability and validation of data delivery, IP relies on upper-layer protocols such as TCP. Currently, there exist two main versions of IP. IPv4, which is the current dominant standard, and IPv6, which is intended to be the successor of IPv4.</p>
<h4>IPv4</h4>
<p>The most common addressing mechanism most are familiar with is the Internet Protocol address version 4 (<code>IPv4</code>). IPv4 addressing is the core method of routing packets across networks to hosts located outside our immediate vicinity. The image below shows us an example of an IPv4 address by the <code>green</code> arrow.</p>
<h4>IP Address</h4>
<p><img alt="Network interface configuration for en0: flags, MAC address, IPv6 and IPv4 addresses, netmask, and status details." src="https://academy.hackthebox.com/storage/modules/81/Addressing.png"/></p>
<p>An IPv4 address is made up of a 32-bit <code>four octet</code> number represented in decimal format. In our example, we can see the address <code>192.168.86.243</code>. Each octet of an IP address can be represented by a number ranging from <code>0</code> to <code>255</code>. When examining a PDU, we will find IP addresses in layer three (<code>Network</code>) of the OSI model and layer two (<code>internet</code>) of the TCP-IP model. We will not deep dive into IPv4 here, but for the sake of this module, understand what these addresses are, what they do for us, and at which layer they are used.</p>
<h4>IPv6</h4>
<p>After a little over a decade of utilizing IPv4, it was determined that we had quickly exhausted the pool of usable IP addresses. With such large chunks sectioned off for special use or private addressing, the world had quickly used up the available space. To help solve this issue, two things were done. The first was implementing variable-length subnet masks (<code>VLSM</code>) and Classless Inter-Domain Routing (<code>CIDR</code>). This allowed us to redefine the useable IP addresses in the v4 format changing how addresses were assigned to users. The second was the creation and continued development of <code>IPv6</code> as a successor to IPv4.</p>
<p>IPv6 provides us a much larger address space that can be utilized for any networked purpose. IPv6 is a 128-bit address <code>16 octets</code> represented in Hexadecimal format. We can see an example of a shortened IPv6 address in the image below by the blue arrow.</p>
<h4>IPv6 Address</h4>
<p><img alt="Network interface configuration for en0: flags, MAC address, IPv6 and IPv4 addresses, netmask, and status details." src="https://academy.hackthebox.com/storage/modules/81/Addressing.png"/></p>
<p>Along with a much larger address space, IPv6 provides:
Better support for Multicasting (sending traffic from one to many)
Global addressing per device
Security within the protocol in the form of IPSec
Simplified Packet headers allow for easier processing and move from connection to connection without being re-assigned an address.</p>
<p>IPv6 uses four main types of addresses within its schema:</p>
<h4>IPv6 Addressing Types</h4>
<table>
<thead>
<tr>
<th><strong>Type</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Unicast</code></td>
<td>Addresses for a single interface.</td>
</tr>
<tr>
<td><code>Anycast</code></td>
<td>Addresses for multiple interfaces, where only one of them receives the packet.</td>
</tr>
<tr>
<td><code>Multicast</code></td>
<td>Addresses for multiple interfaces, where all of them receive the same packet.</td>
</tr>
<tr>
<td><code>Broadcast</code></td>
<td>Does not exist and is realized with multicast addresses.</td>
</tr>
</tbody>
</table>
<p>When thinking about each address type, it is helpful to remember that Unicast traffic is host to host, while Multicast is one to many, and Anycast is one to many in a group where only one will answer the packet. (think load balancing).</p>
<p>Even with its current state providing many advantages over IPv4, the adoption of IPv6 has been slow to catch on.</p>
<h4>Adoption of IPv6</h4>
<p><img alt="World map showing IPv6 adoption: Darker green indicates higher deployment and fewer connectivity issues; lighter green indicates less deployment." src="https://academy.hackthebox.com/storage/modules/81/ipv6-adoption.png"/></p>
<p>At the time of writing, according to statistics published by Google, the adoption rate is only around 40 percent globally.</p>
<hr/>
<h2>TCP / UDP, Transport Mechanisms</h2>
<p>The Transport Layer has several mechanisms to help ensure the seamless delivery of data from source to destination. Think about the Transport layer as a control hub. Application data from the higher layers have to traverse down the stack to the Transport layer. This layer directs how the traffic will be encapsulated and thrown to the lower layer protocols ( IP and MAC ). Once the data reaches its intended recipient, the Transport layer, working with the Network / Internet layer protocols, is responsible for reassembling the encapsulated data back in the correct order. The two mechanisms used to accomplish this task are the Transmission Control  (<code>TCP</code>) and the User Datagram Protocol (<code>UDP</code>).</p>
<h4>TCP vs. UDP</h4>
<p>Let us take a second to examine these two protocols side by side.</p>
<h4>TCP VS. UDP</h4>
<table>
<thead>
<tr>
<th><strong>Characteristic</strong></th>
<th><strong>TCP</strong></th>
<th><strong>UDP</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Transmission</code></td>
<td>Connection-oriented</td>
<td>Connectionless. Fire and forget.</td>
</tr>
<tr>
<td><code>Connection Establishment</code></td>
<td>TCP uses a three-way handshake to ensure that a connection is established.</td>
<td>UDP does not ensure the destination is listening.</td>
</tr>
<tr>
<td><code>Data Delivery</code></td>
<td>Stream-based conversations</td>
<td>packet by packet, the source does not care if the destination is active</td>
</tr>
<tr>
<td><code>Receipt of data</code></td>
<td>Sequence and Acknowledgement numbers are utilized to account for data.</td>
<td>UDP does not care.</td>
</tr>
<tr>
<td><code>Speed</code></td>
<td>TCP has more overhead and is slower because of its built-in functions.</td>
<td>UDP is fast but unreliable.</td>
</tr>
</tbody>
</table>
<p>By looking at the table above, we can see that TCP and UDP provide two very different data transmission methods. TCP is considered a more reliable protocol since it allows for error checking and data acknowledgment as a normal function. In contrast, UDP is a quick, fire, and forget protocol best utilized when we care about speed over quality and validation.</p>
<p>To put this into perspective, TCP is utilized when moving data that requires completeness over speed. For example, when we use Secure Shell (<code>SSH</code>) to connect from one host to another, a connection is opened that stays active while you issue commands and perform actions. This is a function of TCP, ensuring our conversation with the distant host is not interrupted. If it does get interrupted for some reason, TCP will not reassemble a partial fragment of a packet and send it to the application. We can avoid errors this way. What would happen if we issued a command like <code>sudo passwd user</code> to change the user's password on a remote host, and during the change, part of the message drops. If this were over UDP, we would have no way of knowing what happened to the rest of that message and potentially mess up the user's password or worse. TCP helps prevent this by acknowledging each packet received to ensure the destination host has acquired each packet before assembling the command and sending it to the application for action.</p>
<p>On the other hand, when we require quick responses or utilize applications that require speed over completeness, UDP is our answer. Take streaming a video, for example. The user will not notice a pixel or two dropped from a streaming video. We care more about watching the video without it constantly stopping to buffer the next piece. Another example of this would be DNS. When a host requests a record entry for inlanefreight.com, the host is looking for a quick response to continue the process it was performing. The worst thing that happens if a DNS request is dropped is that it is reissued. No harm, no foul. The user will not receive corrupted data because of this drop.</p>
<p>UDP traffic appears like regular traffic; it is a single packet, with no response or acknowledgment that it was sent or received, so there is not much to show here. However, we can take a look at TCP and how it establishes connections.</p>
<hr/>
<h2>TCP Three-way Handshake</h2>
<p>One of the ways TCP ensures the delivery of data from server to client is the utilization of sessions. These sessions are established through what is called a three-way handshake. To make this happen, TCP utilizes an option in the TCP header called flags. We will not deep dive into TCP flags now; know that the common flags we will see in a three-way handshake are Synchronization (<code>SYN</code>) and acknowledgment (<code>ACK</code>). When a host requests to have a conversation with a server over TCP;</p>
<ol>
<li>
<p>The <code>client</code> sends a packet with the SYN flag set to on along with other negotiable options in the TCP header.</p>
<ol>
<li>This is a synchronization packet. It will only be set in the first packet from host and server and enables establishing a session by allowing both ends to agree on a sequence number to start communicating with.</li>
<li>This is crucial for the tracking of packets. Along with the sequence number sync, many other options are negotiated in this phase to include window size, maximum segment size, and selective acknowledgments.</li>
</ol>
</li>
<li>
<p>The <code>server</code> will respond with a TCP packet that includes a SYN flag set for the sequence number negotiation and an ACK flag set to acknowledge the previous SYN packet sent by the host.</p>
<ol>
<li>The server will also include any changes to the TCP options it requires set in the options fields of the TCP header.</li>
</ol>
</li>
<li>
<p>The <code>client</code> will respond with a TCP packet with an ACK flag set agreeing to the negotiation.</p>
<ol>
<li>This packet is the end of the three-way handshake and established the connection between client and server.</li>
</ol>
</li>
</ol>
<p>Let us take a quick look at this in action to be familiar with it when it appears in our packet output later on in the module.</p>
<h4>TCP Three-way Handshake</h4>
<p><img alt="Network packet capture showing TCP connections between IPs 192.168.1.140 and 174.143.213.184, with protocols TCP and HTTP, displaying sequence and acknowledgment numbers." src="https://academy.hackthebox.com/storage/modules/81/three-way-handshake.png"/></p>
<p>When examining this output, we can see the start of our handshake on line one. Looking at the information highlighted in the <code>red box</code>, we can see our initial Syn flag is set. If we look at the port numbers underlined in <code>green</code>, we can see two numbers, <code>57678</code> and <code>80</code>. The first number is the random high port number in use by the client, and the second is the well-known port for HTTP used by the server to listen for incoming web request connections. In line 2, we can see the server's response to the client with an <code>SYN / ACK</code> packet sent to the same ports. On line 3, we can see the client acknowledge the server's synchronization packet to establish the connection.</p>
<p>Packet 4 shows us that the HTTP request was sent, and a session is established to stream the data for the image requested. We can see as the stream continues that TCP sends acknowledgments for each chunk of data sent. This is an example of typical TCP communication.</p>
<p>We have seen how a session is established with TCP; now, let us examine how a session is concluded.</p>
<h4>TCP Session Teardown</h4>
<p><img alt="Network packet capture showing TCP connections between IPs 192.168.1.140 and 174.143.213.184, with protocols TCP and HTTP, displaying sequence and acknowledgment numbers, including SYN, ACK, and FIN flags." src="https://academy.hackthebox.com/storage/modules/81/session-teardown.png"/></p>
<p>In the image above,  a set of packets similar to our three-way handshake visible at the end of the output. This is how TCP gracefully shuts connections. Another flag we will see with TCP is the <code>FIN</code> flag. It is used for signaling that the data transfer is finished and the sender is requesting termination of the connection. The client acknowledges the receipt of the data and then sends a <code>FIN</code> and <code>ACK</code> to begin session termination. The server responds with an acknowledgment of the FIN and sends back its own FIN. Finally, the client acknowledges the session is complete and closes the connection. Before session termination, we should see a packet pattern of:</p>
<ol>
<li>
<code>FIN, ACK</code>
</li>
<li>
<code>FIN, ACK</code>,</li>
<li>
<code>ACK</code>
</li>
</ol>
<p>If we look at the image above detailing a session, we will see that this is the case. An output similar to this is considered an adequately terminated connection.</p>
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
<label class="module-question" for="577"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> How many layers does the OSI model have?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer577" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-577">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="577" id="btnAnswer577">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint577" data-toggle="modal" id="hintBtn577"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="578"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> How many layers are there in the TCP/IP model?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer578" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-578">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="578" id="btnAnswer578">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint578" data-toggle="modal" id="hintBtn578"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="579"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> True or False: Routers operate at layer 2 of the OSI model?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer579" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-579">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="579" id="btnAnswer579">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint579" data-toggle="modal" id="hintBtn579"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="580"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> What addressing mechanism is used at the Link Layer of the TCP/IP model?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer580" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-580">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="580" id="btnAnswer580">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint580" data-toggle="modal" id="hintBtn580"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="581"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> At what layer of the OSI model is a PDU encapsulated into a packet? ( the number )
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer581" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-581">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="581" id="btnAnswer581">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint581" data-toggle="modal" id="hintBtn581"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="582"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> What addressing mechanism utilizes a 32-bit address?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer582" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-582">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="582" id="btnAnswer582">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint582" data-toggle="modal" id="hintBtn582"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="583"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> What Transport layer protocol is connection oriented?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer583" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-583">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="583" id="btnAnswer583">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint583" data-toggle="modal" id="hintBtn583"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="584"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> What Transport Layer protocol is considered unreliable?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer584" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-584">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="584" id="btnAnswer584">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint584" data-toggle="modal" id="hintBtn584"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="585"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> TCP's three-way handshake consists of 3 packets: 1.Syn, 2.Syn &amp; ACK, 3. _? What is the final packet of the handshake?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer585" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-585">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="585" id="btnAnswer585">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint585" data-toggle="modal" id="hintBtn585"><i class="fad fa-life-ring mr-2"></i> Hint
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
