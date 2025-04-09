
<h1>Intercepting Responses</h1>
<hr/>
<p>In some instances, we may need to intercept the HTTP responses from the server before they reach the browser. This can be useful when we want to change how a specific web page looks, like enabling certain disabled fields or showing certain hidden fields, which may help us in our penetration testing activities.</p>
<p>So, let's see how we can achieve that with the exercise we tested in the previous section.</p>
<p>In our previous exercise, the <code>IP</code> field only allowed us to input numeric values. If we intercept the response before it reaches our browser, we can edit it to accept any value, which would enable us to input the payload we used last time directly.</p>
<hr/>
<h2>Burp</h2>
<p>In Burp, we can enable response interception by going to (<code>Proxy&gt;Options</code>) and enabling <code>Intercept Response</code> under <code>Intercept Server Responses</code>:</p>
<p><img alt="Burp Enable Response Int" src="https://academy.hackthebox.com/storage/modules/110/response_interception_enable.jpg"/></p>
<p>After that, we can enable request interception once more and refresh the page with [<code>CTRL+SHIFT+R</code>] in our browser (to force a full refresh). When we go back to Burp, we should see the intercepted request, and we can click on <code>forward</code>. Once we forward the request, we'll see our intercepted response:</p>
<p><img alt="Burp Intercept Response" src="https://academy.hackthebox.com/storage/modules/110/response_intercept_response_1_1.jpg"/></p>
<p>Let's try changing the <code>type="number"</code> on line 27 to <code>type="text"</code>, which should enable us to write any value we want. We will also change the <code>maxlength="3"</code> to <code>maxlength="100"</code> so we can enter longer input:</p>
<pre><code class="language-html">&lt;input type="text" id="ip" name="ip" min="1" max="255" maxlength="100"
    oninput="javascript: if (this.value.length &gt; this.maxLength) this.value = this.value.slice(0, this.maxLength);"
    required&gt;
</code></pre>
<p>Now, once we click on <code>forward</code> again, we can go back to Firefox to examine the edited response:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/110/response_intercept_response_2.jpg"/>
<p>As we can see, we could change the way the page is rendered by the browser and can now input any value we want. We may use the same technique to persistently enable any disabled HTML buttons by modifying their HTML code.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Exercise: Try using the payload we used last time directly within the browser, to test how intercepting responses can make web application penetration testing easier.</p>
</div>
</div>
<hr/>
<h2>ZAP</h2>
<p>Let's try to see how we can do the same with ZAP. As we saw in the previous section, when our requests are intercepted by ZAP, we can click on <code>Step</code>, and it will send the request and automatically intercept the response:</p>
<p><img alt="ZAP Intercept Response" src="https://academy.hackthebox.com/storage/modules/110/zap_response_intercept_response.jpg"/></p>
<p>Once we make the same changes we previously did and click on <code>Continue</code>, we will see that we can also use any input value:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/110/ZAP_edit_response.jpg"/>
<p>However, ZAP HUD also has another powerful feature that can help us in cases like this. While in many instances we may need to intercept the response to make custom changes, if all we wanted was to enable disabled input fields or show hidden input fields, then we can click on the third button on the left (the light bulb icon), and it will enable/show these fields without us having to intercept the response or refresh the page.</p>
<p>For example, the below web application has the <code>IP</code> input field as disabled:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/110/ZAP_disabled_field.jpg"/>
<p>In these cases, we can click on the <code>Show/Enable</code> button, and it will enable the button for us, and we can interact with it to add our input:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/110/ZAP_enable_field.jpg"/>
<p>We can similarly use this feature to show all hidden fields or buttons. <code>Burp</code> also has a similar feature, which we can enable under <code>Proxy&gt;Options&gt;Response Modification</code>, then select one of the options, like <code>Unhide hidden form fields</code>.</p>
<p>Another similar feature is the <code>Comments</code> button, which will indicate the positions where there are HTML comments that are usually only visible in the source code. We can click on the <code>+</code> button on the left pane and select <code>Comments</code> to add the <code>Comments</code> button, and once we click on it, the <code>Comments</code> indicators should be shown. For example, the below screenshot shows an indicator for a position that has a comment, and hovering over it with our cursor shows the comment's content:</p>
<img class="website-screenshot" data-url="http://SERVER_IP:PORT/" src="/storage/modules/110/ZAP_show_comments.jpg"/>
<p>Being able to modify how the web page looks makes it much easier for us to perform web application penetration testing in certain scenarios instead of having to send our input through an intercepted request. Next, we will see how we can automate this process to modify our changes in the response automatically so we don't have to keep intercepting and manually changing the responses.</p>
