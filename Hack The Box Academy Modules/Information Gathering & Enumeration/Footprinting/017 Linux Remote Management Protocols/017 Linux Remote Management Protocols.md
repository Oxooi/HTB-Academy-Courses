
<h1>Linux Remote Management Protocols</h1>
<hr/>
<p>In the world of Linux distributions, there are many ways to manage the servers remotely. For example, let us imagine that we are in one of many locations and one of our employees who just went to a customer in another city needs our help because of an error that he cannot solve. Efficient troubleshooting will look difficult over a phone call in most cases, so it is beneficial if we know how to log onto the remote system to manage it.</p>
<p>These applications and services can be found on almost every server in the public network. It is time-saving since we do not have to be physically present at the server, and the working environment still looks the same. These protocols and applications for remote systems management are an exciting target for these reasons. If the configuration is incorrect, we, as penetration testers, can even quickly gain access to the remote system. Therefore, we should familiarize ourselves with the most important protocols, servers, and applications for this purpose.</p>
<hr/>
<h2>SSH</h2>
<p><a href="https://en.wikipedia.org/wiki/Secure_Shell">Secure Shell</a> (<code>SSH</code>) enables two computers to establish an encrypted and direct connection within a possibly insecure network on the standard port <code>TCP 22</code>. This is necessary to prevent third parties from intercepting the data stream and thus intercepting sensitive data. The SSH server can also be configured to only allow connections from specific clients. An advantage of SSH is that the protocol runs on all common operating systems. Since it is originally a Unix application, it is also implemented natively on all Linux distributions and MacOS. SSH can also be used on Windows, provided we install an appropriate program. The well-known <a href="https://www.openssh.com/">OpenBSD SSH</a> (<code>OpenSSH</code>) server on Linux distributions is an open-source fork of the original and commercial <code>SSH</code> server from SSH Communication Security. Accordingly, there are two competing protocols: <code>SSH-1</code> and <code>SSH-2</code>.</p>
<p><code>SSH-2</code>, also known as SSH version 2, is a more advanced protocol than SSH version 1 in encryption, speed, stability, and security. For example, <code>SSH-1</code> is vulnerable to <code>MITM</code> attacks, whereas SSH-2 is not.</p>
<p>We can imagine that we want to manage a remote host. This can be done via the command line or GUI. Besides, we can also use the SSH protocol to send commands to the desired system, transfer files, or do port forwarding. Therefore, we need to connect to it using the SSH protocol and authenticate ourselves to it. In total, OpenSSH has six different authentication methods:</p>
<ol>
<li>Password authentication</li>
<li>Public-key authentication</li>
<li>Host-based authentication</li>
<li>Keyboard authentication</li>
<li>Challenge-response authentication</li>
<li>GSSAPI authentication</li>
</ol>
<p>We will take a closer look at and discuss one of the most commonly used authentication methods. In addition, we can learn more about the other authentication methods <a href="https://www.golinuxcloud.com/openssh-authentication-methods-sshd-config/">here</a> among others.</p>
<h4>Public Key Authentication</h4>
<p>In a first step, the SSH server and client authenticate themselves to each other. The server sends a certificate to the client to verify that it is the correct server. Only when contact is first established is there a risk of a third party interposing itself between the two participants and thus intercepting the connection. Since the certificate itself is also encrypted, it cannot be imitated. Once the client knows the correct certificate, no one else can pretend to make contact via the corresponding server.</p>
<p>After server authentication, however, the client must also prove to the server that it has access authorization. However, the SSH server is already in possession of the encrypted hash value of the password set for the desired user. As a result, users have to enter the password every time they log on to another server during the same session. For this reason, an alternative option for client-side authentication is the use of a public key and private key pair.</p>
<p>The private key is created individually for the user's own computer and secured with a passphrase that should be longer than a typical password. The private key is stored exclusively on our own computer and always remains secret. If we want to establish an SSH connection, we first enter the passphrase and thus open access to the private key.</p>
<p>Public keys are also stored on the server. The server creates a cryptographic problem with the client's public key and sends it to the client. The client, in turn, decrypts the problem with its own private key, sends back the solution, and thus informs the server that it may establish a legitimate connection. During a session, users only need to enter the passphrase once to connect to any number of servers. At the end of the session, users log out of their local machines, ensuring that no third party who gains physical access to the local machine can connect to the server.</p>
<hr/>
<h2>Default Configuration</h2>
<p>The <a href="https://www.ssh.com/academy/ssh/sshd_config">sshd_config</a> file, responsible for the OpenSSH server, has only a few of the settings configured by default. However, the default configuration includes X11 forwarding, which contained a command injection vulnerability in version 7.2p1 of OpenSSH in 2016. Nevertheless, we do not need a GUI to manage our servers.</p>
<h4>Default Configuration</h4>
<pre><code class="language-shell-session">[!bash!]$ cat /etc/ssh/sshd_config  | grep -v "#" | sed -r '/^\s*$/d'

