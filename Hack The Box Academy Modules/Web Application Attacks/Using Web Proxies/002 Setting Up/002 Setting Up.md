
<h1>Setting Up</h1>
<hr/>
<p>Both Burp and ZAP are available for Windows, macOS, and any Linux distribution. Both are already installed on your PwnBox instance and can be accessed from the bottom dock or top bar menu. Both tools are pre-installed on common Penetration Testing Linux distributions like Parrot or Kali. We will cover the installation and setup process for Burp and Zap in this section which will be helpful if we want to install the tools on our own VM.</p>
<hr/>
<h2>Burp Suite</h2>
<p>If Burp is not pre-installed in our VM, we can start by downloading it from <a href="https://portswigger.net/burp/releases/">Burp's Download Page</a>. Once downloaded, we can run the installer and follow the instructions, which vary from one operating system to another, but should be pretty straightforward. There are installers for Windows, Linux, and macOS.</p>
<p>Once installed, Burp can either be launched from the terminal by typing <code>burpsuite</code>, or from the application menu as previously mentioned. Another option is to download the <code>JAR</code> file (which can be used on all operating systems with a Java Runtime Environment (JRE) installed) from the above downloads page. We can run it with the following command line or by double-clicking it:</p>
<pre><code class="language-shell-session">[!bash!]$ java -jar &lt;/path/to/burpsuite.jar&gt;
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: Both Burp and ZAP rely on Java Runtime Environment to run, but this package should be included in the installer by default. If not, we can follow the instructions found on this <a href="https://docs.oracle.com/goldengate/1212/gg-winux/GDRAD/java.htm">page</a>.</p>
</div>
</div>
<p>Once we start up Burp, we are prompted to create a new project. If we are running the community version, we would only be able to use temporary projects without the ability to save our progress and carry on later:</p>
<p><img alt="Burp Community Project" src="https://academy.hackthebox.com/storage/modules/110/burp_project_community.jpg"/></p>
<p>If we are using the pro/enterprise version, we will have the option to either start a new project or open an existing project.</p>
<p><img alt="Burp Pro Project" src="https://academy.hackthebox.com/storage/modules/110/burp_project_prof.jpg"/></p>
<p>We may need to save our progress if we were pentesting huge web applications or running an <code>Active Web Scan</code>. However, we may not need to save our progress and, in many cases, can start a <code>temporary</code> project every time.</p>
<p>So, let's select <code>temporary project</code>, and click continue. Once we do, we will be prompted to either use <code>Burp Default Configurations</code>, or to <code>Load a Configuration File</code>, and we'll choose the first option:</p>
<p><img alt="Burp Project Config" src="https://academy.hackthebox.com/storage/modules/110/burp_project_config.jpg"/></p>
<p>Once we start heavily utilizing Burp's features, we may want to customize our configurations and load them when starting Burp. For now, we can keep <code>Use Burp Defaults</code>, and <code>Start Burp</code>.  Once all of this is done, we should be ready to start using Burp.</p>
<hr/>
<h2>ZAP</h2>
<p>We can download ZAP from its <a href="https://www.zaproxy.org/download/">download page</a>, choose the installer that fits our operating system, and follow the basic installation instructions to get it installed. ZAP can also be downloaded as a cross-platform JAR file and launched with the <code>java -jar</code> command or by double-clicking on it, similarly to Burp.</p>
<p>To get started with ZAP, we can launch it from the terminal with the <code>zaproxy</code> command or access it from the application menu like Burp. Once ZAP starts up, unlike the free version of Burp, we will be prompted to either create a new project or a temporary project. Let's use a temporary project by choosing <code>no</code>, as we will not be working on a big project that we will need to persist for several days:</p>
<p><img alt="ZAP New Config" src="https://academy.hackthebox.com/storage/modules/110/zap_new_project.jpg"/></p>
<p>After that, we will have ZAP running, and we can continue the proxy setup process, as we will discuss in the next section.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: If you prefer to use to a dark theme, you may do so in Burp by going to (<code>User Options&gt;Display</code>) and selecting "dark" under (<code>theme</code>), and in ZAP by going to (<code>Tools&gt;Options&gt;Display</code>) and selecting "Flat Dark" in (<code>Look and Feel</code>).</p>
</div>
</div>
