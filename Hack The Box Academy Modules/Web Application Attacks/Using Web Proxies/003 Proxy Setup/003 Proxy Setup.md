
<h1>Proxy Setup</h1>
<hr/>
<p>Now that we have installed and started both tools, we'll learn how to use the most commonly used feature; <code>Web Proxy</code>.</p>
<p>We can set up these tools as a proxy for any application, such that all web requests would be routed through them so that we can manually examine what web requests an application is sending and receiving. This will enable us to understand better what the application is doing in the background and allows us to intercept and change these requests or reuse them with various changes to see how the application responds.</p>
<hr/>
<h2>Pre-Configured Browser</h2>
<p>To use the tools as web proxies, we must configure our browser proxy settings to use them as the proxy or use the pre-configured browser. Both tools have a pre-configured browser that comes with pre-configured proxy settings and the CA certificates pre-installed, making starting a web penetration test very quick and easy.</p>
<p>In Burp's (<code>Proxy&gt;Intercept</code>), we can click on <code>Open Browser</code>, which will open Burp's pre-configured browser, and automatically route all web traffic through Burp:
<img alt="Burp Preconfigured Browser" src="https://academy.hackthebox.com/storage/modules/110/burp_preconfigured_browser.jpg"/></p>
<p>In ZAP, we can click on the Firefox browser icon at the end of the top bar, and it will open the pre-configured browser:</p>
<p><img alt="ZAP Preconfigured Browser" src="https://academy.hackthebox.com/storage/modules/110/zap_preconfigured_browser.jpg"/></p>
<p>For our uses in this module, using the pre-configured browser should be enough.</p>
<hr/>
<h2>Proxy Setup</h2>
<p>In many cases, we may want to use a real browser for pentesting, like Firefox. To use Firefox with our web proxy tools, we must first configure it to use them as the proxy. We can manually go to Firefox preferences and set up the proxy to use the web proxy listening port. Both Burp and ZAP use port <code>8080</code> by default, but we can use any available port. If we choose a port that is in use, the proxy will fail to start, and we will receive an error message.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> In case we wanted to serve the web proxy on a different port, we can do that in Burp under (<code>Proxy&gt;Options</code>), or in ZAP under (<code>Tools&gt;Options&gt;Local Proxies</code>). In both cases, we must ensure that the proxy configured in Firefox uses the same port.</p>
</div>
</div>
<p>Instead of manually switching the proxy, we can utilize the Firefox extension <a href="https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/">Foxy Proxy</a> to easily and quickly change the Firefox proxy. This extension is pre-installed in your PwnBox instance and can be installed to your own Firefox browser by visiting the <a href="https://addons.mozilla.org/en-US/firefox/addon/foxyproxy-standard/">Firefox Extensions Page</a> and clicking <code>Add to Firefox</code> to install it.</p>
<p>Once we have the extension added, we can configure the web proxy on it by clicking on its icon on Firefox top bar and then choosing <code>options</code>:</p>
<p><img alt="Foxyproxy Options" src="https://academy.hackthebox.com/storage/modules/110/foxyproxy_options.jpg"/></p>
<p>Once we're on the <code>options</code> page, we can click on <code>add</code> on the left pane, and then use <code>127.0.0.1</code> as the IP, and <code>8080</code> as the port, and name it <code>Burp</code> or <code>ZAP</code>:</p>
<p><img alt="Foxyproxy Add" src="https://academy.hackthebox.com/storage/modules/110/foxyproxy_add.jpg"/></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: This configuration is already added to Foxy Proxy in PwnBox, so you don't have to do this step if you are using PwnBox.</p>
</div>
</div>
<p>Finally, we can click on the <code>Foxy Proxy</code> icon and select <code>Burp</code>/<code>ZAP</code>.
<img alt="Foxyproxy Use" src="https://academy.hackthebox.com/storage/modules/110/foxyproxy_use.jpg"/></p>
<hr/>
<h2>Installing CA Certificate</h2>
<p>Another important step when using Burp Proxy/ZAP with our browser is to install the web proxy's CA Certificates. If we don't do this step, some HTTPS traffic may not get properly routed, or we may need to click <code>accept</code> every time Firefox needs to send an HTTPS request.</p>
<p>We can install Burp's certificate once we select Burp as our proxy in <code>Foxy Proxy</code>, by browsing to <code>http://burp</code>, and download the certificate from there by clicking on <code>CA Certificate</code>:</p>
<img class="website-screenshot" data-url="http://burp" src="/storage/modules/110/burp_cert.jpg"/>
<p>To get ZAP's certificate, we can go to (<code>Tools&gt;Options&gt;Dynamic SSL Certificate</code>), then click on <code>Save</code>:</p>
<p><img alt="ZAP cert" src="https://academy.hackthebox.com/storage/modules/110/zap_cert.jpg"/></p>
<p>We can also change our certificate by generating a new one with the <code>Generate</code> button.</p>
<p>Once we have our certificates, we can install them within Firefox by browsing to <a href="about:preferences#privacy">about:preferences#privacy</a>, scrolling to the bottom, and clicking <code>View Certificates</code>:</p>
<p><img alt="Cert Firefox" src="https://academy.hackthebox.com/storage/modules/110/firefox_cert.jpg"/></p>
<p>After that, we can select the <code>Authorities</code> tab, and then click on <code>import</code>, and select the downloaded CA certificate:</p>
<p><img alt="Import Firefox Cert" src="https://academy.hackthebox.com/storage/modules/110/firefox_import_cert.jpg"/></p>
<p>Finally, we must select <code>Trust this CA to identify websites</code> and <code>Trust this CA to identify email users</code>, and then click OK:
<img alt="Trust Firefox Cert" src="https://academy.hackthebox.com/storage/modules/110/firefox_trust_cert.jpg"/></p>
<p>Once we install the certificate and configure the Firefox proxy, all Firefox web traffic will start routing through our web proxy.</p>
