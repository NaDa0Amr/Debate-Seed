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

**arXiv:2406.07887** (cs)

[Submitted on 12 Jun 2024]

Title:An Empirical Study of Mamba-based Language Models
=======================================================

Authors:[Roger Waleffe](https://arxiv.org/search/cs?searchtype=author&query=Waleffe,+R), [Wonmin Byeon](https://arxiv.org/search/cs?searchtype=author&query=Byeon,+W), [Duncan Riach](https://arxiv.org/search/cs?searchtype=author&query=Riach,+D), [Brandon Norick](https://arxiv.org/search/cs?searchtype=author&query=Norick,+B), [Vijay Korthikanti](https://arxiv.org/search/cs?searchtype=author&query=Korthikanti,+V), [Tri Dao](https://arxiv.org/search/cs?searchtype=author&query=Dao,+T), [Albert Gu](https://arxiv.org/search/cs?searchtype=author&query=Gu,+A), [Ali Hatamizadeh](https://arxiv.org/search/cs?searchtype=author&query=Hatamizadeh,+A), [Sudhakar Singh](https://arxiv.org/search/cs?searchtype=author&query=Singh,+S), [Deepak Narayanan](https://arxiv.org/search/cs?searchtype=author&query=Narayanan,+D), [Garvit Kulshreshtha](https://arxiv.org/search/cs?searchtype=author&query=Kulshreshtha,+G), [Vartika Singh](https://arxiv.org/search/cs?searchtype=author&query=Singh,+V), [Jared Casper](https://arxiv.org/search/cs?searchtype=author&query=Casper,+J), [Jan Kautz](https://arxiv.org/search/cs?searchtype=author&query=Kautz,+J), [Mohammad Shoeybi](https://arxiv.org/search/cs?searchtype=author&query=Shoeybi,+M), [Bryan Catanzaro](https://arxiv.org/search/cs?searchtype=author&query=Catanzaro,+B)

View a PDF of the paper titled An Empirical Study of Mamba-based Language Models, by Roger Waleffe and 15 other authors

[View PDF](/pdf/2406.07887)
[HTML (experimental)](https://arxiv.org/html/2406.07887v1)
> Abstract:Selective state-space models (SSMs) like Mamba overcome some of the shortcomings of Transformers, such as quadratic computational complexity with sequence length and large inference-time memory requirements from the key-value cache. Moreover, recent studies have shown that SSMs can match or exceed the language modeling capabilities of Transformers, making them an attractive alternative. In a controlled setting (e.g., same data), however, studies so far have only presented small scale experiments comparing SSMs to Transformers. To understand the strengths and weaknesses of these architectures at larger scales, we present a direct comparison between 8B-parameter Mamba, Mamba-2, and Transformer models trained on the same datasets of up to 3.5T tokens. We also compare these models to a hybrid architecture consisting of 43% Mamba-2, 7% attention, and 50% MLP layers (Mamba-2-Hybrid). Using a diverse set of tasks, we answer the question of whether Mamba models can match Transformers at larger training budgets. Our results show that while pure SSMs match or exceed Transformers on many tasks, they lag behind Transformers on tasks which require strong copying or in-context learning abilities (e.g., 5-shot MMLU, Phonebook) or long-context reasoning. In contrast, we find that the 8B Mamba-2-Hybrid exceeds the 8B Transformer on all 12 standard tasks we evaluated (+2.65 points on average) and is predicted to be up to 8x faster when generating tokens at inference time. To validate long-context capabilities, we provide additional experiments evaluating variants of the Mamba-2-Hybrid and Transformer extended to support 16K, 32K, and 128K sequences. On an additional 23 long-context tasks, the hybrid model continues to closely match or exceed the Transformer on average. To enable further study, we release the checkpoints as well as the code used to train our models as part of NVIDIA's Megatron-LM project.

|  |  |
| --- | --- |
| Subjects: | Machine Learning (cs.LG); Computation and Language (cs.CL) |
| Cite as: | [arXiv:2406.07887](https://arxiv.org/abs/2406.07887) [cs.LG] |
|  | (or  [arXiv:2406.07887v1](https://arxiv.org/abs/2406.07887v1) [cs.LG] for this version) |
|  | <https://doi.org/10.48550/arXiv.2406.07887> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Roger Waleffe [[view email](/show-email/1b43485e/2406.07887)]   
**[v1]**
Wed, 12 Jun 2024 05:25:15 UTC (223 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled An Empirical Study of Mamba-based Language Models, by Roger Waleffe and 15 other authors

* [View PDF](/pdf/2406.07887)
* [HTML (experimental)](https://arxiv.org/html/2406.07887v1)
* [TeX Source](/src/2406.07887)

[view license](http://arxiv.org/licenses/nonexclusive-distrib/1.0/ "Rights to this article")

### Current browse context:

cs.LG

[< prev](/prevnext?id=2406.07887&function=prev&context=cs.LG "previous in cs.LG (accesskey p)")
  |   
[next >](/prevnext?id=2406.07887&function=next&context=cs.LG "next in cs.LG (accesskey n)")

[new](/list/cs.LG/new)
 | 
[recent](/list/cs.LG/recent)
 | [2024-06](/list/cs.LG/2024-06)

Change to browse by:

[cs](/abs/2406.07887?context=cs)  
[cs.CL](/abs/2406.07887?context=cs.CL)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:2406.07887)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=2406.07887)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:2406.07887)

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/2406.07887&description=An%20Empirical%20Study%20of%20Mamba-based%20Language%20Models "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/2406.07887&title=An%20Empirical%20Study%20of%20Mamba-based%20Language%20Models "Bookmark on Reddit")

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

[Which authors of this paper are endorsers?](/auth/show-endorsers/2406.07887) |
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