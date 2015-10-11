var browserify, coffeeReactify, concatCss, concat, gulp, gutil, minifyCss, path, reactify, rename, source, streamify, uglify, watchify, sourcemaps;

gulp = require('gulp');
concatCss = require('gulp-concat-css');
concat = require('gulp-concat');
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
sourcemaps = require('gulp-sourcemaps');

// CSS
gulp.task('minify-css', function() {
  return gulp.src('css/dev/**/*.css')
    .pipe(sourcemaps.init())
      .pipe(concat('client-bundle.css'))
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest('css/test/'));
});

gulp.task('client-production-css', function() {
  gulp.src(['css/dev/**/*.css', '!css/dev/dashboard/**'])
  .pipe(sourcemaps.init())
    .pipe(concat('client-bundle.css'))
    .pipe(minifyCss())
    .pipe(rename('client-bundle.min.css'))
  .pipe(sourcemaps.write('./'))
  .pipe(gulp.dest('css/bundle/'));
});

gulp.task('client-dev-css', function() {
  gulp.src(['css/dev/**/*.css', '!css/dev/dashboard/**'])
  .pipe(sourcemaps.init())
    .pipe(concat('client-bundle.css'))
  .pipe(sourcemaps.write('./'))
  .pipe(gulp.dest('css/bundle/'));
});

gulp.task('dash-production-css', function() {
  gulp.src(['css/dev/**/*.css', '!css/dev/client/**'])
  .pipe(sourcemaps.init())
    .pipe(concat('dash-bundle.css'))
    .pipe(minifyCss())
    .pipe(rename('dash-bundle.min.css'))
  .pipe(sourcemaps.write('./'))
  .pipe(gulp.dest('css/bundle/'));
});

gulp.task('dash-dev-css', function() {
  gulp.src(['css/dev/**/*.css', '!css/dev/client/**'])
  .pipe(sourcemaps.init())
    .pipe(concat('dash-bundle.css'))
  .pipe(sourcemaps.write('./'))
  .pipe(gulp.dest('css/bundle/'));
});

gulp.task('client-watch-css', function() {
  gulp.watch('css/dev/**/*.css', ['client-dev-css', 'client-production-css']);
});

gulp.task('dash-watch-css', function() {
  gulp.watch('css/dev/**/*.css', ['dash-dev-css', 'dash-production-css']);
});

gulp.task('watch-all-css', function() {
  gulp.watch('css/dev/**/*.css', ['client-dev-css', 'client-production-css', 'dash-dev-css', 'dash-production-css']);
});


// javascript
path = {
  DEST: 'client',
  DEST_BUILD: 'client/build/dev',
  PROD_DEST_BUILD: 'client/build/production',
  DEST_SRC: 'client/dev',
  index: {
    MINIFIED_OUT: 'index-build.min.js',
    OUT: 'index-build.js',
    ENTRY_POINT: './client/dev/index/main.jsx'
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

function buildScript(file, entry, watch, prod) {
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
    function prodRebundle() {
        var stream = bundler.bundle();
        return stream.on('error', console.log.bind(console))
            .pipe(source(file))
            .pipe(streamify(uglify({sequences: true})))
            .pipe(gulp.dest(path.PROD_DEST_BUILD));
    }

    if (prod == false) {
      bundler.on('update', function() {
          rebundle();
          gutil.log('Rebundle...');
      });
      return rebundle();
    } else {
      bundler.on('update', function() {
          prodRebundle();
          gutil.log('Rebundle...');
      });
      return prodRebundle();
    }

}


gulp.task('index-build', function() {
  return buildScript( path.index.OUT, path.index.ENTRY_POINT, false, false);
});
gulp.task('category-build', function() {
  return buildScript( path.category.OUT, path.category.ENTRY_POINT, false, false);
});
gulp.task('product-build', function() {
  return buildScript( path.product.OUT, path.product.ENTRY_POINT, false, false);
});
gulp.task('purchase-build', function() {
  return buildScript( path.purchase.OUT, path.purchase.ENTRY_POINT, false, false);
});

gulp.task('index-watch', ['index-build'], function() {
  return buildScript( path.index.OUT, path.index.ENTRY_POINT, true, false);
});
gulp.task('category-watch', ['category-build'], function() {
  return buildScript( path.category.OUT, path.category.ENTRY_POINT, true, false);
});
gulp.task('product-watch', ['product-build'], function() {
  return buildScript( path.product.OUT, path.product.ENTRY_POINT, true, false);
});
gulp.task('purchase-watch', ['purchase-build'], function() {
  return buildScript( path.purchase.OUT, path.purchase.ENTRY_POINT, true, false);
});


// production
gulp.task('index-prod', function() {
  return buildScript( path.index.MINIFIED_OUT, path.index.ENTRY_POINT, false, true);
});
gulp.task('category-prod', function() {
  return buildScript( path.category.MINIFIED_OUT, path.category.ENTRY_POINT, false, true);
});
gulp.task('product-prod', function() {
  return buildScript( path.product.MINIFIED_OUT, path.product.ENTRY_POINT, false, true);
});
gulp.task('purchase-prod', function() {
  return buildScript( path.purchase.MINIFIED_OUT, path.purchase.ENTRY_POINT, false, true);
});



gulp.task('production', ['index-prod', 'category-prod', 'product-prod', 'purchase-prod']);
gulp.task('watch-all', ['index-watch', 'category-watch', 'product-watch', 'purchase-watch']);
