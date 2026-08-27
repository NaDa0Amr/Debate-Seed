[Skip to main content](#content)

[![archive](/static/base/1.0.1/images/arxiv-logo-primary-light.svg)](https://arxiv.org/)


[Search](https://arxiv.org/search)
[Submit](https://arxiv.org/user/create)
[Donate](https://info.arxiv.org/about/donate.html)
[Log in](https://arxiv.org/login)

Search arXiv

Press Enter to search · [Advanced search](https://arxiv.org/search/advanced)

Computer Science > Distributed, Parallel, and Cluster Computing
===============================================================

**arXiv:2006.15704** (cs)

[Submitted on 28 Jun 2020]

Title:PyTorch Distributed: Experiences on Accelerating Data Parallel Training
=============================================================================

Authors:[Shen Li](https://arxiv.org/search/cs?searchtype=author&query=Li,+S), [Yanli Zhao](https://arxiv.org/search/cs?searchtype=author&query=Zhao,+Y), [Rohan Varma](https://arxiv.org/search/cs?searchtype=author&query=Varma,+R), [Omkar Salpekar](https://arxiv.org/search/cs?searchtype=author&query=Salpekar,+O), [Pieter Noordhuis](https://arxiv.org/search/cs?searchtype=author&query=Noordhuis,+P), [Teng Li](https://arxiv.org/search/cs?searchtype=author&query=Li,+T), [Adam Paszke](https://arxiv.org/search/cs?searchtype=author&query=Paszke,+A), [Jeff Smith](https://arxiv.org/search/cs?searchtype=author&query=Smith,+J), [Brian Vaughan](https://arxiv.org/search/cs?searchtype=author&query=Vaughan,+B), [Pritam Damania](https://arxiv.org/search/cs?searchtype=author&query=Damania,+P), [Soumith Chintala](https://arxiv.org/search/cs?searchtype=author&query=Chintala,+S)

View a PDF of the paper titled PyTorch Distributed: Experiences on Accelerating Data Parallel Training, by Shen Li and 10 other authors

[View PDF](/pdf/2006.15704)
[HTML (experimental)](https://arxiv.org/html/2006.15704v1)
> Abstract:This paper presents the design, implementation, and evaluation of the PyTorch distributed data parallel module. PyTorch is a widely-adopted scientific computing package used in deep learning research and applications. Recent advances in deep learning argue for the value of large datasets and large models, which necessitates the ability to scale out model training to more computational resources. Data parallelism has emerged as a popular solution for distributed training thanks to its straightforward principle and broad applicability. In general, the technique of distributed data parallelism replicates the model on every computational resource to generate gradients independently and then communicates those gradients at each iteration to keep model replicas consistent. Despite the conceptual simplicity of the technique, the subtle dependencies between computation and communication make it non-trivial to optimize the distributed training efficiency. As of v1.5, PyTorch natively provides several techniques to accelerate distributed data parallel, including bucketing gradients, overlapping computation with communication, and skipping gradient synchronization. Evaluations show that, when configured appropriately, the PyTorch distributed data parallel module attains near-linear scalability using 256 GPUs.

|  |  |
| --- | --- |
| Comments: | To appear in VLDB 2020 |
| Subjects: | Distributed, Parallel, and Cluster Computing (cs.DC); Machine Learning (cs.LG) |
| Cite as: | [arXiv:2006.15704](https://arxiv.org/abs/2006.15704) [cs.DC] |
|  | (or  [arXiv:2006.15704v1](https://arxiv.org/abs/2006.15704v1) [cs.DC] for this version) |
|  | <https://doi.org/10.48550/arXiv.2006.15704> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Shen Li [[view email](/show-email/7e67b422/2006.15704)]   
**[v1]**
Sun, 28 Jun 2020 20:39:45 UTC (965 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled PyTorch Distributed: Experiences on Accelerating Data Parallel Training, by Shen Li and 10 other authors

* [View PDF](/pdf/2006.15704)
* [HTML (experimental)](https://arxiv.org/html/2006.15704v1)
* [TeX Source](/src/2006.15704)

[![license icon](https://arxiv.org/icons/licenses/by-nc-sa-4.0.png)view license](http://creativecommons.org/licenses/by-nc-sa/4.0/ "Rights to this article")

### Current browse context:

cs.DC

[< prev](/prevnext?id=2006.15704&function=prev&context=cs.DC "previous in cs.DC (accesskey p)")
  |   
[next >](/prevnext?id=2006.15704&function=next&context=cs.DC "next in cs.DC (accesskey n)")

[new](/list/cs.DC/new)
 | 
[recent](/list/cs.DC/recent)
 | [2020-06](/list/cs.DC/2020-06)

Change to browse by:

[cs](/abs/2006.15704?context=cs)  
[cs.LG](/abs/2006.15704?context=cs.LG)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:2006.15704)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=2006.15704)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:2006.15704)

### [DBLP](https://dblp.uni-trier.de) - CS Bibliography

[listing](https://dblp.uni-trier.de/db/journals/corr/corr2006.html#abs-2006-15704 "listing on DBLP") | [bibtex](https://dblp.uni-trier.de/rec/bibtex/journals/corr/abs-2006-15704 "DBLP bibtex record")

[Shen Li](https://dblp.uni-trier.de/search/author?author=Shen%20Li "DBLP author search")  
[Rohan Varma](https://dblp.uni-trier.de/search/author?author=Rohan%20Varma "DBLP author search")  
[Pieter Noordhuis](https://dblp.uni-trier.de/search/author?author=Pieter%20Noordhuis "DBLP author search")  
[Teng Li](https://dblp.uni-trier.de/search/author?author=Teng%20Li "DBLP author search")  
[Adam Paszke](https://dblp.uni-trier.de/search/author?author=Adam%20Paszke "DBLP author search")

…

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/2006.15704&description=PyTorch%20Distributed:%20Experiences%20on%20Accelerating%20Data%20Parallel%20Training "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/2006.15704&title=PyTorch%20Distributed:%20Experiences%20on%20Accelerating%20Data%20Parallel%20Training "Bookmark on Reddit")

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

[Which authors of this paper are endorsers?](/auth/show-endorsers/2006.15704) |
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