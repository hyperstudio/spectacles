Meta
===
Google Doc Version:
  https://docs.google.com/document/d/1ANnIjQvnyKWnmD3WSWgKiNTe8rUKJMAJppjq38Rxf1o/edit
Wiki
  https://wikis.mit.edu/confluence/pages/viewpage.action?pageId=23855357
  Passwords
    https://wikis.mit.edu/confluence/display/hyperstudio/password+list
Slack
  https://hyperstudio.slack.com/messages


2018-03-05 Monday
=================
How to set up the local postgres password and get it talking to Django:
https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04

How to populate the ES and PG databases
```bash
./manage.py migrate
./manage.py search_index --create
```

Now this works
```python
from app import search
from app.models import User
search.find_annotations('food')
User.objects.all()
```


2018-02-26 Monday
=================
Trying to install FAISS, has bad install instructions, so going with FALCONN

```
brew install llvm --with-clang --with-asan
```

Yeah, struggling through linking `omp.h` is not how I want to spend my time.

Met with my TA, who advised that I talk to Regina again. Good idea.

https://rare-technologies.com/performance-shootout-of-nearest-neighbours-intro/
https://github.com/spotify/annoy

2018-02-25 Sunday
=================
- TODO: blog post due next Friday about the beginning of Spectacles
- TODO: list of capabilities, screenshots/online for Tuesday -- ger
man design students might then give me something useful

Clear all bookmarks concept

## Kurt meeting
Act.mit.esu/cavs

Freezine montfort to kurt

Merchant of venice subsite

Justin ongley american studies new milford highschool 2581 user id

Coannotation.com

Wyn kelley

2018-02-23 Friday
=================

## Todo List
- [x] Spec out ES document model
- [X] use pre-fetched annotations (swap out Store abstraction)
- [X] rich text editing
- [x] Fully index all data on Heroku servers for further development
- [X] Demo
  - [X] Set up React routes
  - [X] Display a list of all documents
  - [X] Display a single document
  - [X] Search
    - [X] Write search queries, check that model supports it
    - [X] Demoable full-text search over documents, annotations
  - [X] Add annotator.js to the document display page to show all annotations for a single document
  - [X] Implement annotation APIs
    - [X] Annotation CRUD
    - [X] Authentication
      - [x] login
      - [x] logout
- [ ] Spring Demo 
  - [ ] Features
    - [ ] Finish up search improvements
      - [x] Make all searches based on the ElasticSearch backend (2/16)
        - [x] Annotations in a document
        - [x] Documents in an archive
      - [x] Simple query language parsing to allow metadata search `title:"Origin of Species" author:"Darwin"` (2/16)
      - [x] Full-text search of documents shows relevant fragment in result
        - [ ] allows deeplinking to that fragment (2/16)
      - [x] Show all of "my" activity (documents annotated, annotations, bookmarks). (2/21)
        - [x] Allow searching over it by scoping the same queries as usual to belong to a certain user
        - [x] Allow linking to a user's activity page, searching
    - [ ] Recommendations
      - [ ] Set up vector store (2/23)
      - [x] "Mark this as useful / bookmarked" for both documents and annotations (2/23)
      - [ ] Intelligent recommendations using vector similarity (2/28)
    - [ ] Home page (3/2)
    - [ ] Account creation/registration flow (3/2)
  - [ ] Implementation details
    - [ ] Consistent data store on the client side
    - [ ] Scope searches by current archive
    - [ ] Separate out recommendation and datastore backend logic to be published as a package

- [ ] Future work
  - [ ] US-IRAN data
  - [ ] Ingestion flow
    - [ ] Text processing through worker queues
    - [ ] Importers for HTML, PDF, .DOC, .TXT
    - [ ] Command-line tools
    - [ ] Online interface

2017-02-16 Friday
=================
# Meeting with Kurt
- author:David or tags:[fish, cat] advanced search
- Bookmarking or marking as relevant

network graphs as maps, automatically labeling "towns" and "roads"

wants to be able to build an argument while demoing the tool

