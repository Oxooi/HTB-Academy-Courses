
<h1>Information Gathering</h1>
<hr/>
<p>Once the pre-engagement phase has been completed, and all parties have signed all contractual terms and conditions, the <code>information gathering</code> phase begins. Information gathering is an essential part of any security assessment. This is the phase in which we gather all available information about the company, its employees and infrastructure, and how they are organized. Information gathering is the most frequent and vital phase throughout the penetration testing process, to which we will return again and again.</p>
<p><img alt="Penetration testing process: Pre-Engagement, Information Gathering, Vulnerability Assessment, Exploitation, Post-Exploitation, Lateral Movement, Proof-of-Concept, Post-Engagement." src="https://academy.hackthebox.com/storage/modules/90/0-PT-Process-IG.png"/></p>
<p>All the steps we take to exploit the vulnerabilities are based on the information we enumerate about our targets. This phase can be considered the cornerstone of any penetration test. We can obtain the necessary information relevant to us in many different ways. However, we can divide them into the following categories:</p>
<ul>
<li>Open-Source Intelligence</li>
<li>Infrastructure Enumeration</li>
<li>Service Enumeration</li>
<li>Host Enumeration</li>
</ul>
<p>All four categories should and must be performed by us for each penetration test. This is because the <code>information</code> is the main component that leads us to successful penetration testing and identifying security vulnerabilities. We can get this information anywhere, whether on social media, job postings, individual hosts and servers, or even the employees. Information is continually being spread and shared everywhere.</p>
<p>After all, we humans communicate by exchanging information, but network components and services communicate similarly. Any exchange of information always has a specific purpose. For computer networks, the aim is always to trigger a particular process. Be it storing data in a database, registering, generating specific values, or forwarding the information.</p>
<hr/>
<h2>Open-Source Intelligence</h2>
<p>Let's assume that our client wants us to see what information we can find about his company on the internet. For this purpose, we use what is known as <code>Open Source Intelligence</code> (<code>OSINT</code>). OSINT is a process for finding publicly available information on a target company or individuals that allows the identification of events (i.e., public and private meetings), external and internal dependencies, and connections. OSINT uses public (Open-Source) information from freely available sources to obtain the desired results. We can often find security-relevant and sensitive information from companies and their employees. Usually, the people who share such information are unaware that they are not the only ones who can access it.</p>
<p>It is possible to find highly sensitive information such as passwords, hashes, keys, tokens, and much more that can give us access to the network within just a few minutes. Repositories on sites like <a href="https://github.com/">Github</a> or other development platforms are often not set up correctly, and external viewers can see this information. If this type of sensitive information is found at the onset of testing, the Incident Handling and Report section of the RoE should describe the procedure for reporting these types of critical security vulnerabilities. Publicly published passwords or SSH keys represent a critical security gap if they have not already been removed or changed. Therefore, our client's administrator must review this information before we proceed.</p>
<h4>Private and Public SSH Keys</h4>
<p><img alt="Searchcode page showing code snippet with redacted OpenSSH private and public keys." src="https://academy.hackthebox.com/storage/modules/90/searchcode3.png"/></p>
<p>Developers often share whole sections of code on <a href="https://stackoverflow.com/">StackOverflow</a> to show other developers a better overview of how their code works to help them solve their problems. This type of information can also be found very quickly and used against the company. Our task is to find such security holes and have them closed. We can learn much more from the <a href="https://academy.hackthebox.com/course/preview/osint-corporate-recon">OSINT: Corporate Recon</a> module. It shows many different techniques for how we can find such information.</p>
<hr/>
<h2>Infrastructure Enumeration</h2>
<p>During the infrastructure enumeration, we try to overview the company's position on the internet and intranet. For this, we use OSINT and the first active scans. We use services such as DNS to create a map of the client's servers and hosts and develop an understanding of how their <code>infrastructure</code> is structured. This includes name servers, mail servers, web servers, cloud instances, and more. We make an accurate list of hosts and their IP addresses and compare them to our scope to see if they are included and listed.</p>
<p>In this phase, we also try to determine the company's security measures. The more precise this information is, the easier it will be to disguise our attacks (<code>Evasive Testing</code>). But identifying firewalls, such as web application firewalls, also gives us an excellent understanding of what techniques could trigger an alarm for our customer and what methods can be used to avoid that alarm.</p>
<p>Here, it also does not matter "where" we are positioned, whether we are trying to gain an overview of the infrastructure from the outside (<code>external</code>) or examining the infrastructure from the inside (<code>internal</code>) of the network. Enumeration from inside the network gives us a good overview of the hosts and servers that we can use as targets for a <code>Password Spraying</code> attack, in which we use one password to attempt to authenticate with as many different user names as possible, hoping for one successful authentication attempt to grant us a foothold in the network. All these methods and techniques used for this purpose will be looked at in more detail in the individual modules.</p>
<hr/>
<h2>Service Enumeration</h2>
<p>In service enumeration, we identify services that allow us to interact with the host or server over the network (or locally, from an internal perspective). Therefore, it is crucial to find out about the service, what <code>version</code> it is, what <code>information</code> it provides us, and the <code>reason</code> it can be used. Once we understand the background of what this service has been provisioned for, some logical conclusions can be drawn to provide us with several options.</p>
<p>Many services have a version history that allows us to identify whether the installed version on the host or server is actually up to date or not. This will also help us find security vulnerabilities that remain with older versions in most cases. Many administrators are afraid to change applications that work, as it could harm the entire infrastructure. Therefore, administrators often prefer to accept the risk of leaving one or more vulnerabilities open and maintaining the functionality instead of closing the security gaps.</p>
<hr/>
<h2>Host Enumeration</h2>
<p>Once we have a detailed list of the customer's infrastructure, we examine every single host listed in the scoping document. We try to identify which <code>operating system</code> is running on the host or server, which <code>services</code> it uses, which <code>versions</code> of the services, and much more. Again, apart from the active scans, we can also use various OSINT methods to tell us how this host or server may be configured.</p>
<p>We can find many different services, such as an FTP server that the company uses to exchange data between employees and even allows anonymous access. Even today, there are many hosts and servers that the manufacturers no longer support. However, vulnerabilities are still found for these older versions of operating systems and services, which then remain and endanger our client's entire infrastructure.</p>
<p>It does not matter here whether we examine each host or server externally or internally. However, from the internal perspective, we will find services that are often not accessible from the outside. Therefore, many administrators become careless and often consider these services "secure" because they are not directly accessible from the internet. Thus, many misconfigurations are often discovered here due to these assumptions or lax practices. During host enumeration, we try to determine what role this host or server plays and what network components it communicates with. In addition, we must also identify which <code>services</code> it uses for this purpose and on which <code>ports</code> they are located.</p>
<p>During internal host enumeration, which in most cases comes after the successful <code>Exploitation</code> of one or more vulnerabilities, we also examine the host or server from the inside. This means we look for sensitive <code>files</code>, local <code>services</code>, <code>scripts</code>, <code>applications</code>, <code>information</code>, and other things that could be stored on the host. This is also an essential part of the <code>Post-Exploitation</code> phase, where we try to exploit and elevate privileges.</p>
<hr/>
<h2>Pillaging</h2>
<p>Another essential step is <code>Pillaging</code>. After hitting the <code>Post-Exploitation</code> stage, pillaging is performed to collect sensitive information locally on the already exploited host, such as employee names, customer data, and much more. However, this information gathering only occurs after exploiting the target host and gaining access to it.</p>
<p>The information we can obtain on the exploited hosts can be divided into many different categories and varies greatly. This depends on the purpose of the host and its positioning in the corporate network. The administrators taking the security measures for these hosts also play a significant role. Nevertheless, such information can show the <code>impact</code> of a potential attack on our client and be used for further steps to <code>escalate our privileges</code> or <code>move laterally</code> further in the network.</p>
<ul>
<li>Note that <code>HTB Academy</code> does not have a module explicitly focused on pillaging.</li>
</ul>
<p>This is intentional for reasons we will clarify here. Pillaging alone is not a stage or a subcategory as many often describe but an integral part of the information gathering and privilege escalation stages that is inevitably performed locally on target systems.</p>
<ul>
<li>
<code>Pillaging is explained in other modules separately, where we consider the corresponding steps valuable and necessary.</code>
</li>
</ul>
<p>Here is a small list of modules where <code>Pillaging</code> is covered, but this topic will be covered in many other modules as well:</p>
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
<td><code>Network Enumeration with Nmap</code></td>
<td><code>Getting Started</code></td>
<td><code>Password Attacks</code></td>
</tr>
<tr>
<td><code>Active Directory Enumeration &amp; Attacks</code></td>
<td><code>Linux Privilege Escalation</code></td>
<td><code>Windows Privilege Escalation</code></td>
</tr>
<tr>
<td><code>Attacking Common Services</code></td>
<td><code>Attacking Common Applications</code></td>
<td><code>Attacking Enterprise Networks</code></td>
</tr>
</tbody>
</table>
<p>We will interact with more than <code>150 targets</code> during the Penetration Tester Job Role Path and perform nine simulated mini penetration tests, giving us plenty of opportunities to work on and practice this topic. Furthermore, operating system-specific modules should be considered from the pillaging point of view because much of what is shown in those modules can be used for information retrieval or privilege escalation on the target systems.</p>
