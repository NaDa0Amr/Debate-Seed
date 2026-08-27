[Skip to main content](#content)

[![archive](/static/base/1.0.1/images/arxiv-logo-primary-light.svg)](https://arxiv.org/)


[Search](https://arxiv.org/search)
[Submit](https://arxiv.org/user/create)
[Donate](https://info.arxiv.org/about/donate.html)
[Log in](https://arxiv.org/login)

Search arXiv

Press Enter to search · [Advanced search](https://arxiv.org/search/advanced)

Computer Science > Computation and Language
===========================================

**arXiv:2104.04473** (cs)

[Submitted on 9 Apr 2021 ([v1](https://arxiv.org/abs/2104.04473v1)), last revised 23 Aug 2021 (this version, v5)]

Title:Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM
=====================================================================================

Authors:[Deepak Narayanan](https://arxiv.org/search/cs?searchtype=author&query=Narayanan,+D), [Mohammad Shoeybi](https://arxiv.org/search/cs?searchtype=author&query=Shoeybi,+M), [Jared Casper](https://arxiv.org/search/cs?searchtype=author&query=Casper,+J), [Patrick LeGresley](https://arxiv.org/search/cs?searchtype=author&query=LeGresley,+P), [Mostofa Patwary](https://arxiv.org/search/cs?searchtype=author&query=Patwary,+M), [Vijay Anand Korthikanti](https://arxiv.org/search/cs?searchtype=author&query=Korthikanti,+V+A), [Dmitri Vainbrand](https://arxiv.org/search/cs?searchtype=author&query=Vainbrand,+D), [Prethvi Kashinkunti](https://arxiv.org/search/cs?searchtype=author&query=Kashinkunti,+P), [Julie Bernauer](https://arxiv.org/search/cs?searchtype=author&query=Bernauer,+J), [Bryan Catanzaro](https://arxiv.org/search/cs?searchtype=author&query=Catanzaro,+B), [Amar Phanishayee](https://arxiv.org/search/cs?searchtype=author&query=Phanishayee,+A), [Matei Zaharia](https://arxiv.org/search/cs?searchtype=author&query=Zaharia,+M)

View a PDF of the paper titled Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM, by Deepak Narayanan and 11 other authors

[View PDF](/pdf/2104.04473)
[HTML (experimental)](https://arxiv.org/html/2104.04473v5)
> Abstract:Large language models have led to state-of-the-art accuracies across a range of tasks. However, training these models efficiently is challenging for two reasons: a) GPU memory capacity is limited, making it impossible to fit large models on even a multi-GPU server, and b) the number of compute operations required to train these models can result in unrealistically long training times. Consequently, new methods of model parallelism such as tensor and pipeline parallelism have been proposed. Unfortunately, naive usage of these methods leads to fundamental scaling issues at thousands of GPUs, e.g., due to expensive cross-node communication or devices spending significant time waiting on other devices to make progress.
>   
> In this paper, we show how different types of parallelism methods (tensor, pipeline, and data parallelism) can be composed to scale to thousands of GPUs and models with trillions of parameters. We survey techniques for pipeline parallelism and propose a novel interleaved pipeline parallelism schedule that can improve throughput by 10+% with memory footprint comparable to existing approaches. We quantitatively study the trade-offs between tensor, pipeline, and data parallelism, and provide intuition as to how to configure distributed training of a large model. Our approach allows us to perform training iterations on a model with 1 trillion parameters at 502 petaFLOP/s on 3072 GPUs with achieved per-GPU throughput of 52% of theoretical peak. Our code is open sourced at [this https URL](https://github.com/nvidia/megatron-lm).

|  |  |
| --- | --- |
| Comments: | Accepted to SC 2021 |
| Subjects: | Computation and Language (cs.CL); Distributed, Parallel, and Cluster Computing (cs.DC) |
| Cite as: | [arXiv:2104.04473](https://arxiv.org/abs/2104.04473) [cs.CL] |
|  | (or  [arXiv:2104.04473v5](https://arxiv.org/abs/2104.04473v5) [cs.CL] for this version) |
|  | <https://doi.org/10.48550/arXiv.2104.04473> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Deepak Narayanan [[view email](/show-email/0b75803d/2104.04473)]   
**[[v1]](/abs/2104.04473v1)**
Fri, 9 Apr 2021 16:43:11 UTC (3,055 KB)  
**[[v2]](/abs/2104.04473v2)**
Fri, 14 May 2021 17:44:52 UTC (1,732 KB)  
**[[v3]](/abs/2104.04473v3)**
Fri, 30 Jul 2021 07:18:32 UTC (1,196 KB)  
**[[v4]](/abs/2104.04473v4)**
Sun, 15 Aug 2021 07:11:58 UTC (2,353 KB)  
**[v5]**
Mon, 23 Aug 2021 19:41:13 UTC (1,195 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM, by Deepak Narayanan and 11 other authors

* [View PDF](/pdf/2104.04473)
* [HTML (experimental)](https://arxiv.org/html/2104.04473v5)
* [TeX Source](/src/2104.04473)

[view license](http://arxiv.org/licenses/nonexclusive-distrib/1.0/ "Rights to this article")

### Current browse context:

cs.CL

[< prev](/prevnext?id=2104.04473&function=prev&context=cs.CL "previous in cs.CL (accesskey p)")
  |   
[next >](/prevnext?id=2104.04473&function=next&context=cs.CL "next in cs.CL (accesskey n)")

[new](/list/cs.CL/new)
 | 
[recent](/list/cs.CL/recent)
 | [2021-04](/list/cs.CL/2021-04)

Change to browse by:

[cs](/abs/2104.04473?context=cs)  
[cs.DC](/abs/2104.04473?context=cs.DC)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:2104.04473)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=2104.04473)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:2104.04473)

### [1 blog link](/tb/2104.04473)

([what is this?](https://info.arxiv.org/help/trackback.html))

### [DBLP](https://dblp.uni-trier.de) - CS Bibliography

[listing](https://dblp.uni-trier.de/db/journals/corr/corr2104.html#abs-2104-04473 "listing on DBLP") | [bibtex](https://dblp.uni-trier.de/rec/bibtex/journals/corr/abs-2104-04473 "DBLP bibtex record")

[Deepak Narayanan](https://dblp.uni-trier.de/search/author?author=Deepak%20Narayanan "DBLP author search")  
[Mohammad Shoeybi](https://dblp.uni-trier.de/search/author?author=Mohammad%20Shoeybi "DBLP author search")  
[Jared Casper](https://dblp.uni-trier.de/search/author?author=Jared%20Casper "DBLP author search")  
[Patrick LeGresley](https://dblp.uni-trier.de/search/author?author=Patrick%20LeGresley "DBLP author search")  
[Bryan Catanzaro](https://dblp.uni-trier.de/search/author?author=Bryan%20Catanzaro "DBLP author search")

…

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/2104.04473&description=Efficient%20Large-Scale%20Language%20Model%20Training%20on%20GPU%20Clusters%20Using%20Megatron-LM "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/2104.04473&title=Efficient%20Large-Scale%20Language%20Model%20Training%20on%20GPU%20Clusters%20Using%20Megatron-LM "Bookmark on Reddit")

Bibliographic Tools

Bibliographic and Citation Tools
================================

Bibliographic Explorer Toggle

Bibliographic Explorer *([What is the Explorer?](https://info.arxiv.org/labs/showcase.html#arxiv-bibliographic-explorer))*

Connected Papers Toggle

Connected Papers *([What is Connected Papers?](https://www.connectedpapers.com/about))*

Litmaps Toggle

Litmaps *([What is Litmaps?](https://www.litmaps.co/))*

scite.ai Toggle

scite Smart Citations *([What are Smart Citations?](https://www.scite.ai/))*

Code, Data, Media

Code, Data and Media Associated with this Article
=================================================

alphaXiv Toggle

alphaXiv *([What is alphaXiv?](https://alphaxiv.org/))*

Links to Code Toggle

CatalyzeX Code Finder for Papers *([What is CatalyzeX?](https://www.catalyzex.com))*

DagsHub Toggle

DagsHub *([What is DagsHub?](https://dagshub.com/))*

GotitPub Toggle

Gotit.pub *([What is GotitPub?](http://gotit.pub/faq))*

Huggingface Toggle

Hugging Face *([What is Huggingface?](https://huggingface.co/huggingface))*

ScienceCast Toggle

ScienceCast *([What is ScienceCast?](https://sciencecast.org/welcome))*

Demos

Demos
=====

Replicate Toggle

Replicate *([What is Replicate?](https://replicate.com/docs/arxiv/about))*

Spaces Toggle

Hugging Face Spaces *([What is Spaces?](https://huggingface.co/docs/hub/spaces))*

Spaces Toggle

TXYZ.AI *([What is TXYZ.AI?](https://txyz.ai))*

Related Papers

Recommenders and Search Tools
=============================

Link to Influence Flower

Influence Flower *([What are Influence Flowers?](https://influencemap.cmlab.dev/))*

Core recommender toggle

CORE Recommender *([What is CORE?](https://core.ac.uk/services/recommender))*

About arXivLabs

arXivLabs: experimental projects with community collaborators
=============================================================

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).

[Which authors of this paper are endorsers?](/auth/show-endorsers/2104.04473) |
[Disable MathJax](javascript:setMathjaxCookie()) ([What is MathJax?](https://info.arxiv.org/help/mathjax.html))

We gratefully acknowledge support from
our **major funders**,
[**member institutions**](https://info.arxiv.org/about/ourmembers.html), ,
and all contributors.

[About](https://info.arxiv.org/about)
[Help](https://info.arxiv.org/help)
[Contact](https://info.arxiv.org/help/contact.html)
[Subscribe](https://info.arxiv.org/help/subscribe)
[Copyright](https://info.arxiv.org/help/license/index.html)
[Privacy](https://info.arxiv.org/help/policies/privacy_policy.html)
[Accessibility](https://info.arxiv.org/help/web_accessibility.html)
[Operational Status (opens in new tab)](https://status.arxiv.org)

Major funding support from

[![Simons Foundation](/static/base/1.0.1/images/funders/simons-foundation.png)](https://www.simonsfoundation.org/)
[![Simons Foundation International](/static/base/1.0.1/images/funders/simons-foundation-international.png)](https://www.sfi.org.bm/)
[![Schmidt Sciences](/static/base/1.0.1/images/funders/schmidt-sciences.png)](https://www.schmidtsciences.org/)