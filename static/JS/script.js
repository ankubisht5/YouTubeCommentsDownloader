document.getElementById('downloadForm').addEventListener('submit', function (event) {
    var numComments = document.getElementById('numComments').value;
    // Validate the number of comments input
    if (numComments && !/^\d+$/.test(numComments)) {
        alert('Please enter a valid number for the "Number of Comments" field.');
        return;
    }
});

//window.addEventListener('beforeunload', function (event) {
//    var inputs = document.querySelectorAll('#downloadForm input[type="text"]');
//    var submitButton = document.querySelector('#downloadForm button[type="submit"]');
//    console.log(inputs)
//    console.log(submitButton)
//    var isSubmitClicked = false;
//    submitButton.addEventListener('click', function () {
//        isSubmitClicked = true;
//    });
//    console.log(isSubmitClicked)
//    if (isSubmitClicked) {
//        return;
//    }
//    for (var i = 0; i < inputs.length; i++) {
//        if (inputs[i].value !== '') {
//            event.preventDefault();
//            event.returnValue = 'Are you sure you want to leave this page? Your entered data will be lost.';
//            return;
//        }
//    }
//});
