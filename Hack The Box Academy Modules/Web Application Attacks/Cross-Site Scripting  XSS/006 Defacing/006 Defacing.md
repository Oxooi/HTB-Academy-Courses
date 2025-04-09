
<h1>Defacing</h1>
<hr/>
<p>Now that we understand the different types of XSS and various methods of discovering XSS vulnerabilities in web pages, we can start learning how to exploit these XSS vulnerabilities. As previously mentioned, the damage and the scope of an XSS attack depends on the type of XSS, a stored XSS being the most critical, while a DOM-based being less so.</p>
<p>One of the most common attacks usually used with stored XSS vulnerabilities is website defacing attacks. <code>Defacing</code> a website means changing its look for anyone who visits the website. It is very common for hacker groups to deface a website to claim that they had successfully hacked it, like when hackers defaced the UK National Health Service (NHS) <a href="https://www.bbc.co.uk/news/technology-43812539">back in 2018</a>. Such attacks can carry great media echo and may significantly affect a company's investments and share prices, especially for banks and technology firms.</p>
<p>Although many other vulnerabilities may be utilized to achieve the same thing, stored XSS vulnerabilities are among the most used vulnerabilities for doing so.</p>
<hr/>
<h2>Defacement Elements</h2>
<p>We can utilize injected JavaScript code (through XSS) to make a web page look any way we like. However, defacing a website is usually used to send a simple message (i.e., we successfully hacked you), so giving the defaced web page a beautiful look isn't really the primary target.</p>
<p>Four HTML elements are usually utilized to change the main look of a web page:</p>
<ul>
<li>Background Color <code>document.body.style.background</code>
</li>
<li>Background <code>document.body.background</code>
</li>
<li>Page Title <code>document.title</code>
</li>
<li>Page Text <code>DOM.innerHTML</code>
</li>
</ul>
<p>We can utilize two or three of these elements to write a basic message to the web page and even remove the vulnerable element, such that it would be more difficult to quickly reset the web page, as we will see next.</p>
<hr/>
<h2>Changing Background</h2>
<p>Let's go back to our <code>Stored XSS</code> exercise and use it as a basis for our attack. You can go back to the <code>Stored XSS</code> section to spawn the server and follow the next steps.</p>
<p>To change a web page's background, we can choose a certain color or use an image. We will use a color as our background since most defacing attacks use a dark color for the background. To do so, we can use the following payload:</p>
<pre><code class="language-html">&lt;script&gt;document.body.style.background = "#141d2b"&lt;/script&gt;
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Tip: Here we set the background color to the default Hack The Box background color. We can use any other hex value, or can use a named color like <code> = "black"</code>.</p>
</div>
</div>
<p>Once we add our payload to the <code>To-Do</code> list, we will see that the background color changed:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/103/xss_defacing_background_color.jpg"/>
<p>This will be persistent through page refreshes and will appear for anyone who visits the page, as we are utilizing a stored XSS vulnerability.</p>
<p>Another option would be to set an image to the background using the following payload:</p>
<pre><code class="language-html">&lt;script&gt;document.body.background = "https://www.hackthebox.eu/images/logo-htb.svg"&lt;/script&gt;
</code></pre>
<p>Try using the above payload to see how the final result may look.</p>
<hr/>
<h2>Changing Page Title</h2>
<p>We can change the page title from <code>2Do</code> to any title of our choosing, using the <code>document.title</code> JavaScript property:</p>
<pre><code class="language-html">&lt;script&gt;document.title = 'HackTheBox Academy'&lt;/script&gt;
</code></pre>
<p>We can see from the page window/tab that our new title has replaced the previous one:
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/103/xss_defacing_page_title.jpg"/></p>
<hr/>
<h2>Changing Page Text</h2>
<p>When we want to change the text displayed on the web page, we can utilize various JavaScript functions for doing so. For example, we can change the text of a specific HTML element/DOM using the <code>innerHTML</code> property:</p>
<pre><code class="language-javascript">document.getElementById("todo").innerHTML = "New Text"
</code></pre>
<p>We can also utilize jQuery functions for more efficiently achieving the same thing or for changing the text of multiple elements in one line (to do so, the <code>jQuery</code> library must have been imported within the page source):</p>
<pre><code class="language-javascript">$("#todo").html('New Text');
</code></pre>
<p>This gives us various options to customize the text on the web page and make minor adjustments to meet our needs. However, as hacking groups usually leave a simple message on the web page and leave nothing else on it, we will change the entire HTML code of the main <code>body</code>, using <code>innerHTML</code>, as follows:</p>
<pre><code class="language-javascript">document.getElementsByTagName('body')[0].innerHTML = "New Text"
</code></pre>
<p>As we can see, we can specify the <code>body</code> element with <code>document.getElementsByTagName('body')</code>, and by specifying <code>[0]</code>, we are selecting the first <code>body</code> element, which should change the entire text of the web page. We may also use <code>jQuery</code> to achieve the same thing. However, before sending our payload and making a permanent change, we should prepare our HTML code separately and then use <code>innerHTML</code> to set our HTML code to the page source.</p>
<p>For our exercise, we will borrow the HTML code from the main page of <code>Hack The Box Academy</code>:</p>
<pre><code class="language-html">&lt;center&gt;
    &lt;h1 style="color: white"&gt;Cyber Security Training&lt;/h1&gt;
    &lt;p style="color: white"&gt;by 
        &lt;img src="https://academy.hackthebox.com/images/logo-htb.svg" height="25px" alt="HTB Academy"&gt;
    &lt;/p&gt;
&lt;/center&gt;
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Tip:</b> It would be wise to try running our HTML code locally to see how it looks and to ensure that it runs as expected, before we commit to it in our final payload.</p>
</div>
</div>
<p>We will minify the HTML code into a single line and add it to our previous XSS payload. The final payload should be as follows:</p>
<pre><code class="language-html">&lt;script&gt;document.getElementsByTagName('body')[0].innerHTML = '&lt;center&gt;&lt;h1 style="color: white"&gt;Cyber Security Training&lt;/h1&gt;&lt;p style="color: white"&gt;by &lt;img src="https://academy.hackthebox.com/images/logo-htb.svg" height="25px" alt="HTB Academy"&gt; &lt;/p&gt;&lt;/center&gt;'&lt;/script&gt;
</code></pre>
<p>Once we add our payload to the vulnerable <code>To-Do</code> list, we will see that our HTML code is now permanently part of the web page's source code and shows our message for anyone who visits the page:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/103/xss_defacing_change_text.jpg"/>
<p>By using three XSS payloads, we were able to successfully deface our target web page. If we look at the source code of the web page, we will see the original source code still exists, and our injected payloads appear at the end:</p>
<pre><code class="language-html">&lt;div&gt;&lt;/div&gt;&lt;ul class="list-unstyled" id="todo"&gt;&lt;ul&gt;
&lt;script&gt;document.body.style.background = "#141d2b"&lt;/script&gt;
&lt;/ul&gt;&lt;ul&gt;&lt;script&gt;document.title = 'HackTheBox Academy'&lt;/script&gt;
&lt;/ul&gt;&lt;ul&gt;&lt;script&gt;document.getElementsByTagName('body')[0].innerHTML = '...SNIP...'&lt;/script&gt;
&lt;/ul&gt;&lt;/ul&gt;
</code></pre>
<p>This is because our injected JavaScript code changes the look of the page when it gets executed, which in this case, is at the end of the source code. If our injection was in an element in the middle of the source code, then other scripts or elements may get added after it, so we would have to account for them to get the final look we need.</p>
<p>However, to ordinary users, the page looks defaced and shows our new look.</p>
