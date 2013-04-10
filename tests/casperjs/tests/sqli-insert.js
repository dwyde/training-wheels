casper.start(baseUrl + 'sqli-insert');

// Successful test.
casper.thenEvaluate(function() {
    var query = "'; INSERT INTO users VALUES ('z')--";
    $('#user input[type=text]').val(query).submit();
});

casper.wait(500);

casper.then(function() {
    var result = this.evaluate(function() {
        return $('#result').html();
    });
    casper.echo(result);
    this.assertSuccess(result, 'Valid SQL INSERT injection.');
});


// Failed test
casper.thenEvaluate(function() {
    $('#user input[type=text]').val("'foo;;'").submit();
});

casper.wait(500);

casper.then(function() {
    var result = this.evaluate(function() {
        return $('#result').html();
    });
    this.assertFailure(result, 'Invalid SQL INSERT injection.');
});


casper.run(function() {
    this.test.done();
});
