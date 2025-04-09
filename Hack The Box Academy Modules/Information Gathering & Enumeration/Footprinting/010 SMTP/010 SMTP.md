
<h1>SMTP</h1>
<hr/>
<p>The <code>Simple Mail Transfer Protocol</code> (<code>SMTP</code>) is a protocol for sending emails in an IP network. It can be used between an email client and an outgoing mail server or between two SMTP servers. SMTP is often combined with the IMAP or POP3 protocols, which can fetch emails and send emails. In principle, it is a client-server-based protocol, although SMTP can be used between a client and a server and between two SMTP servers. In this case, a server effectively acts as a client.</p>
<p>By default, SMTP servers accept connection requests on port <code>25</code>. However, newer SMTP servers also use other ports such as TCP port <code>587</code>. This port is used to receive mail from authenticated users/servers, usually using the STARTTLS command to switch the existing plaintext connection to an encrypted connection. The authentication data is protected and no longer visible in plaintext over the network. At the beginning of the connection, authentication occurs when the client confirms its identity with a user name and password. The emails can then be transmitted. For this purpose, the client sends the server sender and recipient addresses, the email's content, and other information and parameters. After the email has been transmitted, the connection is terminated again. The email server then starts sending the email to another SMTP server.</p>
<p>SMTP works unencrypted without further measures and transmits all commands, data, or authentication information in plain text. To prevent unauthorized reading of data, the SMTP is used in conjunction with SSL/TLS encryption. Under certain circumstances, a server uses a port other than the standard TCP port <code>25</code> for the encrypted connection, for example, TCP port <code>465</code>.</p>
<p>An essential function of an SMTP server is preventing spam using authentication mechanisms that allow only authorized users to send e-mails. For this purpose, most modern SMTP servers support the protocol extension ESMTP with SMTP-Auth. After sending his e-mail, the SMTP client, also known as <code>Mail User Agent</code> (<code>MUA</code>), converts it into a header and a body and uploads both to the SMTP server. This has a so-called <code>Mail Transfer Agent</code> (<code>MTA</code>), the software basis for sending and receiving e-mails. The MTA checks the e-mail for size and spam and then stores it. To relieve the MTA, it is occasionally preceded by a <code>Mail Submission Agent</code> (<code>MSA</code>), which checks the validity, i.e., the origin of the e-mail. This <code>MSA</code> is also called <code>Relay</code> server. These are very important later on, as the so-called <code>Open Relay Attack</code> can be carried out on many SMTP servers due to incorrect configuration. We will discuss this attack and how to identify the weak point for it a little later. The MTA then searches the DNS for the IP address of the recipient mail server.</p>
<p>On arrival at the destination SMTP server, the data packets are reassembled to form a complete e-mail. From there, the <code>Mail delivery agent</code> (<code>MDA</code>) transfers it to the recipient's mailbox.</p>
<table>
<thead>
<tr>
<th>Client (<code>MUA</code>)</th>
<th><code>➞</code></th>
<th>Submission Agent (<code>MSA</code>)</th>
<th><code>➞</code></th>
<th>Open Relay (<code>MTA</code>)</th>
<th><code>➞</code></th>
<th>Mail Delivery Agent (<code>MDA</code>)</th>
<th><code>➞</code></th>
<th>Mailbox (<code>POP3</code>/<code>IMAP</code>)</th>
</tr>
</thead>
</table>
<p>But SMTP has two disadvantages inherent to the network protocol.</p>
<ol>
<li>
<p>The first is that sending an email using SMTP does not return a usable delivery confirmation. Although the specifications of the protocol provide for this type of notification, its formatting is not specified by default, so that usually only an English-language error message, including the header of the undelivered message, is returned.</p>
</li>
<li>
<p>Users are not authenticated when a connection is established, and the sender of an email is therefore unreliable. As a result, open SMTP relays are often misused to send spam en masse. The originators use arbitrary fake sender addresses for this purpose to not be traced (mail spoofing). Today, many different security techniques are used to prevent the misuse of SMTP servers. For example, suspicious emails are rejected or moved to quarantine (spam folder). For example, responsible for this are the identification protocol <a href="http://dkim.org/">DomainKeys</a> (<code>DKIM</code>), the <a href="https://dmarcian.com/what-is-spf/">Sender Policy Framework</a> (<code>SPF</code>).</p>
</li>
</ol>
<p>For this purpose, an extension for SMTP has been developed called <code>Extended SMTP</code> (<code>ESMTP</code>). When people talk about SMTP in general, they usually mean ESMTP. ESMTP uses TLS, which is done after the <code>EHLO</code> command by sending <code>STARTTLS</code>. This initializes the SSL-protected SMTP connection, and from this moment on, the entire connection is encrypted, and therefore more or less secure. Now <a href="https://www.samlogic.net/articles/smtp-commands-reference-auth.htm">AUTH PLAIN</a> extension for authentication can also be used safely.</p>
<hr/>
<h2>Default Configuration</h2>
<p>Each SMTP server can be configured in many ways, as can all other services. However, there are differences because the SMTP server is only responsible for sending and forwarding emails.</p>
<h4>Default Configuration</h4>
<pre><code class="language-shell-session">[!bash!]$ cat /etc/postfix/main.cf | grep -v "#" | sed -r "/^\s*$/d"