potential collaboration with the EPFL
  and with the Guardian, national film board of Canada: rising water levels


- [ ] set up the new digital humanities website
- [ ] Tentative timeline due Friday



2017-12-01 Friday
===

How to install jwt:
```
$ env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" pip install jwt
```


2017-11-17 Friday
===
Kurt has access to some kind of free heroku hosting, so I've set up addons on there for Postgres, Redis, and Elasticsearch.

https://dashboard.heroku.com/apps/spectacles-postgres

```
# Elasticsearch
https://ae43c40d5d45590bf03cb90e8cd571ef.us-east-1.aws.found.io:9243
username: elastic
password: YiOG4JeeidZI1pjm3V0o8jjX

# Postgres
username: u2ldeq1kd89i4f
password: p1dc49aa0b4bd33d263951ee35f6d86940f286a96d91c13d1465e34b918d76ac2
host: ec2-34-236-19-227.compute-1.amazonaws.com
database: d90m0v2sut1kbq
port: 5432
uri: postgres://u2ldeq1kd89i4f:p1dc49aa0b4bd33d263951ee35f6d86940f286a96d91c13d1465e34b918d76ac2@ec2-34-236-19-227.compute-1.amazonaws.com:5432/d90m0v2sut1kbq
```

2017-11-16 Thursday
===
https://www.elastic.co/guide/en/elasticsearch/guide/master/multi-index-multi-type.html

Having trouble inserting more than 16000 records, maybe because my disk is full?
https://stackoverflow.com/questions/33369955/low-disk-watermark-exceeded-on#34221506
```
# Add to
# /usr/local/etc/elasticsearch/elasticsearch.yml
cluster.routing.allocation.disk.threshold_enabled: true
cluster.routing.allocation.disk.watermark.low: 5gb
cluster.routing.allocation.disk.watermark.high: 4gb
```

That didn't seem to be it -- from watching Activity Monitor, I think my laptop is just running out of memory around then.

2017-11-14 Tuesday
===

https://medium.freecodecamp.org/elasticsearch-with-django-the-easy-way-909375bc16cb
https://github.com/elastic/elasticsearch-dsl-py
https://github.com/sabricot/django-elasticsearch-dsl
https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#highlighting

oh yeah this is definitely what I want to be using. Haystack is behind the times.

List all indices on the ES:

```
curl http://localhost:9200/_aliases?pretty=1
```

from https://www.elastic.co/guide/en/elasticsearch/reference/current/_basic_concepts.html
and from https://www.elastic.co/guide/en/elasticsearch/guide/current/mapping.html

> In summary:
>   Good: kitchen and lawn-care types inside the products index, because the two types are essentially the same schema.
>   Bad: products and logs types inside the data index, because the two types are mutually exclusive. Separate these into their own indices. 

need one index per document type

2017-11-11 Saturday
===

```bash
# Home folder for ElasticSearch:
/usr/local/etc/elasticsearch 
# Run elasticsearch in daemon mode
elasticsearch -d
```

Ah, haystack doesn't support searching on elasticsearch 5.x. But it maybe seems to have indexed things correctly?
Going to try to use http://elasticsearch-dsl.readthedocs.io/en/latest/ for searching.

2017-11-10 Friday
===
```
$ psql
\connect d3soppdkjvqvb0
\dt
```

https://stackoverflow.com/questions/7695962/postgresql-password-authentication-failed-for-user-postgres

Had to set up a "spectacle" user on the "spectacles" database.

https://www.postgresql.org/docs/9.0/static/sql-createdatabase.html

https://github.com/hzdg/django-enumfields

https://docs.djangoproject.com/en/1.11/ref/models/fields/

https://github.com/facebookresearch/faiss
https://code.facebook.com/posts/1373769912645926/faiss-a-library-for-efficient-similarity-search/

https://www.quora.com/Is-it-possible-to-create-an-index-with-haystack-in-Django-on-a-json-field-in-Postgres

