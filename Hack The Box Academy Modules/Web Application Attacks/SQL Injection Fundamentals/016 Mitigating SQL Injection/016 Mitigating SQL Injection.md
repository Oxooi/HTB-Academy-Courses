
<h1>Mitigating SQL Injection</h1>
<hr/>
<p>We have learned about SQL injections, why they occur, and how we can exploit them. We should also learn how to avoid these types of vulnerabilities in our code and patch them when found.  Let's look at some examples of how SQL Injection can be mitigated.</p>
<hr/>
<h2>Input Sanitization</h2>
<p>Here's the snippet of the code from the authentication bypass section we discussed earlier:</p>
<pre><code class="language-php">&lt;SNIP&gt;
  $username = $_POST['username'];
  $password = $_POST['password'];

  $query = "SELECT * FROM logins WHERE username='". $username. "' AND password = '" . $password . "';" ;
  echo "Executing query: " . $query . "&lt;br /&gt;&lt;br /&gt;";

  if (!mysqli_query($conn ,$query))
  {
          die('Error: ' . mysqli_error($conn));
  }

  $result = mysqli_query($conn, $query);
  $row = mysqli_fetch_array($result);
&lt;SNIP&gt;
</code></pre>
<p>As we can see, the script takes in the <code>username</code> and <code>password</code> from the POST request and passes it to the query directly. This will let an attacker inject anything they wish and exploit the application. Injection can be avoided by sanitizing any user input, rendering injected queries useless. Libraries provide multiple functions to achieve this, one such example is the <a href="https://www.php.net/manual/en/mysqli.real-escape-string.php">mysqli_real_escape_string()</a> function. This function escapes characters such as <code>'</code> and <code>"</code>, so they don't hold any special meaning.</p>
<pre><code class="language-php">&lt;SNIP&gt;
$username = mysqli_real_escape_string($conn, $_POST['username']);
$password = mysqli_real_escape_string($conn, $_POST['password']);

