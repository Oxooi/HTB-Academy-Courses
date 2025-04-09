
<h1>AXFR Function</h1>
<hr/>
<p>It is always an advantage if we separate individual processes from each other and build a single function out of it. This makes it easier to debug later when errors occur, and it makes the main function more independent. It may seem irrelevant at first with such a small tool, but if we start to extend the code, and eventually, our tool grows to a size of more than 1000 lines of code, we will see this advantage. We can divide the process into the following sections:</p>
<ol>
<li>
<p>We now want to create a function that tries to perform a zone transfer using the given domain and DNS servers.</p>
</li>
<li>
<p>If the zone transfer was successful, we want the found subdomains to be displayed directly and stored in our list.</p>
</li>
<li>
<p>In case an error occurs, we want to be informed about the error.</p>
</li>
</ol>
<hr/>
<h2>Functions</h2>
<p>For the <code>functions</code>, we should try to use as few passing arguments as possible. Therefore there should not be more than three arguments, because otherwise there can be a high error-proneness. So in the next example, we use the two arguments <code>domain</code> and <code>nameserver</code>, which we need for the <code>zone transfer</code>.</p>
<p>Again, we should determine how we define the <code>functions</code> and keep this standard. In this case, we define the functions by capitalizing all letters of them. Many people use this capitalization also for classes. Then we should add comments to the function to divide each step in the function into parts.</p>
<h4>DNS-AXFR.py - Functions</h4>
<pre><code class="language-python">&lt;SNIP&gt;
# List of found subdomains
Subdomains = []

# Define the AXFR Function
def AXFR(domain, nameserver):

        # Try zone transfer for given domain and namerserver
		# Perform the zone transfer
        # If zone transfer was successful
        # Add found subdomains to global 'Subdomain' list
        # If zone transfer fails

# Main
if __name__=="__main__":

        # For each nameserver
        # Try AXFR
        # Print the results
        # Print each subdomain
</code></pre>
<hr/>
<h2>Try-Except</h2>
<p>If a statement or an expression is written correctly in terms of its syntax, errors may occur during execution. Errors that occur during execution are called <code>exceptions</code> and are not necessarily serious. A <code>try</code> statement can contain more than one <code>except</code> block to define different actions for different exceptions. At most, one <code>except</code> block is executed. A block can only handle the exceptions that occurred in the corresponding <code>try</code> block, but not those that occur in another except the block of the same <code>try</code> statement.</p>
<h4>DNS-AXFR.py - Try-Except</h4>
<pre><code class="language-python">&lt;SNIP&gt;
# List of found subdomains
Subdomains = []

# Define the AXFR Function
def AXFR(domain, nameserver):

        # Try zone transfer for given domain and namerserver
        try:
				# Perform the zone transfer
                axfr = dz.from_xfr(dq.xfr(nameserver, domain))
				
                # If zone transfer was successful
                # Add found subdomains to global 'Subdomain' list
				
        # If zone transfer fails
        except Exception as error:
                print(error)
                pass
</code></pre>
<hr/>
<h2>If-Else</h2>
<p>With <code>if-else</code> statements, it depends on how many arguments or values we want to check simultaneously. In the best case, there should be only one value or argument to check at a time. However, if we need to check more than one argument and the line can be very long, it is recommended to write every argument in the brackets in a new line.</p>
<h4>If-Else - Few Arguments</h4>
<pre><code class="language-python"># Few arguments
if (arg1 and arg2):
	# Perform specified actions
else:
	pass
</code></pre>
<h4>If-Else - Many Arguments</h4>
<pre><code class="language-python"># Many arguments
if (arg1 
	and arg2
	and arg3
	and arg4):
	
	# Perform specified actions
else:
	pass
</code></pre>
<p>In our <code>DNS.py</code> script, we use only one tested value, and therefore we don't need multiple lines.</p>
<h4>DNS-AXFR.py - If-Else</h4>
<pre><code class="language-python">&lt;SNIP&gt;
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

        # If zone transfer fails
        except Exception as error:
                print(error)
                pass
</code></pre>
<hr/>
<h2>For-Loop</h2>
<p>The <code>For</code> loops should always be kept as simple as possible, as they can cause errors with the number of passes, which we then have to debug manually for each entry to understand what went wrong in the loop. Therefore, we will now append each "<code>record</code>" to our predefined "<code>Subdomains</code>" list to store the subdomains we found.</p>
<h4>DNS-AXFR.py</h4>
<pre><code class="language-python">&lt;SNIP&gt;
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
</code></pre>
<p>Now we have our function, which only needs the domain and the respective name server as arguments. Next, we need the <code>Main function</code>, which passes the arguments to the <code>AXFR function</code>, executes it, and shows us the results.</p>
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
