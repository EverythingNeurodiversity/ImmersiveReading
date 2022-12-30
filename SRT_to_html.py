import re

def convert_srt(srt_str):
  # Split the .srt string into lines
  lines = srt_str.strip().split('\n')

  # Initialize an empty list to store the transcript segments
  segments = []

  # Iterate through the lines of the transcript
  i = 0
  while i < len(lines):
    # The line with the index number can be ignored
    i += 1

    # Check if the line is a timestamp
    if re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', lines[i]):
      # Split the line into start and end timestamps
      start, end = lines[i].split(' --> ')

      # Convert the start and end timestamps to seconds
      start_sec = hms_to_seconds(start)
      end_sec = hms_to_seconds(end)

      # Initialize an empty string to store the transcript segment
      text = ''

      # Move to the next line
      i += 1

      # Concatenate the lines of the transcript segment until a blank line is encountered
      while i < len(lines) and lines[i]:
        text += lines[i] + ' '
        i += 1

      # Remove the extra space at the end of the transcript segment
      text = text.strip()

      # Add the segment to the list
      segments.append((start_sec, end_sec, text))
    else:
      # The line is a transcript segment
      text = lines[i].strip()

      # Add the segment to the list
      segments.append((start_sec, end_sec, text))

      # Move to the next line
      i += 1

  # Return the list of transcript segments
  return segments

def hms_to_seconds(hms):
  # Split the timestamp into hours, minutes, seconds, and milliseconds
  h, m, s = hms.split(':')
  ms = s.split(',')[1]

  # Convert the values to integers and calculate the total number of seconds
  return int(h) * 3600 + int(m) * 60 + int(s.split(',')[0]) + int(ms) / 1000

def main():
  # Read the .srt file
  with open('huberman69transcript.srt', 'r') as f:
    srt_str = f.read()

  # Convert the .srt transcript to the desired format
  segments = convert_srt(srt_str)

  # Generate the HTML code for the transcript
  html = '<div id="transcript">\n'
  for start, end, text in segments:
    html += f'  <p data-start="{start}" data-end="{end}">{text}</p>\n'
  html += '</div>'

  # Print the HTML code
  print(html)

if __name__ == '__main__':
  main()
