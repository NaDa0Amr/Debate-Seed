"""
Step 1: Data collection.

Crawls a seeded list of URLs known to be on-topic (transformer architecture /
training-strategy content: MoE, attention variants, SSMs, PPO/GRPO) and
converts each page to clean Markdown.

Kept shallow on purpose: we seed with specific known-good pages rather than
letting the crawler wander through an entire domain, which is what was
pulling in off-topic content before.

Key enhancement: deny versioned arXiv URLs (e.g. /abs/1706.03762v1..v7) to
avoid near-duplicate documents. The versionless URL (/abs/1706.03762) always
points to the latest revision.

Run:
    python src/spider.py
Output:
    data/raw_markdown/*.md   (one file per page)
    data/raw_docs.jsonl      (combined: url, title, markdown per line)
"""

from scrapling.spiders import SiteToMarkdownSpider, CrawlRule, LinkExtractor


class TransformerDocsSpider(SiteToMarkdownSpider):
    name = "transformer_docs"

    # --- Seed with pages you already know are on-topic. ---
    # Built from targeted searches (arXiv search, Google Scholar,
    # "site:huggingface.co/blog moe", etc.).
    start_urls = [
        # ── Core architecture papers (arXiv abstract pages) ──
        "https://arxiv.org/abs/1706.03762",   # Attention Is All You Need
        "https://arxiv.org/abs/2101.03961",   # Switch Transformer (MoE)
        "https://arxiv.org/abs/2401.04088",   # Mixtral of Experts
        "https://arxiv.org/abs/2004.05150",   # Longformer (sliding window)
        "https://arxiv.org/abs/2310.06825",   # Mistral 7B
        "https://arxiv.org/abs/2009.14794",   # Performer (linear attention)
        "https://arxiv.org/abs/2312.00752",   # Mamba (SSM)
        "https://arxiv.org/abs/2203.02155",   # InstructGPT (PPO/RLHF)
        "https://arxiv.org/abs/2402.03300",   # DeepSeekMath (GRPO)

        # ── Debate topic 1: MoE vs Dense ──
        "https://arxiv.org/abs/1701.06538",   # Outrageously Large Neural Networks (Shazeer MoE)
        "https://arxiv.org/abs/2112.06905",   # GLaM: Efficient Scaling with MoE
        "https://arxiv.org/abs/2209.07858",   # ST-MoE: Stable Training

        # ── Debate topic 2: Attention variants ──
        "https://arxiv.org/abs/2006.16668",   # Big Bird (sparse attention)
        "https://arxiv.org/abs/2006.03555",   # Linformer (linear attention)
        "https://arxiv.org/abs/2305.14314",   # LongNet (dilated attention)
        "https://arxiv.org/abs/2205.14135",   # FlashAttention
        "https://arxiv.org/abs/2307.08691",   # FlashAttention-2

        # ── Debate topic 3: Sliding window / local attention ──
        "https://arxiv.org/abs/1904.10509",   # Sparse Transformer (Child et al.)
        "https://arxiv.org/abs/2203.10079",   # Efficient Attention with Linear Complexity (ABC)

        # ── Debate topic 4: Hybrid architectures ──
        "https://arxiv.org/abs/2305.13245",   # RWKV (RNN + Transformer hybrid)
        "https://arxiv.org/abs/2402.19427",   # Jamba (SSM + Attention hybrid)
        "https://arxiv.org/abs/2406.07887",   # Samba hybrid architecture
        "https://arxiv.org/abs/2405.04434",   # Mamba-2

        # ── Debate topic 5: Pretraining vs reasoning-oriented training ──
        "https://arxiv.org/abs/2210.11416",   # Scaling Instruction Fine-Tuning (Flan)
        "https://arxiv.org/abs/2305.14705",   # Orca: Progressive Learning
        "https://arxiv.org/abs/2309.12284",   # phi-1.5 (reasoning in pretraining)
        "https://arxiv.org/abs/2501.12948",   # DeepSeek-R1 (reasoning RL)

        # ── Debate topic 6: PPO vs GRPO ──
        "https://arxiv.org/abs/1707.06347",   # PPO original paper
        "https://arxiv.org/abs/2210.01241",   # DPO
        "https://arxiv.org/abs/2209.14375",   # RLHF Anthropic
        "https://arxiv.org/abs/2212.09710",   # Self-Instruct

        # ── Blog posts (high-quality explainers) ──
        "https://huggingface.co/blog/moe",
        "https://huggingface.co/blog/mixtral",
        "https://huggingface.co/blog/mamba-state-space-models",
        "https://huggingface.co/blog/rlhf",
        "https://huggingface.co/blog/deep-rl-ppo",

        # ── Lilian Weng's high-quality blog posts ──
        "https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/",
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/",
    ]

    allowed_domains = {"arxiv.org", "huggingface.co", "lilianweng.github.io"}
    output_dir = "data/raw_markdown"
    max_pages = 300         # headroom above the 50-doc minimum
    main_content_only = True

    def rules(self):
        return [
            CrawlRule(
                LinkExtractor(
                    # Only follow further links that still look on-topic.
                    allow=[
                        r"/abs/\d+\.\d+$",       # arXiv abstracts (versionless only)
                        r"/blog/[a-z0-9\-]*(moe|mixtral|mamba|attention|rlhf|grpo|ppo|reasoning)",
                        r"/posts/\d{4}-\d{2}-\d{2}",  # Lilian Weng blog posts
                    ],
                    deny=[
                        r"/abs/\d+\.\d+v\d+",   # SKIP versioned arXiv pages (v1, v2, ...)
                        r"/pdf/", r"/list/", r"\?",
                        r"/tags/", r"/page/\d+/",
                        r"/html/",               # arXiv HTML renderings
                    ],
                ),
                callback=self.parse,
            )
        ]


if __name__ == "__main__":
    result = TransformerDocsSpider().start()
    result.items.to_jsonl("data/raw_docs.jsonl")
    print(f"Collected {len(result.items)} pages -> data/raw_docs.jsonl")