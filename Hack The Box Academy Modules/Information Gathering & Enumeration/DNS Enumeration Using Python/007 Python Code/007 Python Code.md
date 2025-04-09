
<h1>Python Code</h1>
<hr/>
<p>We have all come across a piece of program code that has confused us more than it has made our work easier. When we open the editor and look at this code, we see a mess of lines of code without any structure:</p>
<ul>
<li>The variables have strange names,</li>
<li>Methods have a few hundred lines with innumerable nested control structures and</li>
<li>a high number of passing parameters.</li>
</ul>
<p>For programmers, bad programming code leads to <code>many lost hours</code>, and entire development departments are caught in a downward spiral, especially when new software is created in a <code>hurry</code>. The work takes place under <code>high pressure</code>, leaving no time for the necessary <code>code revision</code>.</p>
<p>The management has no programming knowledge and does not understand the risks of writing bad code. The more additional functionality the programmers add, the bigger the <code>chaos</code> becomes. Every change to the code leads to further modifications in other components and <code>new errors</code>. Corrections become an overwhelming problem because the programmers have to understand all of the components.</p>
<p>The programming code becomes a complete <code>mess of branches</code> that cannot be cleaned up over time. In the end, the entire development is paralyzed, and productivity drops many times over. The management then usually appoints additional <code>human resources</code> to increase productivity, thereby making the <code>more serious</code> problem. The new people do not understand the existing program, so more and more chaos follows. This leads to inattention on the programmers' part, which is a further factor in the <code>resulting vulnerabilities</code>. Such a bad code can indicate how structured and efficient this software has been developed.</p>
<hr/>
<h2>Programming Guidelines</h2>
<p>The following guidelines for clean programming will enable us to distinguish clear code from bad code and convert bad code into good code. This becomes especially important when we work with different code or when we need to adapt or modify it. The following five guidelines alone will help us keep our code simple, structured, and efficient.</p>
<table>
<thead>
<tr>
<th><strong>Guideline</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Unique names</code></td>
<td>Name variables, functions, and classes with consistent, meaningful, pronounceable, and distinguishable names. These types should be different and clearly identifiable from each other. You can use upper and lower case letters for this.</td>
</tr>
<tr>
<td><code>Avoid error-prone constructs</code></td>
<td>Design control statements in the easiest way. Avoid heavily nested control statements as they are difficult to test and understand.</td>
</tr>
<tr>
<td><code>One task per function</code></td>
<td>Each function should only ever perform one single task. This will later help to understand where the errors occur and to be able to fix them quickly.</td>
</tr>
<tr>
<td><code>Duplicating lines of code are prohibited</code></td>
<td>We must avoid duplicating written code in any case. Otherwise, it will become too big and confusing too fast. Besides, we may also reproduce bugs that will make our code almost impossible to execute until we fix all of them.</td>
</tr>
<tr>
<td><code>Small number of method arguments</code></td>
<td>The fewer arguments have to be used for a function, the easier the function is to understand. Furthermore, the error rate is much lower, and fixing the error is also much more straightforward and, above all, much more time-saving.</td>
</tr>
</tbody>
</table>
<hr/>
<h2>PEP8</h2>
<p>There are guidelines developed especially for Python, known as the <code>Python Enhancement Proposal</code> (<code>PEP8</code>). <a href="https://www.python.org/dev/peps/pep-0008/">PEP8</a> is a document that contains <code>guidelines</code> and <code>best practices</code> for writing Python code and was written in 2001 by Guido van Rossum, Barry Warsaw, and Nick Coghlan. <code>PEP8</code> 's primary focus is to improve the <code>readability</code> and <code>consistency</code> of Python code. When we have more experience in writing Python code, we may start working with others. Writing readable code is crucial because other people who are not familiar with our <code>coding style</code> need to read and understand our code. If we have guidelines that we follow and recognize, others will also find our code easier to read.</p>
<h4>PEP8 Guidelines</h4>
<table>
<thead>
<tr>
<th><strong>Rule</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Indentation</code></td>
<td>4 spaces, no tabs!</td>
</tr>
<tr>
<td><code>Max. Line Length for Code</code></td>
<td>79 characters / line</td>
</tr>
<tr>
<td><code>Max. Line Length for Comments/DocStrings</code></td>
<td>72 characters / line</td>
</tr>
<tr>
<td><code>Encoding</code></td>
<td>UTF-8 for Python 3</td>
</tr>
<tr>
<td><code>Quotes</code></td>
<td>The use of single and double quotes is possible, but we should decide on one of them.</td>
</tr>
<tr>
<td><code>...</code></td>
<td>...</td>
</tr>
</tbody>
</table>
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
