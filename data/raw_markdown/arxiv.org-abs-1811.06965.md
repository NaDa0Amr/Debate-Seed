[Skip to main content](#content)

[![archive](/static/base/1.0.1/images/arxiv-logo-primary-light.svg)](https://arxiv.org/)


[Search](https://arxiv.org/search)
[Submit](https://arxiv.org/user/create)
[Donate](https://info.arxiv.org/about/donate.html)
[Log in](https://arxiv.org/login)

Search arXiv

Press Enter to search · [Advanced search](https://arxiv.org/search/advanced)

Computer Science > Computer Vision and Pattern Recognition
==========================================================

**arXiv:1811.06965** (cs)

[Submitted on 16 Nov 2018 ([v1](https://arxiv.org/abs/1811.06965v1)), last revised 25 Jul 2019 (this version, v5)]

Title:GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism
===================================================================================

Authors:[Yanping Huang](https://arxiv.org/search/cs?searchtype=author&query=Huang,+Y), [Youlong Cheng](https://arxiv.org/search/cs?searchtype=author&query=Cheng,+Y), [Ankur Bapna](https://arxiv.org/search/cs?searchtype=author&query=Bapna,+A), [Orhan Firat](https://arxiv.org/search/cs?searchtype=author&query=Firat,+O), [Mia Xu Chen](https://arxiv.org/search/cs?searchtype=author&query=Chen,+M+X), [Dehao Chen](https://arxiv.org/search/cs?searchtype=author&query=Chen,+D), [HyoukJoong Lee](https://arxiv.org/search/cs?searchtype=author&query=Lee,+H), [Jiquan Ngiam](https://arxiv.org/search/cs?searchtype=author&query=Ngiam,+J), [Quoc V. Le](https://arxiv.org/search/cs?searchtype=author&query=Le,+Q+V), [Yonghui Wu](https://arxiv.org/search/cs?searchtype=author&query=Wu,+Y), [Zhifeng Chen](https://arxiv.org/search/cs?searchtype=author&query=Chen,+Z)

View a PDF of the paper titled GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism, by Yanping Huang and 10 other authors

[View PDF](/pdf/1811.06965)
[HTML (experimental)](https://arxiv.org/html/1811.06965v5)
> Abstract:Scaling up deep neural network capacity has been known as an effective approach to improving model quality for several different machine learning tasks. In many cases, increasing model capacity beyond the memory limit of a single accelerator has required developing special algorithms or infrastructure. These solutions are often architecture-specific and do not transfer to other tasks. To address the need for efficient and task-independent model parallelism, we introduce GPipe, a pipeline parallelism library that allows scaling any network that can be expressed as a sequence of layers. By pipelining different sub-sequences of layers on separate accelerators, GPipe provides the flexibility of scaling a variety of different networks to gigantic sizes efficiently. Moreover, GPipe utilizes a novel batch-splitting pipelining algorithm, resulting in almost linear speedup when a model is partitioned across multiple accelerators. We demonstrate the advantages of GPipe by training large-scale neural networks on two different tasks with distinct network architectures: (i) Image Classification: We train a 557-million-parameter AmoebaNet model and attain a top-1 accuracy of 84.4% on ImageNet-2012, (ii) Multilingual Neural Machine Translation: We train a single 6-billion-parameter, 128-layer Transformer model on a corpus spanning over 100 languages and achieve better quality than all bilingual models.

|  |  |
| --- | --- |
| Comments: | 11 pages. Work in progress. Copyright 2018 by the authors |
| Subjects: | Computer Vision and Pattern Recognition (cs.CV) |
| Cite as: | [arXiv:1811.06965](https://arxiv.org/abs/1811.06965) [cs.CV] |
|  | (or  [arXiv:1811.06965v5](https://arxiv.org/abs/1811.06965v5) [cs.CV] for this version) |
|  | <https://doi.org/10.48550/arXiv.1811.06965> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Yanping Huang [[view email](/show-email/b9b84336/1811.06965)]   
**[[v1]](/abs/1811.06965v1)**
Fri, 16 Nov 2018 18:43:28 UTC (653 KB)  
**[[v2]](/abs/1811.06965v2)**
Mon, 19 Nov 2018 18:32:58 UTC (542 KB)  
**[[v3]](/abs/1811.06965v3)**
Tue, 20 Nov 2018 17:25:46 UTC (543 KB)  
**[[v4]](/abs/1811.06965v4)**
Wed, 12 Dec 2018 17:45:02 UTC (544 KB)  
**[v5]**
Thu, 25 Jul 2019 21:42:58 UTC (779 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism, by Yanping Huang and 10 other authors

* [View PDF](/pdf/1811.06965)
* [HTML (experimental)](https://arxiv.org/html/1811.06965v5)
* [TeX Source](/src/1811.06965)

[view license](http://arxiv.org/licenses/nonexclusive-distrib/1.0/ "Rights to this article")

### Current browse context:

cs.CV

[< prev](/prevnext?id=1811.06965&function=prev&context=cs.CV "previous in cs.CV (accesskey p)")
  |   
[next >](/prevnext?id=1811.06965&function=next&context=cs.CV "next in cs.CV (accesskey n)")

[new](/list/cs.CV/new)
 | 
[recent](/list/cs.CV/recent)
 | [2018-11](/list/cs.CV/2018-11)

Change to browse by:

[cs](/abs/1811.06965?context=cs)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:1811.06965)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=1811.06965)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:1811.06965)

### [2 blog links](/tb/1811.06965)

([what is this?](https://info.arxiv.org/help/trackback.html))

### [DBLP](https://dblp.uni-trier.de) - CS Bibliography

[listing](https://dblp.uni-trier.de/db/journals/corr/corr1811.html#abs-1811-06965 "listing on DBLP") | [bibtex](https://dblp.uni-trier.de/rec/bibtex/journals/corr/abs-1811-06965 "DBLP bibtex record")

[Yanping Huang](https://dblp.uni-trier.de/search/author?author=Yanping%20Huang "DBLP author search")  
[Yonglong Cheng](https://dblp.uni-trier.de/search/author?author=Yonglong%20Cheng "DBLP author search")  
[Dehao Chen](https://dblp.uni-trier.de/search/author?author=Dehao%20Chen "DBLP author search")  
[HyoukJoong Lee](https://dblp.uni-trier.de/search/author?author=HyoukJoong%20Lee "DBLP author search")  
[Jiquan Ngiam](https://dblp.uni-trier.de/search/author?author=Jiquan%20Ngiam "DBLP author search")

…

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/1811.06965&description=GPipe:%20Efficient%20Training%20of%20Giant%20Neural%20Networks%20using%20Pipeline%20Parallelism "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/1811.06965&title=GPipe:%20Efficient%20Training%20of%20Giant%20Neural%20Networks%20using%20Pipeline%20Parallelism "Bookmark on Reddit")

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

[Which authors of this paper are endorsers?](/auth/show-endorsers/1811.06965) |
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