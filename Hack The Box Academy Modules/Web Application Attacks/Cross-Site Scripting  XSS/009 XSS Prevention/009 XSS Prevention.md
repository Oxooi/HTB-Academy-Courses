
<h1>XSS Prevention</h1>
<hr/>
<p>By now, we should have a good understanding of what an XSS vulnerability is and its different types, how to detect an XSS vulnerability, and how to exploit XSS vulnerabilities. We will conclude the module by learning how to defend against XSS vulnerabilities.</p>
<p>As discussed previously, XSS vulnerabilities are mainly linked to two parts of the web application: A <code>Source</code> like a user input field and a <code>Sink</code> that displays the input data. These are the main two points that we should focus on securing, both in the front-end and in the back-end.</p>
<p>The most important aspect of preventing XSS vulnerabilities is proper input sanitization and validation on both the front and back end. In addition to that, other security measures can be taken to help prevent XSS attacks.</p>
<hr/>
<h2>Front-end</h2>
<p>As the front-end of the web application is where most (but not all) of the user input is taken from, it is essential to sanitize and validate the user input on the front-end using JavaScript.</p>
<h4>Input Validation</h4>
<p>For example, in the exercise of the <code>XSS Discovery</code> section, we saw that the web application will not allow us to submit the form if the email format is invalid. This was done with the following JavaScript code:</p>
<pre><code class="language-javascript">function validateEmail(email) {
    const re = /^(([^&lt;&gt;()[\]\\.,;:\s@\"]+(\.[^&lt;&gt;()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test($("#login input[name=email]").val());
}
</code></pre>
<p>As we can see, this code is testing the <code>email</code> input field and returning <code>true</code> or <code>false</code> whether it matches the Regex validation of an email format.</p>
<h4>Input Sanitization</h4>
<p>In addition to input validation, we should always ensure that we do not allow any input with JavaScript code in it, by escaping any special characters. For this, we can utilize the <a href="https://github.com/cure53/DOMPurify">DOMPurify</a> JavaScript library, as follows:</p>
<pre><code class="language-javascript">&lt;script type="text/javascript" src="dist/purify.min.js"&gt;&lt;/script&gt;
let clean = DOMPurify.sanitize( dirty );
</code></pre>
<p>This will escape any special characters with a backslash <code>\</code>, which should help ensure that a user does not send any input with special characters (like JavaScript code), which should prevent vulnerabilities like DOM XSS.</p>
<h4>Direct Input</h4>
<p>Finally, we should always ensure that we never use user input directly within certain HTML tags, like:</p>
<ol>
<li>JavaScript code <code>&lt;script&gt;&lt;/script&gt;</code>
</li>
<li>CSS Style Code <code>&lt;style&gt;&lt;/style&gt;</code>
</li>
<li>Tag/Attribute Fields <code>&lt;div name='INPUT'&gt;&lt;/div&gt;</code>
</li>
<li>HTML Comments <code>&lt;!-- --&gt;</code>
</li>
</ol>
<p>If user input goes into any of the above examples, it can inject malicious JavaScript code, which may lead to an XSS vulnerability. In addition to this, we should avoid using JavaScript functions that allow changing raw text of HTML fields, like:</p>
<ul>
<li>
<code>DOM.innerHTML</code>
</li>
<li>
<code>DOM.outerHTML</code>
</li>
<li>
<code>document.write()</code>
</li>
<li>
<code>document.writeln()</code>
</li>
<li>
<code>document.domain</code>
</li>
</ul>
<p>And the following jQuery functions:</p>
<ul>
<li>
<code>html()</code>
</li>
<li>
<code>parseHTML()</code>
</li>
<li>
<code>add()</code>
</li>
<li>
<code>append()</code>
</li>
<li>
<code>prepend()</code>
</li>
<li>
<code>after()</code>
</li>
<li>
<code>insertAfter()</code>
</li>
<li>
<code>before()</code>
</li>
<li>
<code>insertBefore()</code>
</li>
<li>
<code>replaceAll()</code>
</li>
<li>
<code>replaceWith()</code>
</li>
</ul>
<p>As these functions write raw text to the HTML code, if any user input goes into them, it may include malicious JavaScript code, which leads to an XSS vulnerability.</p>
<hr/>
<h2>Back-end</h2>
<p>On the other end, we should also ensure that we prevent XSS vulnerabilities with measures on the back-end to prevent Stored and Reflected XSS vulnerabilities. As we saw in the <code>XSS Discovery</code> section exercise, even though it had front-end input validation, this was not enough to prevent us from injecting a malicious payload into the form. So, we should have XSS prevention measures on the back-end as well. This can be achieved with Input and Output Sanitization and Validation, Server Configuration, and Back-end Tools that help prevent XSS vulnerabilities.</p>
<h4>Input Validation</h4>
<p>Input validation in the back-end is quite similar to the front-end, and it uses Regex or library functions to ensure that the input field is what is expected. If it does not match, then the back-end server will reject it and not display it.</p>
<p>An example of E-Mail validation on a PHP back-end is the following:</p>
<pre><code class="language-php">if (filter_var($_GET['email'], FILTER_VALIDATE_EMAIL)) {
    // do task
} else {
    // reject input - do not display it
}
</code></pre>
<p>For a NodeJS back-end, we can use the same JavaScript code mentioned earlier for the front-end.</p>
<h4>Input Sanitization</h4>
<p>When it comes to input sanitization, then the back-end plays a vital role, as front-end input sanitization can be easily bypassed by sending custom <code>GET</code> or <code>POST</code> requests. Luckily, there are very strong libraries for various back-end languages that can properly sanitize any user input, such that we ensure that no injection can occur.</p>
<p>For example, for a PHP back-end, we can use the <code>addslashes</code> function to sanitize user input by escaping special characters with a backslash:</p>
<pre><code class="language-php">addslashes($_GET['email'])
</code></pre>
<p>In any case, direct user input (e.g. <code>$_GET['email']</code>) should never be directly displayed on the page, as this can lead to XSS vulnerabilities.</p>
<p>For a NodeJS back-end, we can also use the <a href="https://github.com/cure53/DOMPurify">DOMPurify</a> library as we did with the front-end, as follows:</p>
<pre><code class="language-javascript">import DOMPurify from 'dompurify';
var clean = DOMPurify.sanitize(dirty);
</code></pre>
<h4>Output HTML Encoding</h4>
<p>Another important aspect to pay attention to in the back-end is <code>Output Encoding</code>. This means that we have to encode any special characters into their HTML codes, which is helpful if we need to display the entire user input without introducing an XSS vulnerability. For a PHP back-end, we can use the <code>htmlspecialchars</code> or the <code>htmlentities</code> functions, which would encode certain special characters into their HTML codes (e.g. <code>&lt;</code> into <code>&amp;lt;</code>), so the browser will display them correctly, but they will not cause any injection of any sort:</p>
<pre><code class="language-php">htmlentities($_GET['email']);
</code></pre>
<p>For a NodeJS back-end, we can use any library that does HTML encoding, like <code>html-entities</code>, as follows:</p>
<pre><code class="language-javascript">import encode from 'html-entities';
encode('&lt;'); // -&gt; '&amp;lt;'
</code></pre>
<p>Once we ensure that all user input is validated, sanitized, and encoded on output, we should significantly reduce the risk of having XSS vulnerabilities.</p>
<h4>Server Configuration</h4>
<p>In addition to the above, there are certain back-end web server configurations that may help in preventing XSS attacks, such as:</p>
<ul>
<li>Using HTTPS across the entire domain.</li>
<li>Using XSS prevention headers.</li>
<li>Using the appropriate Content-Type for the page, like <code>X-Content-Type-Options=nosniff</code>.</li>
<li>Using <code>Content-Security-Policy</code> options, like <code>script-src 'self'</code>, which only allows locally hosted scripts.</li>
<li>Using the <code>HttpOnly</code> and <code>Secure</code> cookie flags to prevent JavaScript from reading cookies and only transport them over HTTPS.</li>
</ul>
<p>In addition to the above, having a good <code>Web Application Firewall (WAF)</code> can significantly reduce the chances of XSS exploitation, as it will automatically detect any type of injection going through HTTP requests and will automatically reject such requests. Furthermore, some frameworks provide built-in XSS protection, like <a href="https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting?view=aspnetcore-7.0">ASP.NET</a>.</p>
<p>In the end, we must do our best to secure our web applications against XSS vulnerabilities using such XSS prevention techniques. Even after all of this is done, we should practice all of the skills we learned in this module and attempt to identify and exploit XSS vulnerabilities in any potential input fields, as secure coding and secure configurations may still leave gaps and vulnerabilities that can be exploited. If we practice defending the website using both <code>offensive</code> and <code>defensive</code> techniques, we should reach a reliable level of security against XSS vulnerabilities.</p>
