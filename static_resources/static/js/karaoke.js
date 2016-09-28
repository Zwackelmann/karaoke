var textQueryUrl = "https://ck0at5btn3.execute-api.eu-central-1.amazonaws.com/prod/query/text";
var artistQueryUrl = "https://ck0at5btn3.execute-api.eu-central-1.amazonaws.com/prod/query/artist";
var songQueryUrl = "https://ck0at5btn3.execute-api.eu-central-1.amazonaws.com/prod/query/song";
var randomArtistsQuery = "https://ck0at5btn3.execute-api.eu-central-1.amazonaws.com/prod/query/browse";

var spotifyResultsLimit = 3;

var minWaitTime = 750; // min wait time between two text queries
var timeoutRunning = false; // if a request is pending right now
var lastRequestDate = 0; // last timestamp of sent request

var randomSeed = Math.round(Math.random()*Math.pow(2,31))
var offset = -3

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
        'data': JSON.stringify({
            'artist_id': artist['id']
        }),
        'dataType': 'json',
        'success': function(songs) {
            if (location.hash != "#artist_result") {
                location.hash = "#artist_result";
            }
            artistResultDiv.empty();

            var artistHeadline = $("<h3>").append(artist["name"]);
            artistResultDiv.append($("<p>").append(artistHeadline));

            if (songs.length > 0) {
                var numSongs = songs.length;
                for (var i = 0; i < numSongs; i++) {
                    var song = songs[i];
                    var songButton = $("<button class='uk-button pb-result-item'>");
                    songButton.append($("<span class='song_title'>").append(song["song_title"]));
                    songButton.click(querySongFun(song['song_id']));
                    artistResultDiv.append(songButton);
                }
            }

            if(songs.length == 0) {
                artistResultDiv.append("<h3>Gurkenwasser! Keine Ergebnisse auf Spotify gefunden.</h3>")
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
        'data': JSON.stringify({
            'song_id': songId,
            'limit': spotifyResultsLimit
        }),
        'dataType': 'json',
        'success': function(results) {
            if (location.hash != "#song_result") {
                location.hash = "#song_result";
            }

            songResultDiv.empty();

            var numResults = results.length;
            for (var i = 0; i < numResults; i++) {
                var result = results[i];

                var songButton = $("<div>");
                var songLink = $("<a class='uk-button pb-result-item-button'>");
                songLink.attr("href", result["spotify_link"]);
                songLink.append($("<span class='song_title'>").append(result["song_name"]));
                songLink.append($("<span class='song_artist'>").append(" (" + result["artists"].join(", ") + ")"));
                songButton.append(songLink);

                var previewElem = $("<div class='pb-audio-control-container'>");
                previewElem.append($("<audio id='audio' preload='auto' controls></audio>").attr("src", result["preview_url"]));
                songButton.append(previewElem);
                songResultDiv.append(songButton);
            }

            if(numResults == 0) {
                songResultDiv.append("<h3>Gurkenwasser! Keine Ergebnisse auf Spotify gefunden.</h3>")
            }
        }
    })
}

function queryText() {
    var textQuery = $('#text_query_input').val();
    if (textQuery.length < 3) {
        return
    }

    var textSearchResultDiv = $('#text_search_result');

    if (!timeoutRunning) {
        var requestTimeDiff = Date.now() - lastRequestDate;
        var waitTime = Math.max(minWaitTime - requestTimeDiff, 1);
        lastRequestDate = Date.now();

        timeoutRunning = true;
        setTimeout(function() {
            timeoutRunning = false;
            $.ajax({
                'type': 'POST',
                'url': textQueryUrl,
                'contentType': 'application/json',
                'data': JSON.stringify({
                    'q': textQuery
                }),
                'dataType': 'json',
                'success': function(data) {
                    if (location.hash != "#text_search_result") {
                        location.hash = "#text_search_result";
                        $("#text_query_input").focus();
                    }

                    var artists = data['artists'];
                    var songs = data['songs'];

                    textSearchResultDiv.empty();

                    if (artists.length > 0) {
                        var numArtists = artists.length;
                        var artistParagraph = $("<span></span>");
                        artistParagraph.append("<h3>Künstler</h3>");
                        for (var i = 0; i < numArtists; i++) {
                            var artist = artists[i];

                            var artistButton = $("<button class='uk-button pb-result-item'>");
                            artistButton.append($("<span class='artist'>").append(artist["artist_name"]));
                            artistButton.click(queryAuthorFun({
                                'id': artist['artist_id'],
                                'name': artist['artist_name']
                            }));
                            artistParagraph.append(artistButton);
                        }
                        textSearchResultDiv.append(artistParagraph)
                    }

                    if (songs.length > 0) {
                        var numSongs = songs.length;
                        var songParagraph = $("<span></span>");
                        songParagraph.append("<h3>Songs</h3>");
                        for (var i = 0; i < numSongs; i++) {
                            var song = songs[i];

                            var songButton = $("<button class='uk-button pb-result-item'>");
                            songButton.append($("<span class='song_title'>").append(song["song_title"]));
                            songButton.append($("<span class='song_artist'>").append(" (" + song["artist_name"] + ")"));
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

function random_artists() {
    randomSeed = Math.round(Math.random()*Math.pow(2,31))
    offset = 0
    update_random_artist_panel()
}

function change_artist_offset(offset_change) {
    offset += offset_change
    update_random_artist_panel()
}

function update_random_artist_panel() {
    $.ajax({
        'type': 'GET',
        'url': randomArtistsQuery,
        'contentType': 'application/json',
        'data': $.param({"seed": randomSeed, "offset": offset}),
        'dataType': 'json',
        'success': function(res) {
            artists = res['artists']
            if(location.hash != "#random_artists") {
                location.hash = "#random_artists";
            }
            var randomArtistsDiv = $('#random_artist_list');
            randomArtistsDiv.empty();

            $('#text_query_input').val("")

            var numArtists = artists.length
            for(var i=0; i<numArtists; i++) {
                var artist = artists[i];

                var artistButton = $("<button class='result_item'>");
                artistButton.append($("<p class='artist'>").append(artist["artist_name"]));
                artistButton.click(queryAuthorFun({'id': artist['artist_id'], 'name': artist['artist_name']}));
                randomArtistsDiv.append(artistButton);
            }
        }
    })
}

// Loop Attribute for ios
function init() {
    var myAudio = document.getElementById("audio");
    myAudio.addEventListener('ended', loopAudio, false);
}

function loopAudio() {
    var myAudio = document.getElementById("audio");
    myAudio.play();
}
