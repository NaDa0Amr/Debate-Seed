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

**arXiv:2401.04088** (cs)

[Submitted on 8 Jan 2024]

Title:Mixtral of Experts
========================

Authors:[Albert Q. Jiang](https://arxiv.org/search/cs?searchtype=author&query=Jiang,+A+Q), [Alexandre Sablayrolles](https://arxiv.org/search/cs?searchtype=author&query=Sablayrolles,+A), [Antoine Roux](https://arxiv.org/search/cs?searchtype=author&query=Roux,+A), [Arthur Mensch](https://arxiv.org/search/cs?searchtype=author&query=Mensch,+A), [Blanche Savary](https://arxiv.org/search/cs?searchtype=author&query=Savary,+B), [Chris Bamford](https://arxiv.org/search/cs?searchtype=author&query=Bamford,+C), [Devendra Singh Chaplot](https://arxiv.org/search/cs?searchtype=author&query=Chaplot,+D+S), [Diego de las Casas](https://arxiv.org/search/cs?searchtype=author&query=de+las+Casas,+D), [Emma Bou Hanna](https://arxiv.org/search/cs?searchtype=author&query=Hanna,+E+B), [Florian Bressand](https://arxiv.org/search/cs?searchtype=author&query=Bressand,+F), [Gianna Lengyel](https://arxiv.org/search/cs?searchtype=author&query=Lengyel,+G), [Guillaume Bour](https://arxiv.org/search/cs?searchtype=author&query=Bour,+G), [Guillaume Lample](https://arxiv.org/search/cs?searchtype=author&query=Lample,+G), [Lélio Renard Lavaud](https://arxiv.org/search/cs?searchtype=author&query=Lavaud,+L+R), [Lucile Saulnier](https://arxiv.org/search/cs?searchtype=author&query=Saulnier,+L), [Marie-Anne Lachaux](https://arxiv.org/search/cs?searchtype=author&query=Lachaux,+M), [Pierre Stock](https://arxiv.org/search/cs?searchtype=author&query=Stock,+P), [Sandeep Subramanian](https://arxiv.org/search/cs?searchtype=author&query=Subramanian,+S), [Sophia Yang](https://arxiv.org/search/cs?searchtype=author&query=Yang,+S), [Szymon Antoniak](https://arxiv.org/search/cs?searchtype=author&query=Antoniak,+S), [Teven Le Scao](https://arxiv.org/search/cs?searchtype=author&query=Scao,+T+L), [Théophile Gervet](https://arxiv.org/search/cs?searchtype=author&query=Gervet,+T), [Thibaut Lavril](https://arxiv.org/search/cs?searchtype=author&query=Lavril,+T), [Thomas Wang](https://arxiv.org/search/cs?searchtype=author&query=Wang,+T), [Timothée Lacroix](https://arxiv.org/search/cs?searchtype=author&query=Lacroix,+T), [William El Sayed](https://arxiv.org/search/cs?searchtype=author&query=Sayed,+W+E)

View a PDF of the paper titled Mixtral of Experts, by Albert Q. Jiang and 25 other authors

[View PDF](/pdf/2401.04088)
[HTML (experimental)](https://arxiv.org/html/2401.04088v1)
> Abstract:We introduce Mixtral 8x7B, a Sparse Mixture of Experts (SMoE) language model. Mixtral has the same architecture as Mistral 7B, with the difference that each layer is composed of 8 feedforward blocks (i.e. experts). For every token, at each layer, a router network selects two experts to process the current state and combine their outputs. Even though each token only sees two experts, the selected experts can be different at each timestep. As a result, each token has access to 47B parameters, but only uses 13B active parameters during inference. Mixtral was trained with a context size of 32k tokens and it outperforms or matches Llama 2 70B and GPT-3.5 across all evaluated benchmarks. In particular, Mixtral vastly outperforms Llama 2 70B on mathematics, code generation, and multilingual benchmarks. We also provide a model fine-tuned to follow instructions, Mixtral 8x7B - Instruct, that surpasses GPT-3.5 Turbo, Claude-2.1, Gemini Pro, and Llama 2 70B - chat model on human benchmarks. Both the base and instruct models are released under the Apache 2.0 license.

|  |  |
| --- | --- |
| Comments: | See more details at [this https URL](https://mistral.ai/news/mixtral-of-experts/) |
| Subjects: | Machine Learning (cs.LG); Computation and Language (cs.CL) |
| Cite as: | [arXiv:2401.04088](https://arxiv.org/abs/2401.04088) [cs.LG] |
|  | (or  [arXiv:2401.04088v1](https://arxiv.org/abs/2401.04088v1) [cs.LG] for this version) |
|  | <https://doi.org/10.48550/arXiv.2401.04088> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Devendra Singh Chaplot [[view email](/show-email/d382fa4f/2401.04088)]   
**[v1]**
Mon, 8 Jan 2024 18:47:34 UTC (2,811 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled Mixtral of Experts, by Albert Q. Jiang and 25 other authors

* [View PDF](/pdf/2401.04088)
* [HTML (experimental)](https://arxiv.org/html/2401.04088v1)
* [TeX Source](/src/2401.04088)

[![license icon](https://arxiv.org/icons/licenses/by-4.0.png)view license](http://creativecommons.org/licenses/by/4.0/ "Rights to this article")

### Current browse context:

cs.LG

[< prev](/prevnext?id=2401.04088&function=prev&context=cs.LG "previous in cs.LG (accesskey p)")
  |   
[next >](/prevnext?id=2401.04088&function=next&context=cs.LG "next in cs.LG (accesskey n)")

[new](/list/cs.LG/new)
 | 
[recent](/list/cs.LG/recent)
 | [2024-01](/list/cs.LG/2024-01)

Change to browse by:

[cs](/abs/2401.04088?context=cs)  
[cs.CL](/abs/2401.04088?context=cs.CL)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:2401.04088)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=2401.04088)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:2401.04088)

### [1 blog link](/tb/2401.04088)

([what is this?](https://info.arxiv.org/help/trackback.html))

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/2401.04088&description=Mixtral%20of%20Experts "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/2401.04088&title=Mixtral%20of%20Experts "Bookmark on Reddit")

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

[Which authors of this paper are endorsers?](/auth/show-endorsers/2401.04088) |
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