smtpd_banner = ESMTP Server 
biff = no
append_dot_mydomain = no
readme_directory = no
compatibility_level = 2
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache
myhostname = mail1.inlanefreight.htb
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
smtp_generic_maps = hash:/etc/postfix/generic
mydestination = $myhostname, localhost 
masquerade_domains = $myhostname
mynetworks = 127.0.0.0/8 10.129.0.0/16
mailbox_size_limit = 0
recipient_delimiter = +
smtp_bind_address = 0.0.0.0
inet_protocols = ipv4
smtpd_helo_restrictions = reject_invalid_hostname
home_mailbox = /home/postfix
</code></pre>
<p>The sending and communication are also done by special commands that cause the SMTP server to do what the user requires.</p>
<table>
<thead>
<tr>
<th><strong>Command</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>AUTH PLAIN</code></td>
<td>AUTH is a service extension used to authenticate the client.</td>
</tr>
<tr>
<td><code>HELO</code></td>
<td>The client logs in with its computer name and thus starts the session.</td>
</tr>
<tr>
<td><code>MAIL FROM</code></td>
<td>The client names the email sender.</td>
</tr>
<tr>
<td><code>RCPT TO</code></td>
<td>The client names the email recipient.</td>
</tr>
<tr>
<td><code>DATA</code></td>
<td>The client initiates the transmission of the email.</td>
</tr>
<tr>
<td><code>RSET</code></td>
<td>The client aborts the initiated transmission but keeps the connection between client and server.</td>
</tr>
<tr>
<td><code>VRFY</code></td>
<td>The client checks if a mailbox is available for message transfer.</td>
</tr>
<tr>
<td><code>EXPN</code></td>
<td>The client also checks if a mailbox is available for messaging with this command.</td>
</tr>
<tr>
<td><code>NOOP</code></td>
<td>The client requests a response from the server to prevent disconnection due to time-out.</td>
</tr>
<tr>
<td><code>QUIT</code></td>
<td>The client terminates the session.</td>
</tr>
</tbody>
</table>
<p>To interact with the SMTP server, we can use the <code>telnet</code> tool to initialize a TCP connection with the SMTP server. The actual initialization of the session is done with the command mentioned above, <code>HELO</code> or <code>EHLO</code>.</p>
<h4>Telnet - HELO/EHLO</h4>
<pre><code class="language-shell-session">[!bash!]$ telnet 10.129.14.128 25

Trying 10.129.14.128...
Connected to 10.129.14.128.
Escape character is '^]'.
220 ESMTP Server 


HELO mail1.inlanefreight.htb

250 mail1.inlanefreight.htb


EHLO mail1

