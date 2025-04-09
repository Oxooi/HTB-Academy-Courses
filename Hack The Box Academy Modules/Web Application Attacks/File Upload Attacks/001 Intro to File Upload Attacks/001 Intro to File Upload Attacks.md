
<h1>Intro to File Upload Attacks</h1>
<hr/>
<p>Uploading user files has become a key feature for most modern web applications to allow the extensibility of web applications with user information. A social media website allows the upload of user profile images and other social media, while a corporate website may allow users to upload PDFs and other documents for corporate use.</p>
<p>However, as web application developers enable this feature, they also take the risk of allowing end-users to store their potentially malicious data on the web application's back-end server. If the user input and uploaded files are not correctly filtered and validated, attackers may be able to exploit the file upload feature to perform malicious activities, like executing arbitrary commands on the back-end server to take control over it.</p>
<p>File upload vulnerabilities are amongst the most common vulnerabilities found in web and mobile applications, as we can see in the latest <a href="https://www.cvedetails.com/vulnerability-list/cweid-434/vulnerabilities.html">CVE Reports</a>. We will also notice that most of these vulnerabilities are scored as <code>High</code> or <code>Critical</code> vulnerabilities, showing the level of risk caused by insecure file upload.</p>
<hr/>
<h2>Types of File Upload Attacks</h2>
<p>The most common reason behind file upload vulnerabilities is weak file validation and verification, which may not be well secured to prevent unwanted file types or could be missing altogether. The worst possible kind of file upload vulnerability is an <code>unauthenticated arbitrary file upload</code> vulnerability. With this type of vulnerability, a web application allows any unauthenticated user to upload any file type, making it one step away from allowing any user to execute code on the back-end server.</p>
<p>Many web developers employ various types of tests to validate the extension or content of the uploaded file. However, as we will see in this module, if these filters are not secure, we may be able to bypass them and still reach arbitrary file uploads to perform our attacks.</p>
<p>The most common and critical attack caused by arbitrary file uploads is <code>gaining remote command execution</code> over the back-end server by uploading a web shell or uploading a script that sends a reverse shell. A web shell, as we will discuss in the next section, allows us to execute any command we specify and can be turned into an interactive shell to enumerate the system easily and further exploit the network. It may also be possible to upload a script that sends a reverse shell to a listener on our machine and then interact with the remote server that way.</p>
<p>In some cases, we may not have arbitrary file uploads and may only be able to upload a specific file type. Even in these cases, there are various attacks we may be able to perform to exploit the file upload functionality if certain security protections were missing from the web application.</p>
<p>Examples of these attacks include:</p>
<ul>
<li>Introducing other vulnerabilities like <code>XSS</code> or <code>XXE</code>.</li>
<li>Causing a <code>Denial of Service (DoS)</code> on the back-end server.</li>
<li>Overwriting critical system files and configurations.</li>
<li>And many others.</li>
</ul>
<p>Finally, a file upload vulnerability is not only caused by writing insecure functions but is also often caused by the use of outdated libraries that may be vulnerable to these attacks. At the end of the module, we will go through various tips and practices to secure our web applications against the most common types of file upload attacks, in addition to further recommendations to prevent file upload vulnerabilities that we may miss.</p>
