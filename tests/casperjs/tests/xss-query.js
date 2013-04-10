var exerciseUrl = baseUrl + 'xss-query';

casper.start(exerciseUrl);

casper.thenOpen(exerciseUrl + '?name=foo', function() {
    var result = this.evaluate(function() {
        return $('#result').html();
    });
    this.assertFailure(result, 'No XSS on "name".');
});

casper.thenOpen(exerciseUrl + '?name=<script>alert(1)</script>', function() {
    var result = this.evaluate(function() {
        return $('#result').html();
    });
    this.assertSuccess(result, 'Successful XSS on "name".');
});

casper.run(function() {
    this.test.done();
});
