// The base server URL.
var baseUrl = 'http://localhost:5000/';

// Find a substring of the success result HTML message.
casper.assertSuccess = function(result, message) {
    var index = result.search('Success');
    this.test.assert(index >= 0, message);
};

// Find a substring of the failure result HTML message.
casper.assertFailure = function(result, message) {
    var index = result.search('Keep trying');
    this.test.assert(index >= 0, message);
};
