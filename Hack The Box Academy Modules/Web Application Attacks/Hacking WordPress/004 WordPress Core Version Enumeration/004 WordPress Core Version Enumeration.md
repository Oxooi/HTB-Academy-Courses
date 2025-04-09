
<h1>WordPress Core Version Enumeration</h1>
<p>It is always important to know what type of application we are working with. An essential part of the enumeration phase is uncovering the software version number. This is helpful when searching for common misconfigurations such as default passwords that may be set for certain versions of an application and searching for known vulnerabilities for a particular version number. We can use a variety of methods to discover the version number manually. The first and easiest step is reviewing the page source code. We can do this by right-clicking anywhere on the current page and selecting "View page source" from the menu or using the keyboard shortcut <code>[CTRL + U]</code>.</p>
<p>We can search for the <code>meta generator</code> tag using the shortcut <code>[CTRL + F]</code> in the browser or use <code>cURL</code> along with <code>grep</code> from the command line to filter for this information.</p>
<h4>WP Version - Source Code</h4>
<pre><code class="language-html">...SNIP...
&lt;link rel='https://api.w.org/' href='http://blog.inlanefreight.com/index.php/wp-json/' /&gt;
&lt;link rel="EditURI" type="application/rsd+xml" title="RSD" href="http://blog.inlanefreight.com/xmlrpc.php?rsd" /&gt;
&lt;link rel="wlwmanifest" type="application/wlwmanifest+xml" href="http://blog.inlanefreight.com/wp-includes/wlwmanifest.xml" /&gt; 
&lt;meta name="generator" content="WordPress 5.3.3" /&gt;
...SNIP...
</code></pre>
<pre><code class="language-shell-session">[!bash!]$ curl -s -X GET http://blog.inlanefreight.com | grep '&lt;meta name="generator"'

&lt;meta name="generator" content="WordPress 5.3.3" /&gt;
</code></pre>
<p>Aside from version information, the source code may also contain comments that may be useful. Links to CSS (style sheets) and JS  (JavaScript) can also provide hints about the version number.</p>
<h4>WP Version - CSS</h4>
<pre><code class="language-html">...SNIP...
&lt;link rel='stylesheet' id='bootstrap-css'  href='http://blog.inlanefreight.com/wp-content/themes/ben_theme/css/bootstrap.css?ver=5.3.3' type='text/css' media='all' /&gt;
&lt;link rel='stylesheet' id='transportex-style-css'  href='http://blog.inlanefreight.com/wp-content/themes/ben_theme/style.css?ver=5.3.3' type='text/css' media='all' /&gt;
&lt;link rel='stylesheet' id='transportex_color-css'  href='http://blog.inlanefreight.com/wp-content/themes/ben_theme/css/colors/default.css?ver=5.3.3' type='text/css' media='all' /&gt;
&lt;link rel='stylesheet' id='smartmenus-css'  href='http://blog.inlanefreight.com/wp-content/themes/ben_theme/css/jquery.smartmenus.bootstrap.css?ver=5.3.3' type='text/css' media='all' /&gt;
...SNIP...
</code></pre>
<h4>WP Version - JS</h4>
<pre><code class="language-html">...SNIP...
&lt;script type='text/javascript' src='http://blog.inlanefreight.com/wp-includes/js/jquery/jquery.js?ver=1.12.4-wp'&gt;&lt;/script&gt;
&lt;script type='text/javascript' src='http://blog.inlanefreight.com/wp-includes/js/jquery/jquery-migrate.min.js?ver=1.4.1'&gt;&lt;/script&gt;
&lt;script type='text/javascript' src='http://blog.inlanefreight.com/wp-content/plugins/mail-masta/lib/subscriber.js?ver=5.3.3'&gt;&lt;/script&gt;
&lt;script type='text/javascript' src='http://blog.inlanefreight.com/wp-content/plugins/mail-masta/lib/jquery.validationEngine-en.js?ver=5.3.3'&gt;&lt;/script&gt;
&lt;script type='text/javascript' src='http://blog.inlanefreight.com/wp-content/plugins/mail-masta/lib/jquery.validationEngine.js?ver=5.3.3'&gt;&lt;/script&gt;
...SNIP...
</code></pre>
<p>In older WordPress versions, another source for uncovering version information is the <code>readme.html</code> file in WordPress's root directory.</p>
