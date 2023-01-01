from youtube_transcript_api import YouTubeTranscriptApi
import re

# Python Program to get a youtube transcript from the API and convert the output to an html page that displays the transcript in a clickable format that will plaback as it is clicked. 

def generate_html(transcript):
  # Initialize variables
  html = ""
  current_time = 0
  interval = 15

  # Iterate through each line
  for line in transcript:
    timestamp = line['start']
    text = line['text']
    html += f'<span data-timestamp="{timestamp}" onclick="seekToAndPlay({timestamp})">{text}</span>'

  return html

def get_transcript(url):
  # Extract the video ID from the URL
  video_id = url.split("?v=")[1]

  # Get the transcript
  transcript = YouTubeTranscriptApi.get_transcript(video_id)

  # Convert the transcript to HTML
  html = generate_html(transcript)

    # Create the full HTML document
  html = """
  <html>
  <head>
    <link href='https://fonts.googleapis.com/css?family=Raleway:400,700' rel='stylesheet' type='text/css'>
    <style>
      body {
        font-family: 'Raleway', sans-serif;
        font-size: 18pt;
      }
      .highlighted {
        background-color: yellow;
      }
    </style>
  </head>
  <body>
    <div id="player"></div>
    <br>
    <br>
  """ + html + """  
      <script src="https://www.youtube.com/iframe_api"></script>
    <script>
      var player;
      function onYouTubeIframeAPIReady() {
        player = new YT.Player('player', {
          height: '360',
          width: '640',
          videoId: 'EQ3GjpGq5Y8',
          events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
          }
        });
      }

      function onPlayerReady(event) {
        event.target.playVideo();
      }

      function onPlayerStateChange(event) {
        var currentTime = Math.floor(player.getCurrentTime());
        var highlightedLinks = document.getElementsByClassName('highlighted');
        for (var i = 0; i < highlightedLinks.length; i++) {
          highlightedLinks[i].classList.remove('highlighted');
        }
        var links = document.getElementsByTagName('span');
        for (var i = 0; i < links.length; i++) {
          if (links[i].dataset.timestamp <= currentTime + 2 && links[i].dataset.timestamp >= currentTime - 2) {
            links[i].classList.add('highlighted');
          }
        }
        setTimeout(onPlayerStateChange, 1000);
      }

      function seekTo(seconds) {
        player.seekTo(seconds, true);
      }

      function seekToAndPlay(seconds) {
        player.seekTo(seconds, true);
        player.playVideo();
      }
    </script>
  </body>
</html>  
  """  
  
    
    
  # Save the HTML to a file
  with open(video_id + '.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Test the function with a YouTube video URL
url = "https://www.youtube.com/watch?v=EQ3GjpGq5Y8"
get_transcript(url)
