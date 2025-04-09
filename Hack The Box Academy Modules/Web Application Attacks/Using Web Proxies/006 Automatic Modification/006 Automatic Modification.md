
<h1>Automatic Modification</h1>
<hr/>
<p>We may want to apply certain modifications to all outgoing HTTP requests or all incoming HTTP responses in certain situations. In these cases, we can utilize automatic modifications based on rules we set, so the web proxy tools will automatically apply them.</p>
<hr/>
<h2>Automatic Request Modification</h2>
<p>Let us start with an example of automatic request modification. We can choose to match any text within our requests, either in the request header or request body, and then replace them with different text. For the sake of demonstration, let's replace our <code>User-Agent</code> with <code>HackTheBox Agent 1.0</code>, which may be handy in cases where we may be dealing with filters that block certain User-Agents.</p>
<h4>Burp Match and Replace</h4>
<p>We can go to (<code>Proxy&gt;Options&gt;Match and Replace</code>) and click on <code>Add</code> in Burp. As the below screenshot shows, we will set the following options:</p>
<p><img alt="Burp Match Replace" src="https://academy.hackthebox.com/storage/modules/110/burp_match_replace_user_agent_1.jpg"/></p>
<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Type</code>: <code>Request header</code></td>
<td>Since the change we want to make will be in the request header and not in its body.</td>
</tr>
<tr>
<td><code>Match</code>: <code>^User-Agent.*$</code></td>
<td>The regex pattern that matches the entire line with <code>User-Agent</code> in it.</td>
</tr>
<tr>
<td><code>Replace</code>: <code>User-Agent: HackTheBox Agent 1.0</code></td>
<td>This is the value that will replace the line we matched above.</td>
</tr>
<tr>
<td><code>Regex match</code>: True</td>
<td>We don't know the exact User-Agent string we want to replace, so we'll use regex to match any value that matches the pattern we specified above.</td>
</tr>
</tbody>
</table>
<p>Once we enter the above options and click <code>Ok</code>, our new Match and Replace option will be added and enabled and will start automatically replacing the <code>User-Agent</code> header in our requests with our new User-Agent. We can verify that by visiting any website using the pre-configured Burp browser and reviewing the intercepted request. We will see that our User-Agent has indeed been automatically replaced:</p>
<p><img alt="Burp Match Replace" src="https://academy.hackthebox.com/storage/modules/110/burp_match_replace_user_agent_2.jpg"/></p>
<h4>ZAP Replacer</h4>
<p>ZAP has a similar feature called <code>Replacer</code>, which we can access by pressing [<code>CTRL+R</code>] or clicking on <code>Replacer</code> in ZAP's options menu. It is fairly similar to what we did above, so we can click on <code>Add</code> and add the same options we used earlier:</p>
<p><img alt="ZAP Match Replace" src="https://academy.hackthebox.com/storage/modules/110/zap_match_replace_user_agent_1.jpg"/></p>
<ul>
<li>
<code>Description</code>: <code>HTB User-Agent</code>.</li>
<li>
<code>Match Type</code>: <code>Request Header (will add if not present)</code>.</li>
<li>
<code>Match String</code>: <code>User-Agent</code>. We can select the header we want from the drop-down menu, and ZAP will replace its value.</li>
<li>
<code>Replacement String</code>: <code>HackTheBox Agent 1.0</code>.</li>
<li>
<code>Enable</code>: True.</li>
</ul>
<p>ZAP also has the <code>Request Header String</code> that we can use with a Regex pattern. <code>Try using this option with the same values we used for Burp to see how it works.</code></p>
<p>ZAP also provides the option to set the <code>Initiators</code>, which we can access by clicking on the other tab in the windows shown above. Initiators enable us to select where our <code>Replacer</code> option will be applied. We will keep the default option of <code>Apply to all HTTP(S) messages</code> to apply everywhere.</p>
<p>We can now enable request interception by pressing [<code>CTRL+B</code>], then can visit any page in the pre-configured ZAP browser:</p>
<p><img alt="ZAP Match Replace" src="https://academy.hackthebox.com/storage/modules/110/zap_match_replace_user_agent_2.jpg"/></p>
<hr/>
<h2>Automatic Response Modification</h2>
<p>The same concept can be used with HTTP responses as well. In the previous section, you may have noticed when we intercepted the response that the modifications we made to the <code>IP</code> field were temporary and were not applied when we refreshed the page unless we intercepted the response and added them again. To solve this, we can automate response modification similarly to what we did above to automatically enable any characters in the <code>IP</code> field for easier command injection.</p>
<p>Let us go back to (<code>Proxy&gt;Options&gt;Match and Replace</code>) in Burp to add another rule. This time we will use the type of <code>Response body</code> since the change we want to make exists in the response's body and not in its headers. In this case, we do not have to use regex as we know the exact string we want to replace, though it is possible to use regex to do the same thing if we prefer.</p>
<p><img alt="Burp Match Replace" src="https://academy.hackthebox.com/storage/modules/110/burp_match_replace_response_1.jpg"/></p>
<ul>
<li>
<code>Type</code>: <code>Response body</code>.</li>
<li>
<code>Match</code>: <code>type="number"</code>.</li>
<li>
<code>Replace</code>: <code>type="text"</code>.</li>
<li>
<code>Regex match</code>: False.</li>
</ul>
<p>Try adding another rule to change <code>maxlength="3"</code> to <code>maxlength="100"</code>.</p>
<p>Now, once we refresh the page with [<code>CTRL+SHIFT+R</code>], we'll see that we can add any input to the input field, and this should persist between page refreshes as well:</p>
<p><img alt="Burp Match Replace" src="https://academy.hackthebox.com/storage/modules/110/burp_match_replace_response_2.jpg"/></p>
<p>We can now click on <code>Ping</code>, and our command injection should work without intercepting and modifying the request.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Exercise 1: Try applying the same rules with ZAP Replacer. You can click on the tab below to show the correct options.</p>
</div>
<details>
<summary class="btn btn-sm btn-block mt-1 py-2 text-left btn-lighter">Click to show the answer</summary>
<br/> Change input type to text:
    <br/>- <code>Match Type</code>: <code>Response Body String</code>.
    <br/>- <code>Match Regex</code>: <code>False</code>.
    <br/>- <code>Match String</code>: <code>type="number"</code>.
    <br/>- <code>Replacement String</code>: <code>type="text"</code>.
    <br/>- <code>Enable</code>: <code>True</code>.
    <br/>
<br/> Change max length to 100:
    <br/>- <code>Match Type</code>: <code>Response Body String</code>.
    <br/>- <code>Match Regex</code>: <code>False</code>.
    <br/>- <code>Match String</code>: <code>maxlength="3"</code>.
    <br/>- <code>Replacement String</code>: <code>maxlength="100"</code>.
    <br/>- <code>Enable</code>: <code>True</code>.
    <br/>
</details>
</div>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Exercise 2: Try adding a rule that automatically adds <code>;ls;</code> when we click on <code>Ping</code>, by matching and replace the request body of the <code>Ping</code> request.</p>
</div>
</div>
