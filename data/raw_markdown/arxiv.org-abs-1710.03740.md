[Skip to main content](#content)

[![archive](/static/base/1.0.1/images/arxiv-logo-primary-light.svg)](https://arxiv.org/)


[Search](https://arxiv.org/search)
[Submit](https://arxiv.org/user/create)
[Donate](https://info.arxiv.org/about/donate.html)
[Log in](https://arxiv.org/login)

Search arXiv

Press Enter to search · [Advanced search](https://arxiv.org/search/advanced)

Computer Science > Artificial Intelligence
==========================================

**arXiv:1710.03740** (cs)

[Submitted on 10 Oct 2017 ([v1](https://arxiv.org/abs/1710.03740v1)), last revised 15 Feb 2018 (this version, v3)]

Title:Mixed Precision Training
==============================

Authors:[Paulius Micikevicius](https://arxiv.org/search/cs?searchtype=author&query=Micikevicius,+P), [Sharan Narang](https://arxiv.org/search/cs?searchtype=author&query=Narang,+S), [Jonah Alben](https://arxiv.org/search/cs?searchtype=author&query=Alben,+J), [Gregory Diamos](https://arxiv.org/search/cs?searchtype=author&query=Diamos,+G), [Erich Elsen](https://arxiv.org/search/cs?searchtype=author&query=Elsen,+E), [David Garcia](https://arxiv.org/search/cs?searchtype=author&query=Garcia,+D), [Boris Ginsburg](https://arxiv.org/search/cs?searchtype=author&query=Ginsburg,+B), [Michael Houston](https://arxiv.org/search/cs?searchtype=author&query=Houston,+M), [Oleksii Kuchaiev](https://arxiv.org/search/cs?searchtype=author&query=Kuchaiev,+O), [Ganesh Venkatesh](https://arxiv.org/search/cs?searchtype=author&query=Venkatesh,+G), [Hao Wu](https://arxiv.org/search/cs?searchtype=author&query=Wu,+H)

View a PDF of the paper titled Mixed Precision Training, by Paulius Micikevicius and 10 other authors

[View PDF](/pdf/1710.03740)
[HTML (experimental)](https://arxiv.org/html/1710.03740v3)
> Abstract:Deep neural networks have enabled progress in a wide variety of applications. Growing the size of the neural network typically results in improved accuracy. As model sizes grow, the memory and compute requirements for training these models also increases. We introduce a technique to train deep neural networks using half precision floating point numbers. In our technique, weights, activations and gradients are stored in IEEE half-precision format. Half-precision floating numbers have limited numerical range compared to single-precision numbers. We propose two techniques to handle this loss of information. Firstly, we recommend maintaining a single-precision copy of the weights that accumulates the gradients after each optimizer step. This single-precision copy is rounded to half-precision format during training. Secondly, we propose scaling the loss appropriately to handle the loss of information with half-precision gradients. We demonstrate that this approach works for a wide variety of models including convolution neural networks, recurrent neural networks and generative adversarial networks. This technique works for large scale models with more than 100 million parameters trained on large datasets. Using this approach, we can reduce the memory consumption of deep learning models by nearly 2x. In future processors, we can also expect a significant computation speedup using half-precision hardware units.

|  |  |
| --- | --- |
| Comments: | Published as a conference paper at ICLR 2018 |
| Subjects: | Artificial Intelligence (cs.AI); Machine Learning (cs.LG); Machine Learning (stat.ML) |
| Cite as: | [arXiv:1710.03740](https://arxiv.org/abs/1710.03740) [cs.AI] |
|  | (or  [arXiv:1710.03740v3](https://arxiv.org/abs/1710.03740v3) [cs.AI] for this version) |
|  | <https://doi.org/10.48550/arXiv.1710.03740> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Sharan Narang [[view email](/show-email/8b47b8fa/1710.03740)]   
**[[v1]](/abs/1710.03740v1)**
Tue, 10 Oct 2017 17:42:04 UTC (1,234 KB)  
**[[v2]](/abs/1710.03740v2)**
Thu, 12 Oct 2017 19:09:05 UTC (1,234 KB)  
**[v3]**
Thu, 15 Feb 2018 20:04:02 UTC (1,233 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled Mixed Precision Training, by Paulius Micikevicius and 10 other authors

* [View PDF](/pdf/1710.03740)
* [HTML (experimental)](https://arxiv.org/html/1710.03740v3)
* [TeX Source](/src/1710.03740)

[view license](http://arxiv.org/licenses/nonexclusive-distrib/1.0/ "Rights to this article")

### Current browse context:

cs.AI

[< prev](/prevnext?id=1710.03740&function=prev&context=cs.AI "previous in cs.AI (accesskey p)")
  |   
[next >](/prevnext?id=1710.03740&function=next&context=cs.AI "next in cs.AI (accesskey n)")

[new](/list/cs.AI/new)
 | 
[recent](/list/cs.AI/recent)
 | [2017-10](/list/cs.AI/2017-10)

Change to browse by:

[cs](/abs/1710.03740?context=cs)  
[cs.LG](/abs/1710.03740?context=cs.LG)  
[stat](/abs/1710.03740?context=stat)  
[stat.ML](/abs/1710.03740?context=stat.ML)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:1710.03740)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=1710.03740)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:1710.03740)

### [2 blog links](/tb/1710.03740)

([what is this?](https://info.arxiv.org/help/trackback.html))

### [DBLP](https://dblp.uni-trier.de) - CS Bibliography

[listing](https://dblp.uni-trier.de/db/journals/corr/corr1710.html#abs-1710-03740 "listing on DBLP") | [bibtex](https://dblp.uni-trier.de/rec/bibtex/journals/corr/abs-1710-03740 "DBLP bibtex record")

[Paulius Micikevicius](https://dblp.uni-trier.de/search/author?author=Paulius%20Micikevicius "DBLP author search")  
[Sharan Narang](https://dblp.uni-trier.de/search/author?author=Sharan%20Narang "DBLP author search")  
[Jonah Alben](https://dblp.uni-trier.de/search/author?author=Jonah%20Alben "DBLP author search")  
[Gregory F. Diamos](https://dblp.uni-trier.de/search/author?author=Gregory%20F.%20Diamos "DBLP author search")  
[Erich Elsen](https://dblp.uni-trier.de/search/author?author=Erich%20Elsen "DBLP author search")

…

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/1710.03740&description=Mixed%20Precision%20Training "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/1710.03740&title=Mixed%20Precision%20Training "Bookmark on Reddit")

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

[Which authors of this paper are endorsers?](/auth/show-endorsers/1710.03740) |
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