# How to set up your cluster for Workflows success

## 2
Hi I’m Becky Pauley and I’m a Member of Technical Staff at Tailscale, working on the Kubernetes Operator.


## 3
Tailscale is a secure connectivity platform built for the way modern teams actually develop i.e.
in a distributed and cloud-native environment.
Whether you’re coding locally, in Codespaces, or deploying via GitHub Actions or Argo, Tailscale keeps every connection private and trusted.

## 4
And I’m Tim, I am an Argo Maintainer, and I’m the infrastructure guy at Pipekit.
Pipekit is a group of Argo maintainers and experts who regularly contribute to Argo.
We offer both support services and an enterprise-level control plane for Argo Workflows which; makes your RBAC life easier, sets up triggering events with minimal configuration and gives you a single-pane view of your Workflows across multiple clusters.


## 5
Today, we’re going to give you a list of Do’s and Don’ts around the subtle misconfigurations, scaling challenges, and security gaps to avoid when using Argo workflows in your cluster- and we will give you some hints about things you should be doing instead.

There’s something in this talk for different experience levels: those new to the project, seasoned Argonauts, and for managers making decisions about Day 2 operations challenges.

We are going to cover a lot in this talk so while we aim to leave you with practical advice, pointers to useful docs, and genuine numbers to take away and actually do things with, we mostly won’t be telling you how to do those things.
You’re more than welcome to come and find us throughout Kubecon if you need further pointers.

So let’s get started with a very brief recap of some of the Argo Workflows fundamentals…

## 6
So as the name hints towards; Argo Workflows is a powerful workflow engine.

There are two main components in Argo Workflows:

The Workflow Controller is the main component of Argo Workflows - it’s a Kubernetes operator that manages workflows and everything workflow related.

The Argo Server provides the UI and API for Argo Workflows.
You can also interact with it programmatically via the CLI.

If you’d like to dive deeper into the architecture of Argo Workflows, you can find more information in Becky and Darko’s talk shown on the screen - we will give you a link to download these slides later, so don’t worry about copying down that lengthy URL.

## 7
We have established that Argo Workflows is a tool that you install and run within Kubernetes.
While this is correct, this specific way of thinking is a really common mindset trap that we see people fall into.
Yes, Argo Workflows is a tool that runs in Kubernetes.
But more importantly its a tool designed to orchestrate Kubernetes Pods by interacting with Kubernetes on a deep level.
This distinction is important.
Don’t think of Argo as an app that happens to have a home inside your cluster and think of it as what it is, an operator that interacts heavily with the kubernetes API to achieve orchestrated Kubernetes things.
This also means that if you want to orchestrate things outside of Kubernetes (e.g.
virtual machines, physical hardware things etc.), Argo Workflows probably isn’t the right tool, although with some magic it’s usually possible to nudge it into orchestrating those things.
If you’re not a Kubernetes person, firstly..
Welcome to KubeCon.
I assume it’s your first time?
Secondly, the big not-so-secret to Argo Workflows success is that you’re going to have to know a thing or two about Kubernetes.
Or at least be really friendly with someone who does.

Re-framing your view of Argo in this way will save you a lot of future headaches (and money).


## 8
Given we now understand that Argo Workflows is just doing orchestration magic to pods in our cluster, it stands to reason that we must have some observability in place so that we can understand the impact that running many orchestrated pods is having on Kubernetes.
The goal here is to have enough visibility that we can see problems before they become catastrophes, and we can tune our cluster and/or Argo according to our specific workloads.

This is commonly where there is crossover between, say, a data scientist, (who wants to just get on and use Argo to do data sciency things) and a cluster administrator, who wants to keep the server hamsters purring (or whatever noise it is that hamsters make).
If you’re a data scientist and you have the luxury of having a cluster admin to hand, it’s time for you to start working together.
If you’re a smaller company and you don’t have this luxury, it’s time to start learning!
Here are some base-level questions that we should be able to answer so that we can have the confidence that those server hamsters are purring (squeaking?):

Is my Argo Workflow Controller healthy?
Is my Kubernetes API healthy?
Is the Kubernetes API rate limiting requests from the Workflow Controller or the K8s Scheduler?
How are my workflows steps? (the pods).
Are they starting up in good time?
Are they resource constrained
Are they scheduled onto appropriate nodes?
Are there any delays or issues with Image pulls?
What about dependent tooling?
Object storage, databases, disks

We should use observability tooling to get these answers and provide alerting and possible remediation when we get an answer we don’t like.