250-mail1.inlanefreight.htb
250-PIPELINING
250-SIZE 10240000
250-ETRN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250-DSN
250-SMTPUTF8
250 CHUNKING
</code></pre>
<p>The command <code>VRFY</code> can be used to enumerate existing users on the system. However, this does not always work. Depending on how the SMTP server is configured, the SMTP server may issue <code>code 252</code> and confirm the existence of a user that does not exist on the system. A list of all SMTP response codes can be found <a href="https://serversmtp.com/smtp-error/">here</a>.</p>
<h4>Telnet - VRFY</h4>
<pre><code class="language-shell-session">[!bash!]$ telnet 10.129.14.128 25

Trying 10.129.14.128...
Connected to 10.129.14.128.
Escape character is '^]'.
220 ESMTP Server 

VRFY root

252 2.0.0 root


VRFY cry0l1t3

252 2.0.0 cry0l1t3


VRFY testuser

252 2.0.0 testuser


VRFY aaaaaaaaaaaaaaaaaaaaaaaaaaaa

252 2.0.0 aaaaaaaaaaaaaaaaaaaaaaaaaaaa
</code></pre>
<p>Therefore, one should never entirely rely on the results of automatic tools. After all, they execute pre-configured commands, but none of the functions explicitly state how the administrator configures the tested server.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Sometimes we may have to work through a web proxy. We can also make this web proxy connect to the SMTP server. The command that we would send would then look something like this: <code>CONNECT 10.129.14.128:25 HTTP/1.0</code></p>
</div>
</div>
<p>All the commands we enter in the command line to send an email we know from every email client program like Thunderbird, Gmail, Outlook, and many others. We specify the <code>subject</code>, to whom the email should go, CC, BCC, and the information we want to share with others. Of course, the same works from the command line.</p>
<h4>Send an Email</h4>
<pre><code class="language-shell-session">[!bash!]$ telnet 10.129.14.128 25

Trying 10.129.14.128...
Connected to 10.129.14.128.
Escape character is '^]'.
220 ESMTP Server


EHLO inlanefreight.htb

250-mail1.inlanefreight.htb
250-PIPELINING
250-SIZE 10240000
250-ETRN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250-DSN
250-SMTPUTF8
250 CHUNKING


MAIL FROM: &lt;<a class="__cf_email__" data-cfemail="91f2e3e8a1fda0e5a2d1f8fffdf0fff4f7e3f4f8f6f9e5bff9e5f3" href="/cdn-cgi/l/email-protection">[email protected]</a>&gt;

250 2.1.0 Ok


RCPT TO: &lt;<a class="__cf_email__" data-cfemail="ed809f8fde83ad8483818c83888b9f88848a8599c385998f" href="/cdn-cgi/l/email-protection">[email protected]</a>&gt; NOTIFY=success,failure

250 2.1.5 Ok


DATA

354 End data with &lt;CR&gt;&lt;LF&gt;.&lt;CR&gt;&lt;LF&gt;

From: &lt;<a class="__cf_email__" data-cfemail="7e1d0c074e124f0a4d3e1710121f101b180c1b1719160a50160a1c" href="/cdn-cgi/l/email-protection">[email protected]</a>&gt;
To: &lt;<a class="__cf_email__" data-cfemail="f5988797c69bb59c9b99949b909387909c929d81db9d8197" href="/cdn-cgi/l/email-protection">[email protected]</a>&gt;
Subject: DB
Date: Tue, 28 Sept 2021 16:32:51 +0200
Hey man, I am trying to access our XY-DB but the creds don't work. 
Did you make any changes there?
.

250 2.0.0 Ok: queued as 6E1CF1681AB


QUIT