Include /etc/ssh/sshd_config.d/*.conf
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding yes
PrintMotd no
AcceptEnv LANG LC_*
Subsystem       sftp    /usr/lib/openssh/sftp-server
</code></pre>
<p>Most settings in this configuration file are commented out and require manual configuration.</p>
<hr/>
<h2>Dangerous Settings</h2>
<p>Despite the SSH protocol being one of the most secure protocols available today, some misconfigurations can still make the SSH server vulnerable to easy-to-execute attacks. Let us take a look at the following settings:</p>
<table>
<thead>
<tr>
<th><strong>Setting</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>PasswordAuthentication yes</code></td>
<td>Allows password-based authentication.</td>
</tr>
<tr>
<td><code>PermitEmptyPasswords yes</code></td>
<td>Allows the use of empty passwords.</td>
</tr>
<tr>
<td><code>PermitRootLogin yes</code></td>
<td>Allows to log in as the root user.</td>
</tr>
<tr>
<td><code>Protocol 1</code></td>
<td>Uses an outdated version of encryption.</td>
</tr>
<tr>
<td><code>X11Forwarding yes</code></td>
<td>Allows X11 forwarding for GUI applications.</td>
</tr>
<tr>
<td><code>AllowTcpForwarding yes</code></td>
<td>Allows forwarding of TCP ports.</td>
</tr>
<tr>
<td><code>PermitTunnel</code></td>
<td>Allows tunneling.</td>
</tr>
<tr>
<td><code>DebianBanner yes</code></td>
<td>Displays a specific banner when logging in.</td>
</tr>
</tbody>
</table>
<p>Allowing password authentication allows us to brute-force a known username for possible passwords. Many different methods can be used to guess the passwords of users. For this purpose, specific <code>patterns</code> are usually used to mutate the most commonly used passwords and, frighteningly, correct them. This is because we humans are lazy and do not want to remember complex and complicated passwords. Therefore, we create passwords that we can easily remember, and this leads to the fact that, for example, numbers or characters are added only at the end of the password. Believing that the password is secure, the mentioned patterns are used to guess precisely such "adjustments" of these passwords. However, some instructions and <a href="https://www.ssh-audit.com/hardening_guides.html">hardening guides</a> can be used to harden our SSH servers.</p>
<hr/>
<h2>Footprinting the Service</h2>
<p>One of the tools we can use to fingerprint the SSH server is <a href="https://github.com/jtesta/ssh-audit">ssh-audit</a>. It checks the client-side and server-side configuration and shows some general information and which encryption algorithms are still used by the client and server. Of course, this could be exploited by attacking the server or client at the cryptic level later.</p>
<h4>SSH-Audit</h4>
<pre><code class="language-shell-session">[!bash!]$ git clone https://github.com/jtesta/ssh-audit.git &amp;&amp; cd ssh-audit
[!bash!]$ ./ssh-audit.py 10.129.14.132

# general
(gen) banner: SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3
(gen) software: OpenSSH 8.2p1
(gen) compatibility: OpenSSH 7.4+, Dropbear SSH 2018.76+
(gen) compression: enabled (<a class="__cf_email__" data-cfemail="1a607673785a756a7f7469697234797577" href="/cdn-cgi/l/email-protection">[email protected]</a>)                                   

# key exchange algorithms
(kex) curve25519-sha256                     -- [info] available since OpenSSH 7.4, Dropbear SSH 2018.76                            
(kex) <a class="__cf_email__" data-cfemail="ceadbbbcb8abfcfbfbfff7e3bda6affcfbf88ea2a7acbdbda6e0a1bca9" href="/cdn-cgi/l/email-protection">[email protected]</a>          -- [info] available since OpenSSH 6.5, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp256                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp384                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp521                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) diffie-hellman-group-exchange-sha256 (2048-bit) -- [info] available since OpenSSH 4.4
(kex) diffie-hellman-group16-sha512         -- [info] available since OpenSSH 7.3, Dropbear SSH 2016.73
(kex) diffie-hellman-group18-sha512         -- [info] available since OpenSSH 7.3
(kex) diffie-hellman-group14-sha256         -- [info] available since OpenSSH 7.3, Dropbear SSH 2016.73

# host-key algorithms
(key) rsa-sha2-512 (3072-bit)               -- [info] available since OpenSSH 7.2
(key) rsa-sha2-256 (3072-bit)               -- [info] available since OpenSSH 7.2
(key) ssh-rsa (3072-bit)                    -- [fail] using weak hashing algorithm
                                            `- [info] available since OpenSSH 2.5.0, Dropbear SSH 0.28
                                            `- [info] a future deprecation notice has been issued in OpenSSH 8.2: https://www.openssh.com/txt/release-8.2
(key) ecdsa-sha2-nistp256                   -- [fail] using weak elliptic curves
                                            `- [warn] using weak random number generator could reveal the key
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(key) ssh-ed25519                           -- [info] available since OpenSSH 6.5
...SNIP...
</code></pre>
<p>The first thing we can see in the first few lines of the output is the banner that reveals the version of the OpenSSH server. The previous versions had some vulnerabilities, such as <a href="https://www.cvedetails.com/cve/CVE-2020-14145/">CVE-2020-14145</a>, which allowed the attacker the capability to Man-In-The-Middle and attack the initial connection attempt. The detailed output of the connection setup with the OpenSSH server can also often provide important information, such as which authentication methods the server can use.</p>
<h4>Change Authentication Method</h4>
<pre><code class="language-shell-session">[!bash!]$ ssh -v <a class="__cf_email__" data-cfemail="fa998883ca96cb8ec9bacbcad4cbc8c3d4cbced4cbc9c8" href="/cdn-cgi/l/email-protection">[email protected]</a>

OpenSSH_8.2p1 Ubuntu-4ubuntu0.3, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /etc/ssh/ssh_config 
...SNIP...
debug1: Authentications that can continue: publickey,password,keyboard-interactive
</code></pre>
<p>For potential brute-force attacks, we can specify the authentication method with the SSH client option <code>PreferredAuthentications</code>.</p>
<pre><code class="language-shell-session">[!bash!]$ ssh -v <a class="__cf_email__" data-cfemail="dfbcada6efb3eeabec9feeeff1eeede6f1eeebf1eeeced" href="/cdn-cgi/l/email-protection">[email protected]</a> -o PreferredAuthentications=password

OpenSSH_8.2p1 Ubuntu-4ubuntu0.3, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /etc/ssh/ssh_config
...SNIP...
debug1: Authentications that can continue: publickey,password,keyboard-interactive
debug1: Next authentication method: password

<a class="__cf_email__" data-cfemail="2d4e5f541d411c591e6d1c1d031c1f14031c19031c1e1f" href="/cdn-cgi/l/email-protection">[email protected]</a>'s password:
</code></pre>
<p>Even with this obvious and secure service, we recommend setting up our own OpenSSH server on our VM, experimenting with it, and familiarizing ourselves with the different settings and options.</p>
<p>We may encounter various banners for the SSH server during our penetration tests. By default, the banners start with the version of the protocol that can be applied and then the version of the server itself. For example, with <code>SSH-1.99-OpenSSH_3.9p1</code>, we know that we can use both protocol versions SSH-1 and SSH-2, and we are dealing with OpenSSH server version 3.9p1. On the other hand, for a banner with <code>SSH-2.0-OpenSSH_8.2p1</code>, we are dealing with an OpenSSH version 8.2p1 which only accepts the SSH-2 protocol version.</p>
<hr/>
<h2>Rsync</h2>
<p><a href="https://linux.die.net/man/1/rsync">Rsync</a> is a fast and efficient tool for locally and remotely copying files. It can be used to copy files locally on a given machine and to/from remote hosts. It is highly versatile and well-known for its delta-transfer algorithm. This algorithm reduces the amount of data transmitted over the network when a version of the file already exists on the destination host. It does this by sending only the differences between the source files and the older version of the files that reside on the destination server. It is often used for backups and mirroring. It finds files that need to be transferred by looking at files that have changed in size or the last modified time. By default, it uses port <code>873</code> and can be configured to use SSH for secure file transfers by piggybacking on top of an established SSH server connection.</p>
<p>This <a href="https://book.hacktricks.xyz/network-services-pentesting/873-pentesting-rsync">guide</a> covers some of the ways Rsync can be abused, most notably by listing the contents of a shared folder on a target server and retrieving files. This can sometimes be done without authentication. Other times we will need credentials. If you find credentials during a pentest and run into Rsync on an internal (or external) host, it is always worth checking for password re-use as you may be able to pull down some sensitive files that could be used to gain remote access to the target.</p>
<p>Let's do a bit of quick footprinting. We can see that Rsync is in use using protocol 31.</p>
<h4>Scanning for Rsync</h4>
<pre><code class="language-shell-session">[!bash!]$ sudo nmap -sV -p 873 127.0.0.1

Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-19 09:31 EDT
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0058s latency).

PORT    STATE SERVICE VERSION
873/tcp open  rsync   (protocol version 31)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.13 seconds
</code></pre>
<h4>Probing for Accessible Shares</h4>
<p>We can next probe the service a bit to see what we can gain access to.</p>
<pre><code class="language-shell-session">[!bash!]$ nc -nv 127.0.0.1 873

(UNKNOWN) [127.0.0.1] 873 (rsync) open
@RSYNCD: 31.0
@RSYNCD: 31.0
#list
dev            	Dev Tools
@RSYNCD: EXIT
</code></pre>
<h4>Enumerating an Open Share</h4>
<p>Here we can see a share called <code>dev</code>, and we can enumerate it further.</p>
<pre><code class="language-shell-session">[!bash!]$ rsync -av --list-only rsync://127.0.0.1/dev

receiving incremental file list
drwxr-xr-x             48 2022/09/19 09:43:10 .
-rw-r--r--              0 2022/09/19 09:34:50 build.sh
-rw-r--r--              0 2022/09/19 09:36:02 secrets.yaml
drwx------             54 2022/09/19 09:43:10 .ssh

sent 25 bytes  received 221 bytes  492.00 bytes/sec
total size is 0  speedup is 0.00
</code></pre>
<p>From the above output, we can see a few interesting files that may be worth pulling down to investigate further. We can also see that a directory likely containing SSH keys is accessible. From here, we could sync all files to our attack host with the command <code>rsync -av rsync://127.0.0.1/dev</code>. If Rsync is configured to use SSH to transfer files, we could modify our commands to include the <code>-e ssh</code> flag, or <code>-e "ssh -p2222"</code> if a non-standard port is in use for SSH. This <a href="https://phoenixnap.com/kb/how-to-rsync-over-ssh">guide</a> is helpful for understanding the syntax for using Rsync over SSH.</p>
<hr/>
<h2>R-Services</h2>
<p>R-Services are a suite of services hosted to enable remote access or issue commands between Unix hosts over TCP/IP. Initially developed by the Computer Systems Research Group (<code>CSRG</code>) at the University of California,  Berkeley, <code>r-services</code> were the de facto standard for remote access between Unix operating systems until they were replaced by the Secure Shell (<code>SSH</code>) protocols and commands due to inherent security flaws built into them. Much like <code>telnet</code>, r-services transmit information from client to server(and vice versa.) over the network in an unencrypted format, making it possible for attackers to intercept network traffic (passwords, login information, etc.) by performing man-in-the-middle (<code>MITM</code>) attacks.</p>
<p><code>R-services</code> span across the ports <code>512</code>, <code>513</code>, and <code>514</code> and are only accessible through a suite of programs known as <code>r-commands</code>. They are most commonly used by commercial operating systems such as Solaris, HP-UX, and AIX. While less common nowadays, we do run into them from time to time during our internal penetration tests so it is worth understanding how to approach them.</p>
<p>The <a href="https://en.wikipedia.org/wiki/Berkeley_r-commands">R-commands</a> suite consists of the following programs:</p>
<ul>
<li>rcp (<code>remote copy</code>)</li>
<li>rexec (<code>remote execution</code>)</li>
<li>rlogin (<code>remote login</code>)</li>
<li>rsh (<code>remote shell</code>)</li>
<li>rstat</li>
<li>ruptime</li>
<li>rwho (<code>remote who</code>)</li>
</ul>
<p>Each command has its intended functionality; however, we will only cover the most commonly abused <code>r-commands</code>. The table below will provide a quick overview of the most frequently abused commands, including the service daemon they interact with, over what port and transport method to which they can be accessed, and a brief description of each.</p>
<table>
<thead>
<tr>
<th><strong>Command</strong></th>
<th><strong>Service Daemon</strong></th>
<th><strong>Port</strong></th>
<th><strong>Transport Protocol</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>rcp</code></td>
<td><code>rshd</code></td>
<td>514</td>
<td>TCP</td>
<td>Copy a file or directory bidirectionally from the local system to the remote system (or vice versa) or from one remote system to another. It works like the <code>cp</code> command on Linux but provides <code>no warning to the user for overwriting existing files on a system</code>.</td>
</tr>
<tr>
<td><code>rsh</code></td>
<td><code>rshd</code></td>
<td>514</td>
<td>TCP</td>
<td>Opens a shell on a remote machine without a login procedure. Relies upon the trusted entries in the <code>/etc/hosts.equiv</code> and <code>.rhosts</code> files for validation.</td>
</tr>
<tr>
<td><code>rexec</code></td>
<td><code>rexecd</code></td>
<td>512</td>
<td>TCP</td>
<td>Enables a user to run shell commands on a remote machine. Requires authentication through the use of a <code>username</code> and <code>password</code> through an unencrypted network socket. Authentication is overridden by the trusted entries in the <code>/etc/hosts.equiv</code> and <code>.rhosts</code> files.</td>
</tr>
<tr>
<td><code>rlogin</code></td>
<td><code>rlogind</code></td>
<td>513</td>
<td>TCP</td>
<td>Enables a user to log in to a remote host over the network. It works similarly to <code>telnet</code> but can only connect to Unix-like hosts. Authentication is overridden by the trusted entries in the <code>/etc/hosts.equiv</code> and <code>.rhosts</code> files.</td>
</tr>
</tbody>
</table>
<p>The /etc/hosts.equiv file contains a list of trusted hosts and is used to grant access to other systems on the network. When users on one of these hosts attempt to access the system, they are automatically granted access without further authentication.</p>
<h4>/etc/hosts.equiv</h4>
<pre><code class="language-shell-session">[!bash!]$ cat /etc/hosts.equiv

# &lt;hostname&gt; &lt;local username&gt;
pwnbox cry0l1t3
</code></pre>
<p>Now that we have a basic understanding of <code>r-commands</code>, let's do some quick footprinting using <code>Nmap</code> to determine if all necessary ports are open.</p>
<h4>Scanning for R-Services</h4>
<pre><code class="language-shell-session">[!bash!]$ sudo nmap -sV -p 512,513,514 10.0.17.2

Starting Nmap 7.80 ( https://nmap.org ) at 2022-12-02 15:02 EST
Nmap scan report for 10.0.17.2
Host is up (0.11s latency).

PORT    STATE SERVICE    VERSION
512/tcp open  exec?
513/tcp open  login?
514/tcp open  tcpwrapped

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 145.54 seconds
</code></pre>
<h4>Access Control &amp; Trusted Relationships</h4>
<p>The primary concern for <code>r-services</code>, and one of the primary reasons <code>SSH</code> was introduced to replace it, is the inherent issues regarding access control for these protocols. R-services rely on trusted information sent from the remote client to the host machine they are attempting to authenticate to. By default, these services utilize <a href="https://debathena.mit.edu/trac/wiki/PAM">Pluggable Authentication Modules (PAM)</a> for user authentication onto a remote system; however, they also bypass this authentication through the use of the <code>/etc/hosts.equiv</code> and <code>.rhosts</code> files on the system. The <code>hosts.equiv</code> and <code>.rhosts</code> files contain a list of hosts (<code>IPs</code> or <code>Hostnames</code>) and users that are <code>trusted</code> by the local host when a connection attempt is made using <code>r-commands</code>. Entries in either file can appear like the following:</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> The <code>hosts.equiv</code> file is recognized as the global configuration regarding all users on a system, whereas <code>.rhosts</code> provides a per-user configuration. </p>
</div>
</div>
<h4>Sample .rhosts File</h4>
<pre><code class="language-shell-session">[!bash!]$ cat .rhosts

htb-student     10.0.17.5
+               10.0.17.10
+               +
</code></pre>
<p>As we can see from this example, both files follow the specific syntax of <code>&lt;username&gt; &lt;ip address&gt;</code> or <code>&lt;username&gt; &lt;hostname&gt;</code> pairs. Additionally, the <code>+</code> modifier can be used within these files as a wildcard to specify anything. In this example, the <code>+</code> modifier allows any external user to access r-commands from the <code>htb-student</code> user account via the host with the IP address <code>10.0.17.10</code>.</p>
<p>Misconfigurations in either of these files can allow an attacker to authenticate as another user without credentials, with the potential for gaining code execution. Now that we understand how we can potentially abuse misconfigurations in these files let's attempt to try logging into a target host using <code>rlogin</code>.</p>
<h4>Logging in Using Rlogin</h4>
<pre><code class="language-shell-session">[!bash!]$ rlogin 10.0.17.2 -l htb-student

Last login: Fri Dec  2 16:11:21 from localhost

[htb-student@localhost ~]$
</code></pre>
<p>We have successfully logged in under the <code>htb-student</code> account on the remote host due to the misconfigurations in the <code>.rhosts</code> file. Once successfully logged in, we can also abuse the <code>rwho</code> command to list all interactive sessions on the local network by sending requests to the UDP port 513.</p>
<h4>Listing Authenticated Users Using Rwho</h4>
<pre><code class="language-shell-session">[!bash!]$ rwho

root     web01:pts/0 Dec  2 21:34
htb-student     workstn01:tty1  Dec  2 19:57  2:25       
</code></pre>
<p>From this information, we can see that the <code>htb-student</code> user is currently authenticated to the <code>workstn01</code> host, whereas the <code>root</code> user is authenticated to the <code>web01</code> host. We can use this to our advantage when scoping out potential usernames to use during further attacks on hosts over the network. However, the <code>rwho</code> daemon periodically broadcasts information about logged-on users, so it might be beneficial to watch the network traffic.</p>
<h4>Listing Authenticated Users Using Rusers</h4>
<p>To provide additional information in conjunction with <code>rwho</code>, we can issue the <code>rusers</code> command. This will give us a more detailed account of all logged-in users over the network, including information such as the username, hostname of the accessed machine, TTY that the user is logged in to, the date and time the user logged in, the amount of time since the user typed on the keyboard, and the remote host they logged in from (if applicable).</p>
<pre><code class="language-shell-session">[!bash!]$ rusers -al 10.0.17.5

htb-student     10.0.17.5:console          Dec 2 19:57     2:25
</code></pre>
<p>As we can see, R-services are less frequently used nowadays due to their inherent security flaws and the availability of more secure protocols such as SSH. To be a well-rounded information security professional, we must have a broad and deep understanding of many systems, applications, protocols, etc. So, file away this knowledge about R-services because you never know when you may encounter them.</p>
<hr/>
<h2>Final Thoughts</h2>
<p>Remote management services can provide us with a treasure trove of data and often be abused for unauthorized access through either weak/default credentials or password re-use. We should always probe these services for as much information as we can gather and leave no stone unturned, especially when we have compiled a list of credentials from elsewhere in the target network.</p>
