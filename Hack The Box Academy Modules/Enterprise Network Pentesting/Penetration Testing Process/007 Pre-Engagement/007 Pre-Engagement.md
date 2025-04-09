
<h1>Pre-Engagement</h1>
<hr/>
<p>Pre-engagement is the stage of preparation for the actual penetration test. During this stage, many questions are asked, and some contractual agreements are made. The client informs us about what they want to be tested, and we explain in detail how to make the test as efficient as possible.</p>
<p><img alt="Penetration testing process: Pre-Engagement, Information Gathering, Vulnerability Assessment, Exploitation, Post-Exploitation, Lateral Movement, Proof-of-Concept, Post-Engagement." src="https://academy.hackthebox.com/storage/modules/90/0-PT-Process-PRE.png"/></p>
<p>The entire pre-engagement process consists of three essential components:</p>
<ol>
<li>
<p>Scoping questionnaire</p>
</li>
<li>
<p>Pre-engagement meeting</p>
</li>
<li>
<p>Kick-off meeting</p>
</li>
</ol>
<p>Before any of these can be discussed in detail, a <code>Non-Disclosure Agreement</code> (<code>NDA</code>) must be signed by all parties. There are several types of NDAs:</p>
<table>
<thead>
<tr>
<th><strong>Type</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>Unilateral NDA</code></td>
<td>This type of NDA obligates only one party to maintain confidentiality and allows the other party to share the information received with third parties.</td>
</tr>
<tr>
<td><code>Bilateral NDA</code></td>
<td>In this type, both parties are obligated to keep the resulting and acquired information confidential. This is the most common type of NDA that protects the work of penetration testers.</td>
</tr>
<tr>
<td><code>Multilateral NDA</code></td>
<td>Multilateral NDA is a commitment to confidentiality by more than two parties. If we conduct a penetration test for a cooperative network, all parties responsible and involved must sign this document.</td>
</tr>
</tbody>
</table>
<p>Exceptions can also be made in urgent cases, where we jump into the kick-off meeting, which can also occur via an online conference. It is essential to know <code>who in the company is permitted</code> to contract us for a penetration test. Because we cannot accept such an order from everyone. Imagine, for example, that a company employee hires us with the pretext of checking the corporate network's security. However, after we finished the assessment, it turned out that this employee wanted to harm their own company and had no authorization to have the company tested. This would put us in a critical situation from a legal point of view.</p>
<p>Below is a sample (not exhaustive) list of company members who may be authorized to hire us for penetration testing. This can vary from company to company, with larger organizations not involving the C-level staff directly and the responsibility falling on IT, Audit, or IT Security senior management or the like.</p>
<table>
<thead>
<tr>
<th></th>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>Chief Executive Officer (CEO)</td>
<td>Chief Technical Officer (CTO)</td>
<td>Chief Information Security Officer (CISO)</td>
</tr>
<tr>
<td>Chief Security Officer (CSO)</td>
<td>Chief Risk Officer (CRO)</td>
<td>Chief Information Officer (CIO)</td>
</tr>
<tr>
<td>VP of Internal Audit</td>
<td>Audit Manager</td>
<td>VP or Director of IT/Information Security</td>
</tr>
</tbody>
</table>
<p>It is vital to determine early on in the process who has signatory authority for the contract, Rules of Engagement documents, and who will be the primary and secondary points of contact, technical support, and contact for escalating any issues.</p>
<p>This stage also requires the preparation of several documents before a penetration test can be conducted that must be signed by our client and us so that the declaration of consent can also be presented in written form if required. Otherwise the penetration test could breach the <a href="https://www.legislation.gov.uk/ukpga/1990/18/contents">Computer Misuse Act</a>. These documents include, but are not limited to:</p>
<table>
<thead>
<tr>
<th><strong>Document</strong></th>
<th><strong>Timing for Creation</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>1. Non-Disclosure Agreement</code> (<code>NDA</code>)</td>
<td><code>After</code> Initial Contact</td>
</tr>
<tr>
<td><code>2. Scoping Questionnaire</code></td>
<td><code>Before</code> the Pre-Engagement Meeting</td>
</tr>
<tr>
<td><code>3. Scoping Document</code></td>
<td><code>During</code> the Pre-Engagement Meeting</td>
</tr>
<tr>
<td><code>4. Penetration Testing Proposal</code> (<code>Contract/Scope of Work</code> (<code>SoW</code>))</td>
<td><code>During</code> the Pre-engagement Meeting</td>
</tr>
<tr>
<td><code>5. Rules of Engagement</code> (<code>RoE</code>)</td>
<td><code>Before</code> the Kick-Off Meeting</td>
</tr>
<tr>
<td><code>6. Contractors Agreement</code> (Physical Assessments)</td>
<td><code>Before</code> the Kick-Off Meeting</td>
</tr>
<tr>
<td><code>7. Reports</code></td>
<td><code>During</code> and <code>after</code> the conducted Penetration Test</td>
</tr>
</tbody>
</table>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: Our client may provide a separate scoping document listing in-scope IP addresses/ranges/URLs and any necessary credentials but this information should also be documented as an appendix in the RoE document.</p>
</div>
</div>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0"><b>Important Note:</b><p>These documents should be reviewed and adapted by a lawyer after they have been prepared.</p>
</p></div>
</div>
<hr/>
<h2>Scoping Questionnaire</h2>
<p>After initial contact is made with the client, we typically send them a <code>Scoping Questionnaire</code> to better understand the services they are seeking. This scoping questionnaire should clearly explain our services and may typically ask them to choose one or more from the following list:</p>
<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>☐ Internal Vulnerability Assessment</td>
<td>☐ External Vulnerability Assessment</td>
</tr>
<tr>
<td>☐ Internal Penetration Test</td>
<td>☐ External Penetration Test</td>
</tr>
<tr>
<td>☐ Wireless Security Assessment</td>
<td>☐ Application Security Assessment</td>
</tr>
<tr>
<td>☐ Physical Security Assessment</td>
<td>☐ Social Engineering Assessment</td>
</tr>
<tr>
<td>☐ Red Team Assessment</td>
<td>☐ Web Application Security Assessment</td>
</tr>
</tbody>
</table>
<p>Under each of these, the questionnaire should allow the client to be more specific about the required assessment. Do they need a web application or mobile application assessment? Secure code review? Should the Internal Penetration Test be black box and semi-evasive? Do they want just a phishing assessment as part of the Social Engineering Assessment or also vishing calls? This is our chance to explain the depth and breadth of our services, ensure that we understand our client's needs and expectations, and ensure that we can adequately deliver the assessment they require.</p>
<p>Aside from the assessment type, client name, address, and key personnel contact information, some other critical pieces of information include:</p>
<table>
<thead>
<tr>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td>How many expected live hosts?</td>
<td></td>
</tr>
<tr>
<td>How many IPs/CIDR ranges in scope?</td>
<td></td>
</tr>
<tr>
<td>How many Domains/Subdomains are in scope?</td>
<td></td>
</tr>
<tr>
<td>How many wireless SSIDs in scope?</td>
<td></td>
</tr>
<tr>
<td>How many web/mobile applications? If testing is authenticated, how many roles (standard user, admin, etc.)?</td>
<td></td>
</tr>
<tr>
<td>For a phishing assessment, how many users will be targeted? Will the client provide a list, or we will be required to gather this list via OSINT?</td>
<td></td>
</tr>
<tr>
<td>If the client is requesting a Physical Assessment, how many locations? If multiple sites are in-scope, are they geographically dispersed?</td>
<td></td>
</tr>
<tr>
<td>What is the objective of the Red Team Assessment? Are any activities (such as phishing or physical security attacks) out of scope?</td>
<td></td>
</tr>
<tr>
<td>Is a separate Active Directory Security Assessment desired?</td>
<td></td>
</tr>
<tr>
<td>Will network testing be conducted from an anonymous user on the network or a standard domain user?</td>
<td></td>
</tr>
<tr>
<td>Do we need to bypass Network Access Control (NAC)?</td>
<td></td>
</tr>
</tbody>
</table>
<p>Finally, we will want to ask about information disclosure and evasiveness (if applicable to the assessment type):</p>
<ul>
<li>
<p>Is the Penetration Test black box (no information provided), grey box (only IP address/CIDR ranges/URLs provided), white box (detailed information provided)</p>
</li>
<li>
<p>Would they like us to test from a non-evasive, hybrid-evasive (start quiet and gradually become "louder" to assess at what level the client's security personnel detect our activities), or fully evasive.</p>
</li>
</ul>
<p>This information will help us ensure we assign the right resources and deliver the engagement based on the client's expectations. This information is also necessary for providing an accurate proposal with a project timeline (for example, a Vulnerability Assessment will take considerably less time than a Red Team Assessment) and cost (an External Penetration Test against 10 IPs will cost significantly less than an Internal Penetration Test with 30 /24 networks in-scope).</p>
<p>Based on the information we received from the scoping questionnaire, we create an overview and summarize all information in the <code>Scoping Document</code>.</p>
<hr/>
<h2>Pre-Engagement Meeting</h2>
<p>Once we have an initial idea of the client's project requirements, we can move on to the <code>pre-engagement meeting</code>. This meeting discusses all relevant and essential components with the customer before the penetration test, explaining them to our customer. The information we gather during this phase, along with the data collected from the scoping questionnaire, will serve as inputs to the <code>Penetration Testing Proposal</code>, also known as the <code>Contract</code> or <code>Scope of Work</code> (<code>SoW</code>). We can think of the whole process as a visit to the doctor to inform ourselves regarding the planned examinations. This phase typically occurs via e-mail and during an online conference call or in-person meeting.</p>
<div class="card bg-light">
<div class="card-body">
<p class="mb-0">Note: We may encounter clients during our career that are undergoing their first ever penetration test, or the direct client PoC is not familiar with the process. It is not uncommon to use part of the pre-engagement meeting to review the scoping questionnaire either in part or step-by-step.</p>
</div>
</div>
<h4>Contract - Checklist</h4>
<table>
<thead>
<tr>
<th><strong>Checkpoint</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>☐ NDA</code></td>
<td>Non-Disclosure Agreement (NDA) refers to a secrecy contract between the client and the contractor regarding all written or verbal information concerning an order/project. The contractor agrees to treat all confidential information brought to its attention as strictly confidential, even after the order/project is completed. Furthermore, any exceptions to confidentiality, the transferability of rights and obligations, and contractual penalties shall be stipulated in the agreement. The NDA should be signed before the kick-off meeting or at the latest during the meeting before any information is discussed in detail.</td>
</tr>
<tr>
<td><code>☐ Goals</code></td>
<td>Goals are milestones that must be achieved during the order/project. In this process, goal setting is started with the significant goals and continued with fine-grained and small ones.</td>
</tr>
<tr>
<td><code>☐ Scope</code></td>
<td>The individual components to be tested are discussed and defined. These may include domains, IP ranges, individual hosts, specific accounts, security systems, etc. Our customers may expect us to find out one or the other point by ourselves. However, the legal basis for testing the individual components has the highest priority here.</td>
</tr>
<tr>
<td><code>☐ Penetration Testing Type</code></td>
<td>When choosing the type of penetration test, we present the individual options and explain the advantages and disadvantages. Since we already know the goals and scope of our customers, we can and should also make a recommendation on what we advise and justify our recommendation accordingly. Which type is used in the end is the client's decision.</td>
</tr>
<tr>
<td><code>☐ Methodologies</code></td>
<td>Examples: OSSTMM, OWASP, automated and manual unauthenticated analysis of the internal and external network components, vulnerability assessments of network components and web applications, vulnerability threat vectorization, verification and exploitation, and exploit development to facilitate evasion techniques.</td>
</tr>
<tr>
<td><code>☐ Penetration Testing Locations</code></td>
<td>External: Remote (via secure VPN) and/or Internal: Internal or Remote (via secure VPN)</td>
</tr>
<tr>
<td><code>☐ Time Estimation</code></td>
<td>For the time estimation, we need the start and the end date for the penetration test. This gives us a precise time window to perform the test and helps us plan our procedure. It is also vital to explicitly ask how time windows the individual attacks (Exploitation / Post-Exploitation / Lateral Movement) are to be carried out. These can be carried out during or outside regular working hours. When testing outside regular working hours, the focus is more on the security solutions and systems that should withstand our attacks.</td>
</tr>
<tr>
<td><code>☐ Third Parties</code></td>
<td>For the third parties, it must be determined via which third-party providers our customer obtains services. These can be cloud providers, ISPs, and other hosting providers. Our client must obtain written consent from these providers describing that they agree and are aware that certain parts of their service will be subject to a simulated hacking attack. It is also highly advisable to require the contractor to forward the third-party permission sent to us so that we have actual confirmation that this permission has indeed been obtained.</td>
</tr>
<tr>
<td><code>☐ Evasive Testing</code></td>
<td>Evasive testing is the test of evading and passing security traffic and security systems in the customer's infrastructure. We look for techniques that allow us to find out information about the internal components and attack them. It depends on whether our contractor wants us to use such techniques or not.</td>
</tr>
<tr>
<td><code>☐ Risks</code></td>
<td>We must also inform our client about the risks involved in the tests and the possible consequences. Based on the risks and their potential severity, we can then set the limitations together and take certain precautions.</td>
</tr>
<tr>
<td><code>☐ Scope Limitations &amp; Restrictions</code></td>
<td>It is also essential to determine which servers, workstations, or other network components are essential for the client's proper functioning and its customers. We will have to avoid these and must not influence them any further, as this could lead to critical technical errors that could also affect our client's customers in production.</td>
</tr>
<tr>
<td><code>☐ Information Handling</code></td>
<td>HIPAA, PCI, HITRUST, FISMA/NIST, etc.</td>
</tr>
<tr>
<td><code>☐ Contact Information</code></td>
<td>For the contact information, we need to create a list of each person's name, title, job title, e-mail address, phone number, office phone number, and an escalation priority order.</td>
</tr>
<tr>
<td><code>☐ Lines of Communication</code></td>
<td>It should also be documented which communication channels are used to exchange information between the customer and us. This may involve e-mail correspondence, telephone calls, or personal meetings.</td>
</tr>
<tr>
<td><code>☐ Reporting</code></td>
<td>Apart from the report's structure, any customer-specific requirements the report should contain are also discussed. In addition, we clarify how the reporting is to take place and whether a presentation of the results is desired.</td>
</tr>
<tr>
<td><code>☐ Payment Terms</code></td>
<td>Finally,  prices and the terms of payment are explained.</td>
</tr>
</tbody>
</table>
<p>The most crucial element of this meeting is the detailed presentation of the penetration test to our client and its focus. As we already know, each piece of infrastructure is unique for the most part, and each client has particular preferences on which they place the most importance. Finding out these priorities is an essential part of this meeting.</p>
<p>We can think of it as ordering in a restaurant. If we want a medium-rare steak and the chef gives us a well-done steak because he believes it is better, it will not be what we were hoping for. Therefore, we should prioritize our client's wishes and serve the steak as they ordered.</p>
<p>Based on the <code>Contract Checklist</code> and the input information shared in scoping, the <code>Penetration Testing Proposal</code> (<code>Contract</code>) and the associated <code>Rules of Engagement</code> (<code>RoE</code>) are created.</p>
<h4>Rules of Engagement - Checklist</h4>
<table>
<thead>
<tr>
<th><strong>Checkpoint</strong></th>
<th><strong>Contents</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>☐ Introduction</code></td>
<td>Description of this document.</td>
</tr>
<tr>
<td><code>☐ Contractor</code></td>
<td>Company name, contractor full name, job title.</td>
</tr>
<tr>
<td><code>☐ Penetration Testers</code></td>
<td>Company name, pentesters full name.</td>
</tr>
<tr>
<td><code>☐ Contact Information</code></td>
<td>Mailing addresses, e-mail addresses, and phone numbers of all client parties and penetration testers.</td>
</tr>
<tr>
<td><code>☐ Purpose</code></td>
<td>Description of the purpose for the conducted penetration test.</td>
</tr>
<tr>
<td><code>☐ Goals</code></td>
<td>Description of the goals that should be achieved with the penetration test.</td>
</tr>
<tr>
<td><code>☐ Scope</code></td>
<td>All IPs, domain names, URLs, or CIDR ranges.</td>
</tr>
<tr>
<td><code>☐ Lines of Communication</code></td>
<td>Online conferences or phone calls or face-to-face meetings, or via e-mail.</td>
</tr>
<tr>
<td><code>☐ Time Estimation</code></td>
<td>Start and end dates.</td>
</tr>
<tr>
<td><code>☐ Time of the Day to Test</code></td>
<td>Times of the day to test.</td>
</tr>
<tr>
<td><code>☐ Penetration Testing Type</code></td>
<td>External/Internal Penetration Test/Vulnerability Assessments/Social Engineering.</td>
</tr>
<tr>
<td><code>☐ Penetration Testing Locations</code></td>
<td>Description of how the connection to the client network is established.</td>
</tr>
<tr>
<td><code>☐ Methodologies</code></td>
<td>OSSTMM, PTES, OWASP, and others.</td>
</tr>
<tr>
<td><code>☐ Objectives / Flags</code></td>
<td>Users, specific files, specific information, and others.</td>
</tr>
<tr>
<td><code>☐ Evidence Handling</code></td>
<td>Encryption, secure protocols</td>
</tr>
<tr>
<td><code>☐ System Backups</code></td>
<td>Configuration files, databases, and others.</td>
</tr>
<tr>
<td><code>☐ Information Handling</code></td>
<td>Strong data encryption</td>
</tr>
<tr>
<td><code>☐ Incident Handling and Reporting</code></td>
<td>Cases for contact, pentest interruptions, type of reports</td>
</tr>
<tr>
<td><code>☐ Status Meetings</code></td>
<td>Frequency of meetings, dates, times, included parties</td>
</tr>
<tr>
<td><code>☐ Reporting</code></td>
<td>Type, target readers, focus</td>
</tr>
<tr>
<td><code>☐ Retesting</code></td>
<td>Start and end dates</td>
</tr>
<tr>
<td><code>☐ Disclaimers and Limitation of Liability</code></td>
<td>System damage, data loss</td>
</tr>
<tr>
<td><code>☐ Permission to Test</code></td>
<td>Signed contract, contractors agreement</td>
</tr>
</tbody>
</table>
<hr/>
<h2>Kick-Off Meeting</h2>
<p>The <code>kick-off meeting</code> usually occurs at a scheduled time and in-person after signing all contractual documents. This meeting usually includes client POC(s) (from Internal Audit, Information Security, IT, Governance &amp; Risk, etc., depending on the client), client technical support staff (developers, sysadmins, network engineers, etc.), and the penetration testing team (someone in a management role (such as the Practice Lead), the actual penetration tester(s), and sometimes a Project Manager or even the Sales Account Executive or similar). We will go over the nature of the penetration test and how it will take place. Usually, there is no Denial of Service (DoS) testing. We also explain that if a critical vulnerability is identified, penetration testing activities will be paused, a vulnerability notification report will be generated, and the emergency contacts will be contacted. Typically these are only generated during External Penetration Tests for critical flaws such as unauthenticated remote code execution (RCE), SQL injection, or another flaw that leads to sensitive data disclosure. The purpose of this notification is to allow the client to assess the risk internally and determine if the issue warrants an emergency fix. We would typically only stop an Internal Penetration Test and alert the client if a system becomes unresponsive, we find evidence of illegal activity (such as illegal content on a file share) or the presence of an external threat actor in the network or a prior breach.</p>
<p>We must also inform our customers about potential risks during a penetration test. For example, we should mention that a penetration test can leave many <code>log entries and alarms</code> in their security applications. In addition, if brute forcing or any similar attack is used, it is also worth mentioning that we may accidentally <code>lock some users</code> found during the penetration test. We also must inform our customers that they must contact us immediately if the penetration test performed <code>negatively impacts their network</code>.</p>
<p>Explaining the penetration testing process gives everyone involved a clear idea of our entire process. This demonstrates our professional approach and convinces our questioners that we know what we are doing. Because apart from the technical staff, CTO, and CISO, it will sound like a certain kind of magic that is very difficult for non-technical professionals to understand. So we must be mindful of our audience and target the most technically inexperienced questioner so our approach can be followed by everyone we talk to.</p>
<p>All points related to testing need to be discussed and clarified. It is crucial to respond precisely to the wishes and expectations of the customer/client. Every company structure and network is different and requires an adapted approach. Each client has different goals, and we should adjust our testing to their wishes. We can typically see how experienced our clients are in undergoing penetration tests early in the call, so we may have to shift our focus to explain things in more detail and be prepared to field more questions, or the kickoff call may be very quick and straightforward.</p>
<hr/>
<h2>Contractors Agreement</h2>
<p>If the penetration test also includes physical testing, then an additional contractor's agreement is required. Since it is not only a virtual environment but also a physical intrusion, completely different laws apply here. It is also possible that many of the employees have not been informed about the test. Suppose we encounter employees with a very high-security awareness during the physical attack and social engineering attempts, and we get caught. In that case, the employees will, in most cases, contact the police. This additional <code>contractor's agreement</code> is our "<code>get out of jail free card</code>" in this case.</p>
<h4>Contractors Agreement - Checklist for Physical Assessments</h4>
<table>
<thead>
<tr>
<th><strong>Checkpoint</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><code>☐ Introduction</code></td>
</tr>
<tr>
<td><code>☐ Contractor</code></td>
</tr>
<tr>
<td><code>☐ Purpose</code></td>
</tr>
<tr>
<td><code>☐ Goal</code></td>
</tr>
<tr>
<td><code>☐ Penetration Testers</code></td>
</tr>
<tr>
<td><code>☐ Contact Information</code></td>
</tr>
<tr>
<td><code>☐ Physical Addresses</code></td>
</tr>
<tr>
<td><code>☐ Building Name</code></td>
</tr>
<tr>
<td><code>☐ Floors</code></td>
</tr>
<tr>
<td><code>☐ Physical Room Identifications</code></td>
</tr>
<tr>
<td><code>☐ Physical Components</code></td>
</tr>
<tr>
<td><code>☐ Timeline</code></td>
</tr>
<tr>
<td><code>☐ Notarization</code></td>
</tr>
<tr>
<td><code>☐ Permission to Test</code></td>
</tr>
</tbody>
</table>
<hr/>
<h2>Setting Up</h2>
<p>After all the above points have been worked through, and we have the necessary information, we plan our approach and prepare everything. We will find that the penetration test results are still unknown, but we can prepare our VMs, VPS, and other tools/systems for all scenarios and situations. More information and how to prepare these systems can be found in the <a href="https://academy.hackthebox.com/module/details/87">Setting Up</a> module.</p>
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
<label class="module-question" for="692"><span class="badge badge-soft-dark font-size-14 mr-2">+ 2 <i class="fad fa-cube text-success"></i></span> How many documents must be prepared in total for a penetration test?
                            </label>
<div class="row">
<div class="col-lg-12 mb-4">
<input class="form-control text-success" disabled="true" type="text" value="7"/>
</div>
<div class="d-flex justify-content-end w-100 mr-3">
<div class="mb-4 mr-1 d-flex align-items-center">
<button class="btn btn-primary btn-block btnAnswer" data-question-id="692" disabled="true" id="btnAnswer692">
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
