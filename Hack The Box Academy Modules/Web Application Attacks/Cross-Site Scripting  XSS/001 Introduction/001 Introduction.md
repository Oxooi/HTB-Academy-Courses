
<h1>Introduction</h1>
<p>As web applications become more advanced and more common, so do web application vulnerabilities. Among the most common types of web application vulnerabilities are <a href="https://owasp.org/www-community/attacks/xss/">Cross-Site Scripting (XSS)</a> vulnerabilities. XSS vulnerabilities take advantage of a flaw in user input sanitization to "write" JavaScript code to the page and execute it on the client side, leading to several types of attacks.</p>
<hr/>
<h2>What is XSS</h2>
<p>A typical web application works by receiving the HTML code from the back-end server and rendering it on the client-side internet browser. When a vulnerable web application does not properly sanitize user input, a malicious user can inject extra JavaScript code in an input field (e.g., comment/reply), so once another user views the same page, they unknowingly execute the malicious JavaScript code.</p>
<p>XSS vulnerabilities are solely executed on the client-side and hence do not directly affect the back-end server. They can only affect the user executing the vulnerability. The direct impact of XSS vulnerabilities on the back-end server may be relatively low, but they are very commonly found in web applications, so this equates to a medium risk (<code>low impact + high probability = medium risk</code>), which we should always attempt to <code>reduce</code> risk by detecting, remediating, and proactively preventing these types of vulnerabilities.</p>
<p><img alt="xss risk" src="https://academy.hackthebox.com/storage/modules/103/xss_risk_chart_1.jpg"/></p>
<hr/>
<h2>XSS Attacks</h2>
<p>XSS vulnerabilities can facilitate a wide range of attacks, which can be anything that can be executed through browser JavaScript code. A basic example of an XSS attack is having the target user unwittingly send their session cookie to the attacker's web server. Another example is having the target's browser execute API calls that lead to a malicious action, like changing the user's password to a password of the attacker's choosing. There are many other types of XSS attacks, from Bitcoin mining to displaying ads.</p>
<p>As XSS attacks execute JavaScript code within the browser, they are limited to the browser's JS engine (i.e., V8 in Chrome). They cannot execute system-wide JavaScript code to do something like system-level code execution. In modern browsers, they are also limited to the same domain of the vulnerable website. Nevertheless, being able to execute JavaScript in a user's browser may still lead to a wide variety of attacks, as mentioned above. In addition to this, if a skilled researcher identifies a binary vulnerability in a web browser (e.g., a Heap overflow in Chrome), they can utilize an XSS vulnerability to execute a JavaScript exploit on the target's browser, which eventually breaks out of the browser's sandbox and executes code on the user's machine.</p>
<p>XSS vulnerabilities may be found in almost all modern web applications and have been actively exploited for the past two decades. A well-known XSS example is the <a href="https://en.wikipedia.org/wiki/Samy_(computer_worm)">Samy Worm</a>, which was a browser-based worm that exploited a stored XSS vulnerability in the social networking website MySpace back in 2005. It executed when viewing an infected webpage by posting a message on the victim's MySpace page that read, "Samy is my hero." The message itself also contained the same JavaScript payload to re-post the same message when viewed by others. Within a single day, more than a million MySpace users had this message posted on their pages. Even though this specific payload did not do any actual harm, the vulnerability could have been utilized for much more nefarious purposes, like stealing users' credit card information, installing key loggers on their browsers, or even exploiting a binary vulnerability in user's web browsers (which was more common in web browsers back then).</p>
<p>In 2014, a security researcher accidentally identified an <a href="https://blog.sucuri.net/2014/06/serious-cross-site-scripting-vulnerability-in-tweetdeck-twitter.html">XSS vulnerability</a> in Twitter's TweetDeck dashboard. This vulnerability was exploited to create a <a href="https://twitter.com/derGeruhn/status/476764918763749376">self-retweeting tweet</a> in Twitter, which led the tweet to be retweeted more than 38,000 times in under two minutes. Eventually, it forced Twitter to <a href="https://www.theguardian.com/technology/2014/jun/11/twitter-tweetdeck-xss-flaw-users-vulnerable">temporarily shut down TweetDeck</a> while they patched the vulnerability.</p>
<p>To this day, even the most prominent web applications have XSS vulnerabilities that can be exploited. Even Google's search engine page had multiple XSS vulnerabilities in its search bar, the most recent of which was in <a href="https://www.acunetix.com/blog/web-security-zone/mutation-xss-in-google-search/">2019</a> when an XSS vulnerability was found in the XML library. Furthermore, the Apache Server, the most commonly used web server on the internet, once reported an <a href="https://blogs.apache.org/infra/entry/apache_org_04_09_2010">XSS Vulnerability</a> that was being actively exploited to steal user passwords of certain companies. All of this tells us that XSS vulnerabilities should be taken seriously, and a good amount of effort should be put towards detecting and preventing them.</p>
<hr/>
<h2>Types of XSS</h2>
<p>There are three main types of XSS vulnerabilities:</p>
<table>
<thead>
<tr>
<th>Type</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Stored (Persistent) XSS</code></td>
<td>The most critical type of XSS, which occurs when user input is stored on the back-end database and then displayed upon retrieval (e.g., posts or comments)</td>
</tr>
<tr>
<td><code>Reflected (Non-Persistent) XSS</code></td>
<td>Occurs when user input is displayed on the page after being processed by the backend server, but without being stored (e.g., search result or error message)</td>
</tr>
<tr>
<td><code>DOM-based XSS</code></td>
<td>Another Non-Persistent XSS type that occurs when user input is directly shown in the browser and is completely processed on the client-side, without reaching the back-end server (e.g., through client-side HTTP parameters or anchor tags)</td>
</tr>
</tbody>
</table>
<p>We will cover each of these types in the upcoming sections and work through exercises to see how each of them occurs, and then we will also see how each of them can be utilized in attacks.</p>
