[Skip to main content](#content)

[![archive](/static/base/1.0.1/images/arxiv-logo-primary-light.svg)](https://arxiv.org/)


[Search](https://arxiv.org/search)
[Submit](https://arxiv.org/user/create)
[Donate](https://info.arxiv.org/about/donate.html)
[Log in](https://arxiv.org/login)

Search arXiv

Press Enter to search · [Advanced search](https://arxiv.org/search/advanced)

Computer Science > Machine Learning
===================================

**arXiv:1910.02054** (cs)

[Submitted on 4 Oct 2019 ([v1](https://arxiv.org/abs/1910.02054v1)), last revised 13 May 2020 (this version, v3)]

Title:ZeRO: Memory Optimizations Toward Training Trillion Parameter Models
==========================================================================

Authors:[Samyam Rajbhandari](https://arxiv.org/search/cs?searchtype=author&query=Rajbhandari,+S), [Jeff Rasley](https://arxiv.org/search/cs?searchtype=author&query=Rasley,+J), [Olatunji Ruwase](https://arxiv.org/search/cs?searchtype=author&query=Ruwase,+O), [Yuxiong He](https://arxiv.org/search/cs?searchtype=author&query=He,+Y)

View a PDF of the paper titled ZeRO: Memory Optimizations Toward Training Trillion Parameter Models, by Samyam Rajbhandari and 3 other authors

[View PDF](/pdf/1910.02054)
[HTML (experimental)](https://arxiv.org/html/1910.02054v3)
> Abstract:Large deep learning models offer significant accuracy gains, but training billions to trillions of parameters is challenging. Existing solutions such as data and model parallelisms exhibit fundamental limitations to fit these models into limited device memory, while obtaining computation, communication and development efficiency. We develop a novel solution, Zero Redundancy Optimizer (ZeRO), to optimize memory, vastly improving training speed while increasing the model size that can be efficiently trained. ZeRO eliminates memory redundancies in data- and model-parallel training while retaining low communication volume and high computational granularity, allowing us to scale the model size proportional to the number of devices with sustained high efficiency. Our analysis on memory requirements and communication volume demonstrates: ZeRO has the potential to scale beyond 1 Trillion parameters using today's hardware.
>   
> We implement and evaluate ZeRO: it trains large models of over 100B parameter with super-linear speedup on 400 GPUs, achieving throughput of 15 Petaflops. This represents an 8x increase in model size and 10x increase in achievable performance over state-of-the-art. In terms of usability, ZeRO can train large models of up to 13B parameters (e.g., larger than Megatron GPT 8.3B and T5 11B) without requiring model parallelism which is harder for scientists to apply. Last but not the least, researchers have used the system breakthroughs of ZeRO to create the world's largest language model (Turing-NLG, 17B parameters) with record breaking accuracy.

|  |  |
| --- | --- |
| Subjects: | Machine Learning (cs.LG); Distributed, Parallel, and Cluster Computing (cs.DC); Machine Learning (stat.ML) |
| Cite as: | [arXiv:1910.02054](https://arxiv.org/abs/1910.02054) [cs.LG] |
|  | (or  [arXiv:1910.02054v3](https://arxiv.org/abs/1910.02054v3) [cs.LG] for this version) |
|  | <https://doi.org/10.48550/arXiv.1910.02054> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Jeff Rasley [[view email](/show-email/6da8a2d7/1910.02054)]   
**[[v1]](/abs/1910.02054v1)**
Fri, 4 Oct 2019 17:29:39 UTC (110 KB) *(withdrawn)*  
**[[v2]](/abs/1910.02054v2)**
Mon, 7 Oct 2019 16:55:13 UTC (110 KB)  
**[v3]**
Wed, 13 May 2020 06:45:15 UTC (632 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled ZeRO: Memory Optimizations Toward Training Trillion Parameter Models, by Samyam Rajbhandari and 3 other authors

* [View PDF](/pdf/1910.02054)
* [HTML (experimental)](https://arxiv.org/html/1910.02054v3)
* [TeX Source](/src/1910.02054)

[view license](http://arxiv.org/licenses/nonexclusive-distrib/1.0/ "Rights to this article")

### Current browse context:

cs.LG

[< prev](/prevnext?id=1910.02054&function=prev&context=cs.LG "previous in cs.LG (accesskey p)")
  |   
[next >](/prevnext?id=1910.02054&function=next&context=cs.LG "next in cs.LG (accesskey n)")

[new](/list/cs.LG/new)
 | 
[recent](/list/cs.LG/recent)
 | [2019-10](/list/cs.LG/2019-10)

Change to browse by:

[cs](/abs/1910.02054?context=cs)  
[cs.DC](/abs/1910.02054?context=cs.DC)  
[stat](/abs/1910.02054?context=stat)  
[stat.ML](/abs/1910.02054?context=stat.ML)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:1910.02054)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=1910.02054)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:1910.02054)

### [3 blog links](/tb/1910.02054)

([what is this?](https://info.arxiv.org/help/trackback.html))

### [DBLP](https://dblp.uni-trier.de) - CS Bibliography

[listing](https://dblp.uni-trier.de/db/journals/corr/corr1910.html#abs-1910-02054 "listing on DBLP") | [bibtex](https://dblp.uni-trier.de/rec/bibtex/journals/corr/abs-1910-02054 "DBLP bibtex record")

[Samyam Rajbhandari](https://dblp.uni-trier.de/search/author?author=Samyam%20Rajbhandari "DBLP author search")  
[Yuxiong He](https://dblp.uni-trier.de/search/author?author=Yuxiong%20He "DBLP author search")

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/1910.02054&description=ZeRO:%20Memory%20Optimizations%20Toward%20Training%20Trillion%20Parameter%20Models "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/1910.02054&title=ZeRO:%20Memory%20Optimizations%20Toward%20Training%20Trillion%20Parameter%20Models "Bookmark on Reddit")

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

IArxiv recommender toggle

IArxiv Recommender
*([What is IArxiv?](https://iarxiv.org/about))*

About arXivLabs

arXivLabs: experimental projects with community collaborators
=============================================================

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).

[Which authors of this paper are endorsers?](/auth/show-endorsers/1910.02054) |
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