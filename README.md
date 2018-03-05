# Spectacles

## Architecture
- `app`: contains all of the application-specific logic
- `client`: contains all of the React.js code for the website. This code gets compiled by Webpack and the results are placed in the `static` folder.
- `datastore`: implementation of an Annotator.js-compatible data store, similar to the `annotation-store` project. This can be extracted into a separate github repository in the future and contributed back to the community as a "plugin" for Django.
- `scripts`: contains scripts and script output related to getting data from Annotation Studio into Spectacles.
- `templates`: contains the basic HTML templates that Django looks for in order to render the website. THese are very simple shims, most of the website is defined by the React.js code in `client`.

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