Once we have the metrics to cover those questions, we should consider logs.
The workflow steps emit logs in the form of pod logs.
And the workflow controller is fairly constantly vomiting useful logs that we should collect in case we need them.
As both of these things are just kubernetes pods, we can use a log collection/aggregation tool to slurp those logs and store them for future reference.
You have a couple of options here:
Firstly, Argo Workflows does have an in-built log archiving tool.
You shouldn't use it.
That’s not just my opinion, that’s the opinion of the Workflows documentation too.
The tool will only collect some logs (for example it doesn’t collect those workflow controller logs, or sidecar containers), it makes the logs difficult to parse and is generally not something you want to rely on for anything you consider to be production.

A second option is to use a dedicated log archiving solution such as DataDog or Loki.
You can add custom links to the Workflows UI which allows your users to click through to the exact logs for a given workflow, or step (or both).

## 9
Hopefully, Tim’s convinced us that when we think about Argo Workflows best practices - we actually start by making sure we’re doing Kubernetes Pod things right.
And if that’s our aim, then we don’t want to ignore the resources our Kubernetes Pods need to run.
Generally, we find people start caring about this when things go wrong.
Symptoms of this in our clusters would be things like:  many pods stuck in a pending state, or pods being killed for being Out of Memory.
We might hear people asking: why are our workflows taking longer than usual?
Or Why are all our Workflow steps being scheduled on the same node?
From a business perspective, not dealing with these issues slows things down, makes things unreliable - and cost us more money than we really need to be paying.
Getting these resources right matters.


## 10
When we talk about resources here, what we mean is the CPU and Memory our Workflow Steps need to run.
In other words - Container Requests and Limits.
A very brief recap of these for those less familiar:
Requests are the baseline or average CPU and Memory needed by each container in your Pod .
Our container-level requests are summed up, and are used to make scheduling decisions about which node a pod will be run on.
Meanwhile, Limits are designed, to set a maximum level on the amount of CPU and Memory a pod can consume- preventing a greedy pod or Workflow step causing instability in your cluster.
In terms of Argo Workflows, think about the resources needed by Workflow Controller and Argo Server, those needed by individual workflow steps, sidecars - and don’t forget your init and wait containers.
While there’s no one size fits all answer on how to do set these for Argo Workflows components - we can give some cromulent starting points.

# 11
By default, CPU and Memory request and limits are not set by the helm chart or the official manifests for Workflow Controller or Argo Server- the amount of memory and cpu required will vary hugely depending on the scale and nature of workloads running in your cluster.
In general,  how do we go about setting these values?
Our best friend is observability tooling, which we can use to understand average and peak CPU and Memory utilisation.
Another option that can help us is to use the Vertical Pod Autoscaler in recommendation mode - which can be used to give a starting point for recommended numbers.
One caveat: VPA is not useful if we see very spiky usage in Workflow Controller- so this won’t work for everyone.

## 12
As well as the resources Workflow Controller and Argo Server need, we should also understand the CPU and Memory our Workflow Steps require.
Not every step has the same requirements: so again we need to be looking at actual utilisation to inform the values we set for these.We can start by identifying the average CPU and Memory required by most of our workflow steps - and set this as the Argo Workflows-wide default in the workflow-controller-configmap.
On the screen, we have an example of setting these for the main container - we can also set these defaults for the init and wait container (our executor config).
For steps that are require different CPU- or Memory-, we can set those values on an individual step/task in our Workflow - overriding the defaults we’ve configured here


## 13
Once we’ve set our resource requests and limits right - then to help us with scale and keep Argo running smoothly - we need to keep things tidy.
Why does this matter?
Every workflow we create is a custom resource that exists in our cluster.
In large or busy clusters, these can build up quickly - and can end up hanging around long after our Workflow finished.
If we don’t do anything about this, we’ll notice this impacting the stability of our cluster.
There are things we can configure to help:
You can set workflows to delete themselves once complete.
To do this, look into TTL Strategy.
If you need to keep workflows for regulatory compliance purposes - don’t keep them in your cluster.
Instead, you can archive them to a database.
For this, look into workflow archiving
And we can use Garbage Collection to clean up pods and artifacts.


## 14
And - whilst we’re talking about keeping things tidy - it’s worth checking the versions of Kubernetes and Argo Workflows you are using.
Versions can significantly impact performance.
Generally, our advice is: ensure you are using the latest, stable version of Argo Workflows (not actual latest!).
Tools like Renovate can help here -  they proactively watch for new versions and create Pull Requests to keep things updated.

## 15
We probably really should talk about security.
Argo Workflows is a workflow orchestration engine- and this means Workflow Controller needs to be able to create other workloads in your cluster.
This is a privileged action-  so securing Argo Workflows is important.
There are a few things we can do here - so let’s start by looking at authentication - how human users access Argo Server.

