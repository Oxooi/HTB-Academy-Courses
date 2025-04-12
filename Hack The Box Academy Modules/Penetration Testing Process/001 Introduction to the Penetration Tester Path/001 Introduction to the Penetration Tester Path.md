
<h1>Introduction to the Penetration Tester Path</h1>
<hr/>
<p>This module is an introduction to the Penetration Tester <a href="https://academy.hackthebox.com/paths/jobrole">Job Role Path</a> and a general introduction to Penetration Tests and each of the phases that we cover in-depth throughout the modules. We recommend starting the path with this module and referring to it periodically as you complete other modules to see how each topic area fits in the bigger picture of the penetration testing process. This module is also a great starting point for anyone new to HTB Academy or the industry.</p>
<p>This path is intended for aspiring penetration testers from all walks of life and experienced pentesters looking to upskill in a particular area, become more well-rounded or learn things from a different perspective. This path covers core concepts necessary to succeed at External Penetration Tests, Internal Penetration Tests (both network and Active Directory), and Web Application Security Assessments. Through each module, we dive deep into the specialized techniques, methodologies, and tools needed to succeed in a penetration testing role. The path takes students on a highly hands-on journey through all stages of a penetration test, from reconnaissance and enumeration to documentation and reporting, culminating with a simulated penetration test capstone module. Students who complete this path in its entirety will be armed with the practical skills and mindset necessary to perform professional security assessments against real-world networks at a basic to intermediate level. Each of our modules dives deep into the "why" behind the issues and tactics that we present and is not just a tutorial on running point-and-click tools. We weave in stories and scenarios from our real-world experience performing security assessments for clients in all verticals and local and federal government.</p>
<hr/>
<h2>HTB Academy Learning Philosophy</h2>
<p>Our goal is to teach students how to see both sides of an issue and be able to find flaws that others may miss. We encourage each student to formulate their own repeatable and thorough methodology that can be applied to any assessment type, no matter the size of the environment or the client's industry. Learning in this way and working through hundreds of practical, hands-on examples, with each module culminating in one or more skills assessments, reinforces these concepts and builds "muscle memory" around the things we perform on every assessment. If we can perform the basics well, we have more time to dig deeper and provide extra value to our clients. For every vulnerability and misconfiguration we demonstrate, we discuss the underlying flaw, which helps us better understand how things work, why a particular tool may be failing, and provide more accurate remediation advice to our clients that can be uniquely tailored to their environment and risk appetite.</p>
<p>Our learning philosophy can be summed up as the following:</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Our philosophy is "learn by doing," following a risk-based approach with a heavy emphasis on hands-on learning and legal &amp; ethical use of our skills. We strive to teach our students the "why" behind a vulnerability and how to discover, exploit, remediate, detect, and prevent the flaw to create well-rounded professionals who can pass this all-encompassing knowledge &amp; mindset on to their current/future clients or employers to assist them in securing their people, technologies and missions from modern cyber threats.</p>
</div>
</div>
<hr/>
<h2>Ethical and Legal Considerations</h2>
<p>An essential part of the above philosophy is the terms <code>legal</code> and <code>ethical</code>. Penetration Testing is one of the few professions where you are, for a time (during the authorized testing period), allowed to perform actions against a company that would be against the law under other circumstances. Throughout the modules, in this path and others, we provide individual targets and mini networks (labs) to safely and legally practice the techniques we demonstrate. The HTB main platform contains 100s of boxes and multiple large, real-world lab networks to practice these skills. With the rise of gamification in our industry and access to more hands-on, realistic training material, we must remember that there is a line between legal and illegal actions that can easily be crossed if we try to practice our skills outside of these controlled environments. Performing passive OSINT and information gathering skills against a target to work on those skills is OK, provided we are only using public databases and search engines but not probing a company's external infrastructure. However, performing ANY scanning or activities that interact with <code>ANY</code> of an organization's systems without explicit written consent in the form of a Scope of Work (including a detailed scope of testing, contract, and rules of engagement) signed by both parties is against the law and could lead to legal and even criminal action being taken against us.</p>
<p>If you are ready to practice on real-world targets, you can get additional practice by participating in bug bounty programs hosted by organizations such as <a href="https://hackerone.com/directory/programs">HackerOne</a> and <a href="https://bugcrowd.com/programs">Bugcrowd</a>. Through these bug bounty organizations, you can participate in web application testing activities against many different companies that offer a bug bounty program. Keep in mind that each of these programs has its own scope and rules of engagement, so familiarize yourself with them before starting any testing activities. Most of these programs do not allow automated scanning, making them a great way to practice your information gathering and manual web application testing skills.</p>
<p>Once you land your first penetration testing job, do your due diligence to ensure that the company is a legitimate organization performing assessments only after explicit coordination (and contract paperwork) is completed between the target company and client. While rare, some criminal organizations may pose as legitimate companies to recruit talent to assist with illegal actions. If you participate, even if your intentions are good, you can still be liable and get into legal and even criminal trouble. When working for any company, make sure that you have a copy of the signed scope of work/contract and a formal document listing the scope of testing (URLs, individual IP addresses, CIDR network ranges, wireless SSIDs, facilities for a physical assessment, or lists of email or phone numbers for social engineering engagements), also signed by the client. When in doubt, request additional approvals and documentation before beginning any testing. While performing testing, <code>stay within the scope of testing</code>. Do not stray from the scope if you notice other IP addresses or subdomains that look more interesting. Again, <code>if in doubt, reach out</code>. Perhaps the client forgot to add certain hosts to the scoping sheet. It does not hurt to reach out and ask if other hosts you notice should be included, but, again, make sure this is <code>in writing</code> and not just given on a phone call.</p>
<p>Our clients place great trust in us to come into their network and run tools that could potentially wreak havoc on their network and cause disruptions that could lead to downtime and loss of revenue. We must work with the guiding principle of <code>do no harm</code> and strive to perform all testing activities in a careful and measured way. Just because we can run a certain tool, should we? Could a particular exploit PoC potentially crash one or more servers? If in doubt about anything during an assessment, run it by your manager and the client and gain explicit consent <code>in writing</code> before proceeding.</p>
<p>To sum up, we are highly skilled, and great trust is placed in us. Do not abuse this trust, <code>always work ethically and within the bounds of the law</code>, and you will have a long and fruitful career and make great business and personal relationships along the way. Always strive to take the high road and do the right thing. <code>Document, document, document</code>. When in doubt, document and overcommunicate. Ensure that all of the "boring" compliance issues are taken care of first so you can rest easy and enjoy performing excellent comprehensive assessments for your clients as their trusted advisor.</p>
<hr/>
<h2>Penetration Tester Path Syllabus</h2>
<p>The path simulates a penetration test against the company Inlanefreight broken down into various stages, covering the core concepts and tools that will make us stand out as penetration testers. The path culminates in an in-depth module on critical soft skills such as notetaking, organization, documentation, reporting, and client communication, and then a full-blown mock penetration test to practice all of our skills in one large, simulated company network. The modules that comprise the path are laid out as follows:</p>
<table>
<thead>
<tr>
<th><strong><code>Introduction</code></strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>1. <a href="https://academy.hackthebox.com/module/details/90">Penetration Testing Process</a></td>
</tr>
<tr>
<td>2. <a href="https://academy.hackthebox.com/module/details/77">Getting Started</a></td>
</tr>
</tbody>
</table>
<table>
<thead>
<tr>
<th><strong><code>Reconnaissance, Enumeration &amp; Attack Planning</code></strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>3. <a href="https://academy.hackthebox.com/module/details/19">Network Enumeration with Nmap</a></td>
</tr>
<tr>
<td>4. <a href="https://academy.hackthebox.com/module/details/112">Footprinting</a></td>
</tr>
<tr>
<td>5. <a href="https://academy.hackthebox.com/module/details/144">Information Gathering - Web Edition</a></td>
</tr>
<tr>
<td>6. <a href="https://academy.hackthebox.com/module/details/108">Vulnerability Assessment</a></td>
</tr>
<tr>
<td>7. <a href="https://academy.hackthebox.com/module/details/24">File Transfers</a></td>
</tr>
<tr>
<td>8. <a href="https://academy.hackthebox.com/module/details/115">Shells &amp; Payloads</a></td>
</tr>
<tr>
<td>9. <a href="https://academy.hackthebox.com/module/details/39">Using the Metasploit Framework</a></td>
</tr>
</tbody>
</table>
<table>
<thead>
<tr>
<th><strong><code>Exploitation &amp; Lateral Movement</code></strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>10. <a href="https://academy.hackthebox.com/module/details/147">Password Attacks</a></td>
</tr>
<tr>
<td>11. <a href="https://academy.hackthebox.com/module/details/116">Attacking Common Services</a></td>
</tr>
<tr>
<td>12. <a href="https://academy.hackthebox.com/module/details/158">Pivoting, Tunneling, and Port Forwarding</a></td>
</tr>
<tr>
<td>13. <a href="https://academy.hackthebox.com/module/details/143">Active Directory Enumeration &amp; Attacks</a></td>
</tr>
</tbody>
</table>
<table>
<thead>
<tr>
<th><strong><code>Web Exploitation</code></strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>14. <a href="https://academy.hackthebox.com/module/details/110">Using Web Proxies</a></td>
</tr>
<tr>
<td>15. <a href="https://academy.hackthebox.com/module/details/54">Attacking Web Applications with Ffuf</a></td>
</tr>
<tr>
<td>16. <a href="https://academy.hackthebox.com/module/details/57">Login Brute Forcing</a></td>
</tr>
<tr>
<td>17. <a href="https://academy.hackthebox.com/module/details/33">SQL Injection Fundamentals</a></td>
</tr>
<tr>
<td>18. <a href="https://academy.hackthebox.com/module/details/58">SQLMap Essentials</a></td>
</tr>
<tr>
<td>19. <a href="https://academy.hackthebox.com/module/details/103">Cross-Site Scripting (XSS)</a></td>
</tr>
<tr>
<td>20. <a href="https://academy.hackthebox.com/module/details/23">File Inclusion</a></td>
</tr>
<tr>
<td>21. <a href="https://academy.hackthebox.com/module/details/136">File Upload Attacks</a></td>
</tr>
<tr>
<td>22. <a href="https://academy.hackthebox.com/module/details/109">Command Injections</a></td>
</tr>
<tr>
<td>23. <a href="https://academy.hackthebox.com/module/details/134">Web Attacks</a></td>
</tr>
<tr>
<td>24. <a href="https://academy.hackthebox.com/module/details/113">Attacking Common Applications</a></td>
</tr>
</tbody>
</table>
<table>
<thead>
<tr>
<th><strong><code>Post-Exploitation</code></strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>25. <a href="https://academy.hackthebox.com/module/details/51">Linux Privilege Escalation</a></td>
</tr>
<tr>
<td>26. <a href="https://academy.hackthebox.com/module/details/67">Windows Privilege Escalation</a></td>
</tr>
</tbody>
</table>
<table>
<thead>
<tr>
<th><strong><code>Reporting &amp; Capstone</code></strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>27. <a href="https://academy.hackthebox.com/module/details/162">Documentation &amp; Reporting</a></td>
</tr>
<tr>
<td>28. <a href="https://academy.hackthebox.com/module/details/163">Attacking Enterprise Networks</a></td>
</tr>
</tbody>
</table>
<p>After completing this path, we recommend that students work towards a specialization, be it Active Directory, Web, or Reverse Engineering. We should slowly continue to build our skills in all areas to become as well-rounded as possible while striving for expert-level knowledge in at least one discipline. For those that may not yet feel confident enough to take on this Job Role Path, we recommend working through all of the modules in the <code>Information Security Foundations</code> <a href="https://academy.hackthebox.com/paths">Skill Path</a>, which will help build the prerequisite knowledge necessary to be successful in the Penetration Tester path. It is best to take the modules in the Penetration Tester Path in order, as the concepts build on each other. Throughout the path, we continually reiterate concepts and present things in different ways to give students more practice and scenarios to further their knowledge in a particular area. For example, Lateral Movement and Pillaging are vital skills to succeed as a penetration tester. We do not have separate modules for each of these phases because pillaging and lateral movement can be thought of as iterative processes that we will revisit many times during an assessment. Instead, we introduce tactics, techniques, and procedures for moving laterally and show a wide variety of scenarios where we can benefit from strong pillaging/post-exploitation skills.</p>
<p>The following section breaks down 36 different HTB Academy modules and how they fit into each phase of the penetration testing process.</p>
