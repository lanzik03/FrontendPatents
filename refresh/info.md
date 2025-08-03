**PatentsView**

The API docs are [here](https://search.patentsview.org/docs/docs/Search%20API/SearchAPIReference)

**GooglePatents**

Google Patents classifies documents with multiple CPC codes. Essentially, we are replicating this classification task for HS6 codes.

**CPC Text Categorizer**

CPC has developed a light [version](https://epn.epo.org/cpc-text-categoriser) of the GooglePatents algorithm

**Final product**

Output a concordance table for CPC and HS6

Classify patents with their associated HS6 codes, possibly more than one per patent

**Methods**

- Semantic search, latent Dirichlet allocation, latent semantic analysis, word embeddingd
- Wiki2Vec
- BERT, SBERT, PatentsBERT, ColBERT
- MUVERA

**References**

1) A [Google whitepaper](https://services.google.com/fh/files/blogs/bert_for_patents_white_paper.pdf) on how to leverage BERT for patents
2) There is a 2022 MSc [thesis](https://odr.chalmers.se/server/api/core/bitstreams/2641e2b6-430b-4013-b798-1f0511cbd813/content) on the topic
3) This [repo](https://github.com/ec-jrc/Patents4IPPC) is employed by the European Commission

**Top journals in the field**

ChatGPT suggest [these journals](https://chatgpt.com/s/t_68775c33de648191a44a8b95aad28ef0), taking into account impact factor and acceptance rate