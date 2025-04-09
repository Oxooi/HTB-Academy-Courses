
<h1>Intro to File Inclusions</h1>
<p>Many modern back-end languages, such as <code>PHP</code>, <code>Javascript</code>, or <code>Java</code>, use HTTP parameters to specify what is shown on the web page, which allows for building dynamic web pages, reduces the script's overall size, and simplifies the code. In such cases, parameters are used to specify which resource is shown on the page. If such functionalities are not securely coded, an attacker may manipulate these parameters to display the content of any local file on the hosting server, leading to a <a href="https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion">Local File Inclusion (LFI)</a> vulnerability.</p>
<hr/>
<h2>Local File Inclusion (LFI)</h2>
<p>The most common place we usually find LFI within is templating engines. In order to have most of the web application looking the same when navigating between pages, a templating engine displays a page that shows the common static parts, such as the <code>header</code>, <code>navigation bar</code>, and <code>footer</code>, and then dynamically loads other content that changes between pages. Otherwise, every page on the server would need to be modified when changes are made to any of the static parts. This is why we often see a parameter like <code>/index.php?page=about</code>, where <code>index.php</code> sets static content (e.g. header/footer), and then only pulls the dynamic content specified in the parameter, which in this case may be read from a file called <code>about.php</code>. As we have control over the <code>about</code> portion of the request, it may be possible to have the web application grab other files and display them on the page.</p>
<p>LFI vulnerabilities can lead to source code disclosure, sensitive data exposure, and even remote code execution under certain conditions. Leaking source code may allow attackers to test the code for other vulnerabilities, which may reveal previously unknown vulnerabilities. Furthermore, leaking sensitive data may enable attackers to enumerate the remote server for other weaknesses or even leak credentials and keys that may allow them to access the remote server directly. Under specific conditions, LFI may also allow attackers to execute code on the remote server, which may compromise the entire back-end server and any other servers connected to it.</p>
<hr/>
<h2>Examples of Vulnerable Code</h2>
<p>Let's look at some examples of code vulnerable to File Inclusion to understand how such vulnerabilities occur. As mentioned earlier, file Inclusion vulnerabilities can occur in many of the most popular web servers and development frameworks, like <code>PHP</code>, <code>NodeJS</code>, <code>Java</code>, <code>.Net</code>, and many others. Each of them has a slightly different approach to including local files, but they all share one common thing: loading a file from a specified path.</p>
<p>Such a file could be a dynamic header or different content based on the user-specified language. For example, the page may have a <code>?language</code> GET parameter, and if a user changes the language from a drop-down menu, then the same page would be returned but with a different <code>language</code> parameter (e.g. <code>?language=es</code>). In such cases, changing the language may change the directory the web application is loading the pages from (e.g. <code>/en/</code> or <code>/es/</code>). If we have control over the path being loaded, then we may be able to exploit this vulnerability to read other files and potentially reach remote code execution.</p>
<h4>PHP</h4>
<p>In <code>PHP</code>, we may use the <code>include()</code> function to load a local or a remote file as we load a page. If the <code>path</code> passed to the <code>include()</code> is taken from a user-controlled parameter, like a <code>GET</code> parameter, and <code>the code does not explicitly filter and sanitize the user input</code>, then the code becomes vulnerable to File Inclusion. The following code snippet shows an example of that:</p>
<pre><code class="language-php">if (isset($_GET['language'])) {
    include($_GET['language']);
}
</code></pre>
<p>We see that the <code>language</code> parameter is directly passed to the <code>include()</code> function. So, any path we pass in the <code>language</code> parameter will be loaded on the page, including any local files on the back-end server. This is not exclusive to the <code>include()</code> function, as there are many other PHP functions that would lead to the same vulnerability if we had control over the path passed into them. Such functions include <code>include_once()</code>, <code>require()</code>, <code>require_once()</code>, <code>file_get_contents()</code>, and several others as well.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Note:</b> In this module, we will mostly focus on PHP web applications running on a Linux back-end server. However, most techniques and attacks would work on the majority of other frameworks, so our examples would be the same with a web application written in any other language.</p>
</div>
</div>
<h4>NodeJS</h4>
<p>Just as the case with PHP, NodeJS web servers may also load content based on an HTTP parameters. The following is a basic example of how a GET parameter <code>language</code> is used to control what data is written to a page:</p>
<pre><code class="language-javascript">if(req.query.language) {
    fs.readFile(path.join(__dirname, req.query.language), function (err, data) {
        res.write(data);
    });
}
</code></pre>
<p>As we can see, whatever parameter passed from the URL gets used by the <code>readfile</code> function, which then writes the file content in the HTTP response. Another example is the <code>render()</code> function in the <code>Express.js</code> framework. The following example shows how the <code>language</code> parameter is used to determine which directory to pull the <code>about.html</code> page from:</p>
<pre><code class="language-js">app.get("/about/:language", function(req, res) {
    res.render(`/${req.params.language}/about.html`);
});
</code></pre>
<p>Unlike our earlier examples where GET parameters were specified after a (<code>?</code>) character in the URL, the above example takes the parameter from the URL path (e.g. <code>/about/en</code> or <code>/about/es</code>). As the parameter is directly used within the <code>render()</code> function to specify the rendered file, we can change the URL to show a different file instead.</p>
<h4>Java</h4>
<p>The same concept applies to many other web servers. The following examples show how web applications for a Java web server may include local files based on the specified parameter, using the <code>include</code> function:</p>
<pre><code class="language-jsp">&lt;c:if test="${not empty param.language}"&gt;
    &lt;jsp:include file="&lt;%= request.getParameter('language') %&gt;" /&gt;
