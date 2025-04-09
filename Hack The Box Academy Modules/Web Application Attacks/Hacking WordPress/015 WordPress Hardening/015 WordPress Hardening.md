
<h1>WordPress Hardening</h1>
<hr/>
<h2>Best Practices</h2>
<p>Below are some best practices for preventing attacks against a WordPress site.</p>
<hr/>
<h2>Perform Regular Updates</h2>
<p>This is a key principle for any application or system and can greatly reduce the risk of a successful attack. Make sure that WordPress core, as well as all installed plugins and themes, are kept up-to-date. Researchers continuously find flaws in third-party WordPress plugins. Some hosting providers will even perform continuous automatic updates of WordPress core. The WordPress admin console will usually prompt us when plugins or themes need to be updated or when WordPress itself requires an upgrade. We can even modify the <code>wp-config.php</code> file to enable automatic updates by inserting the following lines:</p>
<pre><code class="language-php">define( 'WP_AUTO_UPDATE_CORE', true );
</code></pre>
<pre><code class="language-php">add_filter( 'auto_update_plugin', '__return_true' );
</code></pre>
<pre><code class="language-php">add_filter( 'auto_update_theme', '__return_true' );
</code></pre>
<hr/>
<h2>Plugin and Theme Management</h2>
<p>Only install trusted themes and plugins from the WordPress.org website. Before installing a plugin or theme, check its reviews, popularity, number of installs, and last update date. If either has not been updated in years, it could be a sign that it is no longer maintained and may suffer from unpatched vulnerabilities. Routinely audit your WordPress site and remove any unused themes and plugins. This will help to ensure that no outdated plugins are left forgotten and potentially vulnerable.</p>
<hr/>
<h2>Enhance WordPress Security</h2>
<p>Several WordPress security plugins can be used to enhance the website's security. These plugins can be used as a Web Application Firewall (WAF), a malware scanner, monitoring, activity auditing, brute force attack prevention, and strong password enforcement for users. Here are a few examples of popular WordPress security plugins.</p>
<h4><a href="https://wordpress.org/plugins/sucuri-scanner/">Sucuri Security</a></h4>
<ul>
<li>This plugin is a security suite consisting of the following features:
<ul>
<li>Security Activity Auditing</li>
<li>File Integrity Monitoring</li>
<li>Remote Malware Scanning</li>
<li>Blacklist Monitoring.</li>
</ul>
</li>
</ul>
<h4><a href="https://wordpress.org/plugins/better-wp-security/">iThemes Security</a></h4>
<ul>
<li>iThemes Security provides 30+ ways to secure and protect a WordPress site such as:
<ul>
<li>Two-Factor Authentication (2FA)</li>
<li>WordPress Salts &amp; Security Keys</li>
<li>Google reCAPTCHA</li>
<li>User Action Logging</li>
</ul>
</li>
</ul>
<h4><a href="https://wordpress.org/plugins/wordfence/">Wordfence Security</a></h4>
<ul>
<li>Wordfence Security consists of an endpoint firewall and malware scanner.
<ul>
<li>The WAF identifies and blocks malicious traffic.</li>
<li>The premium version provides real-time firewall rule and malware signature updates</li>
<li>Premium also enables real-time IP blacklisting to block all requests from known most malicious IPs.</li>
</ul>
</li>
</ul>
<hr/>
<h2>User Management</h2>
<p>Users are often targeted as they are generally seen as the weakest link in an organization. The following user-related best practices will help improve the overall security of a WordPress site.</p>
<ul>
<li>Disable the standard <code>admin</code> user and create accounts with difficult to guess usernames</li>
<li>Enforce strong passwords</li>
<li>Enable and enforce two-factor authentication (2FA) for all users</li>
<li>Restrict users' access based on the concept of least privilege</li>
<li>Periodically audit user rights and access. Remove any unused accounts or revoke access that is no longer needed</li>
</ul>
<hr/>
<h2>Configuration Management</h2>
<p>Certain configuration changes can increase the overall security posture of a WordPress installation.</p>
<ul>
<li>Install a plugin that disallows user enumeration so an attacker cannot gather valid usernames to be used in a password spraying attack</li>
<li>Limit login attempts to prevent password brute-forcing attacks</li>
<li>Rename the <code>wp-login.php</code> login page or relocate it to make it either not accessible to the internet or only accessible by certain IP addresses</li>
</ul>
