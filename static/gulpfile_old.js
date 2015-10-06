//таск для index файла
gulp.task('index-watch', function(){
	var watcher = watchify(browserify({
		entries: [path.index.ENTRY_POINT],
		transform: [coffeeReactify],
		debug: true,
		cache:{}, packageCache: {}, fullPath: true
	}));

	return watcher.on('update', function(){
		watcher.bundle()
			.pipe(source(path.index.OUT))
			.pipe(gulp.dest(path.DEST_BUILD))
			console.log('index-watch Update');
	})
		.bundle()
		.pipe(source(path.index.OUT))
		.pipe(gulp.dest(path.DEST_BUILD))
});

 
//таск для category файла
gulp.task('category-watch', function(){
	var watcher = watchify(browserify({
		entries: [path.category.ENTRY_POINT],
		transform: [coffeeReactify],
		debug: true,
		cache:{}, packageCache: {}, fullPath: true
	}));

	return watcher.on('update', function(){
		watcher.bundle()
			.pipe(source(path.category.OUT))
			.pipe(gulp.dest(path.DEST_BUILD))
			console.log('category-watch Update');
	})
		.bundle()
		.pipe(source(path.category.OUT))
		.pipe(gulp.dest(path.DEST_BUILD))
});


//таск для product файла
gulp.task('product-watch', function(){
	var watcher = watchify(browserify({
		entries: [path.product.ENTRY_POINT],
		transform: [coffeeReactify],
		debug: true,
		cache:{}, packageCache: {}, fullPath: true
	}));

	return watcher.on('update', function(){
		watcher.bundle()
			.pipe(source(path.product.OUT))
			.pipe(gulp.dest(path.DEST_BUILD))
			console.log('product-watch Update');
	})
		.bundle()
		.pipe(source(path.product.OUT))
		.pipe(gulp.dest(path.DEST_BUILD))
});


//таск для product файла
gulp.task('purchase-watch', function(){
	var watcher = watchify(browserify({
		entries: [path.purchase.ENTRY_POINT],
		transform: [coffeeReactify],
		debug: true,
		cache:{}, packageCache: {}, fullPath: true
	}));

	return watcher.on('update', function(){
		watcher.bundle()
			.pipe(source(path.purchase.OUT))
			.pipe(gulp.dest(path.DEST_BUILD))
			console.log('purchase-watch Update');
	})
		.bundle()
		.pipe(source(path.purchase.OUT))
		.pipe(gulp.dest(path.DEST_BUILD))
});