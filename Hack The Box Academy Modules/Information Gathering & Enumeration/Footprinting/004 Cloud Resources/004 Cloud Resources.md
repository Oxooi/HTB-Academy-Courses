
<h1>Cloud Resources</h1>
<hr/>
<p>The use of cloud, such as <a href="https://aws.amazon.com/">AWS</a>, <a href="https://cloud.google.com/">GCP</a>, <a href="https://azure.microsoft.com/en-us/">Azure</a>, and others, is now one of the essential components for many companies nowadays. After all, all companies want to be able to do their work from anywhere, so they need a central point for all management. This is why services from <code>Amazon</code> (<code>AWS</code>), <code>Google</code> (<code>GCP</code>), and <code>Microsoft</code> (<code>Azure</code>) are ideal for this purpose.</p>
<p>Even though cloud providers secure their infrastructure centrally, this does not mean that companies are free from vulnerabilities. The configurations made by the administrators may nevertheless make the company's cloud resources vulnerable. This often starts with the <code>S3 buckets</code> (AWS), <code>blobs</code> (Azure), <code>cloud storage</code> (GCP), which can be accessed without authentication if configured incorrectly.</p>
<h4>Company Hosted Servers</h4>
<pre><code class="language-shell-session">[!bash!]$ for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f1,4;done

blog.inlanefreight.com 10.129.24.93
inlanefreight.com 10.129.27.33
matomo.inlanefreight.com 10.129.127.22
www.inlanefreight.com 10.129.127.33
s3-website-us-west-2.amazonaws.com 10.129.95.250
</code></pre>
<p>Often cloud storage is added to the DNS list when used for administrative purposes by other employees. This step makes it much easier for the employees to reach and manage them. Let us stay with the case that a company has contracted us, and during the IP lookup, we have already seen that one IP address belongs to the <code>s3-website-us-west-2.amazonaws.com</code> server.</p>
<p>However, there are many different ways to find such cloud storage. One of the easiest and most used is Google search combined with Google Dorks. For example, we can use the Google Dorks <code>inurl:</code> and <code>intext:</code> to narrow our search to specific terms. In the following example, we see red censored areas containing the company name.</p>
<h4>Google Search for AWS</h4>
<img alt="Google search results for 'intext: [redacted] inurl:amazonaws.com' showing links to Amazon S3 PDFs." class="website-screenshot" data-url="https://www.google.com" src="/storage/modules/112/gsearch1.png"/>
<h4>Google Search for Azure</h4>
<img alt="Google search results for 'intext: [redacted] inurl:blob.core.windows.net' showing links to PDF files on Azure Blob Storage." class="website-screenshot" data-url="https://www.google.com" src="/storage/modules/112/gsearch2.png"/>
<p>Here we can already see that the links presented by Google contain PDFs. When we search for a company that we may already know or want to know, we will also come across other files such as text documents, presentations, codes, and many others.</p>
<p>Such content is also often included in the source code of the web pages, from where the images, JavaScript codes, or CSS are loaded. This procedure often relieves the web server and does not store unnecessary content.</p>
<h4>Target Website - Source Code</h4>
<p><img alt="HTML code snippet showing DNS prefetch and preconnect links to [redacted] blob.core.windows.net with crossorigin attributes." src="https://academy.hackthebox.com/storage/modules/112/cloud3.png"/></p>
<p>Third-party providers such as <a href="https://domain.glass">domain.glass</a> can also tell us a lot about the company's infrastructure. As a positive side effect, we can also see that Cloudflare's security assessment status has been classified as "Safe". This means we have already found a security measure that can be noted for the second layer (gateway).</p>
<h4>Domain.Glass Results</h4>
<p><img alt="Domain status page showing Cloudflare security assessment as safe for [redacted]. Includes social media links, external tools, IP information, and SSL certificate details with issuer and DNS names." src="https://academy.hackthebox.com/storage/modules/112/cloud1.png"/></p>
<p>Another very useful provider is <a href="https://buckets.grayhatwarfare.com">GrayHatWarfare</a>. We can do many different searches, discover AWS, Azure, and GCP cloud storage, and even sort and filter by file format. Therefore, once we have found them through Google, we can also search for them on GrayHatWarefare and passively discover what files are stored on the given cloud storage.</p>
<h4>GrayHatWarfare Results</h4>
<p><img alt="Dashboard showing filter options and a list of three AWS S3 buckets with file counts: 1, 73, and 0." src="https://academy.hackthebox.com/storage/modules/112/cloud2.png"/></p>
<p>Many companies also use abbreviations of the company name, which are then used accordingly within the IT infrastructure. Such terms are also part of an excellent approach to discovering new cloud storage from the company. We can also search for files simultaneously to see the files that can be accessed at the same time.</p>
<h4>Private and Public SSH Keys Leaked</h4>
<p><img alt="Dashboard showing AWS S3 file listings with two entries: 'id_rsa' and 'id_rsa.pub' from [redacted] bucket, dated August 2021." src="https://academy.hackthebox.com/storage/modules/112/ghw1.png"/></p>
<p>Sometimes when employees are overworked or under high pressure, mistakes can be fatal for the entire company. These errors can even lead to SSH private keys being leaked, which anyone can download and log onto one or even more machines in the company without using a password.</p>
<h4>SSH Private Key</h4>
<p><img alt="Image of an RSA private key block, starting with 'BEGIN RSA PRIVATE KEY' and ending with 'END RSA PRIVATE KEY'." src="https://academy.hackthebox.com/storage/modules/112/ghw2.png"/></p>