&lt;/c:if&gt;
</code></pre>
<p>The <code>include</code> function may take a file or a page URL as its argument and then renders the object into the front-end template, similar to the ones we saw earlier with NodeJS. The <code>import</code> function may also be used to render a local file or a URL, such as the following example:</p>
<pre><code class="language-jsp">&lt;c:import url= "&lt;%= request.getParameter('language') %&gt;"/&gt;
</code></pre>
<h4>.NET</h4>
<p>Finally, let's take an example of how File Inclusion vulnerabilities may occur in .NET web applications. The <code>Response.WriteFile</code> function works very similarly to all of our earlier examples, as it takes a file path for its input and writes its content to the response. The path may be retrieved from a GET parameter for dynamic content loading, as follows:</p>
<pre><code class="language-cs">@if (!string.IsNullOrEmpty(HttpContext.Request.Query['language'])) {
    &lt;% Response.WriteFile("&lt;% HttpContext.Request.Query['language'] %&gt;"); %&gt; 
}
</code></pre>
<p>Furthermore, the <code>@Html.Partial()</code> function may also be used to render the specified file as part of the front-end template, similarly to what we saw earlier:</p>
<pre><code class="language-cs">@Html.Partial(HttpContext.Request.Query['language'])
</code></pre>
<p>Finally, the <code>include</code> function may be used to render local files or remote URLs, and may also execute the specified files as well:</p>
<pre><code class="language-cs">&lt;!--#include file="&lt;% HttpContext.Request.Query['language'] %&gt;"--&gt;
</code></pre>
<h2>Read vs Execute</h2>
<p>From all of the above examples, we can see that File Inclusion vulnerabilities may occur in any web server and any development frameworks, as all of them provide functionalities for loading dynamic content and handling front-end templates.</p>
<p>The most important thing to keep in mind is that <code>some of the above functions only read the content of the specified files, while others also execute the specified files</code>. Furthermore, some of them allow specifying remote URLs, while others only work with files local to the back-end server.</p>
<p>The following table shows which functions may execute files and which only read file content:</p>
<table>
<thead>
<tr>
<th><strong>Function</strong></th>
<th align="center"><strong>Read Content</strong></th>
<th align="center"><strong>Execute</strong></th>
<th align="center"><strong>Remote URL</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>PHP</strong></td>
<td align="center"></td>
<td align="center"></td>
<td align="center"></td>
</tr>
<tr>
<td><code>include()</code>/<code>include_once()</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">✅</td>
</tr>
<tr>
<td><code>require()</code>/<code>require_once()</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">❌</td>
</tr>
<tr>
<td><code>file_get_contents()</code></td>
<td align="center">✅</td>
<td align="center">❌</td>
<td align="center">✅</td>
</tr>
<tr>
<td><code>fopen()</code>/<code>file()</code></td>
<td align="center">✅</td>
<td align="center">❌</td>
<td align="center">❌</td>
</tr>
<tr>
<td><strong>NodeJS</strong></td>
<td align="center"></td>
<td align="center"></td>
<td align="center"></td>
</tr>
<tr>
<td><code>fs.readFile()</code></td>
<td align="center">✅</td>
<td align="center">❌</td>
<td align="center">❌</td>
</tr>
<tr>
<td><code>fs.sendFile()</code></td>
<td align="center">✅</td>
<td align="center">❌</td>
<td align="center">❌</td>
</tr>
<tr>
<td><code>res.render()</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">❌</td>
</tr>
<tr>
<td><strong>Java</strong></td>
<td align="center"></td>
<td align="center"></td>
<td align="center"></td>
</tr>
<tr>
<td><code>include</code></td>
<td align="center">✅</td>
<td align="center">❌</td>
<td align="center">❌</td>
</tr>
<tr>
<td><code>import</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">✅</td>
</tr>
<tr>
<td><strong>.NET</strong></td>
<td align="center"></td>
<td align="center"></td>
<td align="center"></td>
</tr>
<tr>
<td><code>@Html.Partial()</code></td>
<td align="center">✅</td>
<td align="center">❌</td>
<td align="center">❌</td>
</tr>
<tr>
<td><code>@Html.RemotePartial()</code></td>
<td align="center">✅</td>
<td align="center">❌</td>
<td align="center">✅</td>
</tr>
<tr>
<td><code>Response.WriteFile()</code></td>
<td align="center">✅</td>
<td align="center">❌</td>
<td align="center">❌</td>
</tr>
<tr>
<td><code>include</code></td>
<td align="center">✅</td>
<td align="center">✅</td>
<td align="center">✅</td>
</tr>
</tbody>
</table>
<p>This is a significant difference to note, as executing files may allow us to execute functions and eventually lead to code execution, while only reading the file's content would only let us to read the source code without code execution. Furthermore, if we had access to the source code in a whitebox exercise or in a code audit, knowing these actions helps us in identifying potential File Inclusion vulnerabilities, especially if they had user-controlled input going into them.</p>
<p>In all cases, File Inclusion vulnerabilities are critical and may eventually lead to compromising the entire back-end server. Even if we were only able to read the web application source code, it may still allow us to compromise the web application, as it may reveal other vulnerabilities as mentioned earlier, and the source code may also contain database keys, admin credentials, or other sensitive information.</p>
