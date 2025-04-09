
<h1>Domain Information</h1>
<hr/>
<p>Domain information is a core component of any penetration test, and it is not just about the subdomains but about the entire presence on the Internet. Therefore, we gather information and try to understand the company's functionality and which technologies and structures are necessary for services to be offered successfully and efficiently.</p>
<p>This type of information is gathered passively without direct and active scans. In other words, we remain hidden and navigate as "customers" or "visitors" to avoid direct connections to the company that could expose us. The OSINT relevant sections are only a tiny part of how in-depth OSINT goes and describe only a few of the many ways to obtain information in this way. More approaches and strategies for this can be found in the module <a href="https://academy.hackthebox.com/course/preview/osint-corporate-recon">OSINT: Corporate Recon</a>.</p>
<p>However, when <code>passively</code> gathering information, we can use third-party services to understand the company better. However, the first thing we should do is scrutinize the company's <code>main website</code>. Then, we should read through the texts, keeping in mind what technologies and structures are needed for these services.</p>
<p>For example, many IT companies offer app development, IoT, hosting, data science, and IT security services, depending on their industry. If we encounter a service that we have had little to do with before, it makes sense and is necessary to get to grips with it and find out what activities it consists of and what opportunities are available. Those services also give us a good overview of how the company can be structured.</p>
<p>For example, this part is the combination between the <code>first principle</code> and the <code>second principle</code> of enumeration. We pay attention to what <code>we see</code> and <code>we do not see</code>. We see the services but not their functionality. However, services are bound to certain technical aspects necessary to provide a service. Therefore, we take the developer's view and look at the whole thing from their point of view. This point of view allows us to gain many technical insights into the functionality.</p>
<hr/>
<h2>Online Presence</h2>
<p>Once we have a basic understanding of the company and its services, we can get a first impression of its presence on the Internet. Let us assume that a medium-sized company has hired us to test their entire infrastructure from a black-box perspective. This means we have only received a scope of targets and must obtain all further information ourselves.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: Please remember that the examples below will differ from the practical exercises and will not give the same results. However, the examples are based on real penetration tests and illustrate how and what information can be obtained.</p>
</div>
</div>
<p>The first point of presence on the Internet may be the <code>SSL certificate</code> from the company's main website that we can examine. Often, such a certificate includes more than just a subdomain, and this means that the certificate is used for several domains, and these are most likely still active.</p>
<p><img alt="Certificate validity from May 18, 2021, to April 6, 2022, with DNS names: inlanefreight.htb, www.inlanefreight.htb, support.inlanefreight.htb." src="https://academy.hackthebox.com/storage/modules/112/DomInfo-1.png"/></p>
<p>Another source to find more subdomains is <a href="https://crt.sh/">crt.sh</a>. This source is <a href="https://en.wikipedia.org/wiki/Certificate_Transparency">Certificate Transparency</a> logs. Certificate Transparency is a process that is intended to enable the verification of issued digital certificates for encrypted Internet connections. The standard (<a href="https://tools.ietf.org/html/rfc6962">RFC 6962</a>) provides for the logging of all digital certificates issued by a certificate authority in audit-proof logs. This is intended to enable the detection of false or maliciously issued certificates for a domain. SSL certificate providers like <a href="https://letsencrypt.org/">Let's Encrypt</a> share this with the web interface <a href="https://crt.sh/">crt.sh</a>, which stores the new entries in the database to be accessed later.</p>
<img alt="crt.sh search results for 'inlanefreight.com' showing certificates with common names like matomo.inlanefreight.com, smartfactory.inlanefreight.com, and issuer names including Let's Encrypt and Cloudflare." class="website-screenshot" data-url="https://www.crt.sh/?q=inlanefreight.com" src="/storage/modules/112/DomInfo-2.png"/>
<p>We can also output the results in JSON format.</p>
<h4>Certificate Transparency</h4>
<pre><code class="language-shell-session">[!bash!]$ curl -s https://crt.sh/\?q\=inlanefreight.com\&amp;output\=json | jq .

