pv254-blog-post-recsys
======================

Blog post recommender system for signaly.cz

Literature
------------

- [Recommender systems handbook](http://www.cs.bme.hu/nagyadat/Recommender_systems_handbook.pdf) – nice overview of the RecSys techniques and the current state-of-the-art
- [TF-IDF and Cosine Similarity](http://janav.wordpress.com/2013/10/27/tf-idf-and-cosine-similarity/)
- [ When tf*idf and cosine similarity fail](http://www.p-value.info/2013/02/when-tfidf-and-cosine-similarity-fail.html)


Content
-----------

- */cf_rust* – Unary collaborative filtering made in Rust
- */content_based* - TF-IDF and cosine similiarity computation made in Python
- */draft* - originally draft implementations, now contains just a collaborative filtering implementation in Python
- */mahout* - Collaborative filtering made in Apache Mahout

Data
-----

Data on wich the computation was done are proprietary and therefore not part of this repository. The structure was the following:

- *blog-post-likes.csv*: user_id, post_id, like_date
- *blog-posts.csv*: post_id, blog_id, title, content, published_date

