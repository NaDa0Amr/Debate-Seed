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

**arXiv:2210.11416** (cs)

[Submitted on 20 Oct 2022 ([v1](https://arxiv.org/abs/2210.11416v1)), last revised 6 Dec 2022 (this version, v5)]

Title:Scaling Instruction-Finetuned Language Models
===================================================

Authors:[Hyung Won Chung](https://arxiv.org/search/cs?searchtype=author&query=Chung,+H+W), [Le Hou](https://arxiv.org/search/cs?searchtype=author&query=Hou,+L), [Shayne Longpre](https://arxiv.org/search/cs?searchtype=author&query=Longpre,+S), [Barret Zoph](https://arxiv.org/search/cs?searchtype=author&query=Zoph,+B), [Yi Tay](https://arxiv.org/search/cs?searchtype=author&query=Tay,+Y), [William Fedus](https://arxiv.org/search/cs?searchtype=author&query=Fedus,+W), [Yunxuan Li](https://arxiv.org/search/cs?searchtype=author&query=Li,+Y), [Xuezhi Wang](https://arxiv.org/search/cs?searchtype=author&query=Wang,+X), [Mostafa Dehghani](https://arxiv.org/search/cs?searchtype=author&query=Dehghani,+M), [Siddhartha Brahma](https://arxiv.org/search/cs?searchtype=author&query=Brahma,+S), [Albert Webson](https://arxiv.org/search/cs?searchtype=author&query=Webson,+A), [Shixiang Shane Gu](https://arxiv.org/search/cs?searchtype=author&query=Gu,+S+S), [Zhuyun Dai](https://arxiv.org/search/cs?searchtype=author&query=Dai,+Z), [Mirac Suzgun](https://arxiv.org/search/cs?searchtype=author&query=Suzgun,+M), [Xinyun Chen](https://arxiv.org/search/cs?searchtype=author&query=Chen,+X), [Aakanksha Chowdhery](https://arxiv.org/search/cs?searchtype=author&query=Chowdhery,+A), [Alex Castro-Ros](https://arxiv.org/search/cs?searchtype=author&query=Castro-Ros,+A), [Marie Pellat](https://arxiv.org/search/cs?searchtype=author&query=Pellat,+M), [Kevin Robinson](https://arxiv.org/search/cs?searchtype=author&query=Robinson,+K), [Dasha Valter](https://arxiv.org/search/cs?searchtype=author&query=Valter,+D), [Sharan Narang](https://arxiv.org/search/cs?searchtype=author&query=Narang,+S), [Gaurav Mishra](https://arxiv.org/search/cs?searchtype=author&query=Mishra,+G), [Adams Yu](https://arxiv.org/search/cs?searchtype=author&query=Yu,+A), [Vincent Zhao](https://arxiv.org/search/cs?searchtype=author&query=Zhao,+V), [Yanping Huang](https://arxiv.org/search/cs?searchtype=author&query=Huang,+Y), [Andrew Dai](https://arxiv.org/search/cs?searchtype=author&query=Dai,+A), [Hongkun Yu](https://arxiv.org/search/cs?searchtype=author&query=Yu,+H), [Slav Petrov](https://arxiv.org/search/cs?searchtype=author&query=Petrov,+S), [Ed H. Chi](https://arxiv.org/search/cs?searchtype=author&query=Chi,+E+H), [Jeff Dean](https://arxiv.org/search/cs?searchtype=author&query=Dean,+J), [Jacob Devlin](https://arxiv.org/search/cs?searchtype=author&query=Devlin,+J), [Adam Roberts](https://arxiv.org/search/cs?searchtype=author&query=Roberts,+A), [Denny Zhou](https://arxiv.org/search/cs?searchtype=author&query=Zhou,+D), [Quoc V. Le](https://arxiv.org/search/cs?searchtype=author&query=Le,+Q+V), [Jason Wei](https://arxiv.org/search/cs?searchtype=author&query=Wei,+J)

View a PDF of the paper titled Scaling Instruction-Finetuned Language Models, by Hyung Won Chung and 34 other authors

[View PDF](/pdf/2210.11416)
[HTML (experimental)](https://arxiv.org/html/2210.11416v5)
> Abstract:Finetuning language models on a collection of datasets phrased as instructions has been shown to improve model performance and generalization to unseen tasks. In this paper we explore instruction finetuning with a particular focus on (1) scaling the number of tasks, (2) scaling the model size, and (3) finetuning on chain-of-thought data. We find that instruction finetuning with the above aspects dramatically improves performance on a variety of model classes (PaLM, T5, U-PaLM), prompting setups (zero-shot, few-shot, CoT), and evaluation benchmarks (MMLU, BBH, TyDiQA, MGSM, open-ended generation). For instance, Flan-PaLM 540B instruction-finetuned on 1.8K tasks outperforms PALM 540B by a large margin (+9.4% on average). Flan-PaLM 540B achieves state-of-the-art performance on several benchmarks, such as 75.2% on five-shot MMLU. We also publicly release Flan-T5 checkpoints, which achieve strong few-shot performance even compared to much larger models, such as PaLM 62B. Overall, instruction finetuning is a general method for improving the performance and usability of pretrained language models.

|  |  |
| --- | --- |
| Comments: | Public checkpoints: [this https URL](https://huggingface.co/docs/transformers/model_doc/flan-t5) |
| Subjects: | Machine Learning (cs.LG); Computation and Language (cs.CL) |
| Cite as: | [arXiv:2210.11416](https://arxiv.org/abs/2210.11416) [cs.LG] |
|  | (or  [arXiv:2210.11416v5](https://arxiv.org/abs/2210.11416v5) [cs.LG] for this version) |
|  | <https://doi.org/10.48550/arXiv.2210.11416> Focus to learn more  arXiv-issued DOI via DataCite |

Submission history
------------------

From: Jason Wei [[view email](/show-email/f9287979/2210.11416)]   
**[[v1]](/abs/2210.11416v1)**
Thu, 20 Oct 2022 16:58:32 UTC (1,212 KB)  
**[[v2]](/abs/2210.11416v2)**
Fri, 21 Oct 2022 17:46:04 UTC (1,212 KB)  
**[[v3]](/abs/2210.11416v3)**
Wed, 16 Nov 2022 09:44:42 UTC (684 KB)  
**[[v4]](/abs/2210.11416v4)**
Wed, 23 Nov 2022 02:11:56 UTC (760 KB)  
**[v5]**
Tue, 6 Dec 2022 21:39:48 UTC (761 KB)

Full-text links:

Access Paper:
-------------

View a PDF of the paper titled Scaling Instruction-Finetuned Language Models, by Hyung Won Chung and 34 other authors

* [View PDF](/pdf/2210.11416)
* [HTML (experimental)](https://arxiv.org/html/2210.11416v5)
* [TeX Source](/src/2210.11416)

[![license icon](https://arxiv.org/icons/licenses/by-4.0.png)view license](http://creativecommons.org/licenses/by/4.0/ "Rights to this article")

### Current browse context:

cs.LG

[< prev](/prevnext?id=2210.11416&function=prev&context=cs.LG "previous in cs.LG (accesskey p)")
  |   
[next >](/prevnext?id=2210.11416&function=next&context=cs.LG "next in cs.LG (accesskey n)")

[new](/list/cs.LG/new)
 | 
[recent](/list/cs.LG/recent)
 | [2022-10](/list/cs.LG/2022-10)

Change to browse by:

[cs](/abs/2210.11416?context=cs)  
[cs.CL](/abs/2210.11416?context=cs.CL)

### References & Citations

* [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:2210.11416)
* [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=2210.11416)
* [Semantic Scholar](https://api.semanticscholar.org/arXiv:2210.11416)

### [1 blog link](/tb/2210.11416)

([what is this?](https://info.arxiv.org/help/trackback.html))

export BibTeX citation
Loading...

BibTeX formatted citation
-------------------------

×

loading...

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/2210.11416&description=Scaling%20Instruction-Finetuned%20Language%20Models "Bookmark on BibSonomy")
[![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/2210.11416&title=Scaling%20Instruction-Finetuned%20Language%20Models "Bookmark on Reddit")

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

[Which authors of this paper are endorsers?](/auth/show-endorsers/2210.11416) |
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