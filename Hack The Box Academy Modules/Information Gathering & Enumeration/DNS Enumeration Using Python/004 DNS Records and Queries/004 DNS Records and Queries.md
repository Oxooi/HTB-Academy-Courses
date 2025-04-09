
<h1>DNS Records and Queries</h1>
<hr/>
<p>DNS works with many different records. DNS records are instructions that are located on authoritative DNS servers and contain information about a domain.  These entries are written in the DNS syntax that gives the DNS servers the appropriate instructions. Here are the most common DNS records that we will come across during our Penetration Tests:</p>
<table>
<thead>
<tr>
<th><strong>Record</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>A</code></td>
<td>IP Version 4 Address records</td>
</tr>
<tr>
<td><code>AAAA</code></td>
<td>IP Version 6 Address records</td>
</tr>
<tr>
<td><code>CNAME</code></td>
<td>Canonical Name records</td>
</tr>
<tr>
<td><code>HINFO</code></td>
<td>Host Information records</td>
</tr>
<tr>
<td><code>ISDN</code></td>
<td>Integrated Services Digital Network records</td>
</tr>
<tr>
<td><code>MX</code></td>
<td>Mail exchanger record</td>
</tr>
<tr>
<td><code>NS</code></td>
<td>Name Server records</td>
</tr>
<tr>
<td><code>PTR</code></td>
<td>Reverse-lookup Pointer records</td>
</tr>
<tr>
<td><code>SOA</code></td>
<td>Start of Authority records</td>
</tr>
<tr>
<td><code>TXT</code></td>
<td>Text records</td>
</tr>
</tbody>
</table>
<p>There are many tools and resources we can work with to send queries to the DNS servers. For example, we can use tools like:</p>
<ul>
<li>
<code>dig</code>
</li>
<li>
<code>nslookup</code>
</li>
</ul>
<hr/>
<h2>NS Servers</h2>
<p>We want to automate the enumeration process for potential zone transfers on misconfigured DNS servers to check for this vulnerability quickly with the tool we are creating. Let us start by enumerating some NS servers and checking if a DNS zone transfer is possible and, if so, get the information about the subdomains from the zone transfer.</p>
<hr/>
<h2>NS Records</h2>
<p><code>NS</code> records stand for <code>name server</code>. These records specify which DNS server is the authoritative server for the corresponding domain that contains the actual DNS records. Often a domain has several NS records that can specify primary and secondary name servers for that domain. Now that we know our target domain, we still need DNS servers we will interact with. For this, we have to find out which DNS servers are responsible for the domain, and for this, we can use the tool called <code>dig</code>. In this example, we use the domain called: <code>inlanefreight.com</code></p>
<h4>DIG - NS Queries</h4>
<pre><code class="language-shell-session">[!bash!]$ dig NS inlanefreight.com

&lt;SNIP&gt;
;; ANSWER SECTION:
inlanefreight.com.	60	IN	NS	ns2.inlanefreight.com.
inlanefreight.com.	60	IN	NS	ns1.inlanefreight.com.

&lt;SNIP&gt;
</code></pre>
<h4>DIG - SOA Queries</h4>
<pre><code class="language-shell-session">[!bash!]$ dig SOA inlanefreight.com

&lt;SNIP&gt;
;; ANSWER SECTION:
inlanefreight.com.	879	IN	SOA	ns-161.awsdns-20.com. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400

&lt;SNIP&gt;
</code></pre>
<h4>NSLOOKUP - SPF</h4>
<pre><code class="language-shell-session">[!bash!]$ nslookup -type=SPF inlanefreight.com

Non-authoritative answer:
inlanefreight.com	rdata_99 = "v=spf1 include:_spf.google.com include:mail1.inlanefreight.com include:google.com ~all"
</code></pre>
<h4>NSLOOKUP - DMARC</h4>
<pre><code class="language-shell-session">[!bash!]$ nslookup -type=txt _dmarc.inlanefreight.com

Non-authoritative answer:
_dmarc.inlanefreight.com	text = "v=DMARC1; p=reject; rua=mailto:<a class="__cf_email__" data-cfemail="d0bdb1a3a4b5a290b9bebcb1beb5b6a2b5b9b7b8a4feb3bfbd" href="/cdn-cgi/l/email-protection">[email protected]</a>; ruf=mailto:<a class="__cf_email__" data-cfemail="2845495b5c4d5a6841464449464d4e5a4d414f405c064b4745" href="/cdn-cgi/l/email-protection">[email protected]</a>; fo=1;"
</code></pre>
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
</div>
<div class="col-3 text-right float-right">
</div>
</div>
<div>
<div>
<label class="module-question" for="81"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Investigate all records for the domain "inlanefreight.com" with the help of dig or nslookup and submit the one unique record in double quotes as the answer.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="HTB{5Fz6UPNUFFzqjdg0AzXyxCjMZ}"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="81" disabled="true" id="btnAnswer81">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
</button>
</div>
</div>
</div>
<div class="custom-hr">
</div>
</div>
<div>
<label class="module-question" for="82"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Find out the corresponding IPv6 address of the domain "inlanefreight.com" and submit it as the answer.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="2a03:b0c0:1:e0::32c:b001"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="82" disabled="true" id="btnAnswer82">
<div class="submit-button-text">
<i class="fad fa-flag-checkered mr-2"></i> Submit
                                            </div>
<div class="submit-button-loader mx-4 d-none">
<i class="fa fa-circle-notch fa-spin"></i>
</div>
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
