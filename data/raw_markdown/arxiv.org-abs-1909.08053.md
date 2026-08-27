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

**arXiv:1909.08053** (cs)

[Submitted on 17 Sep 2019 ([v1](https://arxiv.org/abs/1909.08053v1)), last revised 13 Mar 2020 (this version, v4)]

Title:Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism
===========================================================================================

Authors:[Mohammad Shoeybi](https://arxiv.org/search/cs?searchtype=author&query=Shoeybi,+M), [Mostofa Patwary](https://arxiv.org/search/cs?searchtype=author&query=Patwary,+M), [Raul Puri](https://arxiv.org/search/cs?searchtype=author&query=Puri,+R), [Patrick LeGresley](https://arxiv.org/search/cs?searchtype=author&query=LeGresley,+P), [Jared Casper](https://arxiv.org/search/cs?searchtype=author&query=Casper,+J), [Bryan Catanzaro](https://arxiv.org/search/cs?searchtype=author&query=Catanzaro,+B)

View a PDF of the paper titled Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism, by Mohammad Shoeybi and 5 other authors

[View PDF](/pdf/1909.08053)
[HTML (experimental)](https://arxiv.org/html/1909.08053v4)
> Abstract:Recent work in language modeling demonstrates that training large transformer models advances the state of the art in Natural Language Processing applications. However, very large models can be quite difficult to train due to memory constraints. In this work, we present our techniques for training very large transformer models and implement a simple, efficient intra-layer model parallel approach that enables training transformer models with billions of parameters. Our approach does not require a new compiler or library changes, is orthogonal and complimentary to pipeline model parallelism, and can be fully implemented with the insertion of a few communication operations in native PyTorch. We illustrate this approach by converging transformer based models up to 8.3 billion parameters using 512 GPUs. We sustain 15.1 PetaFLOPs across the entire application with 76% scaling efficiency when compared to a strong single GPU baseline that sustains 39 TeraFLOPs, which is 30% of peak FLOPs. To demonstrate that large language models can further advance the state of the art (SOTA), we train an 8.3 billion parameter transformer language model similar to GPT-2 and a 3.9 billion parameter model similar to BERT. We show that careful attention to the placement of layer normalization in BERT-like models is critical to achieving increased performance as the model size grows. Using the GPT-2 model we achieve SOTA results on the WikiText103 (10.8 compared to SOTA perplexity of 15.8) and LAMBADA (66.5% compared to SOTA accuracy of 63.2%) datasets. Our BERT model achieves SOTA results on the RACE dataset (90.9% compared to SOTA accuracy of 89.4%).

|  |  |
| --- | --- |
| Subjects: | Computation and Language (cs.CL) |
| Cite as: | [arXiv:1909.08053](https://arxiv.org/abs/1909.08053) [cs.CL] |
|  | (or  [arXiv:1909.08053v4](https://arxiv.org/abs/1909.08053v4) [cs.CL] for this version) |
|  | <https://doi.org/10.48550/arXiv.1909.08053> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Mohammad Shoeybi [[view email](/show-email/7645889c/1909.08053)]   
**[[v1]](/abs/1909.08053v1)**
Tue, 17 Sep 2019 19:42:54 UTC (3,472 KB)  
**[[v2]](/abs/1909.08053v2)**
Thu, 19 Sep 2019 00:30:15 UTC (3,472 KB)  
**[[v3]](/abs/1909.08053v3)**
Sat, 5 Oct 2019 03:27:58 UTC (3,472 KB)  
**[v4]**
Fri, 13 Mar 2020 23:45:18 UTC (4,006 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism, by Mohammad Shoeybi and 5 other authors

* [View PDF](/pdf/1909.08053)
* [HTML (experimental)](https://arxiv.org/html/1909.08053v4)
* [TeX Source](/src/1909.08053)

[view license](http://arxiv.org/licenses/nonexclusive-distrib/1.0/ "Rights to this article")

### Current browse context:

cs.CL

[< prev](/prevnext?id=1909.08053&function=prev&context=cs.CL "previous in cs.CL (accesskey p)")
  |   
[next >](/prevnext?id=1909.08053&function=next&context=cs.CL "next in cs.CL (accesskey n)")

[new](/list/cs.CL/new)
 | 
[recent](/list/cs.CL/recent)
 | [2019-09](/list/cs.CL/2019-09)

Change to browse by:

[cs](/abs/1909.08053?context=cs)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:1909.08053)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=1909.08053)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:1909.08053)

### [DBLP](https://dblp.uni-trier.de) - CS Bibliography

[listing](https://dblp.uni-trier.de/db/journals/corr/corr1909.html#abs-1909-08053 "listing on DBLP") | [bibtex](https://dblp.uni-trier.de/rec/bibtex/journals/corr/abs-1909-08053 "DBLP bibtex record")

[Mohammad Shoeybi](https://dblp.uni-trier.de/search/author?author=Mohammad%20Shoeybi "DBLP author search")  
[Raul Puri](https://dblp.uni-trier.de/search/author?author=Raul%20Puri "DBLP author search")  
[Patrick LeGresley](https://dblp.uni-trier.de/search/author?author=Patrick%20LeGresley "DBLP author search")  
[Jared Casper](https://dblp.uni-trier.de/search/author?author=Jared%20Casper "DBLP author search")  
[Bryan Catanzaro](https://dblp.uni-trier.de/search/author?author=Bryan%20Catanzaro "DBLP author search")

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/1909.08053&description=Megatron-LM:%20Training%20Multi-Billion%20Parameter%20Language%20Models%20Using%20Model%20Parallelism "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/1909.08053&title=Megatron-LM:%20Training%20Multi-Billion%20Parameter%20Language%20Models%20Using%20Model%20Parallelism "Bookmark on Reddit")

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

[Which authors of this paper are endorsers?](/auth/show-endorsers/1909.08053) |
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