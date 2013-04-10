casper.start(baseUrl + 'sqli-select');

// Successful test.
casper.thenEvaluate(function() {
    $('#user input[type=text]').val("' OR '1'='1").submit();
});

casper.wait(500);

casper.then(function() {
    var result = this.evaluate(function() {
        return $('#result').html();
    });
    this.assertSuccess(result, 'Valid SQL SELECT injection.');
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
    this.assertFailure(result, 'Invalid SQL SELECT injection.');
});


casper.run(function() {
    this.test.done();
});