$query = "SELECT * FROM logins WHERE username='". $username. "' AND password = '" . $password . "';" ;
echo "Executing query: " . $query . "&lt;br /&gt;&lt;br /&gt;";
&lt;SNIP&gt;
</code></pre>
<p>The snippet above shows how the function can be used.</p>
<p><img alt="Admin panel with SQL injection query and 'Login failed!' message." src="https://academy.hackthebox.com/storage/modules/33/mysqli_escape.png"/></p>
<p>As expected, the injection no longer works due to escaping the single quotes. A similar example is the <a href="https://www.php.net/manual/en/function.pg-escape-string.php">pg_escape_string()</a> which used to escape PostgreSQL queries.</p>
<hr/>
<h2>Input Validation</h2>
<p>User input can also be validated based on the data used to query to ensure that it matches the expected input.  For example, when taking an email as input, we can validate that the input is in the form of <code><a class="__cf_email__" data-cfemail="d1ffffff91b4bcb0b8bdffb2bebc" href="/cdn-cgi/l/email-protection">[email protected]</a></code>, and so on.</p>
<p>Consider the following code snippet from the ports page, which we used <code>UNION</code> injections on:</p>
<pre><code class="language-php">&lt;?php
if (isset($_GET["port_code"])) {
	$q = "Select * from ports where port_code ilike '%" . $_GET["port_code"] . "%'";
	$result = pg_query($conn,$q);
    
	if (!$result)
	{
   		die("&lt;/table&gt;&lt;/div&gt;&lt;p style='font-size: 15px;'&gt;" . pg_last_error($conn). "&lt;/p&gt;");
	}
&lt;SNIP&gt;
?&gt;
</code></pre>
<p>We see the GET parameter <code>port_code</code> being used in the query directly. It's already known that a port code consists only of letters or spaces. We can restrict the user input to only these characters, which will prevent the injection of queries. A regular expression can be used for validating the input:</p>
<pre><code class="language-php">&lt;SNIP&gt;
$pattern = "/^[A-Za-z\s]+$/";
$code = $_GET["port_code"];

if(!preg_match($pattern, $code)) {
  die("&lt;/table&gt;&lt;/div&gt;&lt;p style='font-size: 15px;'&gt;Invalid input! Please try again.&lt;/p&gt;");
}

$q = "Select * from ports where port_code ilike '%" . $code . "%'";
&lt;SNIP&gt;
</code></pre>
<p>The code is modified to use the <a href="https://www.php.net/manual/en/function.preg-match.php">preg_match()</a> function, which checks if the input matches the given pattern or not. The pattern used is <code>[A-Za-z\s]+</code>, which will only match strings containing letters and spaces. Any other character will result in the termination of the script.</p>
<img alt="Search for a port with fields for Port Code, Port City, and Port Volume." class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=c" src="/storage/modules/33/postgres_copy_write.png"/>
<p>We can test the following injection:</p>
<pre><code class="language-sql">'; SELECT 1,2,3,4-- -
</code></pre>
<img alt="Search for a port with fields for Port Code, Port City, and Port Volume." class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code='; SELECT 1,2,3,4-- -" src="/storage/modules/33/postgres_copy_write.png"/>
<p>As seen in the images above, input with injected queries was rejected by the server.</p>
<hr/>
<h2>User Privileges</h2>
<p>As discussed initially, DBMS software allows the creation of users with fine-grained permissions. We should ensure that the user querying the database only has minimum permissions.</p>
<p>Superusers and users with administrative privileges should never be used with web applications. These accounts have access to functions and features, which could lead to server compromise.</p>
<pre><code class="language-shell-session">MariaDB [(none)]&gt; CREATE USER 'reader'@'localhost';

Query OK, 0 rows affected (0.002 sec)


MariaDB [(none)]&gt; GRANT SELECT ON ilfreight.ports TO 'reader'@'localhost' IDENTIFIED BY 'p@ssw0Rd!!';

Query OK, 0 rows affected (0.000 sec)
</code></pre>
<p>The commands above add a new MariaDB user named <code>reader</code> who is granted only <code>SELECT</code> privileges on the <code>ports</code> table.  We can verify the permissions for this user by logging in:</p>
<pre><code class="language-shell-session">[!bash!]$ mysql -u reader -p

MariaDB [(none)]&gt; use ilfreight;
MariaDB [ilfreight]&gt; SHOW TABLES;

+---------------------+
| Tables_in_ilfreight |
+---------------------+
| ports               |
+---------------------+
1 row in set (0.000 sec)


MariaDB [ilfreight]&gt; SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;

+--------------------+
| SCHEMA_NAME        |
+--------------------+
| information_schema |
| ilfreight          |
+--------------------+
2 rows in set (0.000 sec)


MariaDB [ilfreight]&gt; SELECT * FROM ilfreight.credentials;
ERROR 1142 (42000): SELECT command denied to user 'reader'@'localhost' for table 'credentials'
</code></pre>
<p>The snippet above confirms that the <code>reader</code> user cannot query other tables in the <code>ilfreight</code> database. The user only has access to the <code>ports</code> table that is needed by the application.</p>
<hr/>
<h2>Web Application Firewall</h2>
<p>Web Application Firewalls (WAF) are used to detect malicious input and reject any HTTP requests containing them. This helps in preventing SQL Injection even when the application logic is flawed.  WAFs can be open-source (ModSecurity) or premium (Cloudflare). Most of them have default rules configured based on common web attacks. For example, any request containing the string <code>INFORMATION_SCHEMA</code> would be rejected, as it's commonly used while exploiting SQL injection.</p>
<hr/>
<h2>Parameterized Queries</h2>
<p>Another way to ensure that the input is safely sanitized is by using parameterized queries. Parameterized queries contain placeholders for the input data, which is then escaped and passed on by the drivers. Instead of directly passing the data into the SQL query, we use placeholders and then fill them with PHP functions.</p>
<p>Consider the following modified code:</p>
<pre><code class="language-php">&lt;SNIP&gt;
  $username = $_POST['username'];
  $password = $_POST['password'];

  $query = "SELECT * FROM logins WHERE username=? AND password = ?" ;
  $stmt = mysqli_prepare($conn, $query);
  mysqli_stmt_bind_param($stmt, 'ss', $username, $password);
  mysqli_stmt_execute($stmt);
  $result = mysqli_stmt_get_result($stmt);

  $row = mysqli_fetch_array($result);
  mysqli_stmt_close($stmt);
&lt;SNIP&gt;
</code></pre>
<p>The query is modified to contain two placeholders, marked with <code>?</code> where the username and password will be placed. We then bind the username and password to the query using the <a href="https://www.php.net/manual/en/mysqli-stmt.bind-param.php">mysqli_stmt_bind_param()</a> function. This will safely escape any quotes and place the values in the query.</p>
<hr/>
<h2>Conclusion</h2>
<p>The list above is not exhaustive, and it could still be possible to exploit SQL injection based on the application logic. The code examples shown are based on PHP, but the logic applies across all common languages and libraries.</p>
