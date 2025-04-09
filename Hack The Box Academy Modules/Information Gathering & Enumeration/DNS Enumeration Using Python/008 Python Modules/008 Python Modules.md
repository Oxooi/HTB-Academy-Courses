
<h1>Python Modules</h1>
<hr/>
<p>Before we start coding our tool, we have to determine which modules we need and which are best suited for it. A quick search on Google will bring us to the module called "<a href="https://dnspython.readthedocs.io/en/latest/">dnspython</a>". Our goal is to perform a zone transfer, and accordingly, we need to find the appropriate classes and functions to communicate with the DNS servers. Another extension that we can use to develop such tools with Python 3 is <a href="https://ipython.org/install.html">IPython</a>. It supports auto-completion and shows the different options in the corresponding classes and modules in an interactive Python shell.</p>
<p>After we have installed the module, we can import it. This module offers us the classes <code>Query</code>, <code>Resolver</code>, and <code>Zone</code>. The <code>dns.zone</code> module contains a "<code>from_xfr</code>" class. We can find this out by using the <code>help()</code> function in Python.</p>
<h4>Python Help()</h4>
<pre><code class="language-shell-session">[!bash!]$ ipython

In [1]: import dns.zone as dz

In [2]: help(dz.  #[1x Tab]

                 BadZone       dns           from_text()   generators    NoSOA         PY3           string_types  text_type     Zone
                 BytesIO       from_file()   from_xfr()    NoNS          os            re            sys           UnknownOrigin
</code></pre>
<h4>Dns.Zone.From_XFR()</h4>
<pre><code class="language-shell-session">In [2]: help(dz.from_xfr) 
</code></pre>
<h4>From_XFR() - Documentation</h4>
<pre><code class="language-shell-session">from_xfr(xfr, zone_factory=&lt;class 'dns.zone.Zone'&gt;, relativize=True, check_origin=True)
    Convert the output of a zone transfer generator into a zone object.

    @param xfr: The xfr generator
    @type xfr: generator of dns.message.Message objects
    @param relativize: should names be relativized?  The default is True.
    It is essential that the relativize setting matches the one specified
    to dns.query.xfr().
    @type relativize: bool
    @param check_origin: should sanity checks of the origin node be done?
    The default is True.
    @type check_origin: bool
    @raises dns.zone.NoSOA: No SOA RR was found at the zone origin
    @raises dns.zone.NoNS: No NS RRset was found at the zone origin
    @rtype: dns.zone.Zone object
</code></pre>
<p>We can also find the documentation for this on the <a href="https://dnspython.readthedocs.io/en/latest/zone-make.html">documentation page</a> that describes the required parameters for the <code>from_xfr()</code> function. From the parameter "<code>xfr</code>," we will also need the <code>dns.query</code> class. So we should also note this class for later use.</p>
<h4>Notes</h4>
<pre><code class="language-python"># Notes
import dns.zone as dz
import dns.query as dq

# axfr = dz.from_xfr(dq.xfr())
</code></pre>
<p>We need to take a closer look at the <code>dns.query.xfr()</code> function to determine which parameters are required.</p>
<h4>Dns.Query.XFR()</h4>
<pre><code class="language-shell-session">In [3]: help(dq.xfr) 
</code></pre>
<h4>XFR() - Documentation</h4>
<pre><code class="language-shell-session">Help on function xfr in module dns.query:

xfr(where, zone, rdtype=252, rdclass=1, timeout=None, port=53, keyring=None, keyname=None, relativize=True, af=None, lifetime=None, source=None, source_port=0, serial=0, use_udp=False, keyalgorithm=&lt;DNS name HMAC-MD5.SIG-ALG.REG.INT.&gt;)
    Return a generator for the responses to a zone transfer.

    *where*.  If the inference attempt fails, AF_INET is used.  This
    parameter is historical; you need never set it.
&lt;SNIP&gt;
</code></pre>
<p>Here we can see that only two variables have no value and therefore need specific parameters to perform this function.</p>
<ul>
<li>
<code>where</code>
</li>
<li>
<code>zone</code>
</li>
</ul>
<p>We can also find out the required parameters by executing the function. Because if we do not output any parameters, an error will occur with the description that says which parameters are needed.</p>
<h4>Required Parameters</h4>
<pre><code class="language-shell-session">In [4]: dq.xfr()

---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
&lt;ipython-input-14-672b143b8cfc&gt; in &lt;module&gt;
----&gt; 1 dq.xfr()

TypeError: xfr() missing 2 required positional arguments: 'where' and 'zone'
</code></pre>
<p>In this case, the variable "<code>where</code>" stands for the DNS server and the variable "<code>zone</code>" for the domain. We note this as well.</p>
<h4>Notes</h4>
<pre><code class="language-python"># Notes
import dns.zone as dz
import dns.query as dq

# axfr = dz.from_xfr(dq.xfr(nameserver, domain))
</code></pre>
<hr/>
<h2>DNS Requests</h2>
<p>We have to find out how to resolve our requests by using specific DNS servers. The easiest way with the necessary class would be "<code>dns.resolver</code>". In the <a href="https://dnspython.readthedocs.io/en/latest/resolver-class.html">documentation</a>, we can find the class "<code>Resolver</code>" which allows us to specify the DNS servers we want to send our requests to. Of course, we can also automatically find these DNS servers, so we do not have to change them manually. Nevertheless, we have to be careful because companies often use DNS servers from third party providers for which we usually do not have the permissions to test them. Therefore, we recommend that we specify them manually and preferably in the command line rather than in our code. To make this possible, we import another module called "<code>argparse</code>". Accordingly, we also add this information to our notes.</p>
<h4>Notes</h4>
<pre><code class="language-python"># Notes
import dns.zone as dz
import dns.query as dq
import dns.resolver as dr
import argparse

# axfr = dz.from_xfr(dq.xfr(nameserver, domain))

# NS = dr.Resolver()
# NS.nameservers = ['ns1', 'ns2']
</code></pre>
<hr/>
<p>We now have to find the "NS" records for this domain, and instead of using the <code>dig</code> tool, we do it with our Python modules. In this example, we still use the domain called:</p>
<ul>
<li>
<code>inlanefreight.com</code>
</li>
</ul>
<p>The corresponding NS servers we found by using the following code:</p>
<h4>NS Records - DNS.Resolver</h4>
<pre><code class="language-shell-session">[!bash!]$ python3

&gt;&gt;&gt; import dns.resolver
&gt;&gt;&gt; 
&gt;&gt;&gt; nameservers = dns.resolver.query('inlanefreight.com', 'NS')
&gt;&gt;&gt; for ns in nameservers:
...    	print('NS:', ns)
...
NS: ns1.inlanefreight.com.
NS: ns2.inlanefreight.com.
</code></pre>
<p>In summary, we have the following information now:</p>
<pre><code class="language-python">Domain = 'inlanefreight.com'
DNS Servers = ['ns1.inlanefreight.com', 'ns2.inlanefreight.com']
</code></pre>
<p>Now we can summarize all our information and write the first lines of our code.</p>
<h4>DNS-AXFR.py</h4>
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
