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

**arXiv:2205.14135** (cs)

[Submitted on 27 May 2022 ([v1](https://arxiv.org/abs/2205.14135v1)), last revised 23 Jun 2022 (this version, v2)]

Title:FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness
=================================================================================

Authors:[Tri Dao](https://arxiv.org/search/cs?searchtype=author&query=Dao,+T), [Daniel Y. Fu](https://arxiv.org/search/cs?searchtype=author&query=Fu,+D+Y), [Stefano Ermon](https://arxiv.org/search/cs?searchtype=author&query=Ermon,+S), [Atri Rudra](https://arxiv.org/search/cs?searchtype=author&query=Rudra,+A), [Christopher Ré](https://arxiv.org/search/cs?searchtype=author&query=R%C3%A9,+C)

View a PDF of the paper titled FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness, by Tri Dao and 4 other authors

[View PDF](/pdf/2205.14135)
[HTML (experimental)](https://arxiv.org/html/2205.14135v2)
> Abstract:Transformers are slow and memory-hungry on long sequences, since the time and memory complexity of self-attention are quadratic in sequence length. Approximate attention methods have attempted to address this problem by trading off model quality to reduce the compute complexity, but often do not achieve wall-clock speedup. We argue that a missing principle is making attention algorithms IO-aware -- accounting for reads and writes between levels of GPU memory. We propose FlashAttention, an IO-aware exact attention algorithm that uses tiling to reduce the number of memory reads/writes between GPU high bandwidth memory (HBM) and GPU on-chip SRAM. We analyze the IO complexity of FlashAttention, showing that it requires fewer HBM accesses than standard attention, and is optimal for a range of SRAM sizes. We also extend FlashAttention to block-sparse attention, yielding an approximate attention algorithm that is faster than any existing approximate attention method. FlashAttention trains Transformers faster than existing baselines: 15% end-to-end wall-clock speedup on BERT-large (seq. length 512) compared to the MLPerf 1.1 training speed record, 3$\times$ speedup on GPT-2 (seq. length 1K), and 2.4$\times$ speedup on long-range arena (seq. length 1K-4K). FlashAttention and block-sparse FlashAttention enable longer context in Transformers, yielding higher quality models (0.7 better perplexity on GPT-2 and 6.4 points of lift on long-document classification) and entirely new capabilities: the first Transformers to achieve better-than-chance performance on the Path-X challenge (seq. length 16K, 61.4% accuracy) and Path-256 (seq. length 64K, 63.1% accuracy).

|  |  |
| --- | --- |
| Subjects: | Machine Learning (cs.LG) |
| Cite as: | [arXiv:2205.14135](https://arxiv.org/abs/2205.14135) [cs.LG] |
|  | (or  [arXiv:2205.14135v2](https://arxiv.org/abs/2205.14135v2) [cs.LG] for this version) |
|  | <https://doi.org/10.48550/arXiv.2205.14135> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Tri Dao [[view email](/show-email/00d4bef1/2205.14135)]   
**[[v1]](/abs/2205.14135v1)**
Fri, 27 May 2022 17:53:09 UTC (1,325 KB)  
**[v2]**
Thu, 23 Jun 2022 17:53:32 UTC (1,653 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness, by Tri Dao and 4 other authors

* [View PDF](/pdf/2205.14135)
* [HTML (experimental)](https://arxiv.org/html/2205.14135v2)
* [TeX Source](/src/2205.14135)

[view license](http://arxiv.org/licenses/nonexclusive-distrib/1.0/ "Rights to this article")

### Current browse context:

cs.LG

[< prev](/prevnext?id=2205.14135&function=prev&context=cs.LG "previous in cs.LG (accesskey p)")
  |   
[next >](/prevnext?id=2205.14135&function=next&context=cs.LG "next in cs.LG (accesskey n)")

[new](/list/cs.LG/new)
 | 
[recent](/list/cs.LG/recent)
 | [2022-05](/list/cs.LG/2022-05)

Change to browse by:

[cs](/abs/2205.14135?context=cs)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:2205.14135)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=2205.14135)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:2205.14135)

### [1 blog link](/tb/2205.14135)

([what is this?](https://info.arxiv.org/help/trackback.html))

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/2205.14135&description=FlashAttention:%20Fast%20and%20Memory-Efficient%20Exact%20Attention%20with%20IO-Awareness "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/2205.14135&title=FlashAttention:%20Fast%20and%20Memory-Efficient%20Exact%20Attention%20with%20IO-Awareness "Bookmark on Reddit")

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

[Which authors of this paper are endorsers?](/auth/show-endorsers/2205.14135) |
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