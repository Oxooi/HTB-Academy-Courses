
<h1>Extensions</h1>
<hr/>
<p>Both Burp and ZAP have extension capabilities, such that the community of Burp users can develop extensions for Burp for everyone to use. Such extensions can perform specific actions on any captured requests, for example, or add new features, like decoding and beautifying code. Burp allows extensibility through its <code>Extender</code> feature and its <a href="https://portswigger.net/bappstore">BApp Store</a>, while ZAP has its <a href="https://www.zaproxy.org/addons/">ZAP Marketplace</a> to install new plugins.</p>
<hr/>
<h2>BApp Store</h2>
<p>To find all available extensions, we can click on the <code>Extender</code> tab within Burp and select the <code>BApp Store</code> sub-tab. Once we do this, we will see a host of extensions. We can sort them by <code>Popularity</code> so that we know which ones users are finding most useful:</p>
<p><img alt="BApp Store" src="https://academy.hackthebox.com/storage/modules/110/burp_bapp_store.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: Some extensions are for Pro users only, while most others are available to everyone.</p>
</div>
</div>
<p>We see many useful extensions, take some time to go through them and see which are most useful to you, and then try installing and testing them. Let's try installing the <code>Decoder Improved</code> extension:</p>
<p><img alt="Burp Extension" src="https://academy.hackthebox.com/storage/modules/110/burp_extension.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: Some extensions have requirements that are not usually installed on Linux/macOS/Windows by default, like `Jython`, so you have to install them before being able to install the extension.</p>
</div>
</div>
<p>Once we install <code>Decoder Improved</code>, we will see its new tab added to Burp. Each extension has a different usage, so we may click on any extension's documentation in <code>BApp Store</code> to read more about it or visit its GitHub page for more information about its usage. We can use this extension just as we would use Burp's Decoder, with the benefit of having many additional encoders included. For example, we can input text we want to be hashed with <code>MD5</code>, and select <code>Hash With&gt;MD5</code>:</p>
<p><img alt="Decoder Improved" src="https://academy.hackthebox.com/storage/modules/110/burp_extension_decoder_improved.jpg"/></p>
<p>Similarly, we can perform other types of encoding and hashing. There are many other Burp Extensions that can be utilized to further extend the functionality of Burp.</p>
<p>Some extensions worth checking out include, but are not limited to:</p>
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
<td>.NET beautifier</td>
<td>J2EEScan</td>
<td>Software Vulnerability Scanner</td>
</tr>
<tr>
<td>Software Version Reporter</td>
<td>Active Scan++</td>
<td>Additional Scanner Checks</td>
</tr>
<tr>
<td>AWS Security Checks</td>
<td>Backslash Powered Scanner</td>
<td>Wsdler</td>
</tr>
<tr>
<td>Java Deserialization Scanner</td>
<td>C02</td>
<td>Cloud Storage Tester</td>
</tr>
<tr>
<td>CMS Scanner</td>
<td>Error Message Checks</td>
<td>Detect Dynamic JS</td>
</tr>
<tr>
<td>Headers Analyzer</td>
<td>HTML5 Auditor</td>
<td>PHP Object Injection Check</td>
</tr>
<tr>
<td>JavaScript Security</td>
<td>Retire.JS</td>
<td>CSP Auditor</td>
</tr>
<tr>
<td>Random IP Address Header</td>
<td>Autorize</td>
<td>CSRF Scanner</td>
</tr>
<tr>
<td>JS Link Finder</td>
<td></td>
<td></td>
</tr>
</tbody>
</table>
<hr/>
<h2>ZAP Marketplace</h2>
<p>ZAP also has its own extensibility feature with the <code>Marketplace</code> that allows us to install various types of community-developed add-ons. To access ZAP's marketplace, we can click on the <code>Manage Add-ons</code> button and then select the <code>Marketplace</code> tab:</p>
<p><img alt="Marketplace Button" src="https://academy.hackthebox.com/storage/modules/110/zap_marketplace_button.jpg"/></p>
<p>In this tab, we can see the different available add-ons for ZAP. Some add-ons may be in their <code>Release</code> build, meaning that they should be stable to be used, while others are in their <code>Beta/Alpha</code> builds, which means that they may experience some issues in their use. Let's try installing the <code>FuzzDB Files</code> and <code>FuzzDB Offensive</code> add-ons, which adds new wordlists to be used in ZAP's fuzzer:
<img alt="Install FuzzDB" src="https://academy.hackthebox.com/storage/modules/110/zap_fuzzdb_install.jpg"/></p>
<p>Now, we will have the option to pick from the various wordlists and payloads provided by FuzzDB when performing an attack. For example, suppose we were to perform a Command Injection fuzzing attack on one of the exercises we previously used in this module. In that case, we will see that we have more options in the <code>File Fuzzers</code> wordlists, including an OS Command Injection wordlist under (<code>fuzzdb&gt;attack&gt;os-cmd-execution</code>), which would be perfect for this attack:</p>
<p><img alt="FuzzDB CMD Exec" src="https://academy.hackthebox.com/storage/modules/110/zap_fuzzdb_cmd_exec.jpg"/></p>
<p>Now, if we run the fuzzer on our exercise using the above wordlist, we will see that it was able to exploit it in various ways, which would be very helpful if we were dealing with a WAF protected web application:</p>
<p><img alt="FuzzDB CMD Exec" src="https://academy.hackthebox.com/storage/modules/110/zap_fuzzer_cmd_inj.jpg"/></p>
<p>Try to repeat the above with the first exercise in this module to see how add-ons can help in making your penetration test easier.</p>
<hr/>
<h2>Closing Thoughts</h2>
<p>Throughout this module, we have demonstrated the power of both Burp Suite and ZAP proxies and analyzed the differences and similarities between the free and pro versions of Burp and the free and open-source ZAP proxy. These tools are essential for penetration testers focused on web application security assessments but have many applications for all offensive security practitioners as well blue team practitioners and developers. After working through each of the examples and exercises in this module, attempt some web attack-focused boxes on the main Hack The Box platform and other web application security-related modules within HTB Academy to strengthen your skillsets around both of these tools. They are must-haves in your toolbox alongside Nmap, Hashcat, Wireshark, tcpdump, sqlmap, Ffuf, Gobuster, etc.</p>
