var {NavLink} = require('./nav.jsx');

export const cssurl = function(s) {
    return `url(${s})`;
};

export const backgroundImg = function(url) {
    return {backgroundImage: cssurl(url)};
};

export const goTo = function(url, newPage) {
    return function() {
        if (newPage) {
            var win = window.open(url, '_blank');
            win.focus();
        } else {
            window.location.href = url;
        }
    };
};

export const artworkLink = function(artwork) {
    return "/artwork/" + artwork.id;
};

export const collectionsLink = function(id) {
    return "/collections/" + id;
};

export const homeLinks = [
    new NavLink('Home', '/home'),
    new NavLink('Browse', '/collections'),
    new NavLink('Search', '/search'),
];
