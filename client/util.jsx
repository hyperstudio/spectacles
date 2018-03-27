var Cookie = require('js-cookie');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

export function setupCSRF($) {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        var csrf = Cookie.get('csrftoken');
        xhr.setRequestHeader("X-CSRFToken", csrf);
      }
    }
  });
}

function StoreLogger(element, callbacks) {
  return {
    pluginInit: function () {
      this.annotator
        .subscribe("annotationCreated", function (annotation) {
          if (callbacks.create) {
            console.log('calling create callback!');
            callbacks.create(annotation);
          }
          console.info("The annotation: %o has just been created!", annotation)
        })
      .subscribe("annotationUpdated", function (annotation) {
        if (callbacks.update) {
          console.log('calling update callback!');
          callbacks.update(annotation);
        }
        console.info("The annotation: %o has just been updated!", annotation)
      })
      .subscribe("annotationDeleted", function (annotation) {
        if (callbacks.delete) {
          console.log('calling delete callback!');
          callbacks.delete(annotation);
        }
        console.info("The annotation: %o has just been deleted!", annotation)
      });
    }
  }
};

export function createAnnotator(domRef, onUpdate, userEmail, documentId) {
  // grabs Annotator from client side JS script
  window.Annotator.Plugin.StoreLogger = StoreLogger;
  return new window.Annotator(domRef, {
    popupTarget: document.getElementById('ann-wrapper'),
  })
    .addPlugin('Auth', {
      tokenUrl: '/api/store/token',
    })
  .addPlugin('Tags', {})
    .addPlugin('Permissions', {
      user: userEmail,
    })
  .addPlugin('Store', {
    prefix: `/api/store/${documentId}`,
    urls: {
      create:  '',
      read:    '',
      update:  '/:id',
      destroy: '/:id',
        // Not implemented or used.
      search:  '/search',
    },
    annotationData: {
      // TODO: what to do about this ID?
      uri: documentId,
    },
    callbacks: {
      update: onUpdate('update'),
      delete: onUpdate('delete'),
      create: (ann) => {
        return console.log('create event for:', ann);
      }
    },
    onUpdate: function(annotation, data) {
      console.error('XXXXXXXXXX');
      console.log(annotation, data);
      console.error('XXXXXXXXXX');
    },
  })
  //.addPlugin('StoreLogger', {
  //  // TODO: better callback naming and definitions here.
  //  update: onUpdate('update'),
  //  delete: onUpdate('delete'),
  //  create: onUpdate('create'),
  //})
  .addPlugin('RichText', {
    editor_enabled: true,
    tinymce: {
      selector: "li.annotator-item textarea",
      plugins: "media image insertdatetime link code",
      toolbar_items_size: 'small',
      extended_valid_elements : "iframe[src|frameborder|style|scrolling|class|width|height|name|align|id]",
      toolbar: [
        'undo redo',
        'styleselect',
        'bold italic',
        'bullist numlist outdent indent',
        'link image media rubric'
      ].join(' | '),
    }
  });
}