2017-11-08 Wednesday
===
Looking at creating the document model, and looked at the annotation studio data store project for an example. I also found [`h`](https://github.com/hypothesis/h/tree/master/h), the newer open annotator data store / API project from the people at hypothes.is. I'm starting to think that it would make most sense for me to first create the data store as a Django app that's part of this project. That way others can take advantage of my work, which is nice. There's an existing Flask app but it's built on top of ElasticSearch and kind of complicated.

http://docs.annotatorjs.org/en/v1.2.x/storage.html
https://github.com/openannotation/annotator-store/blob/master/annotator/annotation.py

Hmmm, but the deliverables I have for Friday are 
- Annotations, Documents all stored in a database
- Full text search with Elasticsearch over all the annotations
- Simple viewer to show the relevant text and Annotation

So, I wonder if the best approach here is to use a JSONField

https://docs.djangoproject.com/en/1.11/ref/contrib/postgres/fields/#jsonfield

and simply shove the whole Annotation object into it, after validating against 
a JSON schema

https://pypi.python.org/pypi/jsonschema

which can be done in the `.clean()` method:

https://docs.djangoproject.com/en/1.11/ref/models/instances/#django.db.models.Model.clean

Permissions seem a little strange http://docs.annotatorjs.org/en/v1.2.x/plugins/permissions.html

And the auth model, which is centered around hving a separate server for annotations and the data, might be more useful if we shortcut it to simply link against the current `UserModel`.

But, how will this work with Haystack?

http://django-haystack.readthedocs.io/en/v2.4.1/searchindex_api.html#advanced-data-preparation
http://django-haystack.readthedocs.io/en/v2.4.1/searchindex_api.html#advanced-data-preparation

Randall Leads

2017-11-07 Tuesday
===
Running through the Django startproject. Figure it will look something like:

spectacles/ -- whole project
    specutron/ -- backend
    frame/ -- frontend

created the repo at https://github.com/hyperstudio/spectacles

Custom user model:

https://medium.com/@ramykhuffash/django-authentication-with-just-an-email-and-password-no-username-required-33e47976b517
https://docs.djangoproject.com/en/1.11/ref/django-admin/#django-admin-createsuperuser
https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#specifying-custom-user-model

Had to explicitly create the custom User Model migration before installing

```bash
./manage.py createmigrations app
./manage.py migrate
```

2017-11-03 Friday
===
Some background reading from JSTOR labs:

http://labs.jstor.org/blog/#!you_cant_rollerskate_in_a_buffalo_herd-and_you_cant_innovate_when_youre_afraid

- Prototyping
- Rapid Iteration
- In-person testing
- Labeling
>  Setting expectations with users with a Beta label can be very powerful – it makes it easier to release early in order to get user feedback. We at JSTOR Labs tend to marry this label with a “Help us make this better” feedback link. The Beta label changes the relationship your users have with the tool and you; it brings them under the tent. With Text Analyzer, for example, we’ve received feedback from literally thousands of users through this simple form and social media. That feedback has been invaluable to us in finding and prioritizing issues.

http://labs.jstor.org/blog/#!under_the_hood_of_text_analyzer

Interestingly, they expose the source of the topic -- how it was found:
http://images.contentful.com/xb7lbocpfjk9/2dIteT67lqoQUGe8qOa2W4/fc708ff292fc0be8c4ba160766e337d1/inferred_topic.png

> Topics explicitly mentioned in the text are identified using a the JSTOR thesaurus (a controlled vocabulary containing more than 40,000 concepts) and a human-curated set of rules in the MAIstro product from Access Innovations. Using MAIstro, concepts/terms from the JSTOR thesaruus are identified in unstructured text.

> Latent topics are inferred using an LDA (Latent Dirichlet allocation) topic model trained with JSTOR content associated with the terms in our controlled vocabulary. Our application of LDA topic modeling takes advantage of the controlled vocabulary and rules-based document tagging described above. With these tagged documents we are able to use the Labeled LDA (as described here) variant of LDA to train a model using our thesaurus as a predefined set of labels for the model topics.

> Named entities (persons, locations, organizations) are identified using multiple entity recognition services and tools. This includes Alchemy (part of IBMs Watson services), OpenCalais (from Thompson Reuters), the Stanford Named Entity Recognizer, and Apache OpenNLP. Entities recognized by the individual tools/services are aggregated and ranked using a voting scheme and a basic TF-IDF calculation to estimate the relative importance of the entity to the source document.

http://www.jstor.org/analyze/about

### Django Haystack
https://github.com/Einsteinish/Django-Haystack-Elasticsearch
http://haystacksearch.org/

### Custom Analyzers?
http://stefansavev.com/blog/custom-similarity-for-elasticsearch/
https://www.elastic.co/guide/en/elasticsearch/guide/2.x/pluggable-similarites.html
https://github.com/FALCONN-LIB/FALCONN/tree/master/
https://github.com/FALCONN-LIB/FALCONN/issues/24
https://github.com/FALCONN-LIB/FALCONN/issues/51

These are most relevant?
https://github.com/FALCONN-LIB/FALCONN/issues/2
https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-termvectors.html

### Exporting data from production
https://www.postgresql.org/docs/9.1/static/backup-dump.html
https://www.postgresql.org/docs/9.2/static/app-pgrestore.html
https://www.postgresql.org/docs/9.2/static/app-pgdump.html

https://dashboard.heroku.com/apps/annotationstudio
https://devcenter.heroku.com/articles/heroku-postgres-import-export#import
https://docs.mongodb.com/manual/reference/program/mongodump/#bin.mongodump

Managed to export the data without any issues from the Heroku control interfaces.


2017-09-26 Tuesday
===
Talked to Regina. Explained more of the context behind the project -- active archives, how different researchers can benefit from seeing how other researchers have used the same source materials -- and now she's not angry at me. Before, she thought I had no idea what I was talking about, and that's pretty fair: when put on the spot to give a 5 minute description of my entire project, I was disorganized and unable to convey to her what she wanted to hear. Now that I have a better idea of her preferred communication style ("you have 5 minutes: go.") I was able to push back on her initial objections, explain the background, and then explain the problem I wanted to solve, without going too far into the details. Then, she said, "here's the details i want to here: how you're going to exploit the structure of the annotations and the documents to improve similarity measure performance on documents and annotations." Which is a great NLP-realm phrasing of the problem at hand, that I was unable to come up with because I don't know very much about the field yet.

So, after coming to understand that I'm not a crazy person, she suggested the following things:

- Find an archive with lots of annotations
  - The US-IRAN archive will not work because almost no annotations
  - Instead, I can compile an artificial "archive" out of documents + annotations from Hyperstudio. @Kurt had the same feedback here.
- Evaluate a similarity metric based simply on tf-idf vectors and cosine similarity. This is baseline 0.
- Evaluate a metric based on neural embeddings (sem2vec, fasttext, etc.). This is baseline 1.
- Then, consider developing my own metric that exploits the structure of the problem -- documents and annotations, user history, etc.

This makes a lot of sense and is ~ what I was thinking originally, but having it spelled out for me was useful. Kurt is going to get me access to AS data.

2017-09-22 Friday
===
Documerica https://www.flickr.com/photos/usnationalarchives/sets/72157620856436476/

6.UAR homework with background resources:
  https://docs.google.com/spreadsheets/d/1cWNWlWwOeZrUhA9eJVG3r9Jdx7-iCfuf-Sq9qmU9T_o/edit#gid=0

https://libraries.mit.edu/about/experiments/
-> TODO: ask Carl about who is behind this?

Mackenzie Smith: http://simile.mit.edu/
  HP, CSAIL, Libraries

Haystack @ CSAIL:
  Amy Zhang: https://amyxzhang.wordpress.com/
  Nota Bene: http://nb.mit.edu/welcome
  Joshua Blum!

2017-09-21 Thursday
===
TODO: write up meeting with Regina
Start working on examples

https://docs.google.com/spreadsheets/d/1cWNWlWwOeZrUhA9eJVG3r9Jdx7-iCfuf-Sq9qmU9T_o/edit#gid=0

[StoryBuilder](http://www.everlaw.com/Features.html#case-prep)

2017-09-20 Wednesday
===

TODO: writeup meeting with David
Get back to David


2017-09-19 Tuesday
===

6.UAR Homework 1:

### 1. What are two skills you want to gain with this SuperUROP?
I'm really interested in exploring potential applications of natural language processing techniques. Augmentative AI in general presents huge possibilities but also large design problems; I hope to learn more about user interfaces and user experience design as well, so that I can create useful tools that researchers will understand and use.

### 2. What are two concrete goals you have for yourself for this year?
The focus of my UROP is to release an NLP-based tool that other researchers can use to better understand archives of text. So my primary goal is to build this tool. My secondary goal is to learn more about doing academic research, as all of my past experience has been in industry, so that I can decide whether or not I'd like to enter the M.Eng. program.

### 3. What are your advisor's expectations for you for this semester? Do these seem manageable?
Primarily, Kurt wants me to begin hewing away at a rough design for the research tool I'll build. That means this semester, I need to come up to speed on what has been tried before and what's worked -- so lots of background reading. At the same time, he'd like me to start experimenting with different NLP techniques to see what could be useful and to better understand the possibilities of the final tool. And on top of that, he'd like some technical support for his Digital Humanities classes, one of which I took last Spring. These do all seem manageable; the first two align exactly with what I want to do in order to get my project started, and I'm happy to help out with the third.

### 4. Discuss your research schedule with your advisor and write your agreed weekly schedule here.
I'll be in the lab working on my UROP:

- Tuesday 1000-1200, 1600-1800
- Thursday 1000-1200, 1500-1800
- Friday 1200-1630


### 5. Speak with your research advisor on their preferred form of weekly communication and how often you'll be meeting with them.

Along with Rachel Thompson, Kurt's Digital Humanities class RA, we'll be having a weekly meeting every Friday at noon to talk about progress. For shorter timescale communication we use email and slack.

### 6. Write out your 30-second "elevator pitch" of your project to two audiences (2 versions): Venture Capitalist; Funding Agency.

VCs:
Imagine you're a lawyer working in a law firm, trying to read a large set of related documents, maybe past case files, and extract the most relevant pieces of information for your upcoming case. Modern artificial intelligence, particularly natural language processing techniques, can apply advanced statistics to this problem, but require deep programming and mathematical knowledge. I'm creating a tool for exploring these collections of documents ("archives") that takes the hottest and latest NLP techniques and wraps them in an easy-to-use interface that anyone can use, even lawyers.

Funding Agency:
Humanities research has not changed in years. Fundamentally, research is performed the same way it always has been: someone sitting in a room, poring over the same old texts, trying to come up with relationships between them. Using the power of modern natural language processing techniques, we can inform that research to make better use of our time and learn more about our heritage. The same techniques that work on a collection of a President's memos will work exactly as well on the Iliad, allowing for vast intertextual discourse in a way that cannot be done without computers. As a member of MIT's Hyperstudio, one of the forefront Digital Humanities laboratories, I am creating an archive exploration tool grounded both in the theory of the active archive and in the years of experience Dr. Kurt Fendt has working with humanities researchers, to ensure that what I create is theoretically and practically novel.


2017-09-17 Sunday
===
Research on digital annotation
  https://wikis.mit.edu/confluence/display/Hyperstudio/research+on+digital+annotation
  https://wikis.mit.edu/confluence/display/Hyperstudio/Annotation+and+Tagging

Other DH groups
  https://wikis.mit.edu/confluence/display/Hyperstudio/Digital+Humanities+programs+research



2017-09-15 Friday
===
## Notes
There's too much content in the world to read it all. There are billions of beautiful, increidble pieces of art that will never be read again. IIIF is bringing even more of it online in an even easier, searchable, consumable format. But I fear a tragedy of the modern library: they won't get read. nd as things capitalize, it becomes harder to justify the existence of so much efort that isn't being read, and then it will bel ost.

So imagine, the smart annotation recommendation systems i'm building can be used to automatically work through and search these documents. Hook up with the JSTOR people, figure out ways to go deeper, weaving a thread through this world of books and letters. It's like traveling -- you've never seen an entier country, you've only seen the narrow path you walked through it. Anything to link up and encourage further walking is welcome, in an effort to walk all over the face of the earth, or to make it possible for anyone to walk onto any of the places that they might want to go in this vast, beautiful world.


## Project Planning
![Brainstorm Left](./_journal_figures/brainstorm_left.jpg)
![Brainstorm Right](./_journal_figures/brainstorm_right.jpg)

Goal: explore the effects of ML-backed tools on humanistic research.

---

Specific project: using unsupervised NLP techniques to better relate documents and annotations

Shared archive annotator
  "All writing in the same marginalia"
  Centered around a fixed archive

Annotations work across documents

"basic" nlp tasks:
  - Entity recognition and extraction
  - Wikipedia linking
  - Measures of importance or centrality to a theme (like Bookshrink) with Topic Models

Recommendation engine:
  - Other documents to read based on what you're reading so far
                            based on a specific annotation
  - "You're reading <text>, view relevant annotations from <class>/<person>"
  - "You've made <annotation>, which mentioned A B C; show related texts based on similar annotations from <class>/<person>"

New UI:
  annotation layers
  full-text search

Important to develop this
- Backwards compatible with annotation studio -- this is an exploration, but should be maintainable and, if useful, able to be included in the existing projects
- In the context of users
  So we'll focus on the Iran archive
- Open source

What does success look like?
  - Working, usable tool
  - User feedback from having applied the tool to actual research

Questions?
  What if it were focused on archives designed to change over time? "personal archive" tool
  What does an annotation look like?


Basic plan?
  now: Background research / project scoping
  4 page project proposal for 6.UAR due ~October 1st
  next: Start talking to Iran researchers, annotation studio users ASAP to understand their goals / use cases
  next: start prototyping
    "proof of concept"

## Group Meeting
- Kurt brought down the CMS 633 website somehow, wants me to bring it back up
- Rachel doesn't have access to the Mailchimp user/password
  - Fixed!

* Make sure that we're publishing about the process as we go through it
* Multi-document annotation is the key new functionality
  * Theodore Nelson's Xanadu -- don't spend 40 years building a prototype
* Machine allows filtering through different layers, recommending similar or different annotations

NEH, Berlin Free School grant (didn't work out): apply tools to existing archives
  YOu could go in as a historian and read and annotate an article or text
    But you might not be aware that a physicist annotated the same document from a completely different perspective
    But having access to the other eprson's perspective might enlightenn your historical view

Have to be mindful of larger scholarly qquestions
  How do scholars want to work?
  What other sources do scholars use?
Not focusing on changing documents

Trump/Putin Kasparov event:
  journalist and kasparov more or less agreed, even though they had two different perspectives
  gave insights into the mechanisms: creating chaos supports putin as the strong leader

Next steps:
  Kurt should reach out to John Termin to introduce me
  Masa Huoy?
  Ask about research and writing process?
    How do you go about resourcing sources
    How do you extract information from sources
    How do you assemble what you've extracted when writing?
      Is it different than formulating the ideas in the first place?
    What would help them do this more efficiently

    Throw things back at them, asking the same question in a different way
      "I'm hearing that you need <this kind of thing>, is that what you mean?"

  Alex Humphries @ JSTOR lab
    TODO for peter: read through their work, come up with questions about their techniques

  IIIF:
    Exemplify what they're working on, for text

Keep in mind: different kinds of media sources
  Conceptually: should be able to work on other kinds of media

Got to focus on the Open Annotation Standard

TODO: peter talk to mek about this project

We should think about different milestones and project planning
  Prototypes that can be shown?
  Techn demos that people can play with, focusing on specific functions (multi-doc annotation. machine recommendation)
  Research, not a Service
    Show small tech demos!
    Kurt is into this
      "Tired of doing addons to annotation studio"

How do you successfully collaborate?
  David Clure from NLP class
  Start talking to the other people in Media Lab / SHASS about DH

TODO peter: Hyperstudio Fellows group, rewrite Kurt's language and start
  Mellon fellows not announced

TODO peter: start figuring out milestones

Sussman's "proof of concept"

Kurt: can we get other UROPs / collaborators to help with this research or work?
Interface design: talk to someone?
  Think about talking to GSD
  TODO rachel: look into GSD
  Potsdam design school collaboration?

TODO kurt: send Peter and Rachel trello board
TODO kurt: contact john termin and the other researchers
TODO peter: start compiling questions for the researchers
TODO peter: post urop plan + diagram to personal page
TODO peter: bring up the website
TODO peter: follow up with Glen Robson, Renee Hellenbrecht, Heather Yager


## IIIF Meeting
- Harvard has an internal iiif group
  - this is the first meeting of MIT's
  - different community groups based on different interests: manuscripts, museums, newspapers / serial text, software developers
  - group for working to make these more discoverable?

Smithsonian has a IIIF group working across the whole institution

Newspapers: huge amount of digitized data in the national library of whales

How do you find IIF resources? how do you get notified if someone uses your data?

IIIF annotation resources are all compatible with the W3C web annotation standard


Links:
  Library experiments
    https://libraries.mit.edu/about/experiments/
  IIIF / MIT Library Announcement
    https://libraries.mit.edu/news/libraries-global/20866/
  Universal Viewer
    https://github.com/UniversalViewer/universalviewer
    Examples
      https://d.lib.ncsu.edu/collections/catalog/nubian-message-1992-11-30#?c=0&m=0&s=0&cv=1&z=3268.2353%2C3334.7143%2C1530.2654%2C1328.1066
      https://viewer.library.wales/4642022#?c=0&m=0&s=0&cv=8&xywh=386%2C23%2C2525%2C2243
      http://universalviewer.io/examples/#?c=0&m=0&s=0&cv=1&manifest=http%3A%2F%2Fwellcomelibrary.org%2Fiiif%2Fb18035723%2Fmanifest&xywh=-1%2C-116%2C4872%2C3603
      https://d.lib.ncsu.edu/collections/catalog?f%5Bispartof_facet%5D%5B%5D=Nubian+Message
  IIF Presentation API
    http://iiif.io/api/presentation/2.0/
  Full-Text Search Example
    https://github.com/NCSU-Libraries/ocracoke
    https://d.lib.ncsu.edu/collections/catalog?f%5Bfulltext_bs%5D%5B%5D=true
    http://iiif.io/api/search/1.0/#service-description
    http://www.europeana.eu/portal/en/search?view=grid&q=sv_dcterms_conformsTo%3A*iiif*
  Transfer Learning:
    https://www.analyticsvidhya.com/blog/2017/06/transfer-learning-the-art-of-fine-tuning-a-pre-trained-model/
    https://tech.zegami.com/comparing-pre-trained-deep-learning-models-for-feature-extraction-c617da54641
  W3 Web Annotation
    https://www.w3.org/TR/2017/REC-annotation-model-20170223/

2017-09-14 Thursday
===
Talking with Rachel:
  sound words
    faulty methodology
  republic of letters lab is going to die
    copyright + no intellectual property
  big gap of cms students:
    foundational texts in media studies
    social theory
    anthropology
    NSA by Barthes
      death of the author (barthes) vs. foucault
  cms colloqium thursday 5-7
  chelsea manning and sean spicer @ harvard
  paul dourish -- (stuff of bits)
    lev manovich "makes a good point, but doesn't know how databases work"
  how did joyce make ulysses autobiographical by looking at marginalia
  plces to go drink
    Charlie's Kitchen in Harvard
    Some bar under Staples
    State Park bar ~ Lord Hobo and MIT
