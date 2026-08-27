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

**arXiv:2202.09368** (cs)

[Submitted on 18 Feb 2022 ([v1](https://arxiv.org/abs/2202.09368v1)), last revised 14 Oct 2022 (this version, v2)]

Title:Mixture-of-Experts with Expert Choice Routing
===================================================

Authors:[Yanqi Zhou](https://arxiv.org/search/cs?searchtype=author&query=Zhou,+Y), [Tao Lei](https://arxiv.org/search/cs?searchtype=author&query=Lei,+T), [Hanxiao Liu](https://arxiv.org/search/cs?searchtype=author&query=Liu,+H), [Nan Du](https://arxiv.org/search/cs?searchtype=author&query=Du,+N), [Yanping Huang](https://arxiv.org/search/cs?searchtype=author&query=Huang,+Y), [Vincent Zhao](https://arxiv.org/search/cs?searchtype=author&query=Zhao,+V), [Andrew Dai](https://arxiv.org/search/cs?searchtype=author&query=Dai,+A), [Zhifeng Chen](https://arxiv.org/search/cs?searchtype=author&query=Chen,+Z), [Quoc Le](https://arxiv.org/search/cs?searchtype=author&query=Le,+Q), [James Laudon](https://arxiv.org/search/cs?searchtype=author&query=Laudon,+J)

View a PDF of the paper titled Mixture-of-Experts with Expert Choice Routing, by Yanqi Zhou and Tao Lei and Hanxiao Liu and Nan Du and Yanping Huang and Vincent Zhao and Andrew Dai and Zhifeng Chen and Quoc Le and James Laudon

[View PDF](/pdf/2202.09368)
[HTML (experimental)](https://arxiv.org/html/2202.09368v2)
> Abstract:Sparsely-activated Mixture-of-experts (MoE) models allow the number of parameters to greatly increase while keeping the amount of computation for a given token or a given sample unchanged. However, a poor expert routing strategy (e.g. one resulting in load imbalance) can cause certain experts to be under-trained, leading to an expert being under or over-specialized. Prior work allocates a fixed number of experts to each token using a top-k function regardless of the relative importance of different tokens. To address this, we propose a heterogeneous mixture-of-experts employing an expert choice method. Instead of letting tokens select the top-k experts, we have experts selecting the top-k tokens. As a result, each token can be routed to a variable number of experts and each expert can have a fixed bucket size. We systematically study pre-training speedups using the same computational resources of the Switch Transformer top-1 and GShard top-2 gating of prior work and find that our method improves training convergence time by more than 2x. For the same computational cost, our method demonstrates higher performance in fine-tuning 11 selected tasks in the GLUE and SuperGLUE benchmarks. For a smaller activation cost, our method outperforms the T5 dense model in 7 out of the 11 tasks.

|  |  |
| --- | --- |
| Subjects: | Machine Learning (cs.LG); Artificial Intelligence (cs.AI) |
| Cite as: | [arXiv:2202.09368](https://arxiv.org/abs/2202.09368) [cs.LG] |
|  | (or  [arXiv:2202.09368v2](https://arxiv.org/abs/2202.09368v2) [cs.LG] for this version) |
|  | <https://doi.org/10.48550/arXiv.2202.09368> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Yanqi Zhou [[view email](/show-email/a0468851/2202.09368)]   
**[[v1]](/abs/2202.09368v1)**
Fri, 18 Feb 2022 17:46:11 UTC (350 KB)  
**[v2]**
Fri, 14 Oct 2022 00:08:24 UTC (526 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled Mixture-of-Experts with Expert Choice Routing, by Yanqi Zhou and Tao Lei and Hanxiao Liu and Nan Du and Yanping Huang and Vincent Zhao and Andrew Dai and Zhifeng Chen and Quoc Le and James Laudon

* [View PDF](/pdf/2202.09368)
* [HTML (experimental)](https://arxiv.org/html/2202.09368v2)
* [TeX Source](/src/2202.09368)

[![license icon](https://arxiv.org/icons/licenses/by-nc-sa-4.0.png)view license](http://creativecommons.org/licenses/by-nc-sa/4.0/ "Rights to this article")

### Current browse context:

cs.LG

[< prev](/prevnext?id=2202.09368&function=prev&context=cs.LG "previous in cs.LG (accesskey p)")
  |   
[next >](/prevnext?id=2202.09368&function=next&context=cs.LG "next in cs.LG (accesskey n)")

[new](/list/cs.LG/new)
 | 
[recent](/list/cs.LG/recent)
 | [2022-02](/list/cs.LG/2022-02)

Change to browse by:

[cs](/abs/2202.09368?context=cs)  
[cs.AI](/abs/2202.09368?context=cs.AI)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:2202.09368)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=2202.09368)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:2202.09368)

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/2202.09368&description=Mixture-of-Experts%20with%20Expert%20Choice%20Routing "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/2202.09368&title=Mixture-of-Experts%20with%20Expert%20Choice%20Routing "Bookmark on Reddit")

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

[Which authors of this paper are endorsers?](/auth/show-endorsers/2202.09368) |
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