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
- [ ] Demo v2
  - [ ] Make all searches based on the ElasticSearch backend
  - [ ] Consistent data store on the client side
  - [ ] Scope searches by current archive
  - [ ] Recommendations
    - [ ] Set up vector store
    - [ ] "Mark this as useful / bookmarked"
    - [ ] Intelligent recommendations using vector similarity
  - [x] User auth routes
    - [x] login
    - [x] logout
    - [ ] register
  - [ ] Home page
- [ ] Future work
  - [ ] US-IRAN data
  - [ ] Ingestion
    - [ ] Text processing through worker queues
    - [ ] Upload of texts