221 2.0.0 Bye
Connection closed by foreign host.
</code></pre>
<p>The mail header is the carrier of a large amount of interesting information in an email. Among other things, it provides information about the sender and recipient, the time of sending and arrival, the stations the email passed on its way, the content and format of the message, and the sender and recipient.</p>
<p>Some of this information is mandatory, such as sender information and when the email was created. Other information is optional. However, the email header does not contain any information necessary for technical delivery. It is transmitted as part of the transmission protocol. Both sender and recipient can access the header of an email, although it is not visible at first glance. The structure of an email header is defined by <a href="https://datatracker.ietf.org/doc/html/rfc5322">RFC5322</a>.</p>
<hr/>
<h2>Dangerous Settings</h2>
<p>To prevent the sent emails from being filtered by spam filters and not reaching the recipient, the sender can use a relay server that the recipient trusts. It is an SMTP server that is known and verified by all others. As a rule, the sender must authenticate himself to the relay server before using it.</p>
<p>Often, administrators have no overview of which IP ranges they have to allow. This results in a misconfiguration of the SMTP server that we will still often find in external and internal penetration tests. Therefore, they allow all IP addresses not to cause errors in the email traffic and thus not to disturb or unintentionally interrupt the communication with potential and current customers.</p>
<h4>Open Relay Configuration</h4>
<pre><code class="language-shell-session">mynetworks = 0.0.0.0/0
</code></pre>
<p>With this setting, this SMTP server can send fake emails and thus initialize communication between multiple parties. Another attack possibility would be to spoof the email and read it.</p>
<hr/>
<h2>Footprinting the Service</h2>
<p>The default Nmap scripts include <code>smtp-commands</code>, which uses the <code>EHLO</code> command to list all possible commands that can be executed on the target SMTP server.</p>
<h4>Nmap</h4>
<pre><code class="language-shell-session">[!bash!]$ sudo nmap 10.129.14.128 -sC -sV -p25

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-27 17:56 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00025s latency).

PORT   STATE SERVICE VERSION
25/tcp open  smtp    Postfix smtpd
|_smtp-commands: mail1.inlanefreight.htb, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING, 
MAC Address: 00:00:00:00:00:00 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.09 seconds
</code></pre>
<p>However, we can also use the <a href="https://nmap.org/nsedoc/scripts/smtp-open-relay.html">smtp-open-relay</a> NSE script to identify the target SMTP server as an open relay using 16 different tests. If we also print out the output of the scan in detail, we will also be able to see which tests the script is running.</p>
<h4>Nmap - Open Relay</h4>
<pre><code class="language-shell-session">[!bash!]$ sudo nmap 10.129.14.128 -p25 --script smtp-open-relay -v

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-30 02:29 CEST
NSE: Loaded 1 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 02:29
Completed NSE at 02:29, 0.00s elapsed
Initiating ARP Ping Scan at 02:29
Scanning 10.129.14.128 [1 port]
Completed ARP Ping Scan at 02:29, 0.06s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 02:29
Completed Parallel DNS resolution of 1 host. at 02:29, 0.03s elapsed
Initiating SYN Stealth Scan at 02:29
Scanning 10.129.14.128 [1 port]
Discovered open port 25/tcp on 10.129.14.128
Completed SYN Stealth Scan at 02:29, 0.06s elapsed (1 total ports)
NSE: Script scanning 10.129.14.128.
Initiating NSE at 02:29
Completed NSE at 02:29, 0.07s elapsed
Nmap scan report for 10.129.14.128
Host is up (0.00020s latency).

