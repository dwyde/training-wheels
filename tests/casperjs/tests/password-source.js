casper.start(baseUrl + 'password-source');

casper.then(function() {
    var result = this.evaluate(function() {
        $('#entry input[type=password]').val(password).submit();
        return $('#result').html();
    });
    this.assertSuccess(result, 'Password found in source.');
    
    result = this.evaluate(function() {
        $('#entry input[type=password]').val('').submit();
        return $('#result').html();
    });
    this.assertFailure(result, 'Blank password fails.');
});

casper.run(function() {
    this.test.done();
});
