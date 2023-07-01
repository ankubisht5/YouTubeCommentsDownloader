document.getElementById('downloadForm').addEventListener('submit', function (event) {
    event.preventDefault();

    var youtubeUrl = document.getElementById('youtubeUrl').value;
    var removeDuplicates = document.getElementById('removeDuplicates').checked;
    var keywordFilter = document.getElementById('keywordFilter').value;
    var numComments = document.getElementById('numComments').value;

    // Validate the number of comments input
    if (numComments && !/^\d+$/.test(numComments)) {
        alert('Please enter a valid number for the "Number of Comments" field.');
        return;
    }

    // Display the download link
    document.getElementById('downloadLink').classList.remove('hidden');

    // Set the download URL with query parameters
    var downloadUrl = 'https://example.com/download?youtube_url=' + encodeURIComponent(youtubeUrl);
    if (removeDuplicates) {
        downloadUrl += '&remove_duplicates=true';
    }
    if (keywordFilter) {
        downloadUrl += '&keyword_filter=' + encodeURIComponent(keywordFilter);
    }
    if (numComments) {
        downloadUrl += '&num_comments=' + encodeURIComponent(numComments);
    }

    document.getElementById('downloadButton').href = downloadUrl;
});

window.addEventListener('beforeunload', function (event) {
    var inputs = document.querySelectorAll('#downloadForm input[type="text"]');
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].value !== '') {
            event.returnValue = 'Are you sure you want to leave this page? Your entered data will be lost.';
            return;
        }
    }
});
