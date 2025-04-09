
<h1>Network Traffic Analysis</h1>
<hr/>
<p><code>Network Traffic Analysis (NTA)</code> can be described as the act of examining network traffic to characterize common ports and protocols utilized, establish a baseline for our environment, monitor and respond to threats, and ensure the greatest possible insight into our organization's network.</p>
<p>This process helps security specialists determine anomalies, including security threats in the network, early and effectively pinpoint threats. Network Traffic Analysis can also facilitate the process of meeting security guidelines. Attackers update their tactics frequently to avoid detection and leverage legitimate credentials with tools that most companies allow in their networks, making detection and, subsequently, response challenging for defenders. In such cases, Network Traffic Analysis can again prove helpful. Everyday use cases of NTA include:</p>
<table>
<thead>
<tr>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Collecting</code> real-time traffic within the network to analyze upcoming threats.</td>
</tr>
<tr>
<td><code>Setting</code> a baseline for day-to-day network communications.</td>
</tr>
<tr>
<td><code>Identifying</code> and analyzing traffic from non-standard ports, suspicious hosts, and issues with networking protocols such as HTTP errors, problems with TCP, or other networking misconfigurations.</td>
</tr>
<tr>
<td><code>Detecting</code> malware on the wire, such as ransomware, exploits, and non-standard interactions.</td>
</tr>
<tr>
<td>NTA is also useful when investigating past incidents and during threat hunting.</td>
</tr>
</tbody>
</table>
<p>Try to picture a threat actor targeting and infiltrating our network. If they wish to breach the network, attackers must inevitably interact and communicate with our infrastructure. Network communication takes place over many different ports and protocols, all being utilized concurrently by employees, equipment, and customers. To spot malicious traffic, we would need to use our knowledge of typical network traffic within our enclave. Doing so will narrow down our search and help us quickly find and disrupt adversarial communication.</p>
<p>For example, if we detect many <code>SYN</code> packets on ports that we never (or rarely) utilize in our network, we can conclude that this is most likely someone trying to determine what ports are open on our hosts. Actions like this are typical markers of a <code>portscan</code>. Performing such an analysis and coming to such conclusions requires specific skills and knowledge.</p>
<hr/>
<h2>Required Skills and Knowledge</h2>
<p>The skills we are about to list and describe require theoretical and practical knowledge acquired over time. We do not have to know everything by heart, but we should know what to look for when certain aspects of the content seem unfamiliar. This applies not only to NTA but also to most other topics we will deal with in cybersecurity.</p>
<h4>TCP/IP Stack &amp; OSI Model</h4>
<p>This understanding will ensure we grasp how networking traffic and the host applications interact.</p>
<h4>Basic Network Concepts</h4>
<p>Understanding what types of traffic we will see at each level includes an understanding of the individual layers that make up the TCP/IP and OSI model and the concepts of switching and routing. If we tap a network on a backbone link, we will see much more traffic than usual, and it will be vastly different from what we find tapping an office switch.</p>
<h4>Common Ports and Protocols</h4>
<p>Identifying standard ports and protocols quickly and having a functional understanding of how they communicate will ensure we can identify potentially malicious or malformed network traffic.</p>
<h4>Concepts of IP Packets and the Sublayers</h4>
<p>Foundational knowledge of how TCP and UDP communicate will, at a minimum, ensure we understand what we see or are searching for. TCP, for example, is stream-oriented and allows us to follow a conversation between hosts easily. UDP is quick but not concerned with completeness, so it would be harder to recreate something from this packet type.</p>
<h4>Protocol Transport Encapsulation</h4>
<p>Each layer will encapsulate the previous. Being able to read or dissect when this encapsulation changes will help us move through data quicker. It is easy to see hints based on encapsulation headers.</p>
<hr/>
<h2>Environment and Equipment</h2>
<p>The list below contains many different tools and equipment types that can be utilized to perform network traffic analysis. Each will provide a different way to capture or dissect the traffic. Some offer ways to copy and capture, while others read and ingest. This module will explore just a few of these (<a href="https://www.wireshark.org/">Wireshark</a> and <a href="https://www.tcpdump.org/">tcpdump</a> mostly). Keep in mind these tools are not strictly geared for admins. Many of these can be used for malicious reasons as well.</p>
<h4>Common Traffic Analysis Tools</h4>
<table>
<thead>
<tr>
<th><strong>Tool</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>tcpdump</code></td>
<td><a href="https://www.tcpdump.org/">tcpdump</a> is a command-line utility that, with the aid of LibPcap, captures and interprets network traffic from a network interface or capture file.</td>
</tr>
<tr>
<td><code>Tshark</code></td>
<td><a href="https://www.wireshark.org/docs/man-pages/tshark.html">TShark</a> is a network packet analyzer much like TCPDump. It will capture packets from a live network or read and decode from a file. It is the command-line variant of Wireshark.</td>
</tr>
<tr>
<td><code>Wireshark</code></td>
<td><a href="https://www.wireshark.org/">Wireshark</a> is a graphical network traffic analyzer. It captures and decodes frames off the wire and allows for an in-depth look into the environment. It can run many different dissectors against the traffic to characterize the protocols and applications and provide insight into what is happening.</td>
</tr>
<tr>
<td><code>NGrep</code></td>
<td><a href="https://github.com/jpr5/ngrep">NGrep</a> is a pattern-matching tool built to serve a similar function as grep for Linux distributions. The big difference is that it works with network traffic packets. NGrep understands how to read live traffic or traffic from a PCAP file and utilize regex expressions and BPF syntax. This tool shines best when used to debug traffic from protocols like HTTP and FTP.</td>
</tr>
<tr>
<td><code>tcpick</code></td>
<td><a href="http://tcpick.sourceforge.net/index.php?p=home.inc">tcpick</a> is a command-line packet sniffer that specializes in tracking and reassembling TCP streams. The functionality to read a stream and reassemble it back to a file with tcpick is excellent.</td>
</tr>
<tr>
<td><code>Network Taps</code></td>
<td>Taps (<a href="https://www.gigamon.com/">Gigamon</a>, <a href="https://www.niagaranetworks.com/products/network-tap">Niagra-taps</a>) are devices capable of taking copies of network traffic and sending them to another place for analysis. These can be in-line or out of band. They can actively capture and analyze the traffic directly or passively by putting the original packet back on the wire as if nothing had changed.</td>
</tr>
<tr>
<td><code>Networking Span Ports</code></td>
<td><a href="https://en.wikipedia.org/wiki/Port_mirroring">Span Ports</a> are a way to copy frames from layer two or three networking devices during egress or ingress processing and send them to a collection point. Often a port is mirrored to send those copies to a log server.</td>
</tr>
<tr>
<td><code>Elastic Stack</code></td>
<td>The <a href="https://www.elastic.co/elastic-stack">Elastic Stack</a> is a culmination of tools that can take data from many sources, ingest the data, and visualize it, to enable searching and analysis of it.</td>
</tr>
<tr>
<td><code>SIEMS</code></td>
<td><code>SIEMS</code> (such as <a href="https://www.splunk.com/en_us">Splunk</a>) are a central point in which data is analyzed and visualized. Alerting, forensic analysis, and day-to-day checks against the traffic are all use cases for a SIEM.</td>
</tr>
<tr>
<td>and others.</td>
<td></td>
</tr>
</tbody>
</table>
<hr/>
<h2>BPF Syntax</h2>
<p>Many of the tools mentioned above have their syntax and commands to utilize, but one that is shared among them is <a href="https://en.wikipedia.org/wiki/Berkeley_Packet_Filter">Berkeley Packet Filter (BPF)</a> syntax. This syntax is the primary method we will use. In essence, BPF is a technology that enables a raw interface to read and write from the Data-Link layer. With all this in mind, we care for BPF because of the filtering and decoding abilities it provides us. We will be utilizing BPF syntax through the module, so a basic understanding of how a BPF filter is set up can be helpful. For more information on BPF syntax, check out this <a href="https://www.ibm.com/docs/en/qsip/7.4?topic=queries-berkeley-packet-filters">reference</a>.</p>
<hr/>
<h2>Performing Network Traffic Analysis</h2>
<p>Performing analysis can be as simple as watching live traffic roll by in our console or as complex as capturing data with a tap, sending it back to a SIEM for ingestion, and analyzing the pcap data for signatures and alerts related to common tactics and techniques.</p>
<p>At a minimum, to listen passively, we need to be connected to the network segment we wish to listen on. This is especially true in a switched environment where VLANS and switch ports will not forward traffic outside their broadcast domain. With that in mind, if we wish to capture traffic from a specific VLAN, our capture device should be connected to that same network. Devices like network taps, switch or router configurations like span ports, and port mirroring can allow us to get a copy of all traffic traversing a specific link, regardless of what network segment or destination it belongs to.</p>
<h4>NTA Workflow</h4>
<p>Traffic analysis is not an exact science. NTA can be a very dynamic process and is not a direct loop. It is greatly influenced by what we are looking for (network errors vs. malicious actions) and where we have visibility into our network. Performing traffic analysis can distill down to a few basic tenants.</p>
<h4>NTA Workflow</h4>
<p><img alt="Cycle diagram showing four steps: 1. Ingest Traffic, 2. Reduce Noise by Filtering, 3. Analyze and Explore, 4. Detect and Alert." src="https://academy.hackthebox.com/storage/modules/81/workflow.png"/></p>
<h4>1. Ingest Traffic</h4>
<p>Once we have decided on our placement, begin capturing traffic. Utilize capture filters if we already have an idea of what we are looking for.</p>
<h4>2. Reduce Noise by Filtering</h4>
<p>Capturing traffic of a link, especially one in a production environment, can be extremely noisy. Once we complete the initial capture, an attempt to filter out unnecessary traffic from our view can make analysis easier. (Broadcast and Multicast traffic, for example.)</p>
<h4>3. Analyze and Explore</h4>
<p>Now is the time to start carving out data pertinent to the issue we are chasing down. Look at specific hosts, protocols, even things as specific as flags set in the TCP header. The following questions will help us:</p>
<ol>
<li>
<p>Is the traffic encrypted or plain text? Should it be?</p>
</li>
<li>
<p>Can we see users attempting to access resources to which they should not have access?</p>
</li>
<li>
<p>Are different hosts talking to each other that typically do not?</p>
</li>
</ol>
<h4>4. Detect and Alert</h4>
<ol>
<li>
<p>Are we seeing any errors? Is a device not responding that should be?</p>
</li>
<li>
<p>Use our analysis to decide if what we see is benign or potentially malicious.</p>
</li>
<li>
<p>Other tools like IDS and IPS can come in handy at this point. They can run heuristics and signatures against the traffic to determine if anything within is potentially malicious.</p>
</li>
</ol>
<h4>5. Fix and Monitor</h4>
<p>Fix and monitor is not a part of the loop but should be included in any workflow we perform. If we make a change or fix an issue, we should continue to monitor the source for a time to determine if the issue has been resolved.</p>
