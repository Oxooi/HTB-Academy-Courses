
<h1>Union Injection</h1>
<hr/>
<p>Now that we know how the Union clause works and how to use it let us learn how to utilize it in our SQL injections. Let us take the following example:</p>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entries include CN SHA, Shanghai, 37.13 and CN SHE, Shenzhen, 23.97" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn" src="/storage/modules/33/ports_cn.png"/>
<p>We see a potential SQL injection in the search parameters. We apply the SQLi Discovery steps by injecting a single quote (<code>'</code>), and we do get an error:</p>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. An error message states: You have an error in your SQL syntax; check the manual for the right syntax near" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn'" src="/storage/modules/33/ports_quote.png"/>
<p>Since we caused an error, this may mean that the page is vulnerable to SQL injection.  This scenario is ideal for exploitation through Union-based injection, as we can see our queries' results.</p>
<hr/>
<h2>Detect number of columns</h2>
<p>Before going ahead and exploiting Union-based queries, we need to find the number of columns selected by the server.  There are two methods of detecting the number of columns:</p>
<ul>
<li>Using <code>ORDER BY</code>
</li>
<li>Using <code>UNION</code>
</li>
</ul>
<h4>Using ORDER BY</h4>
<p>The first way of detecting the number of columns is through the <code>ORDER BY</code> function, which we discussed earlier.  We have to inject a query that sorts the results by a column we specified, 'i.e., column 1, column 2, and so on', until we get an error saying the column specified does not exist.</p>
<p>For example, we can start with <code>order by 1</code>, sort by the first column, and succeed, as the table must have at least one column.  Then we will do <code>order by 2</code> and then <code>order by 3</code> until we reach a number that returns an error, or the page does not show any output, which means that this column number does not exist. The final successful column we successfully sorted by gives us the total number of columns.</p>
<p>If we failed at <code>order by 4</code>, this means the table has three columns, which is the number of columns we were able to sort by successfully. Let us go back to our previous example and attempt the same, with the following payload:</p>
<pre><code class="language-sql">' order by 1-- -
</code></pre>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Reminder: We are adding an extra dash (-) at the end, to show you that there is a space after (--).</p>
</div>
</div>
<p>As we see, we get a normal result:</p>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entries include CN SHA, Shanghai, 37.13 and CN SHE, Shenzhen, 23.97" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=' order by 1-- -" src="/storage/modules/33/ports_cn.png"/>
<p>Next, let us try to sort by the second column, with the following payload:</p>
<pre><code class="language-sql">' order by 2-- -
</code></pre>
<p>We still get the results. We notice that they are sorted differently, as expected:</p>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entries include AE DXB, Dubai, 15.73 and BR SSZ, Santos, 3.6" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=' order by 2-- -" src="/storage/modules/33/order_by_2.jpg"/>
<p>We do the same for column <code>3</code> and <code>4</code> and get the results back. However, when we try to <code>ORDER BY</code> column 5, we get the following error:</p>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. An error message states: Unknown column '5' in 'order clause" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=' order by 5-- -" src="/storage/modules/33/order_by_5.jpg"/>
<p>This means that this table has exactly 4 columns .</p>
<h4>Using UNION</h4>
<p>The other method is to attempt a Union injection with a different number of columns until we successfully get the results back. The first method always returns the results until we hit an error, while this method always gives an error until we get a success. We can start by injecting a 3 column <code>UNION</code> query:</p>
<pre><code class="language-sql">cn' UNION select 1,2,3-- -
</code></pre>
<p>We get an error saying that the number of columns don’t match:
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. An error message states: The used SELECT statements have a different number of columns" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION select 1,2,3-- -" src="/storage/modules/33/ports_columns_diff.png"/></p>
<p>So, let’s try four columns and see the response:</p>
<pre><code class="language-sql">cn' UNION select 1,2,3,4-- -
</code></pre>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entries include 2, 3, and 4" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION select 1,2,3,4-- -" src="/storage/modules/33/ports_columns_correct.png"/>
<p>This time we successfully get the results, meaning once again that the table has 4 columns. We can use either method to determine the number of columns. Once we know the number of columns, we know how to form our payload, and we can proceed to the next step.</p>
<hr/>
<h2>Location of Injection</h2>
<p>While a query may return multiple columns, the web application may only display some of them. So, if we inject our query in a column that is not printed on the page, we will not get its output. This is why we need to determine which columns are printed to the page, to determine where to place our injection. In the previous example, while the injected query returned 1, 2, 3, and 4, we saw only 2, 3, and 4 displayed back to us on the page as the output data:</p>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entries include 2, 3, and 4" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION select 1,2,3,4-- -" src="/storage/modules/33/ports_columns_correct.png"/>
<p>It is very common that not every column will be displayed back to the user. For example, the ID field is often used to link different tables together, but the user doesn't need to see it. This tells us that columns 2 and 3, and 4 are printed to place our injection in any of them.  <code>We cannot place our injection at the beginning, or its output will not be printed.</code></p>
<p>This is the benefit of using numbers as our junk data, as it makes it easy to track which columns are printed, so we know at which column to place our query. To test that we can get actual data from the database 'rather than just numbers,' we can use the <code>@@version</code> SQL query as a test and place it in the second column instead of the number 2:</p>
<pre><code class="language-sql">cn' UNION select 1,@@version,3,4-- -
</code></pre>
<img alt="Search interface with a text box and button labeled 'Search'. Below is a table with columns: Port Code, Port City, and Port Volume. Entry includes 10.3.22-MariaDB-1ubuntu1, 3, and 4" class="website-screenshot" data-url="http://SERVER_IP:PORT/search.php?port_code=cn' UNION select 1,@@version,3,4-- -" src="/storage/modules/33/db_version_1.jpg"/>
<p>As we can see, we can get the database version displayed. Now we know how to form our Union SQL injection payloads to successfully get the output of our query printed on the page. In the next section, we will discuss how to enumerate the database and get data from other tables and databases.</p>
<div class="mb-5 pwnbox-select-card"></div>
<div id="screen" style="height: 600px; border: 1px solid;">
<div class="screenPlaceholder">
<div class="instanceLoading" style="display: none;">
<h1 class="text-center" style="margin-top: 270px;"><i class="fa fa-circle-notch fa-spin"></i>
</h1>
<div class="text-center">Instance is starting...</div>
</div>
<div class="instanceTerminating" style="display: none;">
<h1 class="text-center" style="margin-top: 270px;"><i class="fa fa-circle-notch fa-spin"></i>
</h1>
<div class="text-center">Terminating instance...</div>
</div>
<div class="row instanceStart max-width-canvas">
<div class="col-4"></div>
<div class="col-4">
<button class="startInstanceBtn btn btn-success text-light btn-lg btn-block" style="margin-top: 270px;">Start Instance
                            </button>
<p class="text-center mt-2 font-size-13 font-secondary">
<span class="text-success spawnsLeft">
<i class="fal fa-infinity"></i>
</span> / 1 spawns left
                            </p>
</div>
<div class="col-4"></div>
</div>
</div>
</div>
<div class="row align-center justify-center my-4">
<div class="col-5 justify-start">
<button class="instance-button fullScreenBtn btn btn-light btn-sm float-left" style="display:none;" target="_blank"><i class="fad fa-expand text-success mr-1"></i>  Full Screen
                    </button>
<button class="instance-button terminateInstanceBtn btn btn-light btn-sm ml-2" style="display:none;"><i class="fad fa-times text-danger"></i>  Terminate
                    </button>
<button class="instance-button resetInstanceBtn btn btn-light btn-sm ml-1" style="display:none;"><i class="fad fa-sync text-warning mr-2"></i>  Reset
                    </button>
<div class="btn-group" role="group">
<button class="instance-button extendInstanceBtn btn btn-light btn-sm ml-1" style="display:none;cursor: default;">Life Left:
                            <span class="lifeLeft"></span>m
                        </button>
<button class="extendInstanceBtn extendInstanceBtnClicker btn btn-light btn-sm" data-title="Extend Life" data-toggle="tooltip" style="display:none;"><i class="fa fa-plus text-success"></i></button>
</div>
</div>
<div class="col-7 justify-end pt-2 pr-2 font-size-small text-right" id="statusText">Waiting to
                    start...
                </div>
</div>
<div class="d-inline-block mb-2 solutionSettings solutionSettingsOffsets" id="solutionsModuleSetting">
<div class="border border-secondary p-2 rounded">
<div class="custom-control custom-switch d-flex">
<input class="custom-control-input" disabled="" id="showSolutionsModuleSetting" type="checkbox"/>
<label class="custom-control-label font-size-14 font-weight-normal text-white" for="showSolutionsModuleSetting">
                                Enable step-by-step solutions for all questions
                            </label>
<span aria-hidden="true" class="cursor-pointer font-size-14 ml-1 mr-1 text-white" data-content="Access to this feature is exclusive to annual subscribers. To acquire an annual subscription, kindly proceed by clicking &lt;a href='/billing'&gt;here&lt;/a&gt;." data-html="true" data-placement="top" data-toggle="popover" data-trigger="click" title="Activate Solutions">
<i class="fa fa-info-circle font-size-12"></i>
</span>
<img alt="sparkles-icon-decoration" class="ml-2 w-auto sparkles-icon" height="20" src="/images/sparkles-solid.svg">
</img></div>
</div>
</div>
<div class="card" id="questionsDiv">
<div class="card-body">
<div class="row">
<div class="col-9">
<h4 class="card-title mt-0 font-size-medium">Questions</h4>
<p class="card-title-desc font-size-large font-size-15">Answer the question(s) below
                                to complete this Section and earn cubes!</p>
<span class="spawnTargetBtn spawn-target-text-clone d-none">Click here to spawn the target
                                system!</span>
<p class="card-title-desc font-size-large font-size-15 mb-0">
    Target(s): <span class="text-success">
<span class="target" style="cursor:pointer;">
<i class="fad fa-circle-notch fa-spin"></i>
<span class="spawnTargetBtn">Fetching status...</span>
</span>
</span>
<button class="resetTargetBtn btn btn-light btn-sm" data-title="Reset Target(s)" data-toggle="tooltip" style="cursor: pointer; display: none;">
<i class="fad fa-sync text-warning"></i>
</button>
<br/>
<div class="d-flex align-items-center targetLifeContainer">
<span class="targetLifeTimeContainer" style="display: none;">
            Life Left: <span class="targetLifeTime font-size-15">0</span> minute(s)
                    </span>
</div>
</p>
</div>
<div class="col-3 text-right float-right">
<button class="btn btn-light bg-color-blue-nav mt-2 w-100 d-flex align-items-center" data-target="#cheatSheetModal" data-toggle="modal">
<div><i class="fad fa-file-alt mr-2"></i></div>
<div class="text-center w-100 ml-1">Cheat Sheet</div>
</button>
</div>
</div>
<div>
<div>
<label class="module-question" for="462"><span class="badge badge-soft-dark font-size-14 mr-2">+ 0 <i class="fad fa-cube text-success"></i></span> Use a Union injection to get the result of 'user()'
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer462" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-462">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="462" id="btnAnswer462">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint462" data-toggle="modal" id="hintBtn462"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="">
</div>
</div>
</div>
</div>
</div>
