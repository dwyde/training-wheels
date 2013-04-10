/** 
 * Display a message to indicate if an exercise was completed successfully.
 * 
 * @param {Boolean} result An indication whether an answer is correct.
 */
function evaluateSuccess(result) {
    if (result) {
        var output = $('<p>Success!</p>').addClass('success');
    }
    else {
        var output = $('<p>Keep trying!</p>').addClass('failure');
    }
    $('#result').html(output);
}
