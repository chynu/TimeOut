var playing = true;
var btn = $('#audio_button');

btn.click(function(){
  console.log("Clicked!");
  if (playing){
    player.pauseVideo();
    document.getElementById("audio_button").src = "http://www.iconsdb.com/icons/preview/white/mute-2-xxl.png";
  }
  else {
    player.playVideo();
    document.getElementById("audio_button").src = "http://www.iconsplace.com/download/white-volume-up-256.png";
  }
  playing = !playing;
  console.log(playing);
});


var tag = document.createElement('script');

      tag.src = "https://www.youtube.com/iframe_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      // 3. This function creates an <iframe> (and YouTube player)
      //    after the API code downloads.
      var player;
      function onYouTubeIframeAPIReady() {
        player = new YT.Player('player', {
          height: '0',
          width: '0',
          videoId: 'WIbUNfg_wmM',
          events: {
            'onReady': onPlayerReady
          }
        });
      }

      // 4. The API will call this function when the video player is ready.
      function onPlayerReady(event) {
        event.target.playVideo();
      }
