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

**arXiv:2005.11401** (cs)

[Submitted on 22 May 2020 ([v1](https://arxiv.org/abs/2005.11401v1)), last revised 12 Apr 2021 (this version, v4)]

Title:Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
======================================================================

Authors:[Patrick Lewis](https://arxiv.org/search/cs?searchtype=author&query=Lewis,+P), [Ethan Perez](https://arxiv.org/search/cs?searchtype=author&query=Perez,+E), [Aleksandra Piktus](https://arxiv.org/search/cs?searchtype=author&query=Piktus,+A), [Fabio Petroni](https://arxiv.org/search/cs?searchtype=author&query=Petroni,+F), [Vladimir Karpukhin](https://arxiv.org/search/cs?searchtype=author&query=Karpukhin,+V), [Naman Goyal](https://arxiv.org/search/cs?searchtype=author&query=Goyal,+N), [Heinrich Küttler](https://arxiv.org/search/cs?searchtype=author&query=K%C3%BCttler,+H), [Mike Lewis](https://arxiv.org/search/cs?searchtype=author&query=Lewis,+M), [Wen-tau Yih](https://arxiv.org/search/cs?searchtype=author&query=Yih,+W), [Tim Rocktäschel](https://arxiv.org/search/cs?searchtype=author&query=Rockt%C3%A4schel,+T), [Sebastian Riedel](https://arxiv.org/search/cs?searchtype=author&query=Riedel,+S), [Douwe Kiela](https://arxiv.org/search/cs?searchtype=author&query=Kiela,+D)

View a PDF of the paper titled Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, by Patrick Lewis and 11 other authors

[View PDF](/pdf/2005.11401)
[HTML (experimental)](https://arxiv.org/html/2005.11401v4)
> Abstract:Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory can overcome this issue, but have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, the other can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state-of-the-art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

|  |  |
| --- | --- |
| Comments: | Accepted at NeurIPS 2020 |
| Subjects: | Computation and Language (cs.CL); Machine Learning (cs.LG) |
| Cite as: | [arXiv:2005.11401](https://arxiv.org/abs/2005.11401) [cs.CL] |
|  | (or  [arXiv:2005.11401v4](https://arxiv.org/abs/2005.11401v4) [cs.CL] for this version) |
|  | <https://doi.org/10.48550/arXiv.2005.11401> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Patrick Lewis [[view email](/show-email/76d69ce8/2005.11401)]   
**[[v1]](/abs/2005.11401v1)**
Fri, 22 May 2020 21:34:34 UTC (698 KB)  
**[[v2]](/abs/2005.11401v2)**
Mon, 7 Dec 2020 16:23:06 UTC (767 KB)  
**[[v3]](/abs/2005.11401v3)**
Mon, 29 Mar 2021 10:12:16 UTC (767 KB)  
**[v4]**
Mon, 12 Apr 2021 15:42:18 UTC (767 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, by Patrick Lewis and 11 other authors

* [View PDF](/pdf/2005.11401)
* [HTML (experimental)](https://arxiv.org/html/2005.11401v4)
* [TeX Source](/src/2005.11401)

[view license](http://arxiv.org/licenses/nonexclusive-distrib/1.0/ "Rights to this article")

### Current browse context:

cs.CL

[< prev](/prevnext?id=2005.11401&function=prev&context=cs.CL "previous in cs.CL (accesskey p)")
  |   
[next >](/prevnext?id=2005.11401&function=next&context=cs.CL "next in cs.CL (accesskey n)")

[new](/list/cs.CL/new)
 | 
[recent](/list/cs.CL/recent)
 | [2020-05](/list/cs.CL/2020-05)

Change to browse by:

[cs](/abs/2005.11401?context=cs)  
[cs.LG](/abs/2005.11401?context=cs.LG)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:2005.11401)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=2005.11401)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:2005.11401)

### [13 blog links](/tb/2005.11401)

([what is this?](https://info.arxiv.org/help/trackback.html))

### [DBLP](https://dblp.uni-trier.de) - CS Bibliography

[listing](https://dblp.uni-trier.de/db/journals/corr/corr2005.html#abs-2005-11401 "listing on DBLP") | [bibtex](https://dblp.uni-trier.de/rec/bibtex/journals/corr/abs-2005-11401 "DBLP bibtex record")

[Ethan Perez](https://dblp.uni-trier.de/search/author?author=Ethan%20Perez "DBLP author search")  
[Aleksandra Piktus](https://dblp.uni-trier.de/search/author?author=Aleksandra%20Piktus "DBLP author search")  
[Fabio Petroni](https://dblp.uni-trier.de/search/author?author=Fabio%20Petroni "DBLP author search")  
[Vladimir Karpukhin](https://dblp.uni-trier.de/search/author?author=Vladimir%20Karpukhin "DBLP author search")  
[Naman Goyal](https://dblp.uni-trier.de/search/author?author=Naman%20Goyal "DBLP author search")

…

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/2005.11401&description=Retrieval-Augmented%20Generation%20for%20Knowledge-Intensive%20NLP%20Tasks "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/2005.11401&title=Retrieval-Augmented%20Generation%20for%20Knowledge-Intensive%20NLP%20Tasks "Bookmark on Reddit")

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

[Which authors of this paper are endorsers?](/auth/show-endorsers/2005.11401) |
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