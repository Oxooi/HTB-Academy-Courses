
<h1>Intro to SQL Injections</h1>
<hr/>
<p>Now that we have a general idea of how MySQL and SQL queries work let us learn about SQL injections.</p>
<hr/>
<h2>Use of SQL in Web Applications</h2>
<p>First, let us see how web applications use databases MySQL, in this case, to store and retrieve data.  Once a DBMS is installed and set up on the back-end server and is up and running, the web applications can start utilizing it to store and retrieve data.</p>
<!-- 
For example, within a `PHP` web application, we can connect to the database server with:

```php
$conn = new mysqli("localhost", "root", "password");
```

Then, we can create a new database with:

```php
$sql = "CREATE DATABASE users";
$conn->query($sql)
``` -->
<p>For example, within a <code>PHP</code> web application, we can connect to our database, and start using the <code>MySQL</code> database through <code>MySQL</code> syntax, right within <code>PHP</code>, as follows:</p>
<pre><code class="language-php">$conn = new mysqli("localhost", "root", "password", "users");
$query = "select * from logins";
$result = $conn-&gt;query($query);
</code></pre>
<p>Then, the query's output will be stored in <code>$result</code>, and we can print it to the page or use it in any other way. The below PHP code will print all returned results of the SQL query in new lines:</p>
<pre><code class="language-php">while($row = $result-&gt;fetch_assoc() ){
	echo $row["name"]."&lt;br&gt;";
}
</code></pre>
<p>Web applications also usually use user-input when retrieving data. For example, when a user uses the search function to search for other users, their search input is passed to the web application, which uses the input to search within the databases:</p>
<pre><code class="language-php">$searchInput =  $_POST['findUser'];
$query = "select * from logins where username like '%$searchInput'";
$result = $conn-&gt;query($query);
</code></pre>
<p><code>If we use user-input within an SQL query, and if not securely coded, it may cause a variety of issues, like SQL Injection vulnerabilities.</code></p>
<hr/>
<h2>What is an Injection?</h2>
<p>In the above example, we accept user input and pass it directly to the SQL query without sanitization.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Sanitization refers to the removal of any special characters in user-input, in order to break any injection attempts.</p>
</div>
</div>
<p>Injection occurs when an application misinterprets user input as actual code rather than a string, changing the code flow and executing it. This can occur by escaping user-input bounds by injecting a special character like (<code>'</code>), and then writing code to be executed, like JavaScript code or SQL in SQL Injections. Unless the user input is sanitized, it is very likely to execute the injected code and run it.</p>
<hr/>
<h2>SQL Injection</h2>
<p>An SQL injection occurs when user-input is inputted into the SQL query string without properly sanitizing or filtering the input. The previous example showed how user-input can be used within an SQL query, and it did not use any form of input sanitization:</p>
<pre><code class="language-php">$searchInput =  $_POST['findUser'];
$query = "select * from logins where username like '%$searchInput'";
$result = $conn-&gt;query($query);
</code></pre>
<p>In typical cases, the <code>searchInput</code> would be inputted to complete the query, returning the expected outcome. Any input we type goes into the following SQL query:</p>
<pre><code class="language-sql">select * from logins where username like '%$searchInput'
</code></pre>
<p>So, if we input <code>admin</code>, it becomes <code>'%admin'</code>. In this case, if we write any SQL code, it would just be considered as a search term. For example, if we input <code>SHOW DATABASES;</code>, it would be executed as <code>'%SHOW DATABASES;'</code> The web application will search for usernames similar to <code>SHOW DATABASES;</code>. However, as there is no sanitization, in this case, <strong>we can add a single quote (<code>'</code>), which will end the user-input field, and after it, we can write actual SQL code</strong>. For example, if we search for <code>1'; DROP TABLE users;</code>, the search input would be:</p>
<pre><code class="language-php">'%1'; DROP TABLE users;'
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Notice how we added a single quote (') after "1", in order to escape the bounds of the user-input in ('%$searchInput').</p>
</div>
</div>
<p>So, the final SQL query executed would be as follows:</p>
<pre><code class="language-sql">select * from logins where username like '%1'; DROP TABLE users;'
</code></pre>
<p>As we can see from the syntax highlighting, we can escape the original query's bounds and have our newly injected query execute as well. <code>Once the query is run, the </code>users<code> table will get deleted.</code></p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: In the above example, for the sake of simplicity, we added another SQL query after a semi-colon (;). Though this is actually not possible with MySQL, it is possible with MSSQL and PostgreSQL. In the coming sections, we'll discuss the real methods of injecting SQL queries in MySQL.</p>
</div>
</div>
<hr/>
<h2>Syntax Errors</h2>
<p>The previous example of SQL injection would return an error:</p>
<pre><code class="language-php">Error: near line 1: near "'": syntax error
</code></pre>
<p>This is because of the last trailing character, where we have a single extra quote (<code>'</code>) that is not closed, which causes a SQL syntax error when executed:</p>
<pre><code class="language-sql">select * from logins where username like '%1'; DROP TABLE users;'
</code></pre>
<p>In this case, we had only one trailing character, as our input from the search query was near the end of the SQL query. However, the user input usually goes in the middle of the SQL query, and the rest of the original SQL query comes after it.</p>
<p>To have a successful injection, we must ensure that the newly modified SQL query is still valid and does not have any syntax errors after our injection. In most cases, we would not have access to the source code to find the original SQL query and develop a proper SQL injection to make a valid SQL query. So, how would we be able to inject into the SQL query then successfully?</p>
<p>One answer is by using <code>comments</code>, and we will discuss this in a later section. Another is to make the query syntax work by passing in multiple single quotes, as we will discuss next (<code>'</code>).</p>
<p>Now that we understand SQL injections' basics let us start learning some practical uses.</p>
<hr/>
<h2>Types of SQL Injections</h2>
<p>SQL Injections are categorized based on how and where we retrieve their output.</p>
<p><img alt="Diagram of SQL Injection types: In-band with Union and Error-based, Blind with Boolean and Time-based, and Out-of-band" src="https://academy.hackthebox.com/storage/modules/33/types_of_sqli.jpg"/></p>
<p>In simple cases, the output of both the intended and the new query may be printed directly on the front end, and we can directly read it. This is known as <code>In-band</code> SQL injection, and it has two types: <code>Union Based</code> and <code>Error Based</code>.</p>
<p>With <code>Union Based</code> SQL injection, we may have to specify the exact location, 'i.e., column', which we can read, so the query will direct the output to be printed there.  As for <code>Error Based</code> SQL injection, it is used when we can get the <code>PHP</code> or <code>SQL</code> errors in the front-end, and so we may intentionally cause an SQL error that returns the output of our query.</p>
<p>In more complicated cases, we may not get the output printed, so we may utilize SQL logic to retrieve the output character by character. This is known as <code>Blind</code> SQL injection, and it also has two types: <code>Boolean Based</code> and <code>Time Based</code>.</p>
<p>With <code>Boolean Based</code> SQL injection, we can use SQL conditional statements to control whether the page returns any output at all, 'i.e., original query response,' if our conditional statement returns <code>true</code>. As for <code>Time Based</code> SQL injections, we use SQL conditional statements that delay the page response if the conditional statement returns <code>true</code> using the <code>Sleep()</code> function.</p>
<p>Finally, in some cases, we may not have direct access to the output whatsoever, so we may have to direct the output to a remote location, 'i.e., DNS record,' and then attempt to retrieve it from there. This is known as <code>Out-of-band</code> SQL injection.</p>
<p>In this module, we will only be focusing on introducing SQL injections through learning about <code>Union Based</code> SQL injection.</p>
