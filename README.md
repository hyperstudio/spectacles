# Spectacles (alpha)

Spectacles is open source software for creating active archives of digital
texts. It allows for user-created rich media annotations of those texts, as
well as fuzzy search over both texts and annotations. Additionally it uses
natural language processing techniques to allow users to browse annotations and
texts similar to those they've found relevant to their research needs.

**Spectacles is currently still under development** and should be considered to
be alpha-version software. Read, don't run, the code at your own risk.

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
      - [x] Set up vector store (2/23)
      - [x] "Mark this as useful / bookmarked" for both documents and annotations (2/23)
        - [ ] Client side code for actually bookmarking
      - [x] Document recommendations
      - [x] Annotation recommendations
      - [ ] Intelligent recommendations using vector similarity (2/28)
    - [ ] Home page (3/2)
    - [ ] Account creation/registration flow (3/2)
    - [ ] Per-archive scoping
  - [ ] Implementation details
    - [x] Consistent data store on the client side
    - [x] Scope searches by current archive
    - [ ] Separate out recommendation and datastore backend logic to be published as a package
  - [x] Deployment
    - [x] Server up and running
    - [x] Postgres installed
    - [x] Elasticsearch installed
    - [x] SSH keys installed and code cloned
    - [x] Dependencies installed and django app running
    - [x] Django app connected to databases
    - [x] Nginx connected to Django through uWSGI