PORT   STATE SERVICE
25/tcp open  smtp
| smtp-open-relay: Server is an open relay (16/16 tests)
|  MAIL FROM:&lt;&gt; -&gt; RCPT TO:&lt;<a class="__cf_email__" data-cfemail="dcaeb9b0bda5a8b9afa89cb2b1bdacf2afbfbdb2b1b9f2b3aebb" href="/cdn-cgi/l/email-protection">[email protected]</a>&gt;
|  MAIL FROM:&lt;<a class="__cf_email__" data-cfemail="fc9d9288958f8c9d91bc92919d8cd28f9f9d929199d2938e9b" href="/cdn-cgi/l/email-protection">[email protected]</a>&gt; -&gt; RCPT TO:&lt;<a class="__cf_email__" data-cfemail="b1c3d4ddd0c8c5d4c2c5f1dfdcd0c19fc2d2d0dfdcd49fdec3d6" href="/cdn-cgi/l/email-protection">[email protected]</a>&gt;
|  MAIL FROM:&lt;antispam@ESMTP&gt; -&gt; RCPT TO:&lt;<a class="__cf_email__" data-cfemail="cab8afa6abb3beafb9be8aa4a7abbae4b9a9aba4a7afe4a5b8ad" href="/cdn-cgi/l/email-protection">[email protected]</a>&gt;
|  MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;<a class="__cf_email__" data-cfemail="5c2e39303d2528392f281c32313d2c722f3f3d32313972332e3b" href="/cdn-cgi/l/email-protection">[email protected]</a>&gt;
|  MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;relaytest%nmap.scanme.org@[10.129.14.128]&gt;
|  MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;relaytest%nmap.scanme.org@ESMTP&gt;
|  MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;"<a class="__cf_email__" data-cfemail="7c0e19101d0508190f083c12111d0c520f1f1d12111952130e1b" href="/cdn-cgi/l/email-protection">[email protected]</a>"&gt;
|  MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;"relaytest%nmap.scanme.org"&gt;
|  MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;<a class="__cf_email__" data-cfemail="65170009041c11001611250b0804154b1606040b08004b0a1702" href="/cdn-cgi/l/email-protection">[email protected]</a>@[10.129.14.128]&gt;
|  MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;"<a class="__cf_email__" data-cfemail="e89a8d8489919c8d9b9ca886858998c69b8b8986858dc6879a8f" href="/cdn-cgi/l/email-protection">[email protected]</a>"@[10.129.14.128]&gt;
|  MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;<a class="__cf_email__" data-cfemail="b1c3d4ddd0c8c5d4c2c5f1dfdcd0c19fc2d2d0dfdcd49fdec3d6" href="/cdn-cgi/l/email-protection">[email protected]</a>@ESMTP&gt;
|  MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;@[10.129.14.128]:<a class="__cf_email__" data-cfemail="9be9fef7fae2effee8efdbf5f6faebb5e8f8faf5f6feb5f4e9fc" href="/cdn-cgi/l/email-protection">[email protected]</a>&gt;
|  MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;@ESMTP:<a class="__cf_email__" data-cfemail="7705121b160e0312040337191a160759041416191a1259180510" href="/cdn-cgi/l/email-protection">[email protected]</a>&gt;
|  MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;nmap.scanme.org!relaytest&gt;
|  MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;nmap.scanme.org!relaytest@[10.129.14.128]&gt;
|_ MAIL FROM:&lt;antispam@[10.129.14.128]&gt; -&gt; RCPT TO:&lt;nmap.scanme.org!relaytest@ESMTP&gt;
MAC Address: 00:00:00:00:00:00 (VMware)

NSE: Script Post-scanning.
Initiating NSE at 02:29
Completed NSE at 02:29, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.48 seconds
           Raw packets sent: 2 (72B) | Rcvd: 2 (72B)
</code></pre>
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
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 4 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="32" value="13">US Academy 4</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 1 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="33" value="4">US Academy 1</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 2 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="33" value="5">US Academy 2</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 5 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt; &lt;span class='recommended'&gt; &lt;img src='/images/sparkles-solid.svg'/&gt;Recommended&lt;/span&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="37" value="12">EU Academy 5</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 3 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="38" value="9">US Academy 3</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 2 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="39" selected="" value="2">EU Academy 2</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 1 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="40" value="1">EU Academy 1</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 3 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="41" value="14">EU Academy 3</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 4 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="43" value="11">EU Academy 4</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 6 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="47" value="15">EU Academy 6</option>
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
<label class="module-question" for="923"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Enumerate the SMTP service and submit the banner, including its version as the answer.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer923" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-923">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="923" id="btnAnswer923">
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
<label class="module-question" for="924"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Enumerate the SMTP service even further and find the username that exists on the system. Submit it as the answer.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer924" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-924">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="924" id="btnAnswer924">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint924" data-toggle="modal" id="hintBtn924"><i class="fad fa-life-ring mr-2"></i> Hint
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
