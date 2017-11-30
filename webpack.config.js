const path = require('path');
const fs = require('fs');


const src = './client/'
const entry = {};
fs.readdirSync(src).forEach(function(filename) {
    if (!/.jsx?$/g.test(filename)) {
        return;
    }
    var path = src + filename;
    var moduleName = filename.slice(0, filename.lastIndexOf('.'));
    entry[moduleName] = path;
});


module.exports = {
    devtool: 'source-map',
    entry: entry,
    output: {
        path: path.resolve('./static/js'),
        pathinfo: true,
        filename: '[name].js',
    },
    module: {
        loaders: [
            {test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/},
            {test: /\.jsx$/, loader: 'babel-loader', exclude: /node_modules/},
        ]
    }
};
