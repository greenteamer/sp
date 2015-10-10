var browserify, coffeeReactify, concatCss, gulp, gutil, minifyCss, path, reactify, rename, source, streamify, uglify, watchify;

gulp = require('gulp');
concatCss = require('gulp-concat-css');
minifyCss = require('gulp-minify-css');
rename = require('gulp-rename');
uglify = require('gulp-uglify');
notify = require("gulp-notify");
source = require('vinyl-source-stream');
browserify = require('browserify');
coffeeReactify = require('coffee-reactify');
watchify = require('watchify');
gutil = require('gutil');
streamify = require('gulp-streamify');

gulp.task('default', function() {
  gulp.src('css/test/*.css').pipe(concatCss('bundle.css')).pipe(minifyCss()).pipe(rename('bundle.min.css')).pipe(gulp.dest('css/'));
});

gulp.task('watch-css', function() {
  gulp.watch('css/test/*.css', ['default']);
});

path = {
  DEST: 'client',
  DEST_BUILD: 'client/build/dev',
  PROD_DEST_BUILD: 'client/build/production',
  DEST_SRC: 'client/dev',
  index: {
    MINIFIED_OUT: 'index-build.min.js',
    OUT: 'index-build.js',
    ENTRY_POINT: './client/dev/index/main.cjsx'
  },
  category: {
    MINIFIED_OUT: 'category-build.min.js',
    OUT: 'category-build.js',
    ENTRY_POINT: './client/dev/category/main.jsx'
  },
  product: {
    MINIFIED_OUT: 'product-build.min.js',
    OUT: 'product-build.js',
    ENTRY_POINT: './client/dev/product/main.jsx'
  },
  purchase: {
    MINIFIED_OUT: 'purchase-build.min.js',
    OUT: 'purchase-build.js',
    ENTRY_POINT: './client/dev/purchase/main.jsx'
  }
};

gulp.task('index-build', function() {
  browserify({
    entries: [path.index.ENTRY_POINT],
    transform: [coffeeReactify]
  }).bundle().pipe(source(path.index.MINIFIED_OUT)).pipe(streamify(uglify({
    sequences: true
  }))).pipe(gulp.dest(path.PROD_DEST_BUILD));
});



gulp.task('coffee-index-watch', function() {
  var watcher;
  watcher = watchify(browserify({
    entries: [path.index.ENTRY_POINT],
    transform: [coffeeReactify],
    debug: true,
    cache: {},
    packageCache: {},
    fullPath: true
  }));
  return watcher.on('update', function() {
    watcher.bundle().pipe(source(path.index.OUT)).pipe(gulp.dest(path.DEST_BUILD));
    return console.log('coffee index-watch Update');
  }).bundle().pipe(source(path.index.OUT)).pipe(gulp.dest(path.DEST_BUILD));
});



function handleErrors() {
  var args = Array.prototype.slice.call(arguments);
  notify.onError({
    title: "Compile Error",
    message: "<%= error.message %>"
  }).apply(this, args);
  this.emit('end'); // Keep gulp from hanging on this task
}

function buildScript(file, entry, watch) {
    var props = {
        entries: [entry],
        debug: true,
        cache: {},
        packageCache: {},
    };
    var bundler = watch ? watchify(browserify(props)) : browserify(props);
    bundler.transform(coffeeReactify);
    function rebundle() {
        var stream = bundler.bundle();
        return stream.on('error', console.log.bind(console))
            .pipe(source(file))
            .pipe(gulp.dest(path.DEST_BUILD));
    }
    bundler.on('update', function() {
        rebundle();
        gutil.log('Rebundle...');
    });
    return rebundle();
}


gulp.task('index-build', function() {
  return buildScript( path.index.OUT, path.index.ENTRY_POINT, false);
});


gulp.task('index-watch', ['index-build'], function() {
  return buildScript( path.index.OUT, path.index.ENTRY_POINT, true);
});



gulp.task('production', ['index-build', 'category-build', 'product-build', 'purchase-build']);
gulp.task('coffee', ['coffee-index-watch', 'coffee-category-watch', 'coffee-product-watch', 'coffee-purchase-watch']);
