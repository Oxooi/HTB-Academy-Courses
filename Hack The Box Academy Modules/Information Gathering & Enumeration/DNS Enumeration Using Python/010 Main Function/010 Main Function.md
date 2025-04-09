
<h1>Main Function</h1>
<hr/>
<p>The main function is the part of the code where the main program is running. It is essential to keep it as clear as possible, as we will most likely add more functions to our tool later. In this case, we want our tool to try a zone transfer on every DNS server we have specified. We know that the subdomains found will be added to the global subdomain list in the <code>AXFR()</code> function. So if this list is not empty, we want to see all subdomains.</p>
<hr/>
<h2>Main</h2>
<p>If we start a Python program by calling a py file, and there we call <code>"__name__"</code>, the system assigns it to the system variable the identifier "<code>__main__</code>." However, if we import this file into another module, it gets an identifier corresponding to the file name. This construction uses a Python file as a stand-alone program, makes single elements of this file importable, and implements complex module tests. As we did with the <code>AXFR</code> function, we proceed accordingly and define the rough steps that need to be taken as comments.</p>
<h4>DNS-AXFR.py</h4>
<pre><code class="language-python">&lt;SNIP&gt;
# Main
if __name__=="__main__":

        # For each nameserver
        # Try AXFR
        # Print the results
        # Print each subdomain
</code></pre>
<hr/>
<h2>For-Loop - Try AXFR</h2>
<p>Since our <code>AXFR</code> function requires the two parameters, "domain" and "nameserver," we create a <code>For-loop</code> that executes the <code>AXFR</code> function for each nameserver specified.
We use another <code>For-loop</code> combined with the <code>If-Else</code> statement in the area that will output the found subdomains. If the subdomain list, in which the <code>AXFR</code> function stores the found subdomains, is not empty, then every subdomain entry from the subdomain list should be printed.</p>
<h4>DNS-AXFR.py</h4>
<pre><code class="language-python">&lt;SNIP&gt;
# Main
if __name__=="__main__":

        # For each nameserver
        for nameserver in NS.nameservers:

                #Try AXFR
                AXFR(Domain, nameserver)

        # Print the results
        if Subdomains is not None:
                print('-------- Found Subdomains:')

                # Print each subdomain
                for subdomain in Subdomains:
                        print('{}'.format(subdomain))

        else:
                print('No subdomains found.')
                exit()
</code></pre>
<hr/>
<h2>DNS-AXFR.py - Complete Code</h2>
<pre><code class="language-python">#!/usr/bin/env python3

# Dependencies:
# python3-dnspython

# Used Modules:
import dns.zone as dz
import dns.query as dq
import dns.resolver as dr
import argparse

# Initialize Resolver-Class from dns.resolver as "NS"
NS = dr.Resolver()

# Target domain
Domain = 'inlanefreight.com'

# Set the nameservers that will be used
NS.nameservers = ['ns1.inlanefreight.com', 'ns2.inlanefreight.com']

# List of found subdomains
Subdomains = []

# Define the AXFR Function
def AXFR(domain, nameserver):

        # Try zone transfer for given domain and namerserver
        try:
				# Perform the zone transfer
                axfr = dz.from_xfr(dq.xfr(nameserver, domain))

                # If zone transfer was successful
                if axfr:
                        print('[*] Successful Zone Transfer from {}'.format(nameserver))

                        # Add found subdomains to global 'Subdomain' list
                        for record in axfr:
                                Subdomains.append('{}.{}'.format(record.to_text(), domain))

        # If zone transfer fails
        except Exception as error:
                print(error)
                pass

# Main
if __name__=="__main__":

        # For each nameserver
        for nameserver in NS.nameservers:

                #Try AXFR
                AXFR(Domain, nameserver)

        # Print the results
        if Subdomains is not None:
                print('-------- Found Subdomains:')

                # Print each subdomain
                for subdomain in Subdomains:
                        print('{}'.format(subdomain))

        else:
                print('No subdomains found.')
                exit()                
</code></pre>
<hr/>
<h2>Results</h2>
<h4>Make the Script Executable &amp; Execute</h4>
<pre><code class="language-shell-session">[!bash!]$ chmod +x dns-axfr.py
[!bash!]$ ./dns-axfr.py

[*] Successful Zone Transfer from ns1.inlanefreight.com
-------- Found Subdomains:
@.inlanefreight.com
admin.inlanefreight.com
app.inlanefreight.com
blog.inlanefreight.com
&lt;SNIP&gt;
</code></pre>
<div class="my-3 p-3 vpn-switch-card" id="vpn-switch">
<p class="font-size-14 color-white mb-0">VPN Servers</p>
<p class="font-size-13 mb-0">
<i class="fas fa-exclamation-triangle text-warning"></i><span class="color-white ml-1">Warning:</span> Each
                    time you "Switch",
                    your connection keys are regenerated and you must re-download your VPN connection file.
                </p>
