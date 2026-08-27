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

**arXiv:1609.08144** (cs)

[Submitted on 26 Sep 2016 ([v1](https://arxiv.org/abs/1609.08144v1)), last revised 8 Oct 2016 (this version, v2)]

Title:Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation
========================================================================================================

Authors:[Yonghui Wu](https://arxiv.org/search/cs?searchtype=author&query=Wu,+Y), [Mike Schuster](https://arxiv.org/search/cs?searchtype=author&query=Schuster,+M), [Zhifeng Chen](https://arxiv.org/search/cs?searchtype=author&query=Chen,+Z), [Quoc V. Le](https://arxiv.org/search/cs?searchtype=author&query=Le,+Q+V), [Mohammad Norouzi](https://arxiv.org/search/cs?searchtype=author&query=Norouzi,+M), [Wolfgang Macherey](https://arxiv.org/search/cs?searchtype=author&query=Macherey,+W), [Maxim Krikun](https://arxiv.org/search/cs?searchtype=author&query=Krikun,+M), [Yuan Cao](https://arxiv.org/search/cs?searchtype=author&query=Cao,+Y), [Qin Gao](https://arxiv.org/search/cs?searchtype=author&query=Gao,+Q), [Klaus Macherey](https://arxiv.org/search/cs?searchtype=author&query=Macherey,+K), [Jeff Klingner](https://arxiv.org/search/cs?searchtype=author&query=Klingner,+J), [Apurva Shah](https://arxiv.org/search/cs?searchtype=author&query=Shah,+A), [Melvin Johnson](https://arxiv.org/search/cs?searchtype=author&query=Johnson,+M), [Xiaobing Liu](https://arxiv.org/search/cs?searchtype=author&query=Liu,+X), [Łukasz Kaiser](https://arxiv.org/search/cs?searchtype=author&query=Kaiser,+%C5%81), [Stephan Gouws](https://arxiv.org/search/cs?searchtype=author&query=Gouws,+S), [Yoshikiyo Kato](https://arxiv.org/search/cs?searchtype=author&query=Kato,+Y), [Taku Kudo](https://arxiv.org/search/cs?searchtype=author&query=Kudo,+T), [Hideto Kazawa](https://arxiv.org/search/cs?searchtype=author&query=Kazawa,+H), [Keith Stevens](https://arxiv.org/search/cs?searchtype=author&query=Stevens,+K), [George Kurian](https://arxiv.org/search/cs?searchtype=author&query=Kurian,+G), [Nishant Patil](https://arxiv.org/search/cs?searchtype=author&query=Patil,+N), [Wei Wang](https://arxiv.org/search/cs?searchtype=author&query=Wang,+W), [Cliff Young](https://arxiv.org/search/cs?searchtype=author&query=Young,+C), [Jason Smith](https://arxiv.org/search/cs?searchtype=author&query=Smith,+J), [Jason Riesa](https://arxiv.org/search/cs?searchtype=author&query=Riesa,+J), [Alex Rudnick](https://arxiv.org/search/cs?searchtype=author&query=Rudnick,+A), [Oriol Vinyals](https://arxiv.org/search/cs?searchtype=author&query=Vinyals,+O), [Greg Corrado](https://arxiv.org/search/cs?searchtype=author&query=Corrado,+G), [Macduff Hughes](https://arxiv.org/search/cs?searchtype=author&query=Hughes,+M), [Jeffrey Dean](https://arxiv.org/search/cs?searchtype=author&query=Dean,+J)

View a PDF of the paper titled Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation, by Yonghui Wu and 30 other authors

[View PDF](/pdf/1609.08144)
[HTML (experimental)](https://arxiv.org/html/1609.08144v2)
> Abstract:Neural Machine Translation (NMT) is an end-to-end learning approach for automated translation, with the potential to overcome many of the weaknesses of conventional phrase-based translation systems. Unfortunately, NMT systems are known to be computationally expensive both in training and in translation inference. Also, most NMT systems have difficulty with rare words. These issues have hindered NMT's use in practical deployments and services, where both accuracy and speed are essential. In this work, we present GNMT, Google's Neural Machine Translation system, which attempts to address many of these issues. Our model consists of a deep LSTM network with 8 encoder and 8 decoder layers using attention and residual connections. To improve parallelism and therefore decrease training time, our attention mechanism connects the bottom layer of the decoder to the top layer of the encoder. To accelerate the final translation speed, we employ low-precision arithmetic during inference computations. To improve handling of rare words, we divide words into a limited set of common sub-word units ("wordpieces") for both input and output. This method provides a good balance between the flexibility of "character"-delimited models and the efficiency of "word"-delimited models, naturally handles translation of rare words, and ultimately improves the overall accuracy of the system. Our beam search technique employs a length-normalization procedure and uses a coverage penalty, which encourages generation of an output sentence that is most likely to cover all the words in the source sentence. On the WMT'14 English-to-French and English-to-German benchmarks, GNMT achieves competitive results to state-of-the-art. Using a human side-by-side evaluation on a set of isolated simple sentences, it reduces translation errors by an average of 60% compared to Google's phrase-based production system.

|  |  |
| --- | --- |
| Subjects: | Computation and Language (cs.CL); Artificial Intelligence (cs.AI); Machine Learning (cs.LG) |
| Cite as: | [arXiv:1609.08144](https://arxiv.org/abs/1609.08144) [cs.CL] |
|  | (or  [arXiv:1609.08144v2](https://arxiv.org/abs/1609.08144v2) [cs.CL] for this version) |
|  | <https://doi.org/10.48550/arXiv.1609.08144> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Mike Schuster [[view email](/show-email/cea93c63/1609.08144)]   
**[[v1]](/abs/1609.08144v1)**
Mon, 26 Sep 2016 19:59:55 UTC (969 KB)  
**[v2]**
Sat, 8 Oct 2016 19:10:41 UTC (968 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation, by Yonghui Wu and 30 other authors

* [View PDF](/pdf/1609.08144)
* [HTML (experimental)](https://arxiv.org/html/1609.08144v2)
* [TeX Source](/src/1609.08144)

[view license](http://arxiv.org/licenses/nonexclusive-distrib/1.0/ "Rights to this article")

### Current browse context:

cs.CL

[< prev](/prevnext?id=1609.08144&function=prev&context=cs.CL "previous in cs.CL (accesskey p)")
  |   
[next >](/prevnext?id=1609.08144&function=next&context=cs.CL "next in cs.CL (accesskey n)")

[new](/list/cs.CL/new)
 | 
[recent](/list/cs.CL/recent)
 | [2016-09](/list/cs.CL/2016-09)

Change to browse by:

[cs](/abs/1609.08144?context=cs)  
[cs.AI](/abs/1609.08144?context=cs.AI)  
[cs.LG](/abs/1609.08144?context=cs.LG)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:1609.08144)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=1609.08144)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:1609.08144)

### [8 blog links](/tb/1609.08144)

([what is this?](https://info.arxiv.org/help/trackback.html))

### [DBLP](https://dblp.uni-trier.de) - CS Bibliography

[listing](https://dblp.uni-trier.de/db/journals/corr/corr1609.html#WuSCLNMKCGMKSJL16 "listing on DBLP") | [bibtex](https://dblp.uni-trier.de/rec/bibtex/journals/corr/WuSCLNMKCGMKSJL16 "DBLP bibtex record")

[Yonghui Wu](https://dblp.uni-trier.de/search/author?author=Yonghui%20Wu "DBLP author search")  
[Mike Schuster](https://dblp.uni-trier.de/search/author?author=Mike%20Schuster "DBLP author search")  
[Zhifeng Chen](https://dblp.uni-trier.de/search/author?author=Zhifeng%20Chen "DBLP author search")  
[Quoc V. Le](https://dblp.uni-trier.de/search/author?author=Quoc%20V.%20Le "DBLP author search")  
[Mohammad Norouzi](https://dblp.uni-trier.de/search/author?author=Mohammad%20Norouzi "DBLP author search")

…

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/1609.08144&description=Google's%20Neural%20Machine%20Translation%20System:%20Bridging%20the%20Gap%20between%20Human%20and%20Machine%20Translation "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/1609.08144&title=Google's%20Neural%20Machine%20Translation%20System:%20Bridging%20the%20Gap%20between%20Human%20and%20Machine%20Translation "Bookmark on Reddit")

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

[Which authors of this paper are endorsers?](/auth/show-endorsers/1609.08144) |
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