## 16
There are three modes you can use when authenticating to Argo Server: server (which uses the Server's Service Account), client (which uses a kubernetes bearer token) and sso.
The default in Argo Workflows is to use auth mode client.
However, if you haven’t already, we strongly recommend configuring SSO.
First of all- this means authentication can be handled by your identity provider, with MFA enforced.
Also, you can then benefit from SSO RBAC, which allows you to control permissions in Argo Server  by mapping role based access to OIDC groups.
You can find the documentation on how to do this here.

## 17
Even with SSO enabled, our Argo Server instance is more vulnerable than necessary if it’s open to the public internet.
This is by no means an issue unique to Argo Workflows - when we expose things to the internet that don’t need to be, and we don’t have strong authentication and access controls in place - bad things can and do happen (cryptomining!).
We have seen organisations prevent this by getting their engineers to port-forward to Argo Server.
You can do this.
But this is a pain.
Instead, we’d suggest placing Argo Server behind the VPN or secure connectivity tool of your choice.

## 18
Here’s one way of doing using the Tailscale Kubernetes Operator.
In this example, I’m creating an Ingress which points to the existing argo server Service.
However, rather than exposing this over the internet, I’m instead locking things down by adding the tailscale ingressClassName.
This means only authenticated users who are connected to my Tailnet and who have sufficient access permissions can access my argo server instance.
If you’d like to learn more about securing connectivity in and out of your cluster, you can find some examples and further reading linked here.

## 19

let’s talk permissions.
Widely privileged access to kubernetes clusters in engineering teams is still more common than we’d all hope - and we still have seen some organisations giving everyone engineer full admin access to argo workflows, or even to their entire cluster.
Hopefully by now we all know this is a very bad idea.
For our human users, we can use namespaced installations or RBAC permissions to keep things locked down to least privilege approach.
But let’s also not forget our Workflow step permissions because these perform tasks in our cluster.
Don’t give a step more access than it needs to perform its task- and and do avoid using the default service account.


## 20
Now let’s take a step back and consider the Kubernetes cluster as a whole.
It is worth taking the time to plan how your workflow steps will interact with your cluster.

For example, even though it’s 2026 we still talk to Kubernetes users who aren’t aware of cluster autoscaling.
Autoscaling allows you to save compute costs by turning off kubernetes nodes when they aren’t being used (i.e.
when workflows aren’t running), but to also scale them up when they are.

Other areas where you can save a whole load of money is when you consider using ARM64 CPUs instead of AMD64.
ARM is more efficient (and therefore cheaper) than its AMD counterpart, there is usually more server availability for ARM in your cloud provider, and Argo Workflows itself runs very happily on ARM.
I have saved customers upwards of 70% of their costs just by moving as much as possible to ARM and SPOT instances.
If you’re using an On-Prem cluster then these things may not be as easy or as flexible to set compared to your Off-Prem peers, but either way I would encourage you to get into the habit of using NodeSelectors to ensure you’re using the right flavoured node for each workflow step.

## 21
“How many workflows can I run in my cluster?” - it’s a question I’m still asked a lot, and it’s a question that is almost impossible to answer.
No two workflows are the same, no two clusters are the same.
I would say that very broadly, you can consider more than 8000 concurrent workflows to be “massive scale”.
I have seen customers run somewhere in the region of 18-20000 concurrent workflow pods before some Amazon datacenter caught fire.
When the fire happens, the thing that goes pop is usually the Kubernetes API before anything else.
The root cause of that may be your ETCD database being full, or the Kubernetes API itself hitting rate limits - you’ll need your observability to find out that answer.
What you’ll usually find though is that the workflow controller is more than capable of running harder and faster than your Cluster’s control plane can.
There’s some of things you can do to help your workflows run more smoothly at massive scale:
If your observability shows that your control plane is struggling, then beef it up - i.e.
throw more CPU at it or a enlarge the ETCD database.
If your cluster is managed by one of the bigger cloud providers, your control plane will be abstracted away from you; and your ability to tune things in that control plane will be very limited.
This doesn’t mean you can’t drop your cloud provider a support message and beg them to make the control plane bigger.
In our experience you might have to beg a few times until you get a support person who knows that it’s possible, but I promise that it’s possible.
The downside is that it’s usually possible at a hefty price.
It’s often an order of magnitude cheaper to just throw more clusters at the problem.
The headache you will then have is that you have to install the workflow controller and server into each cluster, and you get a whole bunch of different argo server websites to log into or to interact with via the CLI.
If you find yourself in this position, Pipekit can give you a single-pane view over all those clusters, and it’ll still work out cheaper than paying your cloud provider for one mega cluster.


## 22
In terms of setting your workflow controller up for massive scale, again it’s hard to give solid numbers without knowing your specific workloads.
But the numbers on this slide are for a fairly generic 10,000 concurrent workflows.
Maybe use this as a starting point and tune from there - you will need that observability in place to know if you’re hitting the mark, or wasting resources, or even hurting your cluster as a result of implementing these changes.
In addition to those numbers.
Do set
The default requeue time according to your load.
By default, it is 10s.
This means that the controller will check in on the status of your workflow steps every 10 seconds, and if the next step needs to be run, it’ll run it.
If you have a high number of concurrent steps or pods across your cluster, checking the k8s api for their status every 10s might be a little problematic.
Consider increasing the default requeue time, maybe 30s..
maybe 60s even.
Incidentally, if you’re not running at massive scale and you’re starting to fall asleep at this point in the presentation, you could drop the default requeue time down and your workflows will run faster as a result.
Just make sure you have that Kubernetes api observability in place so you can see if you’re going overboard with the numbers.
Also, only set one workflow controller replica:
Workflow controllers do the whole Leader election thing.
Only the ‘lead’ controller is doing anything.
The other is just sat there burning whatever resource request you set when you installed it.
Plus the leader election polling just adds more Kubernetes API calls that you don’t need when running at scale.
If you were to delete your active workflow controller pod, any in-flight workflows steps will just keep working.
Then when your workflow controller pod comes back online, the workflow will just carry on as if nothing happened.
And, often, if you have a single replica of the workflow controller and you delete it, it’s replacement will be up and running faster than a secondary controller could win a leader election.
So I would strongly encourage you to only have 1 replica of the controller, make sure it has solid podpriority (which it does out of the box if you use one of the supported installation mechanisms) and just save yourself those wasted resources.

## 23
The Argo Server on the other hand should have multiple replicas.
There’s no leader election here and you want to ensure that the UI, API, CLI and other features like WorkflowEventBindings always have something on the other end of the phone to talk to them.
You could consider a Horizontal Pod Autoscaler to ensure that the Argo Server pods flex with demand.
The way the Argo Server UI works is it is continuously querying your Kubernetes API for any Workflows CRs, extracting data from them and displaying them to you in a pretty(ish) format.
If you’re running at scale, that’s a whole bunch of CRs to churn through and a lot of Kubernetes API calls that might be better used by the workflow controller to actually run your workflows.
So this is an opportunity again to consider whether you really want to keep those Workflows Custom Resources in your cluster after your workflow has run.
As Becky mentioned, you can delete them or archive them off to the database if you still want to see them in the UI.

## 24
As an infrastructure person, I don’t really understand what all the fuss is about with Yaml.
It’s great.
But I have been told once or twice that some people don’t like trying to build a Workflow in yaml.

Some people apparently prefer grown-up languages like Golang, Python or Typescript (plus whatever you’d describe Java as) and they don’t want to have to get their head around how to make yaml do workflows things.
Luckily there are SDKs for those languages.
You can write your Workflows in the language of your choice and you’ll produce a fully functioning workflow as a result.
Some of these SDKs are auto-generated by the Argo code, others are community maintained.

## 25
When preparing this presentation, we got to this point and realised that we haven’t included enough shiny graphs to keep you managers interested so I wanted to try and give you some real-world numbers on the sort of savings you could make if you do the things we have just laid out to you.

One of our customers took the same advice we have just given in this presentation and their single Workflow runtime was reduced from 6 hours to 30 minutes as indicated by this highly professional graph.

## 26
Another customer had around 30% of their Workflows failing randomly on a given day.
After taking this advice, putting in observability and acting on the results, they reached 99.9% reliability in their Workflow runs.
People no longer had to get out of bed to respond to alerts.

## 27
And finally, by taking the time to understand the relationship between Argo Workflows and Kubernetes, one of the companies we worked with, directly reduced their cloud compute costs by 2/3.

## 28
“Hilarious” graphs aside, the key takeaway we wanted to give to you folks in suits out there is that it does take a bit of planning and some cluster-nudging to get this right… but equally that planning and cluster-nudging will pay off if you give it the space to happen.

Remember that Kubernetes is at the heart of your Argo success and to get the best out of your Workflows at scale, you need to keep coming back to Kubernetes at the core.

## 29
These slides, as well as Becky’s example of using Tailscale to securely access the Argo Server can be found on that github link above.
If you’d like to chat to us about anything you have seen, you can find Becky on the Tailscale booth this week, and I’ll be either on the Pipekit or the Argo booth throughout Kubecon.