<p class="font-size-13 mb-0">
                    All VM instances associated with the old VPN Server will be terminated when switching to
                    a new VPN server. <br/>
                    Existing PwnBox instances will automatically switch to the new VPN server.</p>
<div class="row mb-3">
<div class="col-12 mt-2">
<div class="d-none justify-content-center vpn-loader">
<div class="spinner-border text-success" role="status">
<span class="sr-only">Switching VPN...</span>
</div>
</div>
<select aria-label="vpn server" class="selectpicker custom-form-control vpnSelector badge-select" title="Select VPN Server">
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 6 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt; &lt;span class='recommended'&gt; &lt;img src='/images/sparkles-solid.svg'/&gt;Recommended&lt;/span&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="30" value="17">US Academy 6</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 5 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="31" value="16">US Academy 5</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 1 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="33" value="4">US Academy 1</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 2 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="33" value="5">US Academy 2</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 4 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="33" value="13">US Academy 4</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 5 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt; &lt;span class='recommended'&gt; &lt;img src='/images/sparkles-solid.svg'/&gt;Recommended&lt;/span&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="37" value="12">EU Academy 5</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 2 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="38" selected="" value="2">EU Academy 2</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;US Academy 3 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="38" value="9">US Academy 3</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 1 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="40" value="1">EU Academy 1</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 3 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="41" value="14">EU Academy 3</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 4 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="44" value="11">EU Academy 4</option>
<option data-content="&lt;div class='d-flex justify-content-between align-items-center'&gt; &lt;div class='server-title'&gt;EU Academy 6 &lt;/div&gt; &lt;div class='d-flex align-items-center'&gt;  &lt;div class='d-flex align-items-center justify-content-center mr-2 load load-warning '&gt;medium Load  &lt;/div&gt;  &lt;/div&gt;&lt;/div&gt;" data-level="48" value="15">EU Academy 6</option>
</select>
<p class="font-size-14 color-white mb-0 mt-2">PROTOCOL</p>
<div class="d-flex">
<div class="custom-control custom-radio custom-control-inline">
<input checked="" class="custom-control-input" id="rd_1" name="vpn-protocol" type="radio" value="udp"/>
<label class="custom-control-label green font-size-14" for="rd_1">UDP
                                    1337</label>
</div>
<div class="custom-control custom-radio">
<input class="custom-control-input" id="rd_2" name="vpn-protocol" type="radio" value="tcp"/>
<label class="custom-control-label green font-size-14" for="rd_2">TCP
                                    443</label>
</div>
</div>
<div class="d-flex justify-content-center">
<button class="btn btn-outline-success btn-lg download-vpn-settings mt-3 px-5 font-size-12">
                                DOWNLOAD VPN CONNECTION FILE
                            </button>
</div>
</div>
</div>
</div>
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
                            <button class="extendTargetSystemBtn btn btn-light btn-sm module-button" data-title="Extend Life by 1 hour (up to 6 hours total lifespan)" data-toggle="tooltip">
<i class="fa fa-plus text-success extend-icon"></i>
<div class="extend-loader spinner-border spinner-border-small text-success d-none" role="status">
</div>
</button>
<button class="text-danger btn btn-light btn-sm module-button font-size-16 mb-1" data-target="#terminateVmModal" data-toggle="modal">
                    Terminate <span class="fa-regular fa-x text-danger font-size-13 ml-2"></span>
</button>
</span>
</div>
</p>
</div>
<div class="col-3 text-right float-right">
<a class="btn btn-light bg-color-blue-nav mt-2 d-flex align-items-center" data-title='Key is already installed in "My Workstation"' data-toggle="tooltip" href="https://academy.hackthebox.com/vpn/key">
<div><i class="fad fa-chart-network mr-2"></i></div>
<div class="text-center w-100">Download VPN Connection File</div>
</a>
</div>
</div>
<div>
<div>
<label class="module-question" for="280"><span class="badge badge-soft-dark font-size-14 mr-2">+ 1 <i class="fad fa-cube text-success"></i></span> Perform a zone transfer using the DNS-AXFR.py script against your target for the "inlanefreight.htb" domain and submit the total number of unique subdomains found.
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control bg-color-blue-nav" color="green" id="answer280" maxlength="191" placeholder="Submit your answer here..." type="text"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<p class="mb-0 mr-3 mt-1 font-size-14 font-medium text-white" id="questionStreakPointsText-280">
                                        +10 Streak pts</p>
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="280" id="btnAnswer280">
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