[
  {
    "issuer_ca_id": 23451835427,
    "issuer_name": "C=US, O=Let's Encrypt, CN=R3",
    "common_name": "matomo.inlanefreight.com",
    "name_value": "matomo.inlanefreight.com",
    "id": 50815783237226155,
    "entry_timestamp": "2021-08-21T06:00:17.173",
    "not_before": "2021-08-21T05:00:16",
    "not_after": "2021-11-19T05:00:15",
    "serial_number": "03abe9017d6de5eda90"
  },
  {
    "issuer_ca_id": 6864563267,
    "issuer_name": "C=US, O=Let's Encrypt, CN=R3",
    "common_name": "matomo.inlanefreight.com",
    "name_value": "matomo.inlanefreight.com",
    "id": 5081529377,
    "entry_timestamp": "2021-08-21T06:00:16.932",
    "not_before": "2021-08-21T05:00:16",
    "not_after": "2021-11-19T05:00:15",
    "serial_number": "03abe90104e271c98a90"
  },
  {
    "issuer_ca_id": 113123452,
    "issuer_name": "C=US, O=Let's Encrypt, CN=R3",
    "common_name": "smartfactory.inlanefreight.com",
    "name_value": "smartfactory.inlanefreight.com",
    "id": 4941235512141012357,
    "entry_timestamp": "2021-07-27T00:32:48.071",
    "not_before": "2021-07-26T23:32:47",
    "not_after": "2021-10-24T23:32:45",
    "serial_number": "044bac5fcc4d59329ecbbe9043dd9d5d0878"
  },
  { ... SNIP ...
</code></pre>
<p>If needed, we can also have them filtered by the unique subdomains.</p>
<pre><code class="language-shell-session">[!bash!]$ curl -s https://crt.sh/\?q\=inlanefreight.com\&amp;output\=json | jq . | grep name | cut -d":" -f2 | grep -v "CN=" | cut -d'"' -f2 | awk '{gsub(/\\n/,"\n");}1;' | sort -u

account.ttn.inlanefreight.com
blog.inlanefreight.com
bots.inlanefreight.com
console.ttn.inlanefreight.com
ct.inlanefreight.com
data.ttn.inlanefreight.com
*.inlanefreight.com
inlanefreight.com
integrations.ttn.inlanefreight.com
iot.inlanefreight.com
mails.inlanefreight.com
marina.inlanefreight.com
marina-live.inlanefreight.com
matomo.inlanefreight.com
next.inlanefreight.com
noc.ttn.inlanefreight.com
preview.inlanefreight.com
shop.inlanefreight.com
smartfactory.inlanefreight.com
ttn.inlanefreight.com
vx.inlanefreight.com
www.inlanefreight.com
</code></pre>
<p>Next, we can identify the hosts directly accessible from the Internet and not hosted by third-party providers. This is because we are not allowed to test the hosts without the permission of third-party providers.</p>
<h4>Company Hosted Servers</h4>
<pre><code class="language-shell-session">[!bash!]$ for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f1,4;done

blog.inlanefreight.com 10.129.24.93
inlanefreight.com 10.129.27.33
matomo.inlanefreight.com 10.129.127.22
www.inlanefreight.com 10.129.127.33
s3-website-us-west-2.amazonaws.com 10.129.95.250
</code></pre>
<p>Once we see which hosts can be investigated further, we can generate a list of IP addresses with a minor adjustment to the <code>cut</code> command and run them through <code>Shodan</code>.</p>
<p><a href="https://www.shodan.io/">Shodan</a> can be used to find devices and systems permanently connected to the Internet like <code>Internet of Things</code> (<code>IoT</code>). It searches the Internet for open TCP/IP ports and filters the systems according to specific terms and criteria. For example, open HTTP or HTTPS ports and other server ports for <code>FTP</code>, <code>SSH</code>, <code>SNMP</code>, <code>Telnet</code>, <code>RTSP</code>, or <code>SIP</code> are searched. As a result, we can find devices and systems, such as <code>surveillance cameras</code>, <code>servers</code>, <code>smart home systems</code>, <code>industrial controllers</code>, <code>traffic lights</code> and <code>traffic controllers</code>, and various network components.</p>
<h4>Shodan - IP List</h4>
<pre><code class="language-shell-session">[!bash!]$ for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f4 &gt;&gt; ip-addresses.txt;done
[!bash!]$ for i in $(cat ip-addresses.txt);do shodan host $i;done

10.129.24.93
City:                    Berlin
Country:                 Germany
Organization:            InlaneFreight
Updated:                 2021-09-01T09:02:11.370085
Number of open ports:    2

Ports:
     80/tcp nginx 
    443/tcp nginx 
	
10.129.27.33
City:                    Berlin
Country:                 Germany
Organization:            InlaneFreight
Updated:                 2021-08-30T22:25:31.572717
Number of open ports:    3

Ports:
     22/tcp OpenSSH (7.6p1 Ubuntu-4ubuntu0.3)
     80/tcp nginx 
    443/tcp nginx 
        |-- SSL Versions: -SSLv2, -SSLv3, -TLSv1, -TLSv1.1, -TLSv1.3, TLSv1.2
        |-- Diffie-Hellman Parameters:
                Bits:          2048
                Generator:     2
				
10.129.27.22
City:                    Berlin
Country:                 Germany
Organization:            InlaneFreight
Updated:                 2021-09-01T15:39:55.446281
Number of open ports:    8

Ports:
     25/tcp  
        |-- SSL Versions: -SSLv2, -SSLv3, -TLSv1, -TLSv1.1, TLSv1.2, TLSv1.3
     53/tcp  
     53/udp  
     80/tcp Apache httpd 
     81/tcp Apache httpd 
    110/tcp  
        |-- SSL Versions: -SSLv2, -SSLv3, -TLSv1, -TLSv1.1, TLSv1.2
    111/tcp  
    443/tcp Apache httpd 
        |-- SSL Versions: -SSLv2, -SSLv3, -TLSv1, -TLSv1.1, TLSv1.2, TLSv1.3
        |-- Diffie-Hellman Parameters:
                Bits:          2048
                Generator:     2
                Fingerprint:   RFC3526/Oakley Group 14
    444/tcp  
		
10.129.27.33
City:                    Berlin
Country:                 Germany
Organization:            InlaneFreight
Updated:                 2021-08-30T22:25:31.572717
Number of open ports:    3

Ports:
     22/tcp OpenSSH (7.6p1 Ubuntu-4ubuntu0.3)
     80/tcp nginx 
    443/tcp nginx 
        |-- SSL Versions: -SSLv2, -SSLv3, -TLSv1, -TLSv1.1, -TLSv1.3, TLSv1.2
        |-- Diffie-Hellman Parameters:
                Bits:          2048
                Generator:     2
</code></pre>
<p>We remember the IP <code>10.129.127.22</code> (<code>matomo.inlanefreight.com</code>) for later active investigations we want to perform. Now, we can display all the available DNS records where we might find more hosts.</p>
<h4>DNS Records</h4>
<pre><code class="language-shell-session">[!bash!]$ dig any inlanefreight.com

; &lt;&lt;&gt;&gt; DiG 9.16.1-Ubuntu &lt;&lt;&gt;&gt; any inlanefreight.com
;; global options: +cmd
;; Got answer:
;; -&gt;&gt;HEADER&lt;&lt;- opcode: QUERY, status: NOERROR, id: 52058
;; flags: qr rd ra; QUERY: 1, ANSWER: 17, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;inlanefreight.com.             IN      ANY

;; ANSWER SECTION:
inlanefreight.com.      300     IN      A       10.129.27.33
inlanefreight.com.      300     IN      A       10.129.95.250
inlanefreight.com.      3600    IN      MX      1 aspmx.l.google.com.
inlanefreight.com.      3600    IN      MX      10 aspmx2.googlemail.com.
inlanefreight.com.      3600    IN      MX      10 aspmx3.googlemail.com.
inlanefreight.com.      3600    IN      MX      5 alt1.aspmx.l.google.com.
inlanefreight.com.      3600    IN      MX      5 alt2.aspmx.l.google.com.
inlanefreight.com.      21600   IN      NS      ns.inwx.net.
inlanefreight.com.      21600   IN      NS      ns2.inwx.net.
inlanefreight.com.      21600   IN      NS      ns3.inwx.eu.
inlanefreight.com.      3600    IN      TXT     "MS=ms92346782372"
inlanefreight.com.      21600   IN      TXT     "atlassian-domain-verification=IJdXMt1rKCy68JFszSdCKVpwPN"
inlanefreight.com.      3600    IN      TXT     "google-site-verification=O7zV5-xFh_jn7JQ31"
inlanefreight.com.      300     IN      TXT     "google-site-verification=bow47-er9LdgoUeah"
inlanefreight.com.      3600    IN      TXT     "google-site-verification=gZsCG-BINLopf4hr2"
inlanefreight.com.      3600    IN      TXT     "logmein-verification-code=87123gff5a479e-61d4325gddkbvc1-b2bnfghfsed1-3c789427sdjirew63fc"
inlanefreight.com.      300     IN      TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.24.8 ip4:10.129.27.2 ip4:10.72.82.106 ~all"
inlanefreight.com.      21600   IN      SOA     ns.inwx.net. hostmaster.inwx.net. 2021072600 10800 3600 604800 3600

;; Query time: 332 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
;; WHEN: Mi Sep 01 18:27:22 CEST 2021
;; MSG SIZE  rcvd: 940
</code></pre>
<p>Let us look at what we have learned here and come back to our principles. We see an IP record, some mail servers, some DNS servers, TXT records, and an SOA record.</p>
<ul>
<li>
<p><code>A</code> records: We recognize the IP addresses that point to a specific (sub)domain through the A record. Here we only see one that we already know.</p>
</li>
<li>
<p><code>MX</code> records: The mail server records show us which mail server is responsible for managing the emails for the company. Since this is handled by google in our case, we should note this and skip it for now.</p>
</li>
<li>
<p><code>NS</code> records: These kinds of records show which name servers are used to resolve the FQDN to IP addresses. Most hosting providers use their own name servers, making it easier to identify the hosting provider.</p>
</li>
<li>
<p><code>TXT</code> records: this type of record often contains verification keys for different third-party providers and other security aspects of DNS, such as <a href="https://datatracker.ietf.org/doc/html/rfc7208">SPF</a>, <a href="https://datatracker.ietf.org/doc/html/rfc7489">DMARC</a>, and <a href="https://datatracker.ietf.org/doc/html/rfc6376">DKIM</a>, which are responsible for verifying and confirming the origin of the emails sent. Here we can already see some valuable information if we look closer at the results.</p>
</li>
</ul>
<pre><code class="language-shell-session">...SNIP... TXT     "MS=ms92346782372"
...SNIP... TXT     "atlassian-domain-verification=IJdXMt1rKCy68JFszSdCKVpwPN"
...SNIP... TXT     "google-site-verification=O7zV5-xFh_jn7JQ31"
...SNIP... TXT     "google-site-verification=bow47-er9LdgoUeah"
...SNIP... TXT     "google-site-verification=gZsCG-BINLopf4hr2"
...SNIP... TXT     "logmein-verification-code=87123gff5a479e-61d4325gddkbvc1-b2bnfghfsed1-3c789427sdjirew63fc"
...SNIP... TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.24.8 ip4:10.129.27.2 ip4:10.72.82.106 ~all"
</code></pre>
<p>What we could see so far were entries on the DNS server, which at first glance did not look very interesting (except for the additional IP addresses). However, we could not see the third-party providers behind the entries shown at first glance. The core information we can see now is:</p>
<table>
<thead>
<tr>
<th></th>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="https://www.atlassian.com/">Atlassian</a></td>
<td><a href="https://www.google.com/gmail/">Google Gmail</a></td>
<td><a href="https://www.logmein.com/">LogMeIn</a></td>
</tr>
<tr>
<td><a href="https://www.mailgun.com/">Mailgun</a></td>
<td><a href="https://outlook.live.com/owa/">Outlook</a></td>
<td><a href="https://www.inwx.com/en">INWX</a> ID/Username</td>
</tr>
<tr>
<td>10.129.24.8</td>
<td>10.129.27.2</td>
<td>10.72.82.106</td>
</tr>
</tbody>
</table>
<p>For example, <a href="https://www.atlassian.com/">Atlassian</a> states that the company uses this solution for software development and collaboration. If we are not familiar with this platform, we can try it for free to get acquainted with it.</p>
<p><a href="https://www.google.com/gmail/">Google Gmail</a> indicates that Google is used for email management. Therefore, it can also suggest that we could access open GDrive folders or files with a link.</p>
<p><a href="https://www.logmein.com/">LogMeIn</a> is a central place that regulates and manages remote access on many different levels. However, the centralization of such operations is a double-edged sword. If access as an administrator to this platform is obtained (e.g., through password reuse), one also has complete access to all systems and information.</p>
<p><a href="https://www.mailgun.com/">Mailgun</a> offers several email APIs, SMTP relays, and webhooks with which emails can be managed. This tells us to keep our eyes open for API interfaces that we can then test for various vulnerabilities such as IDOR, SSRF, POST, PUT requests, and many other attacks.</p>
<p><a href="https://outlook.live.com/owa/">Outlook</a> is another indicator for document management. Companies often use Office 365 with OneDrive and cloud resources such as Azure blob and file storage. Azure file storage can be very interesting because it works with the SMB protocol.</p>
<p>The last thing we see is <a href="https://www.inwx.com/en">INWX</a>. This company seems to be a hosting provider where domains can be purchased and registered. The TXT record with the "MS" value is often used to confirm the domain. In most cases, it is similar to the username or ID used to log in to the management platform.</p>
