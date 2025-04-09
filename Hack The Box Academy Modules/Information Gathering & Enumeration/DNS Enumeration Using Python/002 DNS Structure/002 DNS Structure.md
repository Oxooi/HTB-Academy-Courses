
<h1>DNS Structure</h1>
<hr/>
<p>Another significant source of information for us is the Domain Name System (DNS). DNS is also known as the "phone book of the Internet." Like searching a phone book for a name to get the phone number, DNS looks for a computer name (domain name) to get its IP address. The IP address is needed to connect to a server where only the computer name is known. The system makes it easier for the end-user to reach a web server or a host. DNS is generally used to resolve computer names into IP addresses and reversed them. The components of a DNS service consist of:</p>
<ul>
<li>
<code>Name servers</code>
</li>
<li>
<code>Zones</code>
</li>
<li>
<code>Domain names</code>
</li>
<li>
<code>IP addresses</code>
</li>
</ul>
<p>The name servers contain so-called <code>zones</code> or <code>zone files</code>. In simple terms, zone files are lists of entries for the corresponding domain. We can think of it like a telephone book for a specific city. These zone files contain <code>IP addresses</code> to the specific <code>domains</code> and <code>hosts</code>. Such a zone file exists on every system, whether Linux or Windows and is called the "hosts" file. We can find them on the Pwnbox under "<code>/etc/hosts</code>." This file is our local zone file.</p>
<hr/>
<h2>Domain Structure</h2>
<p>Let us take the following fully qualified domain name (<code>FQDN</code>) as an example:</p>
<ul>
<li>
<code>www.domain-A.com</code>
</li>
</ul>
<p>A domain is used to give real names to computer's IP addresses and, at the same time, to divide them into a hierarchical structure. This hierarchical structure looks like a directory tree of an operating system.</p>
<pre><code class="language-shell-session">.
├── com.
│   ├── domain-A.
│   │   ├── blog.
│   │   ├── ns1.
│   │   └── www.
│   │ 
│   ├── domain-B.
│   │   └── ...
│   └── domain-C.
│       └── ...
│
└── net.
│   ├── domain-D.
│   │   └── ...
│   ├── domain-E.
│   │   └── ...
│   └── domain-F.
│       └── ...
└── ...
│   ├── ...
│   └── ...
</code></pre>
<p>To make it a bit clearer, let us look at a real example of how such a structure can look like the appropriate naming.</p>
<p><img alt="Domain hierarchy diagram: Root, Top Level Domains (net, org, com, dev, io), Second Level Domain (inlanefreight.com), Sub-Domains (dev, www, mail), Host (WS01.dev)." src="https://academy.hackthebox.com/storage/modules/27/tooldev-dns.png"/></p>
<hr/>
<p>Each domain consists of at least two parts:</p>
<ol>
<li>
<code>Top-Level Domain</code> (<code>TLD</code>)</li>
<li>
<code>Domain Name</code>
</li>
</ol>
<p>From the last example, the domain name would be "<code>inlanefreight</code>" and the TLD then "<code>com</code>". If we look at the "<code>inlanefreight</code>," we see that it contains some so-called <code>subdomains</code> (<code>dev</code>, <code>www</code>, <code>mail</code>). These subdomains can represent a single host or virtual hosts (<code>vHosts</code>). The DNS servers are divided into four different types:</p>
<ul>
<li>
<code>Recursive resolvers</code> (<code>DNS Recursor</code>)</li>
<li>
<code>Root name server</code>
</li>
<li>
<code>TLD name server</code>
</li>
<li>
<code>Authoritative name servers</code>
</li>
</ul>
<hr/>
<h2>Recursive DNS Resolver</h2>
<p>The recursive resolver acts as an agent between the client and the name server. After the recursive resolver receives a DNS query from a web client, it responds to this query with cached data, or it sends a query to a root name server, followed by a query to a TLD name server and finally a final query to an authoritative name server. Once it has received a response from the authoritative name server with the requested IP address, the recursive resolver sends the client's response.</p>
<p>During this process, the recursive resolver stores the received information from authoritative name servers in its cache. When a client requests the IP address of a domain name that was recently requested by another client, the resolver can skip communication with the name servers and retrieve the requested entry from its cache and send it to the client.</p>
<hr/>
<h2>Root Name Server</h2>
<p>Thirteen root name servers can be reached under IPv4 and IPv6 addresses. An international non-profit organization maintains these root name servers called the Internet Corporation for Assigned Names and Numbers (<code>ICANN</code>). The zone files of these contain all domain names and IP addresses of the TLDs. Every recursive resolver knows these 13 root name servers. These are the first stations in the search for DNS entries for each recursive resolver. Each of these root name servers accepts a recursive resolver query that contains a domain name. The domains' extension answers the query and forwards the recursive resolver to the corresponding TLD name server. We find the 13 root name servers on the domain <code>root-servers.net</code> with the corresponding letter as a subdomain.</p>
<pre><code class="language-shell-session">[!bash!]$ dig ns root-servers.net | grep NS | sort -u                                                                          

; EDNS: version: 0, flags:; udp: 4096
;; ANSWER SECTION:
;; flags: qr rd ra; QUERY: 1, ANSWER: 13, AUTHORITY: 0, ADDITIONAL: 1
;root-servers.net.		IN	NS
root-servers.net.	6882	IN	NS	a.root-servers.net.
root-servers.net.	6882	IN	NS	b.root-servers.net.
root-servers.net.	6882	IN	NS	c.root-servers.net.
root-servers.net.	6882	IN	NS	d.root-servers.net.
root-servers.net.	6882	IN	NS	e.root-servers.net.
root-servers.net.	6882	IN	NS	f.root-servers.net.
root-servers.net.	6882	IN	NS	g.root-servers.net.
root-servers.net.	6882	IN	NS	h.root-servers.net.
root-servers.net.	6882	IN	NS	i.root-servers.net.
root-servers.net.	6882	IN	NS	j.root-servers.net.
root-servers.net.	6882	IN	NS	k.root-servers.net.
root-servers.net.	6882	IN	NS	l.root-servers.net.
root-servers.net.	6882	IN	NS	m.root-servers.net.
</code></pre>
<p>These 13 root name servers represent the 13 different types of root name servers. It does not mean that it only spread over 13 hosts, but over 600 copies of these root name servers worldwide.</p>
<hr/>
<h2>TLD Name Server</h2>
<p>A TLD name server manages the information on all domain names that have the same TLD. These TLD name servers are the responsibility of the Internet Assigned Numbers Authority (<code>IANA</code>) and are managed by it. This means that all domains under the TLD "<code>.com</code>" are managed by the corresponding TLD name server. When we look for a domain registered under this TLD, the recursive resolver, after receiving a response from a root name server, sends a query to a TLD name server responsible for that TLD.</p>
<hr/>
<h2>Authoritative Name Server</h2>
<p>Authoritative name servers store DNS record information for domains. These servers are responsible for providing answers to requests from name servers with the IP address and other DNS entries for a web page so the web page can be addressed and accessed by the client. When a recursive resolver receives a TLD name server response, the response refers it to an authoritative name server. The authoritative name server is the last step to get an IP address.</p>
