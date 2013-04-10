var exerciseUrl = baseUrl + 'xss-attr';

casper.start(exerciseUrl);

casper.thenOpen(exerciseUrl + '?color=foo', function() {
    var result = this.evaluate(function() {
        return $('#result').html();
    });
    this.assertFailure(result, 'No XSS on "color".');
});

casper.thenOpen(exerciseUrl + '?color="><script>alert(1)</script>', function() {
    var result = this.evaluate(function() {
        return $('#result').html();
    });
    this.assertSuccess(result, 'Successful XSS on "color".');
});

casper.run(function() {
    this.test.done();
});
