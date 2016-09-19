var textQueryUrl = "https://ck0at5btn3.execute-api.eu-central-1.amazonaws.com/prod/query/text";
var artistQueryUrl = "https://ck0at5btn3.execute-api.eu-central-1.amazonaws.com/prod/query/artist";
var songQueryUrl = "https://ck0at5btn3.execute-api.eu-central-1.amazonaws.com/prod/query/song";

var spotifyResultsLimit = 3;

var minWaitTime = 750; // min wait time between two text queries
var timeoutRunning = false; // if a request is pending right now
var lastRequestDate = 0; // last timestamp of sent request

function queryAuthorFun(artist) {
    return function() {
        queryAuthor(artist)
    }
}

function queryAuthor(artist) {
    var artistResultDiv = $('#artist_result');

    $.ajax({
        'type': 'POST',
        'url': artistQueryUrl,
        'contentType': 'application/json',
        'data': JSON.stringify({'artist_id': artist['id']}),
        'dataType': 'json',
        'success': function(songs) {
            $("#text_search_result").hide();
            $("#artist_result").show();
            $("#song_result").hide();

            artistResultDiv.empty();

            if(songs.length > 0) {
                var numSongs = songs.length;
                for(var i=0; i<numSongs; i++) {
                    var song = songs[i];
                    var songButton = $("<button class='result_item'>");
                    songButton.append($("<p class='song_title'>").append(song["song_title"]));
                    songButton.append($("<p class='song_artist'>").append(artist["name"]));
                    songButton.click(querySongFun(song['song_id']));
                    artistResultDiv.append(songButton);
                }
            }
        }
    })
}

function querySongFun(songId) {
    return function() {
        querySong(songId)
    }
}

function querySong(songId) {
    var songResultDiv = $('#song_result');

    $.ajax({
        'type': 'POST',
        'url': songQueryUrl,
        'contentType': 'application/json',
        'data': JSON.stringify({'song_id': songId, 'limit': spotifyResultsLimit}),
        'dataType': 'json',
        'success': function(results) {
            $("#text_search_result").hide();
            $("#artist_result").hide();
            $("#song_result").show();

            songResultDiv.empty();

            var numResults = results.length;
            for(var i=0; i<numResults; i++) {
                var result = results[i];

                var songButton = $("<div class='result_item'>");
                var songLink = $("<a>");
                songLink.attr("href", result["spotify_link"]);
                songLink.append($("<p class='song_title'>").append(result["song_name"]));
                songLink.append($("<p class='song_artist'>").append(result["artists"].join(", ")));
                songButton.append(songLink);

                var previewElem = $("<audio preload='auto' controls></audio>").attr("src", result["preview_url"]);
                songButton.append(previewElem);
                songResultDiv.append(songButton);
            }
        }
    })
}

function queryText() {
    var textQuery = $('#text_query_input').val();
    if(textQuery.length < 3) {
        return
    }

    var textSearchResultDiv = $('#text_search_result');

    if(!timeoutRunning) {
        var requestTimeDiff = Date.now()-lastRequestDate;
        var waitTime = Math.max(minWaitTime-requestTimeDiff, 1);
        lastRequestDate = Date.now();

        timeoutRunning = true;
        setTimeout(function () {
            timeoutRunning = false;
            $.ajax({
                'type': 'POST',
                'url': textQueryUrl,
                'contentType': 'application/json',
                'data': JSON.stringify({'q': textQuery}),
                'dataType': 'json',
                'success': function (data) {
                    $("#text_search_result").show();
                    $("#artist_result").hide();
                    $("#song_result").hide();

                    var artists = data['artists'];
                    var songs = data['songs'];

                    textSearchResultDiv.empty();

                    if (artists.length > 0) {
                        var numArtists = artists.length;
                        var artistParagraph = $("<p></p>");
                        artistParagraph.append("<h3>Artist results</h3>");
                        for (var i = 0; i < numArtists; i++) {
                            var artist = artists[i];

                            var artistButton = $("<button class='result_item'>");
                            artistButton.append($("<p class='artist'>").append(artist["artist_name"]));
                            artistButton.click(queryAuthorFun({'id': artist['artist_id'], 'name': artist['artist_name']}));
                            artistParagraph.append(artistButton);
                        }
                        textSearchResultDiv.append(artistParagraph)
                    }

                    if (songs.length > 0) {
                        var numSongs = songs.length;
                        var songParagraph = $("<p></p>");
                        songParagraph.append("<h3>Song results</h3>");
                        for (var i = 0; i < numSongs; i++) {
                            var song = songs[i];

                            var songButton = $("<button class='result_item'>");
                            songButton.append($("<p class='song_title'>").append(song["song_title"]));
                            songButton.append($("<p class='song_artist'>").append(song["artist_name"]));
                            songButton.click(querySongFun(song['song_id']));
                            songParagraph.append(songButton);
                        }
                        textSearchResultDiv.append(songParagraph)
                    }
                }
            })
        }, waitTime)
    }
}
